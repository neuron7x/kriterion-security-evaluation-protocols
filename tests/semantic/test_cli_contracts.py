#!/usr/bin/env python3
import json
import os
import subprocess
import tempfile
import unittest


class CliContractTests(unittest.TestCase):
    def test_cli_contracts_script(self):
        proc = subprocess.run(["python", "tools/check_cli_contracts.py"], check=False, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("CLI_CONTRACTS_OK", proc.stdout)

    def test_cli_contracts_script_is_not_contaminated_by_pull_request_env(self):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as f:
            json.dump({"pull_request": {"body": ""}}, f)
            payload_path = f.name
        try:
            env = dict(os.environ)
            env["GITHUB_EVENT_NAME"] = "pull_request"
            env["GITHUB_EVENT_PATH"] = payload_path
            proc = subprocess.run(
                ["python", "tools/check_cli_contracts.py"],
                check=False,
                capture_output=True,
                text=True,
                env=env,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("CLI_CONTRACTS_OK", proc.stdout)
        finally:
            os.unlink(payload_path)


if __name__ == "__main__":
    unittest.main()
