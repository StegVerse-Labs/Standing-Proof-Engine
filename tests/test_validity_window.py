from datetime import datetime, timezone
import unittest

from spe.validity_window import (
    CONSUME,
    FAIL_CLOSED,
    PENDING,
    QUARANTINE,
    REFRESH_IN_PARALLEL,
    ROTATE,
    evaluate_validity_window,
)


def at(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


class ValidityWindowTests(unittest.TestCase):
    def test_current_material_consumes_inside_validity_window_before_refresh(self):
        record = {
            "token_ref": "token-a",
            "valid_from": "2026-06-24T03:00:00Z",
            "expires_at": "2026-06-24T03:10:00Z",
            "refresh_after": "2026-06-24T03:08:00Z",
            "refresh_deadline": "2026-06-24T03:09:30Z",
        }
        decision = evaluate_validity_window(record, at("2026-06-24T03:05:00Z"))
        self.assertEqual(decision.result, CONSUME)
        self.assertEqual(decision.consume_ref, "token-a")

    def test_refresh_window_opens_while_current_material_remains_consumable(self):
        record = {
            "token_ref": "token-a",
            "valid_from": "2026-06-24T03:00:00Z",
            "expires_at": "2026-06-24T03:10:00Z",
            "refresh_after": "2026-06-24T03:08:00Z",
            "refresh_deadline": "2026-06-24T03:09:30Z",
        }
        decision = evaluate_validity_window(record, at("2026-06-24T03:08:10Z"))
        self.assertEqual(decision.result, REFRESH_IN_PARALLEL)
        self.assertEqual(decision.consume_ref, "token-a")

    def test_expired_current_material_rotates_to_ready_successor(self):
        record = {
            "token_ref": "token-a",
            "valid_from": "2026-06-24T03:00:00Z",
            "expires_at": "2026-06-24T03:10:00Z",
            "refresh_after": "2026-06-24T03:08:00Z",
            "refresh_deadline": "2026-06-24T03:09:30Z",
            "successor": {
                "token_ref": "token-b",
                "valid_from": "2026-06-24T03:09:30Z",
                "expires_at": "2026-06-24T03:20:00Z",
            },
        }
        decision = evaluate_validity_window(record, at("2026-06-24T03:10:00Z"))
        self.assertEqual(decision.result, ROTATE)
        self.assertEqual(decision.consume_ref, "token-b")

    def test_expired_current_material_without_successor_fails_closed(self):
        record = {
            "token_ref": "token-a",
            "valid_from": "2026-06-24T03:00:00Z",
            "expires_at": "2026-06-24T03:10:00Z",
            "refresh_after": "2026-06-24T03:08:00Z",
            "refresh_deadline": "2026-06-24T03:09:30Z",
        }
        decision = evaluate_validity_window(record, at("2026-06-24T03:10:00Z"))
        self.assertEqual(decision.result, FAIL_CLOSED)

    def test_missed_refresh_deadline_before_expiry_fails_closed(self):
        record = {
            "token_ref": "token-a",
            "valid_from": "2026-06-24T03:00:00Z",
            "expires_at": "2026-06-24T03:10:00Z",
            "refresh_after": "2026-06-24T03:08:00Z",
            "refresh_deadline": "2026-06-24T03:09:30Z",
        }
        decision = evaluate_validity_window(record, at("2026-06-24T03:09:31Z"))
        self.assertEqual(decision.result, FAIL_CLOSED)

    def test_revoked_current_material_fails_closed(self):
        record = {
            "token_ref": "token-a",
            "valid_from": "2026-06-24T03:00:00Z",
            "expires_at": "2026-06-24T03:10:00Z",
            "revoked": True,
        }
        decision = evaluate_validity_window(record, at("2026-06-24T03:05:00Z"))
        self.assertEqual(decision.result, FAIL_CLOSED)

    def test_incomplete_validity_record_quarantines(self):
        decision = evaluate_validity_window({"token_ref": "token-a"}, at("2026-06-24T03:05:00Z"))
        self.assertEqual(decision.result, QUARANTINE)

    def test_not_yet_valid_is_pending(self):
        record = {
            "token_ref": "token-a",
            "valid_from": "2026-06-24T03:10:00Z",
            "expires_at": "2026-06-24T03:20:00Z",
        }
        decision = evaluate_validity_window(record, at("2026-06-24T03:05:00Z"))
        self.assertEqual(decision.result, PENDING)


if __name__ == "__main__":
    unittest.main()
