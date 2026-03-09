import unittest

from pcos.analysis.static_analyzer import StaticAnalyzer
from pcos.compiler.parser import parse_prompt_text


class StaticAnalyzerTests(unittest.TestCase):
    def test_static_analyzer_machine_readable_findings(self):
        p = parse_prompt_text("OBJECTIVE: a or b\nSTEP: loop forever")
        findings = StaticAnalyzer().analyze(p)
        self.assertIsInstance(findings["findings"], list)
        self.assertEqual(findings["status"], "FAILED")

    def test_static_analyzer_fail_closed_blocks(self):
        p = parse_prompt_text("OBJECTIVE: a or b\nSTEP: loop forever")
        with self.assertRaises(SystemExit):
            StaticAnalyzer().analyze(p, fail_closed=True)


if __name__ == "__main__":
    unittest.main()
