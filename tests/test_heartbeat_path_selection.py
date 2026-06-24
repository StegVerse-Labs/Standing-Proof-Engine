import unittest

from spe.heartbeat_path_selection import (
    AUTHORITY_AT_RISK,
    CONTINUE,
    DEEPEN_VERIFICATION,
    DEGRADED,
    FAIL_CLOSED,
    LOAD_SHED,
    NORMAL,
    PRE_ROTATE_AND_CONTINUE,
    REFRESH_DERIVED_STATE,
    REROUTE,
    ROLLBACK_OR_RECONSTRUCT,
    STRESS_OBSERVED,
    factor_bound_receipt,
    select_path,
)


class HeartbeatPathSelectionTests(unittest.TestCase):
    def test_nominal_state_continues(self):
        decision = select_path({
            "nominal_heartbeat_interval": 1.0,
            "observed_heartbeat_interval": 1.0,
        })
        self.assertEqual(decision.degradation_state, NORMAL)
        self.assertEqual(decision.selected_path, CONTINUE)

    def test_delta_heartbeat_alone_observes_stress_without_hard_failure(self):
        decision = select_path({
            "nominal_heartbeat_interval": 1.0,
            "observed_heartbeat_interval": 1.08,
        })
        self.assertEqual(decision.degradation_state, STRESS_OBSERVED)
        self.assertEqual(decision.selected_path, CONTINUE)

    def test_hash_drift_selects_derived_state_refresh(self):
        decision = select_path({
            "nominal_heartbeat_interval": 1.0,
            "observed_heartbeat_interval": 1.02,
            "hash_drift": True,
        })
        self.assertEqual(decision.selected_path, REFRESH_DERIVED_STATE)
        self.assertIn(CONTINUE, decision.rejected_paths)

    def test_high_token_pressure_with_ready_successor_pre_rotates(self):
        decision = select_path({
            "nominal_heartbeat_interval": 1.0,
            "observed_heartbeat_interval": 1.03,
            "token_refresh_pressure": "HIGH",
            "successor_ready": True,
        })
        self.assertEqual(decision.selected_path, PRE_ROTATE_AND_CONTINUE)

    def test_receipt_latency_reroutes_when_alternate_route_available(self):
        decision = select_path({
            "nominal_heartbeat_interval": 1.0,
            "observed_heartbeat_interval": 1.10,
            "receipt_latency": "HIGH",
            "alternate_route_available": True,
        })
        self.assertEqual(decision.selected_path, REROUTE)

    def test_queue_pressure_sheds_load(self):
        decision = select_path({
            "nominal_heartbeat_interval": 1.0,
            "observed_heartbeat_interval": 1.10,
            "queue_depth": "HIGH",
        })
        self.assertEqual(decision.selected_path, LOAD_SHED)

    def test_weak_evidence_deepens_verification(self):
        decision = select_path({
            "nominal_heartbeat_interval": 1.0,
            "observed_heartbeat_interval": 1.02,
            "evidence_currency": "WEAK",
        })
        self.assertEqual(decision.selected_path, DEEPEN_VERIFICATION)

    def test_authority_at_risk_uses_rollback_when_available(self):
        decision = select_path({
            "nominal_heartbeat_interval": 1.0,
            "observed_heartbeat_interval": 1.30,
            "missed_refresh_boundary": True,
            "rollback_available": True,
        })
        self.assertEqual(decision.degradation_state, AUTHORITY_AT_RISK)
        self.assertEqual(decision.selected_path, ROLLBACK_OR_RECONSTRUCT)

    def test_authority_at_risk_fails_closed_without_rollback(self):
        decision = select_path({
            "nominal_heartbeat_interval": 1.0,
            "observed_heartbeat_interval": 1.30,
            "missed_refresh_boundary": True,
            "rollback_available": False,
        })
        self.assertEqual(decision.degradation_state, AUTHORITY_AT_RISK)
        self.assertEqual(decision.selected_path, FAIL_CLOSED)

    def test_correlated_pressure_reports_degraded_state(self):
        decision = select_path({
            "nominal_heartbeat_interval": 1.0,
            "observed_heartbeat_interval": 1.25,
            "receipt_latency": "HIGH",
            "queue_depth": "HIGH",
        })
        self.assertEqual(decision.degradation_state, DEGRADED)

    def test_factor_bound_receipt_records_vector_and_rejected_paths(self):
        receipt = factor_bound_receipt({
            "nominal_heartbeat_interval": 1.0,
            "observed_heartbeat_interval": 1.02,
            "hash_drift": True,
        })
        self.assertEqual(receipt["receipt_type"], "factor_bound_path_selection")
        self.assertEqual(receipt["selected_path"], REFRESH_DERIVED_STATE)
        self.assertIn("state_vector", receipt)
        self.assertIn(CONTINUE, receipt["rejected_paths"])


if __name__ == "__main__":
    unittest.main()
