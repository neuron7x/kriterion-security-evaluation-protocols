#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.pr_intake_contract import REQUIRED_HEADINGS

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'tools' / 'validate_pr_intake.py'


def run_with_payload(payload: dict) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory(prefix='pr-intake-') as td:
        event = Path(td) / 'event.json'
        event.write_text(json.dumps(payload), encoding='utf-8')
        env = os.environ.copy()
        env['GITHUB_EVENT_NAME'] = 'pull_request'
        env['GITHUB_EVENT_PATH'] = str(event)
        return subprocess.run([sys.executable, str(SCRIPT)], env=env, capture_output=True, text=True, check=False)


def valid_body() -> str:
    return (
        '## Problem\nDetailed problem statement with concrete governance risk and affected behavior.\n\n'
        '## Scope\nExplicitly bounded list of changed files and excluded areas to avoid scope creep.\n\n'
        '## Invariants touched\nEnumerates changed invariant identifiers and machine-verification classes.\n\n'
        '## Evidence\nLists deterministic command outputs and observed gate status signals.\n\n'
        '## Risks\nNames realistic failure modes and concrete mitigation already implemented.\n\n'
        '## Non-goals\nStates what was intentionally excluded from this pull request.\n\n'
        '## Manifest refresh justification\nExplains exactly why MANIFEST hashes changed and which files were updated.\n\n'
        '## Human review required\nIdentifies reviewer judgments that remain constitutionally human.\n\n'
        '## Policy-drift review (mandatory for governance-critical surfaces)\nDocuments governance-surface drift assessment and reviewer decision rationale.\n'
    )


class PRIntakeValidatorTests(unittest.TestCase):


    def test_pull_request_template_headings_match_contract(self):
        template = (ROOT / '.github' / 'pull_request_template.md').read_text(encoding='utf-8')
        headings = [line.strip() for line in template.splitlines() if line.startswith('## ')]
        self.assertEqual(headings[: len(REQUIRED_HEADINGS)], REQUIRED_HEADINGS)

    def test_missing_required_section_fails(self):
        payload = {'pull_request': {'body': '## Problem\nOnly one section present with enough words to avoid placeholder detection.\n'}}
        proc = run_with_payload(payload)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('PR_INTAKE_INVALID', proc.stdout + proc.stderr)

    def test_placeholder_content_fails(self):
        payload = {
            'pull_request': {
                'body': (
                    '## Problem\nplaceholder\n\n'
                    '## Scope\nplaceholder\n\n'
                    '## Invariants touched\nplaceholder\n\n'
                    '## Evidence\nplaceholder\n\n'
                    '## Risks\nplaceholder\n\n'
                    '## Non-goals\nplaceholder\n\n'
                    '## Manifest refresh justification\nplaceholder\n\n'
                    '## Human review required\nplaceholder\n\n'
                    '## Policy-drift review (mandatory for governance-critical surfaces)\nplaceholder\n'
                )
            }
        }
        proc = run_with_payload(payload)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('PR_INTAKE_INVALID', proc.stdout + proc.stderr)

    def test_valid_structured_pr_passes(self):
        payload = {'pull_request': {'body': valid_body()}}
        proc = run_with_payload(payload)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn('PR_INTAKE_OK', proc.stdout)

    def test_substantive_text_with_none_or_na_passes(self):
        body = valid_body().replace(
            '## Non-goals\nStates what was intentionally excluded from this pull request.\n\n',
            '## Non-goals\nNone beyond documentation changes; benchmark path untouched.\n\n',
        ).replace(
            '## Manifest refresh justification\nExplains exactly why MANIFEST hashes changed and which files were updated.\n\n',
            '## Manifest refresh justification\nN/A for manifest refresh because hashes did not change.\n\n',
        )
        payload = {'pull_request': {'body': body}}
        proc = run_with_payload(payload)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn('PR_INTAKE_OK', proc.stdout)


    def test_concise_but_substantive_section_passes(self):
        body = valid_body().replace(
            '## Manifest refresh justification\nExplains exactly why MANIFEST hashes changed and which files were updated.\n\n',
            '## Manifest refresh justification\nNo manifest changes required.\n\n',
        )
        payload = {'pull_request': {'body': body}}
        proc = run_with_payload(payload)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn('PR_INTAKE_OK', proc.stdout)

    def test_trivially_short_section_fails(self):
        body = valid_body().replace(
            '## Evidence\nLists deterministic command outputs and observed gate status signals.\n\n',
            '## Evidence\nLooks fine now.\n\n',
        )
        payload = {'pull_request': {'body': body}}
        proc = run_with_payload(payload)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('PR_INTAKE_INVALID ## Evidence', proc.stdout + proc.stderr)

    def test_placeholder_only_sections_fail(self):
        body = valid_body().replace(
            '## Evidence\nLists deterministic command outputs and observed gate status signals.\n\n',
            '## Evidence\nN/A\n\n',
        )
        payload = {'pull_request': {'body': body}}
        proc = run_with_payload(payload)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('PR_INTAKE_INVALID', proc.stdout + proc.stderr)

    def test_out_of_order_required_headings_fail(self):
        body = valid_body().replace('## Scope', '## Scope_TMP').replace('## Invariants touched', '## Scope').replace('## Scope_TMP', '## Invariants touched')
        payload = {'pull_request': {'body': body}}
        proc = run_with_payload(payload)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('PR_INTAKE_INVALID ORDER', proc.stdout + proc.stderr)

    def test_duplicate_required_heading_fails(self):
        body = valid_body() + '\n## Scope\nDuplicate heading should be rejected even if text is substantive enough.\n'
        payload = {'pull_request': {'body': body}}
        proc = run_with_payload(payload)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('PR_INTAKE_INVALID DUPLICATE ## Scope', proc.stdout + proc.stderr)

    def test_missing_required_heading_fails_explicitly(self):
        body = valid_body().replace(
            '## Risks\nNames realistic failure modes and concrete mitigation already implemented.\n\n',
            '',
        )
        payload = {'pull_request': {'body': body}}
        proc = run_with_payload(payload)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('PR_INTAKE_INVALID MISSING ## Risks', proc.stdout + proc.stderr)


if __name__ == '__main__':
    unittest.main()
