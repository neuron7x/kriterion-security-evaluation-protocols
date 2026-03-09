# Contributing

This repository is designed as a protocol system, not an unbounded content dump.

## Contribution standards

Any contribution should preserve:
- evidence-first reasoning,
- fail-closed behavior,
- explicit schemas or contracts where relevant,
- benchmark honesty,
- visual coherence with the repository design system.

## Pull request expectations

A meaningful PR should state:
- what layer is affected,
- why the change is needed,
- whether the change alters protocol logic, doctrine, benchmark governance, or only presentation,
- whether MANIFEST.json requires refresh.

PR bodies must follow `.github/pull_request_template.md` in this exact order, using these exact headings:
1. `## Problem`
2. `## Scope`
3. `## Invariants touched`
4. `## Evidence`
5. `## Risks`
6. `## Non-goals`
7. `## Manifest refresh justification`
8. `## Human review required`
9. `## Policy-drift review (mandatory for governance-critical surfaces)`

Do not rename, reorder, duplicate, or omit these headings. `tools/validate_pr_intake.py` is fail-closed and rejects non-compliant PR bodies.

For deterministic local PR-intake compilation from live branch state + validator output, use `tools/pr --dry-run` (artifact only) or `tools/pr --apply` (updates current PR body via `gh`).

## Pre-merge governance model

Before opening or merging a PR:
- run the local baseline in `docs/PR_PREMERGE_ENGINEERING_CHECKLIST.md`,
- treat **MACHINE_VERIFIED** items as hard gates,
- treat **MACHINE_ASSISTED** items as hygiene/structure, not correctness proof,
- treat **HUMAN_REVIEW_ONLY** items as reviewer constitutional judgment.

Repository-embedded governance structures:
- `.github/CODEOWNERS`
- `.github/pull_request_template.md`
- `.pre-commit-config.yaml`

Canonical governance enforcer:
- `tools/validate_governance.py` (deterministic MACHINE_VERIFIED validator executed in `governance-hygiene` and local parity hooks)

## Disallowed patterns

Do not introduce:
- unverifiable benchmark claims,
- decorative visual clutter,
- generic “AI landing page” copy,
- redundant documents with no system role,
- silent drift in scoring logic.

## Review principle

Every accepted change should make the repository either:
- clearer,
- stricter,
- more reproducible,
- more navigable,
- or more professionally publishable.

## Note on GitHub platform settings

Branch protection, required check selection, required code-owner review, merge restrictions, and bypass restrictions are configured in GitHub settings after merge, not inside repository files.


CI hygiene defaults in this repository:
- stale runs are automatically canceled via workflow concurrency,
- benchmark/worked-example evidence artifacts are uploaded when produced for reviewer inspection,


The `governance-hygiene` workflow job also machine-verifies one-PR doctrine (no `.github/dependabot.yml`) and workflow self-discipline (concurrency, SHA-pinned official actions, evidence artifact retention/uploads, and dependency-install ordering for benchmark/fail-closed jobs).

Governance self-hosting rule: any change to `tools/validate_governance.py` must preserve/update `tests/governance/test_validate_governance.py` and fixture mutations so validator pass/fail and failure-mode behavior remain regression-tested.


Governance contract versioning discipline:
- Canonical policy metadata lives in `governance/invariant-registry.json` (`policy_version`).
- Any governance contract change must also append `docs/GOVERNANCE_CONTRACT_CHANGELOG.md` and keep generated checklist sections in sync (`python tools/render_governance_checklist.py`).
- Invariant scope MUST be explicitly classified as `SHARED`, `CI_ONLY`, or `LOCAL_ONLY`; failure modes MUST use canonical `FM_*` vocabulary from the registry.


Additional governance controls in policy versions 2026.10.0 / 2026.11.0 / 2026.12.0:
- Workflow trust-model hardening is machine-validated (trigger/permission/escalation policy and strict-shell expectations).
- Inventory truthfulness is validated symmetrically across tracked tree, `MANIFEST.json`, and `repo-map.json`.
- governance-hygiene remains the CI policy-verifier role and now executes canonical baseline checks as hard gates.


Minimum external GitHub settings baseline (machine-readable):
- `governance/github-settings-baseline.json`

Machine-checkable required-check mapping (immutable reviewer-facing names):
- `governance/ci-required-checks.json`

Policy-drift incidents MUST follow:
- `docs/GOVERNANCE_POLICY_DRIFT_RUNBOOK.md`

Normative governance source (doctrine-level):
- `docs/GOVERNANCE_NORMATIVE_SPEC.md`

Operational governance source (workflow/runbook-level):
- `CONTRIBUTING.md`
- `docs/GOVERNANCE_POLICY_DRIFT_RUNBOOK.md`

Documentation truthfulness rule:
- Do not claim repo-native enforcement for controls that are external GitHub settings.

Job taxonomy note:
- `governance-hygiene` is the CI policy-verifier role (not a generic lint bucket).
