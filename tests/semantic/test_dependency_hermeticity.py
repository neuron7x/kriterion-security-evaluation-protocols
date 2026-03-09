#!/usr/bin/env python3
import subprocess
import unittest


class DependencyHermeticityTests(unittest.TestCase):
    def test_dependency_hermeticity_script(self):
        proc = subprocess.run(["python", "tools/check_dependency_hermeticity.py"], check=False, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("DEPENDENCY_HERMETICITY_OK", proc.stdout)


if __name__ == "__main__":
    unittest.main()
