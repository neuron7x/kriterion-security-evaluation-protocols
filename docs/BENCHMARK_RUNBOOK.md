# Benchmark Runbook — KRITERION

## Objective
Run the protocol benchmark in a way that supports public, defensible claims.

## Required artifacts before the first run
- benchmark/dataset_manifest.json
- benchmark/prompt_bundle/
- benchmark/human_raters.csv
- benchmark/adjudication_rules.md
- benchmark/adversarial_manifest.json
- benchmark/results/
- benchmark/compute_metrics.py or equivalent notebook/script

## Required logging per run
1. provider
2. exact model ID
3. reasoning mode / effort
4. tool configuration
5. timestamp
6. prompt bundle hash
7. token counts
8. raw per-case outputs
9. gate outcomes
10. final classification

## Human rating protocol
- minimum 3 independent raters
- raters score tasks on the same 0-5 rubric
- disagreements are adjudicated into a canonical label set
- record weighted inter-rater reliability before model comparison

## Minimum repeated-run protocol
- 5 runs per model for consistency claims
- fixed benchmark input set
- stable system prompt
- no silent prompt edits between runs

## Mandatory outputs
- benchmark/metrics.json
- benchmark/case_level_results.csv
- benchmark/confusion_matrices/
- benchmark/reproducibility.md

## Publication rule
Do not publish results as validated unless:
- raw manifests are present,
- metric code is present,
- model identifiers are exact,
- human labels are archived,
- adversarial taxonomy is recorded.


## Full demo execution path
```bash
python tools/reference_runner.py examples/worked-example/SE_WORKED_EXAMPLE_INPUT.json --output examples/worked-example/SE_WORKED_EXAMPLE_OUTPUT.json
python benchmark/benchmark_runner.py
python tools/validate_json.py schemas/evaluation-result.schema.json examples/worked-example/SE_WORKED_EXAMPLE_OUTPUT.json
```
