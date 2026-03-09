# Governance Policy-Drift Incident Runbook

## Purpose

This runbook defines mandatory response steps when governance policy drift is detected between:
- repository-enforced CI checks,
- external GitHub branch protection / required-status-check settings,
- and governance policy documents.

## Incident triggers

Treat any of the following as a governance incident:
- `tools/validate_governance.py` reports `GITHUB_REQUIRED_CHECKS` violations,
- mismatch between `governance/ci-required-checks.json` and workflow job names,
- mismatch between `governance/github-settings-baseline.json.required_status_checks` and repository check mapping,
- missing mandatory policy-drift review section in PR body for governance-critical changes.

## Severity model

- **SEV-1**: required checks or branch-protection settings drift in a way that can permit unsafe merges.
- **SEV-2**: drift in documentation or mapping metadata without immediate bypass risk.

## Response procedure

1. **Containment**
   - Pause merges to governance-critical surfaces until drift is resolved.
   - Capture current GitHub branch-protection snapshot and required checks list.
2. **Diagnosis**
   - Run `python tools/validate_governance.py --json` and preserve output.
   - Compare workflow jobs vs `governance/ci-required-checks.json`.
   - Compare external settings vs `governance/github-settings-baseline.json`.
3. **Remediation**
   - Restore immutable reviewer-facing check names and canonical job IDs.
   - Restore required status checks in GitHub settings to baseline.
   - Update governance docs/changelog only when policy intentionally changes.
4. **Verification**
   - Re-run governance checks and attach evidence artifacts in PR.
   - Require code-owner review and explicit policy-drift review sign-off.
5. **Post-incident hardening**
   - Document root cause and prevention action in PR notes.
   - If policy changes were intentional, bump policy version and update changelog.

## Evidence requirements

Incident PR must include:
- before/after required-check mapping,
- validator JSON output,
- explicit reviewer statement for policy-drift review.
