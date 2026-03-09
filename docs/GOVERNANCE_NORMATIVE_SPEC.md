# Governance Normative Spec

This document is the concise normative governance doctrine.

## Canonical acceptance criteria for governance-complete state

A repository state is governance-complete only if:
- `python tools/validate_governance.py` returns `GOVERNANCE_OK`;
- required checks mapping (`governance/ci-required-checks.json`) matches immutable workflow job IDs/names;
- external GitHub baseline dependency (`governance/github-settings-baseline.json`) is declared and drift-managed via runbook;
- MANIFEST and repo-map inventories are truthful and denylisted artifacts are absent;
- governance-critical surfaces require explicit policy-drift review.

## Evolution plan

- **v1**: text-backed validator and explicit policy docs.
- **v2**: semantic parser checks for workflow/CODEOWNERS/PR-template strictness.
- **v3**: generated policy registry-driven enforcement with minimal manual duplication.

## Taxonomy

`governance-hygiene` job is the policy verifier role; it is not a generic lint bucket.
