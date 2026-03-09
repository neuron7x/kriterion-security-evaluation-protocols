#!/usr/bin/env python3
import subprocess
import unittest


class CanonicalizationEdgeCaseTests(unittest.TestCase):
    def test_negative_cases_script(self):
        proc = subprocess.run(
            ["python", "tools/check_canonicalization_negative_cases.py"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("CANONICALIZATION_NEGATIVE_CASES_OK", proc.stdout)

    def test_negative_cases_script_via_runpy_entrypoint(self):
        proc = subprocess.run(
            [
                "python",
                "-c",
                "import runpy; runpy.run_path('tools/check_canonicalization_negative_cases.py', run_name='__main__')",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("CANONICALIZATION_NEGATIVE_CASES_OK", proc.stdout)


if __name__ == "__main__":
    unittest.main()
