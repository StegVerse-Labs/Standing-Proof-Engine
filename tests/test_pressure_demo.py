import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.verify import PARTIAL, verify_trace


def test_pressure_demo_reports_partial_authority_proof():
    trace_path = ROOT / "samples" / "pressure_demo_001.json"
    trace = json.loads(trace_path.read_text(encoding="utf-8"))

    status, checks = verify_trace(trace)
    check_map = {check.name: check for check in checks}

    assert status == PARTIAL
    assert check_map["parse_trace"].status == "PASS"
    assert check_map["baseline_reconstruction"].status == "PASS"
    assert check_map["drift_observation"].status == "PASS"
    assert check_map["pressure_receipt"].status == "PASS"
    assert check_map["local_predicates"].status == "PASS"
    assert check_map["aggregate_admissibility"].status == "PASS"
    assert check_map["commit_boundary"].status == "PASS"
    assert check_map["replay_path"].status == "PASS"
    assert check_map["authority_context_proof"].status == "PARTIAL"
