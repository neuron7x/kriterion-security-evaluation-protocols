#!/usr/bin/env python3
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class VerifyCiArtifactManifestTests(unittest.TestCase):
    def test_required_artifact_class_and_required_name_enforced(self):
        with tempfile.TemporaryDirectory(prefix='ci-artifact-manifest-') as td:
            root = Path(td)
            out = root / 'out.json'
            out_bytes = b'{"status":"OK"}\n'
            out.write_bytes(out_bytes)
            manifest = {
                'artifacts': [
                    {
                        'name': 'worked-example-output',
                        'path': out.name,
                        'artifact_class': 'required',
                        'size_bytes': len(out_bytes),
                        'sha256': sha256_bytes(out_bytes),
                        'producer_job': 'job-a',
                    }
                ]
            }
            mpath = root / 'manifest.json'
            mpath.write_text(json.dumps(manifest), encoding='utf-8')
            proc = subprocess.run(
                [
                    'python', 'tools/verify_ci_artifact_manifest.py', str(mpath),
                    '--root', str(root),
                    '--expected-producer', 'job-a',
                    '--name-prefix', 'worked-example',
                    '--require-name', 'worked-example-output',
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn('CI_ARTIFACT_MANIFEST_OK', proc.stdout)

    def test_missing_required_name_fails(self):
        with tempfile.TemporaryDirectory(prefix='ci-artifact-manifest-') as td:
            root = Path(td)
            out = root / 'out.log'
            data = b'log\n'
            out.write_bytes(data)
            manifest = {
                'artifacts': [
                    {
                        'name': 'worked-example-log',
                        'path': out.name,
                        'artifact_class': 'diagnostic',
                        'size_bytes': len(data),
                        'sha256': sha256_bytes(data),
                        'producer_job': 'job-a',
                    }
                ]
            }
            mpath = root / 'manifest.json'
            mpath.write_text(json.dumps(manifest), encoding='utf-8')
            proc = subprocess.run(
                [
                    'python', 'tools/verify_ci_artifact_manifest.py', str(mpath),
                    '--root', str(root),
                    '--expected-producer', 'job-a',
                    '--name-prefix', 'worked-example',
                    '--require-name', 'worked-example-output',
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('required-artifact-missing:worked-example-output', proc.stdout + proc.stderr)

    def test_zero_byte_diagnostic_artifact_is_allowed(self):
        with tempfile.TemporaryDirectory(prefix='ci-artifact-manifest-') as td:
            root = Path(td)
            out = root / 'benchmark.runner.log'
            data = b''
            out.write_bytes(data)
            manifest = {
                'artifacts': [
                    {
                        'name': 'benchmark-log',
                        'path': out.name,
                        'artifact_class': 'diagnostic',
                        'size_bytes': len(data),
                        'sha256': sha256_bytes(data),
                        'producer_job': 'job-b',
                    }
                ]
            }
            mpath = root / 'manifest.json'
            mpath.write_text(json.dumps(manifest), encoding='utf-8')
            proc = subprocess.run(
                [
                    'python', 'tools/verify_ci_artifact_manifest.py', str(mpath),
                    '--root', str(root),
                    '--expected-producer', 'job-b',
                    '--name-prefix', 'benchmark',
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn('CI_ARTIFACT_MANIFEST_OK', proc.stdout)


if __name__ == '__main__':
    unittest.main()
