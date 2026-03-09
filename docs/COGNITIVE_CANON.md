# COGNITIVE CANON

## Purpose

This document defines the canonical cognitive design principles behind the project. It is a canon not because it is rigidly dogmatic, but because it identifies the stable mental patterns that produce reliable, high-resolution work with frontier models.

The subject here is not human cognition in general. It is the design of model-facing cognition: how one should structure thought so that advanced systems can execute it without collapsing into ambiguity, drift, or decorative complexity.

---

## Canon 1 — Separate observation from interpretation

Every serious reasoning system must distinguish:
- what is observed,
- what is inferred,
- what is assumed,
- what remains unknown.

When these categories blur, models begin treating assumption as evidence and style as certainty.

A canonical workflow explicitly labels the difference.

---

## Canon 2 — Treat ambiguity as a state, not as a defect to hide

Ambiguity is often informative. It may indicate:
- insufficient evidence,
- under-specified intent,
- conflicting sources,
- unresolved trade-offs.

The wrong response to ambiguity is improvisational certainty.
The right response is structured handling:
- clarification,
- narrowed scope,
- multiple bounded interpretations,
- explicit uncertainty markers,
- conservative defaults.

---

## Canon 3 — Thought must be decomposable

High-quality reasoning can be partitioned into parts:
- claim,
- evidence,
- rule,
- exception,
- output consequence.

If the reasoning cannot be decomposed, it is difficult to debug, reproduce, or audit.

Decomposability is one of the clearest signs that cognition has crossed from inspiration into engineering.

---

## Canon 4 — Depth should be earned, not assumed

Not every task deserves the same reasoning depth.

Cognitive over-expansion creates:
- latency,
- noise,
- false complexity,
- self-distraction,
- hidden inconsistency.

The canon favors depth-gating:
- fast path for routine validation,
- deeper analysis for conflict, architecture, or adversarial review,
- refusal or deferral when evidence remains weak.

This preserves both rigor and efficiency.

---

## Canon 5 — Reasoning should be geometry-aware

Tasks differ by geometry:
- some are linear,
- some are branching,
- some are hierarchical,
- some are adversarial,
- some are graph-structured,
- some are primarily comparative.

The same reasoning pattern should not be forced onto every problem.

Cognitive design improves when the reasoning shape matches the task shape.

---

## Canon 6 — Comparison is more informative than isolated judgment

Many weak evaluations fail because they ask only:
- “Is this good?”
- “Is this strong?”
- “Is this sufficient?”

Canonical cognition instead asks:
- compared to what,
- under which criteria,
- with what evidence class,
- against which alternatives,
- under what failure modes.

Comparative structure reveals trade-offs that isolated judgments conceal.

---

## Canon 7 — A claim is not mature until its failure conditions are explicit

A strong design claim includes:
- where it works,
- where it weakens,
- what would falsify it,
- what evidence would overturn it,
- what failure mode it creates elsewhere.

Without failure conditions, a claim is still promotional.

---

## Canon 8 — Precision requires taxonomy

A model cannot reason precisely about a domain that has not been taxonomized.

Taxonomy reduces drift by defining:
- object types,
- relation types,
- evidence types,
- error types,
- attack types,
- output classes.

This is why robust prompt systems rely on typed artifacts, gates, schemas, and explicit categories.

---

## Canon 9 — Internal elegance must serve external verification

A reasoning process may feel elegant internally and still be operationally weak.

Canonical cognition judges thought by:
- correctness,
- traceability,
- usefulness,
- reproducibility,
- adversarial stability.

Beauty in thought is welcome, but only when it survives verification.

---

## Canon 10 — Verification must remain closer to reality than explanation

Models are excellent at explanation. They are less reliable at self-verification unless forced into evidence-bearing structures.

Therefore the canon places verification closer to:
- artifacts,
- tests,
- logs,
- schemas,
- hashes,
- measured outputs,

than to interpretive prose.

Explanation should illuminate verification, not replace it.

---

## Canon 11 — Reasoning must maintain conservation of evidence

A conclusion cannot legitimately contain more confidence than its evidence base can support.

This canon prohibits:
- confidence inflation,
- evidence laundering through summary,
- certainty gained by repetition,
- authority inferred from tone.

The system may refine structure, but it may not create epistemic mass from nothing.

---

## Canon 12 — Good cognitive systems expose their own edges

A mature reasoning system knows where it becomes less trustworthy:
- context saturation,
- evidence sparsity,
- source conflict,
- specification gaps,
- model/tool boundary ambiguity.

By exposing edges explicitly, the system becomes safer and easier to improve.

---

## Canon 13 — Adversarial review is part of thought, not a late add-on

A reasoning process is incomplete until it has asked:
- how could this be gamed,
- how could this fail under pressure,
- what false positive path exists,
- what false negative path exists,
- what manipulation vector remains open.

Red-teaming is not anti-creativity. It is disciplined creativity.

---

## Canon 14 — The highest form of prompt design is cognitive governance

At the frontier, prompt engineering is no longer merely instruction writing. It becomes governance of model cognition:
- what is allowed,
- what is mandatory,
- what is evidence,
- what counts as completion,
- what uncertainty looks like,
- how outputs enter institutional systems.

That governance function is the real canon.

---

## Closing statement

The canonical question is not:
“Can the model produce an impressive answer?”

The canonical question is:
“Can the model participate in a disciplined cognitive system that remains valid under constraint, ambiguity, and audit?”

Everything in this repository is downstream of that question.
