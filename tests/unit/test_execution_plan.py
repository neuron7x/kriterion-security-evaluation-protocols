import unittest

from pcos.compiler.ir_builder import build_prompt_ir
from pcos.compiler.parser import parse_prompt_text


class ExecutionPlanTests(unittest.TestCase):
    def test_execution_plan_has_closure_after_verification(self):
        p = parse_prompt_text("OBJECTIVE: x\nSTEP: do\nVERIFY: check\nCLOSE: close")
        ir = build_prompt_ir(p)
        plan = ir["execution_plan"]
        self.assertEqual(plan["closure_node"], "closure_1")
        self.assertEqual(plan["verification_points"], ["verify_1"])
        self.assertEqual(
            plan["ordered_execution"],
            [
                {"node_id": "step_1", "node_type": "STEP"},
                {"node_id": "verify_1", "node_type": "VERIFY"},
                {"node_id": "closure_1", "node_type": "CLOSE"},
            ],
        )

    def test_close_before_verify_fails_closed(self):
        p = parse_prompt_text("OBJECTIVE: x\nCLOSE: close\nVERIFY: check")
        with self.assertRaises(SystemExit):
            build_prompt_ir(p)


if __name__ == "__main__":
    unittest.main()
