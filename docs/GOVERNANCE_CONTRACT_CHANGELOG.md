# Governance Contract Changelog

## 2026.24.0
- Closed required-regression execution gaps by adding `tests/semantic/test_reference_runner_injection_detection.py` and `tests/semantic/test_verify_ci_artifact_manifest.py` to required CI execution in `inv-python-entrypoints-and-compile`.
- Hardened governance self-hosting enforcement so validator fails closed if either semantic regression command is removed from required CI.
- Restored manifest truthfulness by adding tracked semantic regression file coverage for `tests/semantic/test_verify_ci_artifact_manifest.py`.

## 2026.23.0
- Shifted CI evidence model to artifact-first proof semantics by introducing explicit `artifact_class` categories (`required`, `optional`, `diagnostic`) and required-artifact assertions in `tools/verify_ci_artifact_manifest.py`.
- Added deterministic run-status proof artifacts (`worked-example.run.status.json`, `benchmark.run.status.json`) to producer manifests and required-name checks in artifact-provenance verification.
- Unified benchmark evidence staging to include per-case evaluation outputs in artifact evidence and kept parity gate fail-closed across metrics, case-level CSV, and case evaluation set.
- Hardened governance validator enforcement for required artifact-manifest contract tokens and run-status artifact generation, with regression coverage.

## 2026.22.0
- Eliminated benchmark regeneration nondeterminism by making `tools/reference_runner.py` evaluation timestamp deterministic (`evaluation_timestamp` input override, otherwise fixed epoch), so benchmark case outputs do not drift across runs.
- Expanded benchmark regenerated-output parity enforcement to include tracked per-case evaluation artifacts (`benchmark/results/case-*.evaluation.json`) in CI hard-fail parity checks.
- Synced validator enforcement and regression coverage to the expanded benchmark parity command contract.

## 2026.21.0
- Hardened canonicalization negative-case script import path handling so execution remains deterministic across direct script and `runpy` invocation modes.
- Hardened reference-runner injection detection by using normalized-whitespace regex policy matching instead of fragile plain substring checks.
- Added explicit assurance-depth invariant (`INV_ASSURANCE_DEPTH_POLICY`) aligned with benchmark overclaim prevention semantics and existing benchmark gate enforcer.

## 2026.20.0
- Fixed CI artifact manifest producer/consumer path contract by verifying manifests against per-artifact download roots with explicit path-prefix normalization (`--root` + `--strip-path-prefix`) in `inv-ci-artifact-semantics-and-provenance`.
- Hardened governance validator to fail closed on artifact upload policy drift (`if-no-files-found: error`, `retention-days >= 14`) for all upload-artifact steps.
- Added fail-closed benchmark regenerated-output parity gate (`git diff --exit-code -- benchmark/metrics.json benchmark/results/case_level_results.csv`) and validator enforcement for its presence.
- Added governance regressions covering list/scalar/boolean-key workflow trigger parsing, artifact-manifest verification contract tokens, artifact retention floor enforcement, and benchmark parity-step presence.

## 2026.19.0

- Aligned PR-intake executable contract with repository PR template/CONTRIBUTING sections and removed payload file-list dependence from intake gating semantics.
- Hardened governance validator severity mapping to fail closed for critical codes (`PR_TEMPLATE`, `BENCHMARK_HONESTY`, `GOVERNANCE_STATUS_ARTIFACT`, `ORDERING`) and added regression coverage.

## 2026.18.0

- Hardened repo-map governance truthfulness by requiring explicit `root` mapping for governance-critical root files (`MANIFEST.json`, `repo-map.json`, `CONTRIBUTING.md`, `.pre-commit-config.yaml`) and added regression coverage.
- Added missing schema invariants for evaluation-result acceptance/rejection and synchronized local baseline execution metadata and generated checklist parity.
- Expanded CODEOWNERS-required governance coverage to include `repo-map.json` and `requirements.txt` with validator enforcement and regression tests.
- Hardened PR intake validator contract (`WHAT_CHANGED`, `WHY_THIS_WAS_REQUIRED`, `PROOF`, `FINAL_DECISION`) with placeholder rejection and governance-critical diff awareness, with dedicated tests.
- Added governance self-hosting test execution commands to `governance-hygiene` CI gate and validator checks for required self-hosting coverage.

