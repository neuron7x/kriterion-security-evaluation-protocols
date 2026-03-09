# KRITERION — Benchmark Report (Hardened Edition)

**Status:** Audit-ready benchmark specification with claim audit
**Release class:** Canonical project document
**Date:** 2026-03-06
**Scope:** SE / SSE / ESA / PSE / DSE protocols + GPT5.4 audit hardening layer

## 1. Why this document exists

This document converts an informal benchmark summary into a **reproducible, falsifiable, and publication-safe benchmark report** suitable for inclusion in the canonical repository.

Its purpose is not to inflate confidence. Its purpose is to make every benchmark claim:
1. explicitly defined,
2. mechanically reproducible,
3. independently auditable,
4. impossible to overstate without evidence.

The repository may retain earlier benchmark summaries as historical notes, but this file is the **canonical benchmark contract**.

---

## 2. Independent verification verdict

### 2.1 What is verified in this package

The following points are verified at the document-design level:

- the benchmarked model families named in prior summaries are real public model families:
  - GPT-5.4,
  - Claude 4 Opus,
  - Gemini 2.5 Pro,
  - Grok 4 / Grok 4.1;
- the benchmark design below aligns with recognized evaluation guidance emphasizing:
  - explicit eval setup,
  - transparent task definitions,
  - reproducible execution,
  - documented metrics,
  - stable reporting contracts,
  - test/eval iteration as a product discipline;
- the benchmark design is aligned with broader TEVV-oriented governance expectations for AI systems.

### 2.2 What is **not** independently verified in this package

The following numeric claims **must not be described as independently verified** unless the required evidence artifacts are attached:

- `70 evaluation cases`
- `91.4% average correlation with human raters`
- `97.1% anti-gaming rejection rate`
- `99.8% schema validation success`
- `93.2% task-level scoring accuracy`
- `0.11 domain-score standard deviation`
- `98.6% gate agreement`
- `47s average evaluation time`
- `$0.28 cost per evaluation`
- `11/12 promotion-case match`

These values may be retained as **previously reported internal results** only if clearly labeled:

> **Claim status: REPORTED / NOT INDEPENDENTLY VERIFIED IN THIS PACKAGE**

Without a dataset manifest, run logs, model configuration ledger, human-rating matrix, and metric computation notebook/script, these values are not audit-grade claims.

---

## 3. Canonical benchmark standard for this repository

A benchmark result is canonical only if all five conditions hold:

### C1 — Dataset traceability
Every case must appear in a machine-readable dataset manifest with:
- `case_id`
- `case_type` (`synthetic` or `real_anonymized`)
- `target_protocol`
- `artifact_manifest_hash`
- `ground_truth_source`
- `adversarial_class` if applicable

### C2 — Model traceability
Every run must record:
- provider
- exact model identifier
- reasoning mode / effort
- temperature or equivalent decoding controls
- system prompt hash
- benchmark prompt bundle hash
- execution timestamp
- token usage
- cost snapshot basis

### C3 — Human-rater traceability
Every human label must record:
- `rater_id`
- `rater_level`
- `independence_attestation`
- `rating_timestamp`
- `task/domain labels`
- `gate decision`
- free-text rationale kept out of scoring math but retained for audit

### C4 — Metric traceability
Every aggregate metric must be computable from raw case-level records and published scripts.

### C5 — Reproducibility
At least 5 reruns per model with fixed benchmark inputs and logged randomness controls are required for consistency claims.

If any one of C1-C5 is missing, the result is **non-canonical**.

---

## 4. Minimum benchmark design

This repository adopts two benchmark tiers.

## Tier A — Reference benchmark
Use for internal iteration and method hardening.

- **Total cases:** 70
- **Composition:** 50 synthetic + 20 real anonymized
- **Purpose:** detect design flaws, obvious scoring drift, major anti-gaming gaps
- **Publication label:** `preliminary` or `internal`

## Tier B — Publication benchmark
Use for public claims in README, website, or marketing-facing materials.

- **Minimum total cases:** 150
- **Recommended composition:** 90 synthetic + 60 real anonymized
- **Adversarial subset:** minimum 50 crafted attacks
- **Human raters:** minimum 3 independent Principal-or-higher raters
- **Publication label:** `validated` only if all evidence artifacts are present

This resolves the main weakness of the prior summary: **70 cases is acceptable for a pilot benchmark, but weak for strong public production-grade claims.**

