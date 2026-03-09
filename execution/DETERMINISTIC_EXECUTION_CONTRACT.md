# Deterministic Execution Contract

## Purpose

This document translates the hardening protocol into an operational execution contract.
It defines what a conformant evaluator must do, in what order, and with what outputs.

## Required sequence

1. Load target role protocol.
2. Load hardening protocol.
3. Load schemas.
4. Extract artifact candidates from input bundle.
5. Canonicalize every admissible artifact.
6. Compute or verify SHA-256 fingerprints.
7. Validate every canonical object against schema.
8. Exclude INVALID objects from admissible evidence.
9. Score tasks only from admissible evidence.
10. Compute domain scores.
11. Evaluate gates G0, G1, G2.
12. Derive final classification.
13. Produce evidence trace.
14. Validate final EvaluationResult against schema.
15. Fail closed if any required step is incomplete.

## Determinism rules

A conformant run must keep fixed:
- target protocol version
- hardening protocol version
- schema set
- execution mode
- scoring equations
- gate definitions
- output ordering

## Admissible repair

A conformant implementation may normalize formatting.
It may not repair missing evidence by inference.
It may not override invalid schema state with narrative explanation.

## Final output

Only a valid `EvaluationResult` object counts as a complete run.
Anything else is a failed or non-conformant run.
