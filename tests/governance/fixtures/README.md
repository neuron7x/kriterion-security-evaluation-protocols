# Governance validator golden fixture notes

This directory stores canonical mutation intents used by `tests/governance/test_validate_governance.py`
to assert deterministic fail-closed diagnostics for regression classes including:
- workflow action pinning drift,
- invalid fail-closed mutation logic,
- stale generated checklist blocks versus canonical registry,
- inventory truthfulness drift (`MANIFEST`/`repo-map`),
- workflow trust-model and strictness weakening,
- policy-drift intake/ownership/documentation alignment failures.
