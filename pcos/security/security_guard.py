from __future__ import annotations

import re

PATTERNS = [
    re.compile(r"ignore previous instructions", re.IGNORECASE),
    re.compile(r"override constraints", re.IGNORECASE),
    re.compile(r"escalate role", re.IGNORECASE),
    re.compile(r"hidden prompt", re.IGNORECASE),
]


class SecurityGuard:
    def scan(self, prompt_text: str) -> dict[str, object]:
        findings = []
        for p in PATTERNS:
            if p.search(prompt_text):
                findings.append({"code": "SECURITY_FLAG", "pattern": p.pattern, "severity": "HIGH"})
        return {
            "status": "BLOCK" if findings else "ALLOW",
            "findings": findings,
        }
