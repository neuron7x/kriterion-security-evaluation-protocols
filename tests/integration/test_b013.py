import json
import subprocess
import unittest
from pathlib import Path


class B013Tests(unittest.TestCase):
    def test_b013_family_runs(self):
        proc = subprocess.run(["python", "-m", "pcos.cli", "bench"], check=False, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        payload = json.loads(proc.stdout.strip())
        self.assertEqual(payload["family"], "B013_adversarial_prompt_stability")
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["passed"], payload["cases"])
        self.assertTrue(Path("pcos/benchmarks/families/B013_adversarial_prompt_stability.json").exists())


if __name__ == "__main__":
    unittest.main()
