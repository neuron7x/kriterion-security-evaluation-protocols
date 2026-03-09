# Multi-Agent Orchestration Contract

## Purpose

This document defines the required agent boundaries for a conformant multi-agent implementation.

## Canonical agents

- `ARTIFACT_AGENT` — extracts and packages candidate evidence
- `VALIDATION_AGENT` — validates canonical objects against schemas
- `INTEGRITY_AGENT` — checks fingerprints, duplicates, provenance, and reviewer independence
- `EVALUATION_AGENT` — computes task scores from admissible evidence
- `CLASSIFICATION_AGENT` — computes domain totals, gates, and final classification
- `AUDIT_TRACE_AGENT` — produces the evidence trace table and preserves object lineage

## Boundary rules

No agent may perform work outside its authority if that would bypass a gate.

Examples:
- `EVALUATION_AGENT` may not mark an invalid artifact as admissible.
- `CLASSIFICATION_AGENT` may not fabricate task scores.
- `AUDIT_TRACE_AGENT` may not alter score values.

## Handoff rules

Every cross-agent handoff must use a valid `OrchestrationHandoff` object.
The handoff must include the produced object reference and its integrity state.

## Shared store

All agents must reference the same canonical object store.
Private, divergent representations are non-conformant.
