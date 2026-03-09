import json
import subprocess
import unittest
from pathlib import Path


class CliIntegrationTests(unittest.TestCase):
    def test_cli_commands(self):
        tmp = Path("/tmp/pcos-cli-tests")
        tmp.mkdir(parents=True, exist_ok=True)
        ir = tmp / "out.ir.json"
        manifest = tmp / "run_manifest.json"
        prompt = Path("examples/pure_symbolic.prompt")

        self.assertEqual(subprocess.run(["python", "-m", "pcos.cli", "compile", str(prompt), "--out", str(ir)], check=False).returncode, 0)
        self.assertEqual(subprocess.run(["python", "-m", "pcos.cli", "run", str(ir), "--out", str(manifest)], check=False).returncode, 0)
        self.assertEqual(subprocess.run(["python", "-m", "pcos.cli", "verify", str(manifest)], check=False).returncode, 0)
        self.assertEqual(subprocess.run(["python", "-m", "pcos.cli", "bench"], check=False).returncode, 0)
        self.assertEqual(subprocess.run(["python", "-m", "pcos.cli", "replay", str(manifest)], check=False).returncode, 0)

        payload = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual(payload["verifier_result"]["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
