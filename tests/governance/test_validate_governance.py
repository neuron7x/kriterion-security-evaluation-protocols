#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys
import tempfile

import yaml
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / 'tools' / 'validate_governance.py'
FIXTURES = ROOT / 'tests' / 'governance' / 'fixtures' / 'mutations.json'

REQUIRED_FILES = [
    '.gitignore',
    '.github/workflows/quality-gates.yml',
    '.github/workflows/pages.yml',
    '.github/CODEOWNERS',
    '.github/pull_request_template.md',
    '.pre-commit-config.yaml',
    'docs/PR_PREMERGE_ENGINEERING_CHECKLIST.md',
    'docs/GOVERNANCE_CONTRACT_CHANGELOG.md',
    'CONTRIBUTING.md',
    'repo-map.json',
    'MANIFEST.json',
    'governance/invariant-registry.json',
    'governance/ci-required-checks.json',
    'governance/github-settings-baseline.json',
    'docs/GOVERNANCE_POLICY_DRIFT_RUNBOOK.md',
    'tools/check_cli_contracts.py',
    'tools/check_dependency_hermeticity.py',
    'tools/check_governance_nondeterminism.py',
    'tools/run_local_governance_baseline.py',
    'tools/validate_pr_intake.py',
    'governance/requirements-governance.lock.json',
    'governance/ci-required-checks.json',
    'governance/github-settings-baseline.json',
    'docs/GOVERNANCE_POLICY_DRIFT_RUNBOOK.md',
    'docs/GOVERNANCE_NORMATIVE_SPEC.md',
    'requirements.txt',
    'schemas/governance-invariant-registry.schema.json',
    'tools/governance_contract.py',
    'tools/render_governance_checklist.py',
    'tools/validate_governance.py',
    'tools/check_internal_links.py',
    'tools/check_external_links.py',
    'tools/validate_publication_surfaces.py',
    'tools/verify_ci_artifact_manifest.py',
    'tools/assert_fail_closed_semantics.py',
    'tools/assert_gate_benchmark_invariants.py',
    'tools/assert_worked_example_semantics.py',
    'tools/check_canonical_hash_stability.py',
    'tools/check_canonicalization_negative_cases.py',
    'tools/reference_runner.py',
    'tools/verify_execution_chain.py',
    'tests/fixtures/evaluation-result.invalid.missing-execution-state-chain.json',
    'tests/fixtures/evaluation-result.invalid.execution-chain-invalid-step-hash-format.json',
    'tests/semantic/test_verify_execution_chain.py',
    'schemas/evaluation-result.schema.json',
    'examples/worked-example/SE_WORKED_EXAMPLE_INPUT.json',
    'benchmark/benchmark_runner.py',
    'benchmark/metrics.json',
    'benchmark/results/case_level_results.csv',
    'index.html',
    'system-map.html',
    'protocol-explorer.html',
    'benchmark-dashboard.html',
    'doctrine.html',
    'execution-layer.html',
    '404.html',
]



def run_validator(root: Path, as_json: bool = False):
    env = os.environ.copy()
    env['GOVERNANCE_VALIDATOR_ROOT'] = str(root)
    cmd = [sys.executable, str(VALIDATOR)]
    if as_json:
        cmd.append('--json')
    return subprocess.run(cmd, capture_output=True, text=True, check=False, env=env)


def make_temp_root() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix='gov-validator-'))
    for rel in REQUIRED_FILES:
        src = ROOT / rel
        dst = tmp / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return tmp


