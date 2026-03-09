#!/usr/bin/env python3
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))

from validate_governance import severity_for_code  # noqa: E402


class GovernanceSeverityTests(unittest.TestCase):
    def test_critical_codes_are_errors(self):
        for code in ("PR_TEMPLATE", "BENCHMARK_HONESTY", "GOVERNANCE_STATUS_ARTIFACT", "ORDERING"):
            with self.subTest(code=code):
                self.assertEqual(severity_for_code(code), "error")


if __name__ == '__main__':
    unittest.main()
