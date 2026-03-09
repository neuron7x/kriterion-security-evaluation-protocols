# Protocol Validation Tests

## Purpose

These tests exist to demonstrate that the hardening layer is executable and verifiable.
They provide concrete positive and negative cases for schema validation and
execution-contract behavior.

## Positive tests

1. `fixtures/artifact.valid.json`
   - must validate against `schemas/canonical-artifact.schema.json`
2. `fixtures/evaluation-result.valid.json`
   - must validate against `schemas/evaluation-result.schema.json`
3. `examples/canonical_artifact.example.json`
   - must produce a stable SHA-256 under `tools/canonicalize_and_hash.py`

## Negative tests

1. `fixtures/artifact.invalid.missing-valid-fingerprint.json`
   - must fail integrity expectations even if it may pass superficial JSON typing
2. `fixtures/evaluation-result.invalid.bad-gate.json`
   - must fail schema validation because `gate_id` is not canonical

## Suggested commands

```bash
python tools/validate_json.py schemas/canonical-artifact.schema.json tests/fixtures/artifact.valid.json
python tools/validate_json.py schemas/evaluation-result.schema.json tests/fixtures/evaluation-result.valid.json
python tools/canonicalize_and_hash.py examples/canonical_artifact.example.json
python tools/verify_manifest.py MANIFEST.json .
```

## Expected behavior

- valid fixtures return `VALID`
- invalid gate fixture must raise a schema validation error
- manifest verification returns `MANIFEST_OK` after package creation


## Additional complete-run tests

```bash
python tools/reference_runner.py examples/worked-example/SE_WORKED_EXAMPLE_INPUT.json --output examples/worked-example/SE_WORKED_EXAMPLE_OUTPUT.json
python tools/validate_json.py schemas/evaluation-result.schema.json examples/worked-example/SE_WORKED_EXAMPLE_OUTPUT.json
python benchmark/benchmark_runner.py
```
