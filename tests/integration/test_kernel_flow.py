import unittest

from pcos.compiler.ir_builder import build_prompt_ir
from pcos.compiler.parser import parse_prompt_text
from pcos.kernel.execution_kernel import ExecutionKernel


class KernelFlowTests(unittest.TestCase):
    def test_kernel_end_to_end_flow(self):
        p = parse_prompt_text("OBJECTIVE: x\nSTEP: a\nVERIFY: v\nCLOSE: c")
        ir = build_prompt_ir(p)
        manifest = ExecutionKernel().run(ir)
        self.assertEqual(manifest["status"], "PASS")
        self.assertIs(manifest["verifier_result"]["verified"], True)
        self.assertTrue(manifest["trace"]["events"])


if __name__ == "__main__":
    unittest.main()
