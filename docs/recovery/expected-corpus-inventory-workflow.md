# Expected Corpus Inventory Workflow

Status: merged to `main`.

The `Expected Corpus Inventory` workflow runs automatically on `push` and `pull_request`.

It also remains available through `workflow_dispatch`.

Artifact: `expected-corpus-inventory`

Primary repair files:

- `expected_corpus_failed_fixtures.md`
- `expected_corpus_failed_fixtures.json`

Shared writer:

- `tools/write_expected_corpus_failed_summary.py`

Schema contract:

- inventory root must be a JSON object
- `failed_fixtures` must be a list when present
- every `failed_fixtures` row must be an object
- `fixture` must be scalar when present
- `path` must be scalar when present
- `failed_checks` must be a list when present
- every `failed_checks` entry must be scalar

Failure behavior:

- malformed JSON fails loudly
- malformed schema fails loudly
- malformed inputs must not produce partial summary artifacts
- bad CLI usage returns exit code `2`
