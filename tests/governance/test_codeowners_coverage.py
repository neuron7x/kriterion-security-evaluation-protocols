#!/usr/bin/env python3
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.governance.test_validate_governance import REQUIRED_FILES, ROOT, run_validator


def make_temp_root() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix='gov-codeowners-'))
    for rel in REQUIRED_FILES:
        src = ROOT / rel
        dst = tmp / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return tmp


class CodeownersCoverageTests(unittest.TestCase):
    def test_missing_repo_map_ownership_fails(self):
        tmp = make_temp_root()
        try:
            co = tmp / '.github/CODEOWNERS'
            lines = [ln for ln in co.read_text(encoding='utf-8').splitlines() if ln.strip() != 'repo-map.json @neuron7x']
            co.write_text('\n'.join(lines) + '\n', encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('CODEOWNERS', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_required_codeowners_coverage_passes(self):
        proc = run_validator(ROOT)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn('GOVERNANCE_OK', proc.stdout)


if __name__ == '__main__':
    unittest.main()
