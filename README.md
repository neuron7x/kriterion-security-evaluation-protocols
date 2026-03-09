# KRITERION

*Fail-Closed Security Capability Evaluation Framework*


<p align="center">
  <img src="assets/img/logo.svg" alt="Repository logo" width="112" />
</p>

<p align="center">
  <strong>Protocolized intelligence · evidence-first evaluation · execution-grade hardening · complete community edition</strong>
</p>

<p align="center">
  <a href="index.html">Live Index</a> ·
  <a href="system-map.html">System Map</a> ·
  <a href="protocol-explorer.html">Protocol Explorer</a> ·
  <a href="benchmark-dashboard.html">Benchmark Dashboard</a> ·
  <a href="doctrine.html">Doctrine Index</a>
</p>

---

## What this repository is

A complete community edition of an audit-grade evaluation framework for security roles and frontier prompt architecture.
It includes:
- role protocols
- an execution-grade GPT5.4 hardening layer
- machine-readable schemas
- runnable examples
- a synthetic benchmark demo with manifests, logs, and metric scripts
- Pages-ready visual presentation
- licensing and commercial-permissions templates

This repository is a runnable demonstration framework with executable examples, schemas, tools, and licensing boundaries already in place.

---

## Why this exists

Every existing security capability evaluation framework has the same flaw:
it fails open.

Missing evidence → evaluator fills the gap with narrative judgment.
Confident-sounding candidate → scores drift upward.
Self-attested credentials → treated as evidence.

This repository is the correction.

Six protocols. Fail-closed gates. Evidence Confidence tiering that caps scores
when artifacts can't be independently verified. Anti-gaming enforcement that
detects artifact reuse and self-referential approval loops. Prompt injection
resistance that treats artifact content as data, not instructions.

The first system where the evaluation cannot be fooled by the candidate being
better at communicating than at security engineering.

## License

Community tier:
- `LICENSE.txt` / `LICENSE.md` — Audit-Grade Community License 1.0 (AGCL-1.0)

Commercial tier:
- `SOVEREIGN_TERMS.md`
- `COMMERCIAL_LICENSE_AGREEMENT_TEMPLATE.md`
- `NOTICE.md`
- `TRADEMARK_USAGE_GUIDELINES.md`

The community tier is restrictive by design: non-commercial sharing of complete unmodified copies only; no commercial use; no white-labeling; no AI training / embedding / RAG ingestion.

---

## Run a worked example

```bash
python tools/reference_runner.py examples/worked-example/SE_WORKED_EXAMPLE_INPUT.json --output examples/worked-example/SE_WORKED_EXAMPLE_OUTPUT.json
python tools/validate_json.py schemas/evaluation-result.schema.json examples/worked-example/SE_WORKED_EXAMPLE_OUTPUT.json
```

## Run the synthetic demo benchmark

```bash
python benchmark/benchmark_runner.py
```

Outputs are written to:
- `examples/worked-example/`
- `benchmark/results/`
- `benchmark/metrics.json`
- `benchmark/logs/demo_benchmark_run.log`

---

## Repository layout

```text
.
├── index.html
├── system-map.html
├── protocol-explorer.html
├── benchmark-dashboard.html
├── doctrine.html
├── execution-layer.html
├── LICENSE.txt
├── LICENSE.md
├── NOTICE.md
├── COMMERCIAL_LICENSE_AGREEMENT_TEMPLATE.md
├── TRADEMARK_USAGE_GUIDELINES.md
├── CHANGELOG.md
├── ROADMAP.md
├── VERSION
├── robots.txt
├── protocols/
├── schemas/
├── execution/
├── examples/
├── benchmark/
├── docs/
├── tools/
├── self-evaluation/
└── assets/
```

---

## Worked example and traces

The repository includes a full end-to-end worked example under `examples/worked-example/`:
- input bundle
- output result
- evidence trace CSV
- worked-example notes

---

## Benchmark note

The included benchmark is a **synthetic harness-validation benchmark**. It proves completeness, reproducibility, and execution path for the framework itself.
It does **not** claim independently verified real-world superiority over frontier models.

---

## Integrity and reproducibility

- `MANIFEST.json` provides SHA-256 fingerprints for repository files
- `tools/verify_manifest.py` verifies repository integrity
- `schemas/` define machine-readable contracts
- `execution/` documents the deterministic run path

### Self-evaluation proof surface

Deterministic self-evaluation artifacts live under `self-evaluation/`:
- `self-evaluation/kriterion-self-eval-bundle.json`
- `self-evaluation/kriterion-self-eval-result.json`
- `self-evaluation/REPRODUCIBILITY.md`

Local verification:

```bash
python tools/validate_json.py schemas/reference-input-bundle.schema.json self-evaluation/kriterion-self-eval-bundle.json
python tools/validate_json.py schemas/evaluation-result.schema.json self-evaluation/kriterion-self-eval-result.json
python tools/verify_execution_chain.py --input self-evaluation/kriterion-self-eval-bundle.json --result self-evaluation/kriterion-self-eval-result.json
python tools/reference_runner.py self-evaluation/kriterion-self-eval-bundle.json --output /tmp/kriterion-self-eval-result.repro.json
diff -u self-evaluation/kriterion-self-eval-result.json /tmp/kriterion-self-eval-result.repro.json
```

---

## Visual identity

The repository interface uses a constrained black / white / signal-red visual system, documented in:
- `docs/REPO_VISUAL_SYSTEM_2026.md`
- `docs/DESIGN_SOURCES_2026.md`

The design is intentionally severe, high-contrast, and non-template.


## Business activation layer

Core business documents:
- `METHODOLOGY.md`
- `THREAT_MODEL_FOR_AI_EVALUATION.md`
- `SOVEREIGN_TERMS.md`
- `FIELD_REPORT.md`
- `COGNITIVE_FINGERPRINT.md`

Commercial and go-to-market documents:
- `business/LINKEDIN_POST_01_PRIMARY.md`
- `business/LINKEDIN_POST_02_EVIDENCE_CONFIDENCE.md`
- `business/LINKEDIN_POST_03_ANTI_GAMING.md`
- `business/LINKEDIN_POST_04_UKRAINE_CONTEXT.md`
- `business/GUMROAD_PRODUCT_LISTING.md`
- `business/COMMERCIAL_INQUIRY_EMAIL.md`
- `business/GITHUB_METADATA.md`
- `business/TIMESTAMP_PRIORITY_EVIDENCE_BRIEF.md`
