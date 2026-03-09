#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
SPEC = importlib.util.spec_from_file_location("compile_pr_intake", ROOT / "tools" / "compile_pr_intake.py")
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
sys.modules["compile_pr_intake"] = mod
SPEC.loader.exec_module(mod)


class CompilePRIntakeTests(unittest.TestCase):
    def default_policy(self):
        return mod.GovernanceCriticalPolicy(prefixes=("governance/",), exact_paths=frozenset({"CONTRIBUTING.md"}))

    def test_headings_order_exact(self):
        body = mod.compile_markdown(
            branch="work",
            base_branch="main",
            pr=mod.PRInfo(number=1, base_ref="main", head_ref="work", url="u"),
            merge_base="abc123",
            changed_files=["tools/compile_pr_intake.py"],
            commit_subjects=["Add compiler"],
            validators=[mod.ValidatorResult(command="python -V", exit_code=0, summary="Python 3")],
            governance_policy=self.default_policy(),
        )
        observed = [line.strip() for line in body.splitlines() if line.startswith("## ")]
        self.assertEqual(observed, mod.REQUIRED_HEADINGS)

    def test_fail_when_base_unresolved(self):
        with patch.object(mod, "_run") as run:
            run.return_value.returncode = 1
            run.return_value.stdout = ""
            with self.assertRaises(RuntimeError):
                mod.resolve_base_name(None, None)

    def test_fail_when_validator_fails(self):
        with patch.object(mod, "get_current_pr", return_value=mod.PRInfo(9, "main", "work", "url")), \
            patch.object(mod, "resolve_base_ref", return_value=mod.BaseRef(name="main", revspec="origin/main")), \
            patch.object(mod, "compute_merge_base", return_value="abc"), \
            patch.object(mod, "list_changed_files", return_value=["a.py"]), \
            patch.object(mod, "list_commit_subjects", return_value=["msg"]), \
            patch.object(mod, "run_validators", return_value=[mod.ValidatorResult("python bad.py", 1, "failed")]), \
            patch.object(mod, "current_branch", return_value="work"):
            with self.assertRaises(RuntimeError):
                mod.main(["--validate", "python bad.py", "--output", ".artifacts/test.md"])

    def test_compiled_output_contains_diff_commit_and_validator(self):
        body = mod.compile_markdown(
            branch="work",
            base_branch="main",
            pr=mod.PRInfo(number=1, base_ref="main", head_ref="work", url="u"),
            merge_base="basehash",
            changed_files=["tools/compile_pr_intake.py", "tests/governance/test_compile_pr_intake.py"],
            commit_subjects=["Implement compiler"],
            validators=[mod.ValidatorResult(command="python tools/validate_governance.py", exit_code=0, summary="GOVERNANCE_OK")],
            governance_policy=self.default_policy(),
        )
        self.assertIn("tools/compile_pr_intake.py", body)
        self.assertIn("Implement compiler", body)
        self.assertIn("python tools/validate_governance.py", body)


    def test_policy_loads_governance_paths_from_repo_map(self):
        import tempfile
        import json

        with tempfile.TemporaryDirectory(prefix="policy-") as td:
            repo_map = Path(td) / "repo-map.json"
            repo_map.write_text(json.dumps({"governance": ["governance/custom-policy.json"]}), encoding="utf-8")
            policy = mod.load_governance_critical_policy(repo_map)
            self.assertIn("governance/custom-policy.json", policy.exact_paths)

    def test_dry_run_does_not_apply(self):
        out = Path(".artifacts/dry-run-test.md")
        if out.exists():
            out.unlink()
        with patch.object(mod, "get_current_pr", return_value=mod.PRInfo(9, "main", "work", "url")), \
            patch.object(mod, "resolve_base_ref", return_value=mod.BaseRef(name="main", revspec="origin/main")), \
            patch.object(mod, "compute_merge_base", return_value="abc"), \
            patch.object(mod, "list_changed_files", return_value=["a.py"]), \
            patch.object(mod, "list_commit_subjects", return_value=["msg"]), \
            patch.object(mod, "run_validators", return_value=[mod.ValidatorResult("python ok.py", 0, "ok")]), \
            patch.object(mod, "current_branch", return_value="work"), \
            patch.object(mod, "apply_pr_body") as apply_body:
            rc = mod.main(["--validate", "python ok.py", "--dry-run", "--output", str(out)])
            self.assertEqual(rc, 0)
            apply_body.assert_not_called()
            self.assertTrue(out.exists())

    def test_dry_run_allows_missing_pr(self):
        out = Path(".artifacts/dry-run-no-pr.md")
        if out.exists():
            out.unlink()
        with patch.object(mod, "get_current_pr", return_value=None), \
            patch.object(mod, "resolve_base_ref", return_value=mod.BaseRef(name="main", revspec="origin/main")), \
            patch.object(mod, "compute_merge_base", return_value="abc"), \
            patch.object(mod, "list_changed_files", return_value=["a.py"]), \
            patch.object(mod, "list_commit_subjects", return_value=["msg"]), \
            patch.object(mod, "run_validators", return_value=[mod.ValidatorResult("python ok.py", 0, "ok")]), \
            patch.object(mod, "current_branch", return_value="work"), \
            patch.object(mod, "apply_pr_body") as apply_body:
            rc = mod.main(["--validate", "python ok.py", "--dry-run", "--output", str(out)])
            self.assertEqual(rc, 0)
            apply_body.assert_not_called()
            self.assertTrue(out.exists())

    def test_resolve_base_ref_prefers_origin_when_local_missing(self):
        with patch.object(mod, "resolve_base_name", return_value="main"), patch.object(mod, "_ref_exists", side_effect=[True, False, False]):
            self.assertEqual(mod.resolve_base_ref(None, None), mod.BaseRef(name="main", revspec="origin/main"))

    def test_policy_load_invalid_repo_map_fails_closed(self):
        import tempfile

        with tempfile.TemporaryDirectory(prefix="policy-invalid-") as td:
            repo_map = Path(td) / "repo-map.json"
            repo_map.write_text("{broken", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                mod.load_governance_critical_policy(repo_map)

    def test_policy_load_requires_governance_list(self):
        import tempfile
        import json

        with tempfile.TemporaryDirectory(prefix="policy-type-") as td:
            repo_map = Path(td) / "repo-map.json"
            repo_map.write_text(json.dumps({"governance": "bad"}), encoding="utf-8")
            with self.assertRaises(RuntimeError):
                mod.load_governance_critical_policy(repo_map)


if __name__ == "__main__":
    unittest.main()