## 2026.17.0

- Removed uncontrolled external-link reachability from required merge checks by converting it to advisory CI audit (`audit-publication-external-link-reachability`) and updating required-check mappings/baselines accordingly.
- Expanded governance validator workflow coverage to all `.github/workflows/*.yml` with machine-checked reserved-pages exception semantics.
- Added canonical pip toolchain policy in CI (`env.PIP_VERSION`, pinned upgrade, and `python -m pip --version` logging) with validator enforcement and regression tests.
- Expanded governance dependency-hermeticity coverage across governance-critical tools used by the governance model.

## 2026.16.0

- Hardened CI shell-discipline contract by requiring workflow-level `defaults.run.shell` to be strict (`bash --noprofile --norc -euo pipefail {0}`) and enforcing it in `tools/validate_governance.py`.
- Added governance regression coverage for workflow strict-shell drift (`test_workflow_defaults_shell_drift_is_rejected`).

## 2026.15.0

- Hardened tracked-tree dirtiness detection in `tools/run_local_governance_baseline.py` by switching to `git status --porcelain --untracked-files=no`, so staged and unstaged tracked changes are both fail-closed before `--execute`.
- Expanded baseline execution policy regressions with stale dirty-policy mapping coverage in `tests/governance/test_run_local_governance_baseline.py`.

## 2026.14.0

- Strengthened `tools/run_local_governance_baseline.py` execution semantics: execution now fails on pre-existing tracked-tree drift, rejects stale execute-policy mappings, and keeps command-policy metadata synchronized with checklist-derived command sets.
- Added governance regression tests for local baseline execution policy and clean-tree fail-closed behavior (`tests/governance/test_run_local_governance_baseline.py`).

## 2026.13.0

- Hardened canonical local baseline executor to use explicit command exit metadata and controlled tracked-file mutation allowances (with automatic restoration), removing residual heuristic behavior and preventing hidden tree taint after execution.

## 2026.12.0

- Restored governance truthfulness inventory entries for `.github/workflows/pages.yml` and `.gitignore` across manifest/repo-map/allowed surfaces/tests.
- Enforced explicit governance-document ownership rules in CODEOWNERS for normative spec and policy-drift runbook.
- Hardened policy-drift intake requirements in PR template with expanded governance-critical surface list.
- Switched governance-hygiene local baseline to executable hard gate (`python tools/run_local_governance_baseline.py --execute`) and replaced command-string heuristic with explicit exit metadata in baseline runner.
- Added pull-request intake quality validator (`tools/validate_pr_intake.py`) and CI gate `inv-pr-intake-quality` for non-empty mandatory sections.
- Elevated strict workflow/publication governance violations to blocking errors and replaced scope-creep diff with merge-base aware calculation.
- Added regression tests and fixture coverage for inventory truthfulness drift cases (`.gitignore`, `.github/workflows/pages.yml`).

## 2026.11.0

- Tightened policy-drift mandatory section requirements in PR template (explicit governance-critical file classes).
- Added validator checks for silent job weakening patterns (artifact retention floor, shell-download restrictions, and stronger strict-shell requirements).
- Added repo-map corruption regression test and strengthened documentation truthfulness enforcement in CONTRIBUTING.
- Enforced fail-closed decoding policy by forbidding `errors='ignore'` in publication/link validators.
- Added machine-assisted governance scope-creep signal to surface overly broad mixed governance/content diffs.

## 2026.10.0

- Hardened workflow trust-model validation in `tools/validate_governance.py` (forbidden triggers, permission escalation, matrix/reusable workflow controls, shell-download restrictions, and strictness checks for `|| true`/pipefail-sensitive runs).
- Added symmetric MANIFEST/repo-map truthfulness checks against tracked git tree and governance-surface inventory expectations.
- Added CODEOWNERS anti-dilution and PR-template quality checks (canonical section prompts/quality guardrails).
- Added deterministic governance artifact checker `tools/check_governance_nondeterminism.py` and canonical local baseline contract script `tools/run_local_governance_baseline.py` with CI/pre-commit parity.
- Added concise normative governance spec `docs/GOVERNANCE_NORMATIVE_SPEC.md` and clarified operational vs normative governance documentation boundaries.
- Expanded validator regression tests for corrupted JSON/YAML and permissions-escalation failure modes.

