import json
import subprocess
import unittest
from pathlib import Path


class SourceOrderFailClosedTests(unittest.TestCase):
    def test_compile_fails_when_close_precedes_verify(self):
        prompt = Path('/tmp/pcos-invalid-order.prompt')
        prompt.write_text('OBJECTIVE: x\nCLOSE: close\nVERIFY: verify', encoding='utf-8')
        ir = Path('/tmp/pcos-invalid-order.ir.json')
        proc = subprocess.run(
            ['python', '-m', 'pcos.cli', 'compile', str(prompt), '--out', str(ir)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('PCOS_IR_INVALID', proc.stdout + proc.stderr)

    def test_verify_and_replay_fail_on_trace_tamper(self):
        tmp = Path('/tmp/pcos-tamper-tests')
        tmp.mkdir(parents=True, exist_ok=True)
        prompt = Path('examples/pure_symbolic.prompt')
        ir = tmp / 'out.ir.json'
        manifest = tmp / 'manifest.json'
        subprocess.run(['python', '-m', 'pcos.cli', 'compile', str(prompt), '--out', str(ir)], check=True)
        subprocess.run(['python', '-m', 'pcos.cli', 'run', str(ir), '--out', str(manifest)], check=True)

        payload = json.loads(manifest.read_text(encoding='utf-8'))
        payload['trace']['events'][0]['node_id'] = 'tampered-node'
        bad_manifest = tmp / 'manifest.tampered.json'
        bad_manifest.write_text(json.dumps(payload), encoding='utf-8')

        verify = subprocess.run(['python', '-m', 'pcos.cli', 'verify', str(bad_manifest)], check=False)
        replay = subprocess.run(['python', '-m', 'pcos.cli', 'replay', str(bad_manifest)], check=False)
        self.assertNotEqual(verify.returncode, 0)
        self.assertNotEqual(replay.returncode, 0)


if __name__ == '__main__':
    unittest.main()