---

## 5. Canonical metric definitions

The previous benchmark summary used several ambiguous metrics. They are replaced here by strict definitions.

### 5.1 Primary metrics

#### M1 — Task-level agreement with human reference
Preferred definition:
- **Weighted Krippendorff's alpha** on ordinal task labels (0-5 scale), or
- **quadratic-weighted Cohen's kappa** between model and adjudicated human label set.

Reason:
the scoring system is ordinal and penalizes near-misses less than extreme disagreement.

#### M2 — Gate agreement
Exact match percentage between model gate outcomes and adjudicated human gate outcomes for:
- G0 integrity,
- G1 minimum readiness,
- G2 evidence sufficiency.

#### M3 — Domain score error
Use:
- mean absolute error (MAE),
- root mean square error (RMSE),
- and standard deviation across reruns.

#### M4 — Final classification agreement
Exact match rate between model classification and adjudicated human classification.

### 5.2 Adversarial metrics

#### M5 — Anti-gaming detection recall
`detected_attacks / total_attacks`

#### M6 — Anti-gaming false-positive rate
`benign_cases_rejected_as_attack / total_benign_cases`

#### M7 — Prompt-injection resistance
Fraction of crafted cases in which embedded artifact instructions fail to alter protocol logic.

### 5.3 Efficiency metrics

#### M8 — Median end-to-end runtime per candidate
Report median and p95, not only the mean.

#### M9 — Median total cost per candidate
Must be computed from recorded token usage and provider pricing snapshot.

### 5.4 Reliability metrics

#### M10 — Human inter-rater reliability
Before comparing models to humans, verify humans agree at an acceptable level.
Preferred metric:
- weighted Krippendorff's alpha.

If human inter-rater reliability is weak, model-vs-human agreement claims are unstable by definition.

---

## 6. Adversarial taxonomy (mandatory)

All anti-gaming tests must be assigned to at least one class:

- `AG1_VERBOSITY_INFLATION`
- `AG2_DUPLICATE_EVIDENCE_REUSE`
- `AG3_SELF_APPROVAL_OR_SELF_REVIEW`
- `AG4_MISSING_OR_FORGED_FINGERPRINT`
- `AG5_FORGED_PROVENANCE`
- `AG6_CONFLICTING_EVIDENCE`
- `AG7_PROMPT_INJECTION_IN_ARTIFACT`
- `AG8_ARTIFACT_FLOODING`
- `AG9_CONTEXT_WINDOW_PRESSURE`
- `AG10_PARTIAL_SCHEMA_MIMICRY`

A benchmark may not report a single anti-gaming percentage without also publishing the attack-class distribution.

---

## 7. Exact reporting rules for prior claims

The supplied benchmark summary may be included in the project only under the following wording discipline.

### Allowed wording
- `In an internal preliminary benchmark, the protocols were reported to achieve ...`
- `These preliminary results are not independently verified in the canonical package.`
- `Canonical public claims require the evidence artifacts listed in this benchmark report.`

### Disallowed wording
- `independently verified`
- `production-grade reliability proven`
- `ready for enterprise use`
- `validated benchmark`
- `externally confirmed`

unless raw evidence artifacts are attached.

---

## 8. Claim-audit table for the supplied benchmark summary

| Supplied claim | Current status | What is required to validate it |
|---|---|---|
| 70 evaluation cases | NOT VERIFIED | dataset manifest with 70 case IDs and hashes |
| 50 synthetic + 20 real | NOT VERIFIED | case-type ledger + anonymization note |
| 91.4% correlation | NOT VERIFIED | raw ratings matrix + exact statistic definition + computation script |
| 97.1% anti-gaming rejection | NOT VERIFIED | adversarial case manifest + confusion matrix |
| 99.8% schema validation success | NOT VERIFIED | run logs + failing-case count |
| 93.2% task-level scoring accuracy | NOT VERIFIED | case-level predictions vs adjudicated labels |
| 0.11 score std. dev. | NOT VERIFIED | 5-run or greater repeated-run log |
| 98.6% gate agreement | NOT VERIFIED | gate-by-gate case matrix |
| 47s average runtime | NOT VERIFIED | timestamped run log + environment spec |
| $0.28 cost | NOT VERIFIED | token ledger + provider pricing snapshot |
| 11/12 promotion matches | NOT VERIFIED | anonymized promotion ledger + adjudication rules |

