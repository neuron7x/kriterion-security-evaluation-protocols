# EVIDENCE-FIRST ENGINEERING

## Thesis

Engineering quality should be inferred from validated artifacts, not from retrospective narrative. This document defines the evidence-first doctrine that underlies the protocols in this repository.

The central move is simple but severe:
**no claim receives full evaluative force unless it is attached to evidence that survives normalization, validation, and integrity checks.**

---

## 1. Why evidence-first matters

Traditional evaluation systems over-reward:
- memory,
- fluency,
- persuasive framing,
- seniority theater,
- vague ownership language,
- selective storytelling.

An evidence-first system changes the center of gravity.

Instead of asking:
- “Can the candidate explain the work?”
it asks:
- “What artifacts demonstrate the work?”
- “How independent is the validation?”
- “What survives adversarial inspection?”

This does not trivialize explanation. It correctly demotes it.

---

## 2. Evidence hierarchy

Not all artifacts carry the same weight. A robust system needs an explicit hierarchy.

### Primary evidence
Direct operational or implementation artifacts:
- pull requests,
- merged code,
- runbooks,
- dashboards,
- architecture decisions,
- policy definitions,
- validated configurations,
- incident records,
- test reports,
- pipeline outputs.

### Secondary evidence
Artifacts about artifacts:
- summaries,
- reviews,
- meeting notes,
- tickets,
- retrospectives,
- design commentary.

### Tertiary evidence
Narrative statements that lack direct mechanical or operational anchoring.

A mature evaluation system should privilege primary evidence, use secondary evidence as context, and treat tertiary evidence cautiously.

---

## 3. Canonical evidence object

Evidence should not remain a loose attachment. It should be transformed into a stable object.

A canonical evidence object should capture:
- `artifact_id`
- `artifact_type`
- `title`
- `provenance`
- `reviewer`
- `timestamp`
- `references`
- `fingerprint.sha256`
- `evidence_class`
- `domain_mapping`
- `validation_status`

Once normalized, evidence becomes computable rather than merely discussable.

---

## 4. Provenance is part of correctness

An artifact without provenance is weaker than an artifact with provenance, even if the content is technically impressive.

Provenance answers:
- who created it,
- when it was created,
- who reviewed it,
- whether the reviewer was independent,
- how it entered the evaluation process.

Without provenance, impressive artifacts can still be strategically ambiguous.

---

## 5. Fingerprints and temporal fixity

The purpose of a fingerprint is not ceremony. It is temporal stabilization.

A cryptographic fingerprint:
- freezes the artifact at evaluation time,
- prevents quiet post-hoc mutation,
- supports reproducible re-evaluation,
- makes audit disagreement concrete.

In an evidence-first architecture, hashes are not decorative metadata. They are anchors against drift.

---

## 6. Evidence sufficiency is not evidence volume

Large evidence bundles can still be weak.

Sufficiency depends on:
- relevance,
- directness,
- coverage of critical tasks,
- independence,
- internal consistency.

A thousand loosely related files do not outperform three decisive primary artifacts.

This is why anti-flooding logic matters.

---

## 7. The role of schemas

Schemas are the bridge between raw artifacts and reliable computation.

They force explicitness around:
- required fields,
- admissible formats,
- missing values,
- structural validity,
- downstream scoring compatibility.

Schema discipline does not reduce intelligence. It removes ambiguity that masquerades as intelligence.

---

## 8. Human review in an evidence-first system

Human judgment remains essential, but it must attach to evidence rather than float above it.

Good human review asks:
- what artifact supports this claim,
- is the reviewer independent,
- does the artifact actually map to the claimed domain,
- what would falsify the claim?

Weak human review asks:
- does this “feel senior,”
- does this “sound strategic,”
- does this “seem impressive.”

The evidence-first doctrine rejects those weaker forms.

---

## 9. Evidence-first and frontier models

Frontier models become more useful when they are forced to operate on canonicalized evidence rather than free-form narrative.

This improves:
- scoring consistency,
- hallucination resistance,
- auditability,
- multi-agent coordination,
- reproducibility.

The model stops being a charismatic interpreter and becomes a bounded evaluator.

---

## 10. Evidence-first and security work

Security is especially vulnerable to narrative inflation because much of the work is invisible until failure.

That makes evidence discipline even more important.

For security roles, strong evidence often includes:
- control state evidence,
- incident response material,
- attack-path analysis,
- IAM policy changes,
- threat models,
- detection engineering outputs,
- measurable reduction in risk or recovery time.

The standard is not “I improved security.”
The standard is “Here is the evidence surface through which that statement becomes evaluable.”

---

## 11. Failure cases this doctrine prevents

Evidence-first engineering directly reduces:
- self-credit inflation,
- unverifiable strategic claims,
- portfolio theater,
- duplicate artifact reuse,
- confidence without provenance,
- post-hoc rewriting of contribution boundaries.

The doctrine is harsh because the environment is adversarial: both people and models are tempted to smooth uncertainty into persuasive coherence.

---

## 12. Practical operating rule

For any important claim, ask the sequence:

1. What is the primary artifact?
2. Has it been normalized?
3. Is the schema valid?
4. Is the provenance clear?
5. Is the fingerprint fixed?
6. Is the reviewer independent?
7. Does the artifact map directly to the scored task?
8. What gate fails if this artifact is removed?

If the sequence cannot be completed, the claim is not yet robust.

---

## Closing statement

Evidence-first engineering does not make systems cold. It makes them honest.

It does not deny the value of judgment. It gives judgment a disciplined substrate.

In this repository, intelligence becomes credible only when it passes through evidence.
