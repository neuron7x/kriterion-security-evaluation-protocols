#!/usr/bin/env python3
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class VerifyExecutionChainTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="verify-chain-"))
        self.input_bundle = Path("examples/worked-example/SE_WORKED_EXAMPLE_INPUT.json")
        self.result = self.tmp / "result.json"
        run = subprocess.run(
            [
                "python",
                "tools/reference_runner.py",
                str(self.input_bundle),
                "--allow-non-authoritative-git",
                "--output",
                str(self.result),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)

    def _verify(self, result_path: Path):
        return subprocess.run(
            [
                "python",
                "tools/verify_execution_chain.py",
                "--input",
                str(self.input_bundle),
                "--result",
                str(result_path),
                "--allow-non-authoritative-git",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_verifier_passes_on_canonical_output(self):
        proc = self._verify(self.result)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["status"], "VERIFIED")
        self.assertEqual(payload["chain_format_version"], "execution_chain.v1")
        self.assertIn("input_bundle_hash", payload)

    def test_verifier_rejects_continuity_drift(self):
        payload = json.loads(self.result.read_text(encoding="utf-8"))
        payload["execution_state_chain"][3]["previous_step_hash"] = "0" * 64
        tampered = self.tmp / "tampered-continuity.json"
        tampered.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        proc = self._verify(tampered)
        self.assertNotEqual(proc.returncode, 0)

    def test_verifier_rejects_terminal_mismatch(self):
        payload = json.loads(self.result.read_text(encoding="utf-8"))
        payload["execution_chain_terminal_hash"] = "0" * 64
        tampered = self.tmp / "tampered-terminal.json"
        tampered.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        proc = self._verify(tampered)
        self.assertNotEqual(proc.returncode, 0)

    def test_verifier_rejects_replay_capsule_mismatch(self):
        payload = json.loads(self.result.read_text(encoding="utf-8"))
        payload["execution_state_chain"][1]["replay_capsule"]["admitted_artifact_ids"] = []
        tampered = self.tmp / "tampered-capsule.json"
        tampered.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        proc = self._verify(tampered)
        self.assertNotEqual(proc.returncode, 0)

    def test_verifier_rejects_admitted_fingerprint_mismatch(self):
        payload = json.loads(self.result.read_text(encoding="utf-8"))
        payload["execution_state_chain"][1]["replay_capsule"]["admitted_artifact_fingerprints"] = ["0" * 64]
        tampered = self.tmp / "tampered-fps.json"
        tampered.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        proc = self._verify(tampered)
        self.assertNotEqual(proc.returncode, 0)

    def test_verifier_rejects_gate_state_mismatch(self):
        payload = json.loads(self.result.read_text(encoding="utf-8"))
        payload["execution_state_chain"][4]["replay_capsule"]["gate_state"]["G0_INTEGRITY"] = "FAIL"
        tampered = self.tmp / "tampered-gate-state.json"
        tampered.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        proc = self._verify(tampered)
        self.assertNotEqual(proc.returncode, 0)

    def test_verifier_rejects_phase_duplication(self):
        payload = json.loads(self.result.read_text(encoding="utf-8"))
        payload["execution_state_chain"][3]["phase_id"] = payload["execution_state_chain"][2]["phase_id"]
        tampered = self.tmp / "tampered-dup-phase.json"
        tampered.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        proc = self._verify(tampered)
        self.assertNotEqual(proc.returncode, 0)

    def test_verifier_rejects_phase_order_swap(self):
        payload = json.loads(self.result.read_text(encoding="utf-8"))
        payload["execution_state_chain"][1], payload["execution_state_chain"][2] = payload["execution_state_chain"][2], payload["execution_state_chain"][1]
        tampered = self.tmp / "tampered-order.json"
        tampered.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        proc = self._verify(tampered)
        self.assertNotEqual(proc.returncode, 0)

    def test_verifier_rejects_contract_version_tamper(self):
        payload = json.loads(self.result.read_text(encoding="utf-8"))
        payload["execution_state_chain"][0]["contract_version"] = "9999.0"
        tampered = self.tmp / "tampered-contract-version.json"
        tampered.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        proc = self._verify(tampered)
        self.assertNotEqual(proc.returncode, 0)

    def test_verifier_rejects_chain_format_version_tamper(self):
        payload = json.loads(self.result.read_text(encoding="utf-8"))
        payload["execution_chain_format_version"] = "execution_chain.v999"
        tampered = self.tmp / "tampered-chain-format.json"
        tampered.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        proc = self._verify(tampered)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("UNKNOWN_CHAIN_FORMAT", proc.stdout + proc.stderr)

    def test_verifier_rejects_admitted_artifact_id_mismatch(self):
        payload = json.loads(self.result.read_text(encoding="utf-8"))
        payload["execution_state_chain"][1]["replay_capsule"]["admitted_artifact_ids"] = ["NON_EXISTENT_ARTIFACT"]
        tampered = self.tmp / "tampered-admitted-ids.json"
        tampered.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        proc = self._verify(tampered)
        self.assertNotEqual(proc.returncode, 0)

    def test_verifier_rejects_bundle_payload_fingerprint_inconsistency(self):
        bundle = json.loads(self.input_bundle.read_text(encoding="utf-8"))
        bundle["artifacts"][0]["payload"]["summary"] = "tampered"
        tampered_bundle = self.tmp / "tampered-input-bundle.json"
        tampered_bundle.write_text(json.dumps(bundle, indent=2), encoding="utf-8")
        proc = subprocess.run(
            [
                "python",
                "tools/verify_execution_chain.py",
                "--input",
                str(tampered_bundle),
                "--result",
                str(self.result),
                "--allow-non-authoritative-git",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("bundle artifact fingerprint mismatch", proc.stdout + proc.stderr)


    def test_verifier_strict_git_authority_rejects_untracked_critical_file(self):
        marker = Path("tools/.tmp.verify-chain.untracked")
        marker.write_text("x", encoding="utf-8")
        try:
            proc = subprocess.run(
                [
                    "python",
                    "tools/verify_execution_chain.py",
                    "--input",
                    str(self.input_bundle),
                    "--result",
                    str(self.result),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("GIT_AUTHORITY_INVALID", proc.stdout + proc.stderr)
        finally:
            marker.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
