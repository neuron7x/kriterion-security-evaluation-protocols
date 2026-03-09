from __future__ import annotations

from dataclasses import dataclass

from pcos.compiler.ast import PromptNode


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    message: str
    node: str

    def to_dict(self) -> dict[str, str]:
        return {"code": self.code, "severity": self.severity, "message": self.message, "node": self.node}


FATAL_CODES = {
    "CONTRADICTION",
    "AMBIGUOUS_OBJECTIVE",
    "UNBOUNDED_RECURSION",
    "SCOPE_LEAK",
    "MISSING_VERIFICATION_BEFORE_CLOSURE",
}


class StaticAnalyzer:
    def analyze(self, prompt: PromptNode, *, fail_closed: bool = False) -> dict[str, object]:
        findings: list[Finding] = []
        findings.extend(self.detect_contradictions(prompt))
        findings.extend(self.detect_ambiguous_objective(prompt))
        findings.extend(self.detect_unbounded_recursion(prompt))
        findings.extend(self.detect_scope_leak(prompt))
        findings.extend(self.detect_missing_verification_before_closure(prompt))
        payload = {
            "status": "FAILED" if any(f.code in FATAL_CODES for f in findings) else "OK",
            "fatal": [f.to_dict() for f in findings if f.code in FATAL_CODES],
            "findings": [f.to_dict() for f in findings],
        }
        if fail_closed and payload["fatal"]:
            raise SystemExit("PCOS_ANALYSIS_FATAL")
        return payload

    def detect_contradictions(self, prompt: PromptNode) -> list[Finding]:
        texts = [c.text.lower() for c in prompt.constraints]
        out: list[Finding] = []
        for t in texts:
            if t.startswith("not ") and t[4:] in texts:
                out.append(Finding("CONTRADICTION", "FATAL", f"Contradiction detected: {t}", "constraints"))
        return out

    def detect_ambiguous_objective(self, prompt: PromptNode) -> list[Finding]:
        o = prompt.objective.lower().strip()
        if not o or " or " in o:
            return [Finding("AMBIGUOUS_OBJECTIVE", "FATAL", "Objective is empty or ambiguous", "objective")]
        return []

    def detect_unbounded_recursion(self, prompt: PromptNode) -> list[Finding]:
        for step in prompt.steps:
            t = step.text.lower()
            if ("recurse" in t or "loop" in t) and "max" not in t and "until" not in t:
                return [Finding("UNBOUNDED_RECURSION", "FATAL", "Potential unbounded recursion", step.symbol)]
        return []

    def detect_scope_leak(self, prompt: PromptNode) -> list[Finding]:
        for node in [*prompt.constraints, *prompt.steps]:
            if "global" in node.text.lower() or "outside scope" in node.text.lower():
                return [Finding("SCOPE_LEAK", "FATAL", "Scope leak detected", node.symbol)]
        return []

    def detect_missing_verification_before_closure(self, prompt: PromptNode) -> list[Finding]:
        if prompt.closure and not prompt.verifications:
            return [
                Finding(
                    "MISSING_VERIFICATION_BEFORE_CLOSURE",
                    "FATAL",
                    "Closure declared without verification",
                    prompt.closure.symbol,
                )
            ]
        return []
