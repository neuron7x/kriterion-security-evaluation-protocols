#!/usr/bin/env python3
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.governance.test_validate_governance import REQUIRED_FILES, ROOT, run_validator


def make_temp_root() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix='gov-root-map-'))
    for rel in REQUIRED_FILES:
        src = ROOT / rel
        dst = tmp / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return tmp


class GovernanceRootMappingTests(unittest.TestCase):
    def test_missing_root_governance_file_fails(self):
        tmp = make_temp_root()
        try:
            repo_map = tmp / 'repo-map.json'
            payload = json.loads(repo_map.read_text(encoding='utf-8'))
            payload['root'] = [x for x in payload['root'] if x != 'MANIFEST.json']
            repo_map.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('REPO_MAP', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_root_governance_mapping_passes(self):
        proc = run_validator(ROOT)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn('GOVERNANCE_OK', proc.stdout)


if __name__ == '__main__':
    unittest.main()
