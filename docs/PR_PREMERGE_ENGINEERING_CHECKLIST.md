# PR Pre-Merge Engineering Checklist (Truthful Governance)

This checklist separates hard CI enforcement from machine-assisted hygiene and human constitutional review.

Policy source of truth:
- registry: `governance/invariant-registry.json`
- schema: `schemas/governance-invariant-registry.schema.json`
- changelog discipline: `docs/GOVERNANCE_CONTRACT_CHANGELOG.md`

## Authority classes

- **MACHINE_VERIFIED**: deterministic hard gate.
- **MACHINE_ASSISTED**: structure/hygiene support; not correctness proof by itself.
- **HUMAN_REVIEW_ONLY**: human constitutional review.

## Canonical authority + invariant map (generated)

`INVARIANT_ID | DOMAIN_CLASS | SCOPE | AUTHORITY | ENFORCER | FAILURE_MODE_CODES`

<!-- GOVERNANCE_REGISTRY_TABLE:START -->
- `INV_MANIFEST_TREE_MATCH | integrity | SHARED | MACHINE_VERIFIED | python tools/verify_manifest.py MANIFEST.json . | FM_MANIFEST_DRIFT`
- `INV_VALID_CANONICAL_ARTIFACT_ACCEPTED | validity | SHARED | MACHINE_VERIFIED | python tools/validate_json.py schemas/canonical-artifact.schema.json tests/fixtures/artifact.valid.json | FM_SCHEMA_REGRESSION`
- `INV_INVALID_CANONICAL_ARTIFACT_REJECTED | validity | SHARED | MACHINE_VERIFIED | python tools/validate_json.py schemas/canonical-artifact.schema.json tests/fixtures/artifact.invalid.missing-valid-fingerprint.json | FM_SCHEMA_REGRESSION`
- `INV_VALID_EVALUATION_RESULT_ACCEPTED | validity | SHARED | MACHINE_VERIFIED | python tools/validate_json.py schemas/evaluation-result.schema.json tests/fixtures/evaluation-result.valid.json | FM_SCHEMA_REGRESSION`
- `INV_INVALID_EVALUATION_RESULT_REJECTED | validity | SHARED | MACHINE_VERIFIED | python tools/validate_json.py schemas/evaluation-result.schema.json tests/fixtures/evaluation-result.invalid.bad-gate.json | FM_SCHEMA_REGRESSION`
- `INV_DEPENDENCY_HERMETICITY_LOCKED | integrity | SHARED | MACHINE_VERIFIED | python tools/check_dependency_hermeticity.py | FM_DEPENDENCY_HERMETICITY, FM_UNDECLARED_DEPENDENCY`
- `INV_CANONICAL_HASH_STABLE | integrity | CI_ONLY | MACHINE_VERIFIED | python tools/check_canonical_hash_stability.py --repeat 3 + python tools/check_canonicalization_negative_cases.py | FM_NONDETERMINISTIC_HASH`
- `INV_WORKED_EXAMPLE_EXECUTES | semantic_sufficiency | SHARED | MACHINE_VERIFIED | python tools/assert_worked_example_semantics.py --out-dir .ci-artifacts | FM_RUNNER_EXECUTION_DRIFT`
- `INV_FAIL_CLOSED_MISSING_EVIDENCE | semantic_sufficiency | CI_ONLY | MACHINE_VERIFIED | python tools/assert_fail_closed_semantics.py (via inv-fail-closed-missing-evidence job) | FM_FAIL_CLOSED_REGRESSION`
- `INV_GATE_IDS_CANONICAL | validity | CI_ONLY | MACHINE_VERIFIED | python tools/assert_gate_benchmark_invariants.py --gate-fixture tests/fixtures/evaluation-result.valid.json | FM_GATE_ID_DRIFT`
- `INV_BENCHMARK_HONESTY_DEMO_ONLY | semantic_sufficiency | SHARED | MACHINE_VERIFIED | python tools/assert_gate_benchmark_invariants.py --metrics benchmark/metrics.json | FM_BENCHMARK_OVERCLAIM`
- `INV_ASSURANCE_DEPTH_POLICY | semantic_sufficiency | SHARED | MACHINE_VERIFIED | python tools/assert_gate_benchmark_invariants.py --metrics benchmark/metrics.json --gate-fixture tests/fixtures/evaluation-result.valid.json | FM_BENCHMARK_OVERCLAIM`
- `INV_PYTHON_ENTRYPOINTS_INVOKABLE | hygiene | CI_ONLY | MACHINE_VERIFIED | python tools/check_cli_contracts.py (via inv-python-entrypoints-and-compile job) | FM_ENTRYPOINT_BREAKAGE, FM_CLI_CONTRACT_DRIFT`
- `INV_COMPILE_SANITY | hygiene | SHARED | MACHINE_VERIFIED | python -m compileall tools benchmark pcos | FM_SYNTAX_BREAKAGE`
- `INV_PUBLICATION_INTERNAL_LINK_INTEGRITY | publication | CI_ONLY | MACHINE_VERIFIED | inv-publication-internal-link-integrity job | FM_INTERNAL_LINK_BREAKAGE`
- `INV_PUBLICATION_EXTERNAL_LINK_AUDIT | publication | CI_ONLY | MACHINE_ASSISTED | audit-publication-external-link-reachability job (advisory) | FM_EXTERNAL_LINK_BREAKAGE`
- `INV_PUBLICATION_SURFACE_STRUCTURE | publication | CI_ONLY | MACHINE_VERIFIED | inv-publication-surface-structure job | FM_PAGES_SURFACE_BREAKAGE`
- `INV_CI_ARTIFACT_SEMANTICS_AND_PROVENANCE | integrity | CI_ONLY | MACHINE_VERIFIED | inv-ci-artifact-semantics-and-provenance job | FM_ARTIFACT_PROVENANCE_DRIFT`
- `INV_ONE_PR_DOCTRINE_ENFORCED | hygiene | SHARED | MACHINE_VERIFIED | python tools/validate_governance.py | FM_DOCTRINE_DRIFT`
- `INV_GOVERNANCE_CONTRACT_ALIGNMENT | hygiene | SHARED | MACHINE_VERIFIED | python tools/validate_governance.py | FM_POLICY_DOC_DRIFT`
- `INV_GOVERNANCE_VALIDATOR_SELF_HOSTING | hygiene | LOCAL_ONLY | MACHINE_VERIFIED | python -m unittest tests/governance/test_validate_governance.py | FM_GOVERNANCE_REGRESSION`
- `INV_REQUIRED_CHECK_MAPPING_STABLE | hygiene | SHARED | MACHINE_VERIFIED | python tools/validate_governance.py | FM_REQUIRED_CHECK_MAPPING_DRIFT`
- `INV_GITHUB_SETTINGS_BASELINE_DECLARED | hygiene | SHARED | MACHINE_VERIFIED | python tools/validate_governance.py | FM_GITHUB_SETTINGS_BASELINE_DRIFT, FM_POST_MERGE_OPS_DRIFT`
- `INV_POLICY_DRIFT_REVIEW_MANDATORY | hygiene | SHARED | MACHINE_VERIFIED | python tools/validate_governance.py | FM_POLICY_DRIFT_REVIEW_MISSING`
- `INV_WORKFLOW_TRUST_SURFACE_HARDENED | integrity | SHARED | MACHINE_VERIFIED | python tools/validate_governance.py | FM_WORKFLOW_PRIVILEGE_ESCALATION, FM_JOB_WEAKENING`
- `INV_MANIFEST_REPOMAP_TRUTHFUL | integrity | SHARED | MACHINE_VERIFIED | python tools/validate_governance.py | FM_MANIFEST_INVENTORY_UNTRUTHFUL, FM_REPO_MAP_UNTRUTHFUL`
- `INV_CODEOWNERS_EFFECTIVE_OWNERSHIP | hygiene | SHARED | MACHINE_VERIFIED | python tools/validate_governance.py | FM_CODEOWNERS_DILUTION`
- `INV_PR_TEMPLATE_INTAKE_QUALITY | hygiene | SHARED | MACHINE_VERIFIED | python tools/validate_governance.py | FM_PR_TEMPLATE_WEAKENING`
- `INV_LOCAL_BASELINE_CANONICAL | hygiene | SHARED | MACHINE_VERIFIED | python tools/validate_governance.py | FM_LOCAL_BASELINE_DRIFT`
- `INV_GOVERNANCE_ARTIFACTS_DETERMINISTIC | integrity | SHARED | MACHINE_VERIFIED | python tools/validate_governance.py | FM_GOVERNANCE_ARTIFACT_NONDETERMINISM`
- `INV_ONE_PR_DOCTRINE_EXTENDED | hygiene | SHARED | MACHINE_VERIFIED | python tools/validate_governance.py | FM_ONE_PR_DOCTRINE_WEAKENING`
- `INV_GOVERNANCE_DOCUMENTATION_TRUTHFUL | hygiene | SHARED | MACHINE_VERIFIED | python tools/validate_governance.py | FM_DOCUMENTATION_UNTRUTHFUL`
- `INV_CANONICAL_LOCAL_BASELINE_EXECUTABLE | hygiene | SHARED | MACHINE_VERIFIED | python tools/run_local_governance_baseline.py | FM_LOCAL_BASELINE_DRIFT`
- `INV_PR_INTAKE_NONEMPTY_ON_PULL_REQUEST | hygiene | CI_ONLY | MACHINE_VERIFIED | python tools/validate_pr_intake.py (via inv-pr-intake-quality job) | FM_PR_INTAKE_QUALITY`
- `INV_EXECUTION_CHAIN_INDEPENDENTLY_RECOMPUTABLE | integrity | SHARED | MACHINE_VERIFIED | python tools/verify_execution_chain.py --input examples/worked-example/SE_WORKED_EXAMPLE_INPUT.json --result /tmp/SE_WORKED_EXAMPLE_OUTPUT.check.json | FM_EXECUTION_CHAIN_VERIFICATION_DRIFT`
- `INV_GIT_AUTHORITATIVE_EXECUTION_SURFACE | integrity | CI_ONLY | MACHINE_VERIFIED | python tools/verify_execution_chain.py --input examples/worked-example/SE_WORKED_EXAMPLE_INPUT.json --result /tmp/SE_WORKED_EXAMPLE_OUTPUT.chain.json | FM_GIT_AUTHORITY_EXECUTION_DRIFT`
<!-- GOVERNANCE_REGISTRY_TABLE:END -->

