import subprocess
import unittest
from pathlib import Path


class E2EPipelineTests(unittest.TestCase):
    def test_e2e_pipeline(self):
        tmp = Path("/tmp/pcos-e2e-tests")
        tmp.mkdir(parents=True, exist_ok=True)
        ir = tmp / "e2e.ir.json"
        manifest = tmp / "e2e.manifest.json"
        prompt = Path("examples/e2e.prompt")

        self.assertEqual(subprocess.run(["python", "-m", "pcos.cli", "compile", str(prompt), "--out", str(ir)], check=False).returncode, 0)
        self.assertEqual(subprocess.run(["python", "-m", "pcos.cli", "run", str(ir), "--out", str(manifest)], check=False).returncode, 0)
        self.assertEqual(subprocess.run(["python", "-m", "pcos.cli", "verify", str(manifest)], check=False).returncode, 0)
        self.assertEqual(subprocess.run(["python", "-m", "pcos.cli", "replay", str(manifest)], check=False).returncode, 0)


if __name__ == "__main__":
    unittest.main()