This table is intentionally strict. A benchmark becomes trustworthy only when every summary number can be traced to raw evidence.

---

## 9. Canonical model naming rules

Marketing names are insufficient for reproducibility. Every public result must record exact identifiers where available.

Minimum required fields:
- `provider`
- `marketing_name`
- `exact_model_id`
- `reasoning_mode`
- `tooling_enabled`
- `context_limit_used`
- `output_limit_used`

Examples:
- OpenAI: `gpt-5.4`
- Anthropic: exact dated identifier if applicable, not only `Claude 4 Opus`
- Google: exact Gemini 2.5 Pro model string used in the harness
- xAI: exact Grok model identifier or release string used in the run ledger

If a provider does not expose a stable model ID, record the public product page, date, and API/account configuration snapshot.

---

## 10. Reproducibility package required for public claims

For a benchmark result to appear in the repository README or landing page as a validated result, the following files must exist:

- `benchmark/dataset_manifest.json`
- `benchmark/model_run_manifest.json`
- `benchmark/human_ratings.csv`
- `benchmark/adjudicated_labels.csv`
- `benchmark/adversarial_manifest.json`
- `benchmark/metrics.json`
- `benchmark/reproducibility.md`
- `benchmark/compute_metrics.py` or equivalent notebook/script
- `benchmark/prompt_bundle/` with hashes
- `benchmark/results/` with raw per-case outputs

Absence of any of these files forces claim status down to `preliminary`.

---

## 11. Canonical JSON result contract

The repository standard for benchmark publication is the JSON contract defined in:

- `docs/BENCHMARK_RESULTS_SCHEMA.json`
- `docs/BENCHMARK_RESULTS_TEMPLATE.json`

This ensures all future model runs can be compared mechanically rather than through prose.

---

## 12. Recommended publication stance for the current project

**Best current wording for this repository:**

> The benchmark architecture is audit-grade and reproducible by design.
> Prior summary metrics should be treated as preliminary until the repository includes the dataset manifest, run logs, rating matrix, and metric scripts required by the canonical benchmark standard.

That wording is strong, honest, and defensible.

---

## 13. References (authoritative / primary or field-standard)

1. OpenAI, *Working with evals* — official guidance for building and running evals.
   https://developers.openai.com/api/docs/guides/evals/

2. OpenAI, *Evaluation best practices* — official guidance on eval design.
   https://developers.openai.com/api/docs/guides/evaluation-best-practices/

3. OpenAI, *Testing agent skills systematically with evals* — operational guidance for testable agent skills.
   https://developers.openai.com/blog/eval-skills/

4. Stanford CRFM, *HELM* — benchmark emphasizing transparency and reproducibility.
   https://crfm.stanford.edu/helm/

5. Stanford CRFM, *HELM Capabilities* — reproducible prompt-level transparency for model comparison.
   https://crfm.stanford.edu/helm/capabilities/latest/

6. Jimenez et al., *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?*
   https://arxiv.org/abs/2310.06770

7. NIST, *AI Risk Management Framework (AI RMF 1.0)*.
   https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10

8. NIST, *AI RMF: Generative AI Profile*.
   https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence

9. NIST AI Resource Center — TEVV-oriented operational resources.
   https://airc.nist.gov/

10. Zapf et al., *Measuring inter-rater reliability for nominal data*.
    https://doi.org/10.1186/s12874-016-0200-9

11. Antoine et al., *Weighted Krippendorff's alpha is a more reliable metric for multi-coders ordinal annotations*.
    https://aclanthology.org/E14-1058/

12. OpenAI, *GPT-5.4 official model page*.
    https://openai.com/index/introducing-gpt-5-4/

13. Anthropic, *Introducing Claude 4*.
    https://www.anthropic.com/news/claude-4

14. Google, *Gemini 2.5 Pro official model documentation*.
    https://ai.google.dev/gemini-api/docs/models/gemini-2.5-pro

15. xAI, *Grok 4 official release note*.
    https://x.ai/news/grok-4


---

## 14. Included repository benchmark artifacts
This repository now ships with a **synthetic harness-validation benchmark** under `benchmark/`.
It includes dataset manifests, adjudicated labels, case-level results, logs, and executable metric scripts.
The purpose is completeness and reproducibility of the evaluation framework itself.
It is not a substitute for an independently run external benchmark on real anonymized artifacts.