## Scope model

- `SHARED`: must exist in both CI and local governance model.
- `CI_ONLY`: enforced in CI jobs only.
- `LOCAL_ONLY`: enforced as local discipline checks (still machine-verifiable).

## Required local baseline commands (generated)

<!-- GOVERNANCE_BASELINE_COMMANDS:START -->
```bash
python tools/verify_manifest.py MANIFEST.json .
python tools/validate_json.py schemas/canonical-artifact.schema.json tests/fixtures/artifact.valid.json
python tools/validate_json.py schemas/canonical-artifact.schema.json tests/fixtures/artifact.invalid.missing-valid-fingerprint.json
python tools/validate_json.py schemas/evaluation-result.schema.json tests/fixtures/evaluation-result.valid.json
python tools/validate_json.py schemas/evaluation-result.schema.json tests/fixtures/evaluation-result.invalid.bad-gate.json
python tools/check_dependency_hermeticity.py
python tools/reference_runner.py examples/worked-example/SE_WORKED_EXAMPLE_INPUT.json --output /tmp/SE_WORKED_EXAMPLE_OUTPUT.check.json
python benchmark/benchmark_runner.py
python -m compileall tools benchmark pcos
python tools/validate_governance.py
python -m unittest tests/governance/test_validate_governance.py
python tools/run_local_governance_baseline.py
python tools/verify_execution_chain.py --input examples/worked-example/SE_WORKED_EXAMPLE_INPUT.json --result /tmp/SE_WORKED_EXAMPLE_OUTPUT.check.json
```
<!-- GOVERNANCE_BASELINE_COMMANDS:END -->

