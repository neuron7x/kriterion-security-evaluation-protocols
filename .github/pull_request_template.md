## Problem
Describe the concrete engineering risk or governance gap this PR addresses.

## Scope
List exactly which layers/files are intentionally changed.

## Invariants touched
List invariant IDs affected and whether each is MACHINE_VERIFIED, MACHINE_ASSISTED, or HUMAN_REVIEW_ONLY.

## Evidence
Provide commands run and observed outputs/artifacts.

## Risks
State realistic failure modes and mitigation.

## Non-goals
State what this PR intentionally does not change.

## Manifest refresh justification
If `MANIFEST.json` changed, explain exactly why and which files required hash refresh.

## Human review required
List reviewer judgments that cannot be automated (constitutional fit, doctrine drift, scope legitimacy).


## Policy-drift review (mandatory for governance-critical surfaces)
Required when changing any governance-critical surface, including:
- `.github/` workflows/settings files
- `tools/validate_governance.py`
- `docs/PR_PREMERGE_ENGINEERING_CHECKLIST.md` (checklist)
- `.github/pull_request_template.md` (template)
- `.github/CODEOWNERS`
- `MANIFEST.json`
- `repo-map.json`
- `governance/ci-required-checks.json`
- `governance/github-settings-baseline.json`
- `docs/GOVERNANCE_NORMATIVE_SPEC.md`
- `docs/GOVERNANCE_POLICY_DRIFT_RUNBOOK.md`
- `tools/check_governance_nondeterminism.py`
- `tools/run_local_governance_baseline.py`

Reviewer MUST explicitly record drift assessment and approve/reject drift as intentional.
