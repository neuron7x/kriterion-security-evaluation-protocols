# LINKEDIN_POST_02_EVIDENCE_CONFIDENCE

Rubric scoring alone is not enough.

A candidate can look like a 4/5 under a standard rubric and still deserve a 2/5 cap once you ask a harder question:

How much of this score is actually supported by independently verifiable evidence?

That is why the protocols in this repository do not stop at rubric labels.
They apply Evidence Confidence tiering.

LOW confidence means the artifacts may be relevant but cannot justify a high score.
MED means partially verified, partially bounded.
HIGH means the evidence can carry real weight because provenance, structure, and independent review hold.

This matters because most evaluation systems collapse these states into one number.

Cloudflare’s public confidence scoring work is useful because it shows how structured confidence can improve consistency. The difference here is that I do not use confidence as commentary. I use it as a score cap.

So the evaluator is not free to say:
“Looks like a 4.”

The evaluator has to say:
“Raw 4, capped to 2 because EC is LOW.”

That changes hiring and promotion outcomes immediately.

It prevents clean communication from outrunning proof.
It makes missing provenance expensive.
It forces the evaluator to separate quality from admissibility.

Repository:
https://github.com/neuron7x/kriterion-security-protocols

If your current framework has one rubric number but no confidence cap tied to evidence quality, it is still failing open.
