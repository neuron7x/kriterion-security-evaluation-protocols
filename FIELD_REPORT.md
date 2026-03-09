# FIELD_REPORT

This document shows what the protocols actually do when confronted with candidate evidence. The cases below are synthetic but structured to match real evaluation pressure.

## Field Report 1 — Senior Security Engineer candidate, fintech company

### Submitted evidence
The candidate submitted:
- two merged pull requests for detection rule improvements,
- one post-incident retrospective,
- one runbook revision,
- one dashboard screenshot,
- one manager note claiming the candidate “led the response.”

### What the protocol found
The artifact bundle was operationally relevant but uneven.

Execution and incident handling evidence was admissible. Detection work mapped cleanly to role requirements. The manager note did not qualify as independent proof of leadership. The dashboard screenshot lacked enough provenance to support a HIGH confidence claim.

**Observed pattern:**
- operational execution: strong
- metrics traceability: medium
- cross-team leadership claim: weak
- reviewer independence: insufficient for HIGH confidence

**Gate outcome:** pass on integrity, pass on minimum readiness, pass on evidence sufficiency with score caps applied.

**Classification verdict:** solid Senior-level execution, not Lead-level breadth.

### What a standard evaluation would likely miss
A standard panel review would probably over-credit the leadership claim because the candidate communicated clearly and the manager note sounded authoritative. The protocol did not. It treated that note as weak evidence and prevented score inflation.

---

## Field Report 2 — Enterprise Security Architect candidate, B2B SaaS company

### Submitted evidence
The candidate submitted:
- a trust-boundary diagram,
- an architecture decision record,
- an IAM policy proposal,
- a migration plan,
- a design review signed by the same architect who authored the decision record.

### What the protocol found
The architecture material was conceptually strong. The trust-boundary work was meaningful. But the review chain was circular. The same actor appeared in authoring and approval pathways. The migration plan also lacked operational validation artifacts.

**Observed pattern:**
- architecture reasoning: high potential
- authorization and trust-boundary structure: credible
- execution proof: incomplete
- reviewer independence: compromised

**Gate outcome:** integrity warning triggered; evidence confidence reduced; final classification constrained by capped scores.

**Classification verdict:** architect-capable, but not enterprise-grade under fail-closed review.

### What a standard evaluation would likely miss
A conventional architecture interview would likely reward the quality of the diagram and the clarity of the ADR. This protocol asked a harder question: who independently validated it, and what operational evidence shows it survived implementation pressure? That question changed the result.

---

## Field Report 3 — Principal Security Engineer promotion case, internal review

### Submitted evidence
The promotion packet included:
- a platform roadmap,
- three architecture review notes,
- one internal strategy memo,
- two references from adjacent managers,
- reused artifacts that had already been cited in multiple unrelated domain claims.

### What the protocol found
The packet showed broad influence but also classic internal-promotion inflation. The same artifacts were being stretched across too many domain tasks. Several claims of platform impact were supported only by strategy language rather than measurable control-state changes.

**Observed pattern:**
- systems thinking: present
- platform leverage: partially evidenced
- artifact reuse across domains: excessive
- measurable implementation effect: under-documented

**Gate outcome:** anti-gaming pressure applied; reused artifacts reduced admissible support; evidence sufficiency for some domains failed.

**Classification verdict:** strong senior/principal trajectory, but promotion case not clean enough to justify Principal classification under this framework.

### What a standard evaluation would likely miss
Internal promotion processes often reward coherence of narrative, organizational visibility, and executive confidence. The protocol does not ignore those signals, but it refuses to score them as proof. The result is harsher, but also more defensible.