For invalid fixtures, non-zero rejection is the expected success signal.

## What is not verified (generated)

<!-- GOVERNANCE_NOT_VERIFIED:START -->
- Does not attest external compute environment provenance.
- Does not configure remote repository settings.
- Does not control third-party organization-level automations outside repository settings.
- Does not cover all adversarial scenarios.
- Does not enforce GitHub settings directly from repository files.
- Does not enforce GitHub-hosted runner internals.
- Does not enforce reviewer staffing availability.
- Does not execute external GitHub settings operations.
- Does not guarantee determinism for non-governance artifacts.
- Does not imply production representativeness.
- Does not measure external URL uptime.
- Does not prove algorithmic correctness.
- Does not prove all semantic edge cases.
- Does not prove artifact semantic correctness.
- Does not prove artifact semantic truthfulness by itself.
- Does not prove semantic quality of non-governance content.
- Does not prove semantic quality.
- Does not provide external hardware attestation.
- Does not provide full transitive lock reproducibility across all operating systems.
- Does not provide repository-native proof for third-party availability.
- Does not replace constitutional human review.
- Does not replace direct code review of validator changes.
- Does not substitute UX/content quality review.
- Does not validate all runtime states.
- Does not validate final human-authored PR narrative quality.
- Does not validate production payload diversity.
- Does not verify full score decomposition.
- External network uptime is non-deterministic and not a required merge gate.
<!-- GOVERNANCE_NOT_VERIFIED:END -->

## Canonical failure-mode vocabulary

Failure modes are canonicalized in the registry as `FM_*` codes and mapped per invariant to prevent ambiguous failure language across docs/workflow/validator.

## MACHINE_ASSISTED controls in this repository

- `.github/pull_request_template.md`
- `.github/CODEOWNERS`
- `.pre-commit-config.yaml`

## HUMAN_REVIEW_ONLY controls

- minimal diff discipline
- manifest refresh justification adequacy
- PR evidence quality and proportionality
- doctrine drift judgment
- declared scope vs true intent

## Post-merge GitHub settings to apply manually

These settings are outside repository files and must be configured in GitHub:
- protect `main`
- require pull requests before merge
- require status checks to pass and select stable checks from `quality-gates` (including immutable names from `governance/ci-required-checks.json`)
- require review from code owners
- require linear history
- block force pushes and bypass where available
- external baseline: `governance/github-settings-baseline.json`
- required-check mapping source: `governance/ci-required-checks.json`
- if drift detected, execute `docs/GOVERNANCE_POLICY_DRIFT_RUNBOOK.md`
