# CHANGELOG

## 2026.4.5 — identity rename pass
- renamed the public project identity from `Audit-Grade Security Protocols 2026` to `KRITERION`
- updated the repository slug to `kriterion-security-protocols`
- aligned README, citation metadata, visual pages, benchmark docs, legal references, and business documents with the new name
- preserved protocol filenames and core evaluation logic unchanged

## 2026.4.4 — final polish pass
- removed trailing whitespace from DSE protocol, benchmark report, and cognitive fingerprint formatting
- normalized README list style and removed public link to the internal pricing decision tree
- added `date-released` to `CITATION.cff`
- replaced one remaining buzzword in `CAPABILITY_EVOLUTION_PATHWAY.md`
- tightened spacing in `SOVEREIGN_TERMS.md`
- sharpened the closing line in LinkedIn Post 04
- added `**/__pycache__/` to `.gitignore`

## 2026.4.3 — validation, naturalness, and output-consistency pass
- regenerated example and result JSON objects to include `final_classification.integrity_hash`
- patched benchmark runner to survive fail-closed injection cases during demo runs
- normalized Anthropic references in benchmark and bibliography files
- removed defensive placeholder wording from public-facing documents
- added `docs/STYLE_AND_NATURALNESS_REPORT.md`
- added `docs/VALIDATION_REPORT_2026.4.3.md`

## 2026.4.2 — integrity hardening pass
- hardened `tools/verify_manifest.py` to block deploy on first integrity violation
- tightened `LICENSE.md` with explicit 10× liquidated-damages AI-system clause
- updated `tools/reference_runner.py` to halt fail-closed on injection detection
- extended `schemas/evaluation-result.schema.json` to require `final_classification.integrity_hash`
- updated benchmark metrics to include `integrity_violation_count`

## 2026.4.1 — Business activation layer
- added `METHODOLOGY.md`
- added `THREAT_MODEL_FOR_AI_EVALUATION.md`
- added `SOVEREIGN_TERMS.md`
- added `FIELD_REPORT.md`
- added `COGNITIVE_FINGERPRINT.md`
- added LinkedIn, Gumroad, inquiry, pricing, GitHub metadata, and priority-evidence business documents
- updated `README.md` with the “Why this exists” section and business activation references
- updated `CITATION.cff` with public repository URL, business-oriented keywords, and version 2026.4.1
- removed `tools/__pycache__/` from the publishable repository state where possible
- refreshed `repo-map.json` and `MANIFEST.json`

# Changelog

## 2026.4.0 — Complete community edition
- replaced placeholder licensing layer with active community and commercial licensing documents
- added reference runner, input-bundle schema, worked example, and end-to-end runbook
- added synthetic benchmark demo pack with dataset manifest, logs, results, and metric scripts
- refreshed bibliography and model references to current official pages
- added roadmap, version file, robots.txt, and additional repository governance docs

## 2026.3.0
- execution-grade hardening bundle added with schemas, execution contracts, fixtures, and tools

## 2026.2.0
- benchmark governance and doctrine layer introduced

## 2026.1.0
- base protocol set assembled
