import unittest

from pcos.compiler.parser import parse_prompt_text


class PromptAstTests(unittest.TestCase):
    def test_prompt_to_ast_preserves_symbols_and_order(self):
        prompt = parse_prompt_text(
            """
OBJECTIVE: test objective
SECTION: one
CONSTRAINT: deterministic
STEP: do x
VERIFY: check x
CLOSE: done
"""
        )
        self.assertEqual(prompt.objective, "test objective")
        self.assertEqual(prompt.sections[0].symbol, "section_1")
        self.assertEqual(prompt.constraints[0].symbol, "constraint_1")
        self.assertEqual(prompt.steps[0].symbol, "step_1")
        self.assertEqual(prompt.verifications[0].symbol, "verify_1")
        self.assertTrue(prompt.closure and prompt.closure.symbol == "closure_1")
        self.assertEqual([n.node_type for n in prompt.ordered_nodes], ["CONSTRAINT", "STEP", "VERIFY", "CLOSE"])


if __name__ == "__main__":
    unittest.main()
