# Canonicalization Rules

## Input normalization

- Text encoded as UTF-8
- Newlines normalized to LF
- Object keys sorted lexicographically
- Arrays preserve semantic order
- Duplicate references collapsed while preserving first occurrence order
- Whitespace outside string values removed in canonical JSON encoding

## Fingerprinting

Canonical bytes are the exact bytes of the canonical JSON string representation.
Fingerprint value:

`sha256(canonical_bytes)`

## Prohibited behavior

- altering semantic content while “cleaning” data
- merging separate evidence units into one artifact without trace
- discarding provenance fields during normalization
