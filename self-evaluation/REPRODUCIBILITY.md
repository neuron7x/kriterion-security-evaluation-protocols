# Self-Evaluation Reproducibility

This report captures a full local validation and verification cycle for the
self-evaluation artifacts.

## Artifacts

- `self-evaluation/kriterion-self-eval-bundle.json`
- `self-evaluation/kriterion-self-eval-result.json`

## Validation commands and outcomes

1. Bundle schema validation

```bash
python3 tools/validate_json.py schemas/reference-input-bundle.schema.json self-evaluation/kriterion-self-eval-bundle.json
```

Outcome: `VALID`

2. Result schema validation

```bash
python3 tools/validate_json.py schemas/evaluation-result.schema.json self-evaluation/kriterion-self-eval-result.json
```

Outcome: `VALID`

3. Execution-chain verification

```bash
python3 tools/verify_execution_chain.py --input self-evaluation/kriterion-self-eval-bundle.json --result self-evaluation/kriterion-self-eval-result.json
```

Outcome:

- `status`: `VERIFIED`
- `result_terminal_hash`: `b88b377a094fcea33f023458bf4ec80f5e75ebbcbfaa40899c017ac0f246d033`
- `input_bundle_hash`: `5d82bc55a3db0b0ec47c0128f93d101308ee5f92048f0fb738253f3fd05fc212`

4. Deterministic regeneration check

```bash
python3 tools/reference_runner.py self-evaluation/kriterion-self-eval-bundle.json --output /tmp/kriterion-self-eval-result.repro.json

diff -u self-evaluation/kriterion-self-eval-result.json /tmp/kriterion-self-eval-result.repro.json
```

Outcome: `diff` returned no differences (bit-for-bit deterministic reproduction).

5. Full repository test harness

```bash
pytest -q
```

Outcome: `95 passed, 2 warnings, 9 subtests passed`

6. Governance baseline

```bash
python tools/validate_governance.py
```

Outcome: `GOVERNANCE_OK`

7. Manifest integrity

```bash
python tools/verify_manifest.py MANIFEST.json .
```

Outcome: `MANIFEST_OK`

## Readiness verdict

Self-evaluation artifacts are schema-valid, cryptographically verified,
deterministically reproducible, and compatible with current governance and test
baselines.
