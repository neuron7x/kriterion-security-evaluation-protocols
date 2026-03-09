# Quickstart

```bash
python tools/reference_runner.py examples/worked-example/SE_WORKED_EXAMPLE_INPUT.json --output examples/worked-example/SE_WORKED_EXAMPLE_OUTPUT.json
python tools/validate_json.py schemas/evaluation-result.schema.json examples/worked-example/SE_WORKED_EXAMPLE_OUTPUT.json
```

For the synthetic harness-validation benchmark:
```bash
python benchmark/benchmark_runner.py
```
