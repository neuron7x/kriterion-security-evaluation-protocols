# LINKEDIN_POST_01_PRIMARY

Every security capability framework I have seen fails at the same point: the evidence runs out, and the evaluator keeps scoring anyway.

Missing proof gets replaced with narrative judgment.
Confident candidates get overrated.
Self-attested contribution gets treated as evidence.
Promotion packets become persuasion contests.

I built the correction.

The repository I just published is a fail-closed, audit-grade evaluation system for the human security engineering role ladder:
Security Engineer → Senior / Lead → Architect → Principal → Distinguished.

It does not score from impression first and artifacts second. It does the opposite.

Six protocols.
Deterministic scoring.
Evidence Confidence tiering that caps scores when artifacts cannot be independently verified.
Gate logic that can fail a candidate even when the narrative looks strong.
Prompt-injection resistance that treats artifact content as data, not instructions.

One concrete example: the anti-gaming layer can detect when the same artifact is being stretched across too many domain tasks and reduce its admissible support instead of rewarding repetition as breadth.

That matters because the easiest candidate to over-promote is not the weakest engineer.
It is the engineer who is strongest at filling evidence gaps with a clean story.

The repository includes the protocols, the hardening layer, schemas, a worked example, a synthetic benchmark harness, and the commercial/community licensing split.

GitHub:
https://github.com/neuron7x/kriterion-security-protocols

If you have ever promoted someone who looked great on paper and failed in the role, read `THREAT_MODEL_FOR_AI_EVALUATION.md` first.