class GovernanceValidatorTests(unittest.TestCase):
    def test_real_repo_passes(self):
        proc = run_validator(ROOT)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn('GOVERNANCE_OK', proc.stdout)

    def test_json_output_has_severity(self):
        proc = run_validator(ROOT, as_json=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        start = proc.stdout.find('{')
        end = proc.stdout.rfind('}')
        self.assertNotEqual(start, -1, proc.stdout)
        self.assertGreater(end, start, proc.stdout)
        payload = json.loads(proc.stdout[start:end+1])
        self.assertEqual(payload['policy_version'], '2026.24.0')
        self.assertIn(payload['status'], {'OK', 'FAILED'})
        self.assertIn('violations', payload)

    def test_missing_file_failure_mode(self):
        tmp = make_temp_root()
        try:
            (tmp / 'CONTRIBUTING.md').unlink()
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('FILE_MISSING', proc.stdout)
            self.assertIn('GOVERNANCE_CHECK_FAILED', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_golden_mutation_regressions_fail_closed(self):
        mutations = json.loads(FIXTURES.read_text(encoding='utf-8'))
        for name, mutation in mutations.items():
            with self.subTest(name=name):
                tmp = make_temp_root()
                try:
                    target = tmp / mutation['target']
                    text = target.read_text(encoding='utf-8')
                    self.assertIn(mutation['replace'], text)
                    text = text.replace(mutation['replace'], mutation['with'])
                    target.write_text(text, encoding='utf-8')

                    proc = run_validator(tmp)
                    self.assertNotEqual(proc.returncode, 0)
                    self.assertIn(mutation['expected_violation_substring'], proc.stdout)
                    self.assertIn('GOVERNANCE_CHECK_FAILED', proc.stdout)
                finally:
                    shutil.rmtree(tmp)

    def test_required_check_mapping_drift_is_rejected(self):
        tmp = make_temp_root()
        try:
            mapping = tmp / 'governance/ci-required-checks.json'
            payload = json.loads(mapping.read_text(encoding='utf-8'))
            payload['required_checks'][0]['check_name'] = 'mutable-check-name'
            mapping.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('GITHUB_REQUIRED_CHECKS', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_corrupted_registry_json_fails_with_parse_signal(self):
        tmp = make_temp_root()
        try:
            (tmp / 'governance/invariant-registry.json').write_text('{', encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('JSON_PARSE_ERROR', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_corrupted_workflow_yaml_fails_with_parse_signal(self):
        tmp = make_temp_root()
        try:
            (tmp / '.github/workflows/quality-gates.yml').write_text(':\n  - bad', encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('YAML_PARSE_ERROR', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_workflow_defaults_shell_drift_is_rejected(self):
        tmp = make_temp_root()
        try:
            wf = tmp / '.github/workflows/quality-gates.yml'
            text = wf.read_text(encoding='utf-8')
            self.assertIn('shell: bash --noprofile --norc -euo pipefail {0}', text)
            wf.write_text(text.replace('shell: bash --noprofile --norc -euo pipefail {0}', 'shell: bash'), encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('WORKFLOW_DISCIPLINE', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_quality_workflow_workflow_dispatch_is_rejected_when_on_is_unquoted(self):
        tmp = make_temp_root()
        try:
            wf = tmp / '.github/workflows/quality-gates.yml'
            text = wf.read_text(encoding='utf-8')
            self.assertIn('  pull_request:', text)
            wf.write_text(text.replace('  pull_request:\n', '  pull_request:\n  workflow_dispatch:\n'), encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('WORKFLOW_TRIGGER', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_quality_workflow_pull_request_target_is_rejected(self):
        tmp = make_temp_root()
        try:
            wf = tmp / '.github/workflows/quality-gates.yml'
            text = wf.read_text(encoding='utf-8')
            self.assertIn('  pull_request:', text)
            wf.write_text(text.replace('  pull_request:\n', '  pull_request_target:\n  pull_request:\n'), encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('WORKFLOW_TRIGGER', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_pages_workflow_dispatch_allowance_still_passes(self):
        proc = run_validator(ROOT)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


    def test_quality_workflow_on_sequence_forbidden_trigger_is_rejected(self):
        tmp = make_temp_root()
        try:
            wf = tmp / '.github/workflows/quality-gates.yml'
            text = wf.read_text(encoding='utf-8')
            payload = yaml.safe_load(text)
            payload['on'] = ['pull_request', 'workflow_dispatch']
            wf.write_text(yaml.safe_dump(payload, sort_keys=False), encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('WORKFLOW_TRIGGER', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_quality_workflow_on_scalar_forbidden_trigger_is_rejected(self):
        tmp = make_temp_root()
        try:
            wf = tmp / '.github/workflows/quality-gates.yml'
            text = wf.read_text(encoding='utf-8')
            payload = yaml.safe_load(text)
            payload['on'] = 'pull_request_target'
            wf.write_text(yaml.safe_dump(payload, sort_keys=False), encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('WORKFLOW_TRIGGER', proc.stdout)
        finally:
            shutil.rmtree(tmp)


    def test_quality_workflow_true_key_fallback_is_rejected_forbidden_trigger(self):
        tmp = make_temp_root()
        try:
            wf = tmp / '.github/workflows/quality-gates.yml'
            text = wf.read_text(encoding='utf-8')
            payload = yaml.safe_load(text)
            payload[True] = {'pull_request': None, 'workflow_dispatch': None}
            if 'on' in payload:
                payload.pop('on')
            wf.write_text(yaml.safe_dump(payload, sort_keys=False), encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('WORKFLOW_TRIGGER', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_artifact_manifest_verify_contract_tokens_are_required(self):
        tmp = make_temp_root()
        try:
            wf = tmp / '.github/workflows/quality-gates.yml'
            text = wf.read_text(encoding='utf-8')
            self.assertIn('--strip-path-prefix .ci-artifacts/', text)
            wf.write_text(text.replace(' --strip-path-prefix .ci-artifacts/', ''), encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('ARTIFACT_SEMANTICS', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_benchmark_regenerated_output_parity_step_is_required(self):
        tmp = make_temp_root()
        try:
            wf = tmp / '.github/workflows/quality-gates.yml'
            text = wf.read_text(encoding='utf-8')
            cmd = '          git diff --exit-code -- benchmark/metrics.json benchmark/results/case_level_results.csv benchmark/results/case-*.evaluation.json\n'
            self.assertIn(cmd, text)
            wf.write_text(text.replace(cmd, ''), encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('BENCHMARK_HONESTY', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_reference_runner_injection_regression_test_is_required(self):
        tmp = make_temp_root()
        try:
            wf = tmp / '.github/workflows/quality-gates.yml'
            text = wf.read_text(encoding='utf-8')
            cmd = '      - run: python -m unittest tests/semantic/test_reference_runner_injection_detection.py\n'
            self.assertIn(cmd, text)
            wf.write_text(text.replace(cmd, ''), encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('WORKFLOW_STRICTNESS', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_verify_ci_artifact_manifest_regression_test_is_required(self):
        tmp = make_temp_root()
        try:
            wf = tmp / '.github/workflows/quality-gates.yml'
            text = wf.read_text(encoding='utf-8')
            cmd = '      - run: python -m unittest tests/semantic/test_verify_ci_artifact_manifest.py\n'
            self.assertIn(cmd, text)
            wf.write_text(text.replace(cmd, ''), encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('WORKFLOW_STRICTNESS', proc.stdout)
        finally:
            shutil.rmtree(tmp)


    def test_artifact_manifest_required_names_are_required(self):
        tmp = make_temp_root()
        try:
            wf = tmp / '.github/workflows/quality-gates.yml'
            text = wf.read_text(encoding='utf-8')
            self.assertIn('--require-name benchmark-status', text)
            wf.write_text(text.replace(' --require-name benchmark-status', ''), encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('ARTIFACT_SEMANTICS', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_worked_example_status_artifact_generation_is_required(self):
        tmp = make_temp_root()
        try:
            wf = tmp / '.github/workflows/quality-gates.yml'
            text = wf.read_text(encoding='utf-8')
            self.assertIn('worked-example.run.status.json', text)
            wf.write_text(text.replace('worked-example.run.status.json', 'worked-example.status.json'), encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('ARTIFACT_SEMANTICS', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_upload_artifact_retention_floor_is_required(self):
        tmp = make_temp_root()
        try:
            wf = tmp / '.github/workflows/quality-gates.yml'
            text = wf.read_text(encoding='utf-8')
            self.assertIn('retention-days: 14', text)
            wf.write_text(text.replace('retention-days: 14', 'retention-days: 7', 1), encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('ARTIFACT_SEMANTICS', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_pages_workflow_permissions_escalation_is_rejected(self):
        tmp = make_temp_root()
        try:
            wf = tmp / '.github/workflows/pages.yml'
            text = wf.read_text(encoding='utf-8')
            self.assertIn('contents: read', text)
            wf.write_text(text.replace('contents: read', 'contents: write'), encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('PERMISSIONS', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_unexpected_workflow_surface_is_rejected(self):
        tmp = make_temp_root()
        try:
            wf = tmp / '.github/workflows/extra.yml'
            wf.write_text('name: extra\non: [push]\npermissions:\n  contents: read\ndefaults:\n  run:\n    shell: bash --noprofile --norc -euo pipefail {0}\njobs:\n  noop:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo nope\n', encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('WORKFLOW_JOBS', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_pip_policy_drift_is_rejected(self):
        tmp = make_temp_root()
        try:
            wf = tmp / '.github/workflows/quality-gates.yml'
            text = wf.read_text(encoding='utf-8')
            self.assertIn('python -m pip --version', text)
            wf.write_text(text.replace('      - run: python -m pip --version\n', ''), encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('WORKFLOW_ORDERING', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_permissions_escalation_is_rejected(self):
        tmp = make_temp_root()
        try:
            wf = tmp / '.github/workflows/quality-gates.yml'
            text = wf.read_text(encoding='utf-8')
            self.assertIn('contents: read', text)
            wf.write_text(text.replace('contents: read', 'contents: write'), encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('PERMISSIONS', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_repo_map_violation_is_rejected(self):
        tmp = make_temp_root()
        try:
            repo_map = tmp / 'repo-map.json'
            payload = json.loads(repo_map.read_text(encoding='utf-8'))
            payload['tools'] = [x for x in payload['tools'] if x != 'validate_governance.py']
            repo_map.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('REPO_MAP', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_manifest_missing_gitignore_is_rejected(self):
        tmp = make_temp_root()
        try:
            manifest = tmp / 'MANIFEST.json'
            payload = json.loads(manifest.read_text(encoding='utf-8'))
            payload.pop('.gitignore', None)
            manifest.write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n', encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('MANIFEST_POLICY', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_repo_map_missing_pages_workflow_is_rejected(self):
        tmp = make_temp_root()
        try:
            repo_map = tmp / 'repo-map.json'
            payload = json.loads(repo_map.read_text(encoding='utf-8'))
            payload['github'] = [x for x in payload['github'] if x != '.github/workflows/pages.yml']
            repo_map.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('REPO_MAP', proc.stdout)
        finally:
            shutil.rmtree(tmp)


    def test_missing_execution_chain_invariant_is_rejected(self):
        tmp = make_temp_root()
        try:
            reg = tmp / 'governance/invariant-registry.json'
            payload = json.loads(reg.read_text(encoding='utf-8'))
            payload['invariants'] = [inv for inv in payload.get('invariants', []) if inv.get('invariant_id') != 'INV_EXECUTION_CHAIN_INDEPENDENTLY_RECOMPUTABLE']
            reg.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('REGISTRY_INVARIANTS', proc.stdout)
        finally:
            shutil.rmtree(tmp)

    def test_missing_worked_example_verifier_step_is_rejected(self):
        tmp = make_temp_root()
        try:
            wf = tmp / '.github/workflows/quality-gates.yml'
            text = wf.read_text(encoding='utf-8')
            self.assertIn('verify_execution_chain.py', text)
            wf.write_text(text.replace('      - run: python tools/verify_execution_chain.py --input examples/worked-example/SE_WORKED_EXAMPLE_INPUT.json --result /tmp/SE_WORKED_EXAMPLE_OUTPUT.check.json\n', ''), encoding='utf-8')
            proc = run_validator(tmp)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn('WORKFLOW_STRICTNESS', proc.stdout)
        finally:
            shutil.rmtree(tmp)

if __name__ == '__main__':
    unittest.main()