## 2026.9.0

- Added machine-readable external GitHub settings baseline at `governance/github-settings-baseline.json` with explicit minimum branch protection expectations and required status checks.
- Added canonical required-check mapping at `governance/ci-required-checks.json` to enforce immutable reviewer-facing check names and stable workflow job mapping.
- Extended `tools/validate_governance.py` to validate required-check/job-name immutability, baseline-vs-mapping drift, and policy-drift review/runbook presence.
- Added governance incident response runbook `docs/GOVERNANCE_POLICY_DRIFT_RUNBOOK.md` and made policy-drift review mandatory in PR template and contributing policy.

## 2026.8.0

- Enforced deterministic dependency policy by requiring exact pinning in `requirements.txt` and synchronized lock metadata in `governance/requirements-governance.lock.json`.
- Added hermetic dependency validator `tools/check_dependency_hermeticity.py` to detect lock drift and hidden undeclared third-party imports in governance-critical tools.
- Added governance CLI contract validator `tools/check_cli_contracts.py` and integrated it into CI/local checks.
- Added dedicated CI job `inv-dependency-hermeticity` and expanded workflow ordering enforcement as structured invariant (dependency install must occur before repository tool execution in dependency-sensitive jobs).
- Expanded semantic test suite with `tests/semantic/test_cli_contracts.py` and `tests/semantic/test_dependency_hermeticity.py`.

## 2026.7.0

- Moved fail-closed semantic assertions from workflow inline blocks into repository script `tools/assert_fail_closed_semantics.py` and added dedicated unit coverage.
- Moved gate-id and benchmark-honesty assertions from workflow inline Python blocks into `tools/assert_gate_benchmark_invariants.py`.
- Added worked-example semantic invariant and repeat-run consistency script `tools/assert_worked_example_semantics.py`.
- Expanded canonical hash stability to representative multi-input runs and added canonicalization edge-case negative controls via `tools/check_canonical_hash_stability.py` and `tools/check_canonicalization_negative_cases.py`.
- Hardened workflow governance checks to require repository scripts (not inline assertions) for semantic-critical controls.

## 2026.6.0

- Split publication controls into dedicated invariants/jobs: internal link integrity, external reachability, and publication structure validation.
- Added structural publication validator requirements (`<title>`, required meta tags, canonical link, local asset existence, repo-map publication coverage parity).
- Added CI artifact semantics/provenance control with canonical artifact names, non-empty size checks, checksum manifests, and producer-job assertions.
- Added reviewer-inspectability summary artifact in CI.
- Added machine-readable final governance status artifact upload (`governance-status.json`) from governance-hygiene.
- Centralized publication exclusion and metadata policy constants in `tools/governance_contract.py`.
- Added critical artifact class model (`governance` / `publication` / `benchmark` / `execution`) with validator enforcement.

## 2026.5.0

- Introduced machine-readable canonical invariant registry at `governance/invariant-registry.json`.
- Added registry JSON schema at `schemas/governance-invariant-registry.schema.json`.
- Formalized canonical authority model, verification scopes (`SHARED`/`CI_ONLY`/`LOCAL_ONLY`), domain classes, claim classes, and minimum evidence requirement typing.
- Introduced canonical failure-mode vocabulary (`FM_*`) and typed invariant-to-failure-mode mapping.
- Added checklist generated sections (registry table, baseline commands, and "what is not verified") derived from the registry.
- Added policy versioning discipline and validator JSON output with severity-typed violations.

## Discipline

- Every change to governance policy semantics MUST:
  1. bump `policy_version` in `governance/invariant-registry.json`,
  2. append a new heading in this changelog,
  3. keep `tools/validate_governance.py` and tests aligned,
  4. refresh generated sections in `docs/PR_PREMERGE_ENGINEERING_CHECKLIST.md`.
