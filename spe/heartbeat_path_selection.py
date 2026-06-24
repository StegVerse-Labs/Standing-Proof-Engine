#!/usr/bin/env python3
"""Heartbeat-guided path selection primitives for SPE research.

The heartbeat does not make hard standing determinations by itself. It is one
input to a broader state vector used to select an admissible convergence path.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

NORMAL = "NORMAL"
STRESS_OBSERVED = "STRESS_OBSERVED"
DEGRADED = "DEGRADED"
AUTHORITY_AT_RISK = "AUTHORITY_AT_RISK"
FAIL_CLOSED = "FAIL_CLOSED"

CONTINUE = "CONTINUE"
PRE_ROTATE_AND_CONTINUE = "PRE_ROTATE_AND_CONTINUE"
REFRESH_DERIVED_STATE = "REFRESH_DERIVED_STATE"
REROUTE = "REROUTE"
LOAD_SHED = "LOAD_SHED"
DEEPEN_VERIFICATION = "DEEPEN_VERIFICATION"
ROLLBACK_OR_RECONSTRUCT = "ROLLBACK_OR_RECONSTRUCT"
QUARANTINE = "QUARANTINE"


@dataclass(frozen=True)
class PathSelection:
    selected_path: str
    degradation_state: str
    reasons: tuple[str, ...]
    rejected_paths: dict[str, str] = field(default_factory=dict)


def heartbeat_ratio(vector: dict[str, Any]) -> float:
    observed = float(vector.get("observed_heartbeat_interval", 0.0))
    nominal = float(vector.get("nominal_heartbeat_interval", 0.0))
    if observed <= 0 or nominal <= 0:
        return 0.0
    return max(0.0, (observed - nominal) / nominal)


def degradation_state(vector: dict[str, Any]) -> tuple[str, tuple[str, ...]]:
    reasons: list[str] = []
    ratio = heartbeat_ratio(vector)
    if ratio > 0:
        reasons.append(f"delta_heartbeat_ratio={ratio:.6f}")

    missed_refresh = bool(vector.get("missed_refresh_boundary"))
    failed_successor = bool(vector.get("successor_ready") is False and vector.get("token_refresh_pressure") == "HIGH")
    receipt_latency_high = bool(vector.get("receipt_latency") == "HIGH")
    queue_high = bool(vector.get("queue_depth") == "HIGH")
    hash_drift = bool(vector.get("hash_drift"))
    rollback_fail = bool(vector.get("rollback_failed"))

    if rollback_fail or bool(vector.get("revoked_or_conflicted")):
        reasons.append("hard_failure_signal")
        return FAIL_CLOSED, tuple(reasons)
    if missed_refresh or failed_successor:
        reasons.append("authority_timing_boundary_at_risk")
        return AUTHORITY_AT_RISK, tuple(reasons)
    if ratio >= 0.20 or sum([receipt_latency_high, queue_high, hash_drift]) >= 2:
        reasons.append("corroborated_system_degradation")
        return DEGRADED, tuple(reasons)
    if ratio >= 0.05 or receipt_latency_high or queue_high or hash_drift:
        reasons.append("stress_observed_without_hard_failure")
        return STRESS_OBSERVED, tuple(reasons)
    return NORMAL, tuple(reasons or ["within_nominal_bounds"])


def select_path(vector: dict[str, Any]) -> PathSelection:
    state, reasons = degradation_state(vector)
    rejected: dict[str, str] = {}

    if state == FAIL_CLOSED:
        return PathSelection(FAIL_CLOSED, state, reasons, {"CONTINUE": "hard failure signal present"})

    if state == AUTHORITY_AT_RISK:
        if vector.get("rollback_available") is True:
            return PathSelection(ROLLBACK_OR_RECONSTRUCT, state, reasons, {"CONTINUE": "authority boundary at risk"})
        return PathSelection(FAIL_CLOSED, state, reasons, {"ROLLBACK_OR_RECONSTRUCT": "rollback unavailable"})

    if vector.get("hash_drift") is True:
        rejected[CONTINUE] = "derived state drift requires refresh before consumption"
        return PathSelection(REFRESH_DERIVED_STATE, state, reasons, rejected)

    if vector.get("token_refresh_pressure") == "HIGH" and vector.get("successor_ready") is True:
        rejected[CONTINUE] = "successor is ready and token pressure is high"
        return PathSelection(PRE_ROTATE_AND_CONTINUE, state, reasons, rejected)

    if vector.get("receipt_latency") == "HIGH" and vector.get("alternate_route_available") is True:
        rejected[CONTINUE] = "receipt latency high; alternate route available"
        return PathSelection(REROUTE, state, reasons, rejected)

    if vector.get("queue_depth") == "HIGH":
        rejected[CONTINUE] = "queue pressure high"
        return PathSelection(LOAD_SHED, state, reasons, rejected)

    if vector.get("evidence_currency") == "WEAK":
        rejected[CONTINUE] = "evidence currency weak"
        return PathSelection(DEEPEN_VERIFICATION, state, reasons, rejected)

    return PathSelection(CONTINUE, state, reasons, rejected)


def factor_bound_receipt(vector: dict[str, Any]) -> dict[str, Any]:
    selected = select_path(vector)
    return {
        "receipt_type": "factor_bound_path_selection",
        "selected_path": selected.selected_path,
        "degradation_state": selected.degradation_state,
        "reasons": list(selected.reasons),
        "rejected_paths": selected.rejected_paths,
        "state_vector": vector,
    }
