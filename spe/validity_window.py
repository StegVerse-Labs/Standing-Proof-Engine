#!/usr/bin/env python3
"""Evaluate validity-window rotation for micro-node inputs.

Short-lived material is consumable during its declared validity window. The
refresh cycle begins before expiry and should prepare an admissible successor.
At expiry, the node rotates to the successor if one is available; otherwise it
fails closed.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

VALID_CONSUME = "CONSUME"
REFRESH_IN_PARALLEL = "REFRESH_IN_PARALLEL"
ROTATE = "ROTATE"
FAIL_CLOSED = "FAIL_CLOSED"
QUARANTINE = "QUARANTINE"
PENDING = "PENDING"


@dataclass(frozen=True)
class ValidityDecision:
    result: str
    reason: str
    consume_ref: str | None = None
    refresh_ref: str | None = None


def parse_instant(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        normalized = value.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return None


def successor_is_ready(record: dict[str, Any], now: datetime) -> tuple[bool, str | None]:
    successor = record.get("successor")
    if not isinstance(successor, dict):
        return False, None
    if successor.get("revoked") is True or successor.get("conflicted") is True:
        return False, successor.get("token_ref") if isinstance(successor.get("token_ref"), str) else None
    valid_from = parse_instant(successor.get("valid_from"))
    expires_at = parse_instant(successor.get("expires_at"))
    token_ref = successor.get("token_ref") if isinstance(successor.get("token_ref"), str) else None
    if valid_from is None or expires_at is None or token_ref is None:
        return False, token_ref
    return valid_from <= now < expires_at, token_ref


def evaluate_validity_window(record: dict[str, Any], now: datetime | None = None) -> ValidityDecision:
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    token_ref = record.get("token_ref") if isinstance(record.get("token_ref"), str) else None

    if record.get("revoked") is True:
        return ValidityDecision(FAIL_CLOSED, "current material revoked", token_ref)
    if record.get("conflicted") is True:
        return ValidityDecision(FAIL_CLOSED, "current material conflicted", token_ref)

    valid_from = parse_instant(record.get("valid_from"))
    expires_at = parse_instant(record.get("expires_at"))
    refresh_after = parse_instant(record.get("refresh_after"))
    refresh_deadline = parse_instant(record.get("refresh_deadline"))

    if token_ref is None or valid_from is None or expires_at is None:
        return ValidityDecision(QUARANTINE, "validity record incomplete", token_ref)

    if now < valid_from:
        return ValidityDecision(PENDING, "current material not valid yet", token_ref)

    successor_ready, successor_ref = successor_is_ready(record, now)

    if now >= expires_at:
        if successor_ready:
            return ValidityDecision(ROTATE, "current material expired and successor is ready", successor_ref, successor_ref)
        return ValidityDecision(FAIL_CLOSED, "current material expired without ready successor", token_ref, successor_ref)

    if refresh_deadline is not None and now >= refresh_deadline and not successor_ready:
        return ValidityDecision(FAIL_CLOSED, "refresh deadline missed before expiry", token_ref, successor_ref)

    if refresh_after is not None and now >= refresh_after:
        if successor_ready:
            return ValidityDecision(REFRESH_IN_PARALLEL, "successor ready before expiry", token_ref, successor_ref)
        return ValidityDecision(REFRESH_IN_PARALLEL, "refresh window open; successor not ready yet", token_ref, successor_ref)

    return ValidityDecision(VALID_CONSUME, "current material valid within declared window", token_ref, successor_ref)


def decision_payload(record: dict[str, Any], now: datetime | None = None) -> dict[str, Any]:
    decision = evaluate_validity_window(record, now)
    return {
        "result": decision.result,
        "reason": decision.reason,
        "consume_ref": decision.consume_ref,
        "refresh_ref": decision.refresh_ref,
    }
