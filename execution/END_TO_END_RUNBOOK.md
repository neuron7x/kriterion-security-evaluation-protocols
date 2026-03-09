# End-to-End Runbook

## Goal
Produce a complete evaluation result from an input bundle.

## Full execution path
```bash
python tools/reference_runner.py examples/worked-example/SE_WORKED_EXAMPLE_INPUT.json --output examples/worked-example/SE_WORKED_EXAMPLE_OUTPUT.json
python tools/validate_json.py schemas/evaluation-result.schema.json examples/worked-example/SE_WORKED_EXAMPLE_OUTPUT.json
python benchmark/benchmark_runner.py
python tools/verify_manifest.py MANIFEST.json
```

## Outputs
- validated `EvaluationResult`
- benchmark results CSV and JSON
- run log
- manifest verification

## Failure handling
- invalid fingerprint -> G0 fail
- injection phrase in artifact -> G0 fail
- no admissible evidence -> G2 fail
- must-have domain score below threshold -> G1 fail
