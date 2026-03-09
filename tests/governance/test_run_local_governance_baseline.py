#!/usr/bin/env python3
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools" / "run_local_governance_baseline.py"

sys.path.insert(0, str(ROOT / "tools"))
import run_local_governance_baseline as baseline  # noqa: E402


class RunLocalGovernanceBaselineTests(unittest.TestCase):
    def test_execute_policy_map_rejects_stale_exit_overrides(self):
        with self.assertRaises(SystemExit) as ctx:
            baseline.validate_execute_contract([])
        self.assertIn("BASELINE_EXIT_OVERRIDE_STALE", str(ctx.exception))


    def test_execute_policy_map_rejects_stale_dirty_policies(self):
        commands = list(baseline.EXPECTED_EXIT_OVERRIDES)
        with self.assertRaises(SystemExit) as ctx:
            baseline.validate_execute_contract(commands)
        self.assertIn("BASELINE_DIRTY_POLICY_STALE", str(ctx.exception))

    def test_execute_refuses_dirty_tracked_tree(self):
        target = ROOT / "docs" / "GOVERNANCE_NORMATIVE_SPEC.md"
        original = target.read_text(encoding="utf-8")
        try:
            target.write_text(original + "\n", encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--execute"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            combined = proc.stdout + proc.stderr
            self.assertNotEqual(proc.returncode, 0, combined)
            self.assertIn("BASELINE_REQUIRES_CLEAN_TREE", combined)
        finally:
            subprocess.run(["git", "checkout", "--", str(target.relative_to(ROOT))], cwd=ROOT, check=True)


if __name__ == "__main__":
    unittest.main()
