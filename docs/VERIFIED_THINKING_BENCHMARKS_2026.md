# VERIFIED THINKING BENCHMARKS 2026

## Purpose

This document defines the benchmark philosophy and publication discipline for evaluating the project’s reasoning quality, protocol robustness, and evidence-handling behavior.

It is intentionally strict.

The objective is not to manufacture flattering numbers. The objective is to make benchmark claims worthy of long-term scrutiny.

This document should be read together with:
- `docs/BENCHMARK_REPORT_2026.md`
- `docs/BENCHMARK_RUNBOOK.md`
- `docs/BENCHMARK_RESULTS_SCHEMA.json`
- `docs/BENCHMARK_RESULTS_TEMPLATE.json`

---

## 1. What “verified thinking” means in this project

“Verified thinking” does not mean:
- the model sounds intelligent,
- the model explains itself elegantly,
- the model agrees with the author,
- the benchmark produced high summary numbers once.

Within this repository, verified thinking means the system can demonstrate, under controlled evaluation:
- disciplined handling of evidence,
- stable scoring under repeat runs,
- resistance to adversarial manipulation,
- bounded uncertainty,
- output compatibility with mechanical review.

The benchmark is therefore about the quality of governed cognition, not only answer quality.

---

## 2. Benchmark object of evaluation

The benchmarked object is not just the base model.

The benchmarked object is the full execution unit:
- model,
- protocol,
- system prompt/kernel,
- routing rules,
- evidence normalization layer,
- tool configuration,
- output contract,
- evaluation harness.

This matters because benchmark claims become meaningless if they blur model capability with protocol capability.

---

## 3. Benchmark tiers

### Tier 1 — Exploratory
Used for rapid iteration and weakness discovery.
Claims must remain internal or clearly labeled preliminary.

### Tier 2 — Reference
Used for stable internal comparison across protocols, models, or versions.
Requires documented datasets, run manifests, and metric definitions.

### Tier 3 — Public validated
Used for README, landing page, and external project claims.
Requires full reproducibility package and strict claim governance.

This tiering prevents a common failure mode: publishing pilot results with production language.

---

## 4. Core benchmark dimensions

### Dimension A — Evidence discipline
Can the system distinguish primary from secondary evidence?
Can it refuse unsupported conclusions?

### Dimension B — Structural correctness
Does the system normalize artifacts, satisfy schemas, and preserve canonical output form?

### Dimension C — Scoring fidelity
Do task/domain/gate decisions align with adjudicated human references under explicit metrics?

### Dimension D — Adversarial resistance
Can the system resist duplication, injection, forged provenance, missing fingerprints, and artifact flooding?

### Dimension E — Reproducibility
Do repeated runs remain acceptably stable under fixed conditions?

### Dimension F — Efficiency
Can the protocol deliver reliable outputs with tractable time and cost?

These dimensions together are a better measure than one composite number.

---

## 5. Metrics philosophy

A benchmark should prefer metrics that preserve interpretability.

Recommended metric family:
- weighted agreement metrics for ordinal task scores,
- exact match for gates and final classifications,
- MAE / RMSE for domain scores,
- recall and false-positive rate for anti-gaming behavior,
- median and p95 for runtime and cost,
- inter-rater reliability for human baselines.

A benchmark should avoid ambiguous vanity metrics, especially when the calculation method is not explicit.

---

## 6. Human benchmark discipline

Human evaluators are not an oracle merely because they are senior.

A serious human benchmark requires:
- minimum three independent raters,
- common rubric,
- documented adjudication,
- role-appropriate expertise,
- independence attestation,
- archived disagreements.

Before claiming model-human agreement, the benchmark must first establish that human-human agreement is sufficiently stable.

Otherwise model agreement is being measured against noise.

---

## 7. Adversarial benchmark discipline

A system that has not been attacked has not yet been benchmarked seriously.

Mandatory adversarial classes should include:
- verbosity inflation,
- duplicate evidence reuse,
- self-review masquerading as independence,
- missing or forged fingerprints,
- forged provenance,
- conflicting evidence bundles,
- prompt injection inside artifacts,
- context flooding,
- partial-schema mimicry.

Adversarial testing should not be a footnote. It should be a first-class benchmark track.

---

## 8. Claim governance

This repository distinguishes between:
- **reported** results,
- **validated** results,
- **superseded** results,
- **withdrawn** results.

A result may only be labeled **validated** when:
- raw manifests exist,
- model identifiers are exact,
- prompt bundle hashes are recorded,
- human labels are archived,
- metric code is present,
- repeated runs are logged.

This is the minimum bar for benchmark dignity.

---

## 9. Benchmark output contract

Every benchmark publication should be convertible into machine-readable form and should include:
- report metadata,
- dataset manifest,
- model run manifest,
- human rater ledger,
- metrics,
- claim status,
- reproducibility instructions.

This prevents the benchmark from becoming prose that cannot be recomputed.

---

## 10. What this document refuses

It refuses:
- unqualified “independently verified” language without evidence,
- benchmark summaries without methods,
- high confidence from one-off runs,
- model comparisons without exact identifiers,
- adversarial percentages without attack taxonomy,
- publication claims disconnected from raw artifacts.

These refusals protect the project more than inflated metrics ever could.

---

## 11. Strategic value

Why invest in such strict benchmark discipline?

Because it creates:
- durable trust,
- easier collaboration,
- clearer iteration loops,
- better failure diagnosis,
- safer public claims,
- stronger differentiation from generic prompt packs.

A protocol project without benchmark governance remains impressionistic.
A protocol project with benchmark governance becomes a serious engineering artifact.

---

## 12. Canonical publication stance

The strongest honest stance is:

> The benchmark architecture is designed for reproducibility and audit.  
> Public performance claims become validated only when raw case manifests, run logs, adjudicated labels, and metric scripts are published in the canonical benchmark structure.

That stance is stronger than inflated certainty because it survives scrutiny.

---

## Closing statement

Verified thinking is not a metaphor in this repository.

It is a benchmark discipline for proving that a reasoning system:
- respects evidence,
- stays inside protocol,
- resists manipulation,
- produces repeatable outputs,
- and remains legible under audit.

That is the benchmark worth defending.
