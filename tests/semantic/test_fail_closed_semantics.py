#!/usr/bin/env python3
import subprocess
import unittest


class FailClosedSemanticTests(unittest.TestCase):
    def test_fail_closed_script(self):
        proc = subprocess.run(
            ["python", "tools/assert_fail_closed_semantics.py"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("FAIL_CLOSED_SEMANTIC_OK", proc.stdout)


if __name__ == "__main__":
    unittest.main()
