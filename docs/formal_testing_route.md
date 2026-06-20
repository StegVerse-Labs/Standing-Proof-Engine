# Formal Testing Route Reference

This repository is the standing-proof route.

It should consume standing-proof artifacts only after `StegVerse-org/StegVerse-SDK` has bound the artifact to a manifest and intake receipt.

## Required Flow

```text
Dataset / fixture / governance artifact
→ StegVerse-org/StegVerse-SDK ingestion
→ manifest binding
→ receipt binding
→ Standing-Proof-Engine route declaration
→ commit-time standing proof
→ standing result receipt
```

## Route Responsibility

Standing-Proof-Engine proves whether a reviewed artifact still has consequence-binding standing at commit time.

It is not a replacement for:

- `StegVerse-org/stegverse-demo-suite` public demos;
- `StegVerse-org/demo-suite-runner` formalism probes;
- `StegGhost/entity-sandbox-runner` adversarial sandbox testing;
- `StegVerse-Labs/Boundary-Test` GLM-style boundary cases.

## Receipt Rule

Every standing result must preserve the SDK intake manifest reference and SDK intake receipt reference.
