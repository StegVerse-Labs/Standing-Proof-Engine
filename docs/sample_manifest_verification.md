# Sample Manifest Verification

## Assumption

The sample manifest is the public route package for the current SPE proof corpus. It does not replace individual sample verification. It binds the declared samples into one route-level verification pass.

## Done Criteria

Manifest verification is done when a verifier can run one command and confirm:

```text
pressure receipt trace -> expected SPE result PARTIAL
stale-state proof -> expected SPE result PASS
Aegis incident standing proof -> expected SPE result PASS
all declared governance results -> DENY
manifest result -> PARTIAL
```

The manifest result is `PARTIAL` because the pressure receipt sample intentionally contains a partial proof condition. That is expected and not a workflow failure.

## Manifest

```text
samples/manifest.json
```

## Command

```bash
python spe/verify_manifest.py samples/manifest.json
```

## Expected Shape

```json
{
  "manifest_id": "SPE-SAMPLE-MANIFEST-001",
  "sample_count": 3,
  "spe_result": "PARTIAL",
  "samples": [
    {
      "path": "samples/pressure_demo_001.json",
      "route": "pressure_receipt_trace",
      "spe_result": "PARTIAL",
      "governance_result": "DENY",
      "matches_expectation": true
    },
    {
      "path": "samples/stale_state_review_commit_001.json",
      "route": "stale_state_review_to_commit",
      "spe_result": "PASS",
      "governance_result": "DENY",
      "matches_expectation": true
    },
    {
      "path": "samples/aegis_incident_standing_001.json",
      "route": "incident_standing_proof",
      "spe_result": "PASS",
      "governance_result": "DENY",
      "matches_expectation": true
    }
  ]
}
```

## Governance Meaning

The manifest proves that the public SPE sample corpus is internally coherent:

```text
The pressure case proves a partial but reconstructable drift denial.
The stale-state case proves prior review does not carry stale execution standing.
The Aegis case proves incident detection does not authorize defensive consequence by itself.
```

## Use in Automation

The workflow should run both individual samples and the manifest. Individual sample verification identifies local failures. Manifest verification proves the declared route package remains aligned with expected SPE and governance results.
