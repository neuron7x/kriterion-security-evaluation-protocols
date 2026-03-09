from __future__ import annotations

from pathlib import Path

from pcos.compiler.ast import (
    ClosureNode,
    ConstraintNode,
    OrderedNode,
    PromptNode,
    SectionNode,
    StepNode,
    VerificationNode,
)


PREFIX_MAP = {
    "OBJECTIVE:": "objective",
    "SECTION:": "section",
    "CONSTRAINT:": "constraint",
    "STEP:": "step",
    "VERIFY:": "verify",
    "CLOSE:": "close",
}


def parse_prompt_text(text: str) -> PromptNode:
    objective = ""
    sections: list[SectionNode] = []
    constraints: list[ConstraintNode] = []
    steps: list[StepNode] = []
    verifications: list[VerificationNode] = []
    ordered_nodes: list[OrderedNode] = []
    closure: ClosureNode | None = None

    counters = {"section": 0, "constraint": 0, "step": 0, "verify": 0}

    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        matched = False
        for prefix, kind in PREFIX_MAP.items():
            if line.startswith(prefix):
                body = line[len(prefix) :].strip()
                matched = True
                if kind == "objective":
                    objective = body
                elif kind == "section":
                    counters["section"] += 1
                    node = SectionNode(symbol=f"section_{counters['section']}", text=body)
                    sections.append(node)
                elif kind == "constraint":
                    counters["constraint"] += 1
                    node = ConstraintNode(symbol=f"constraint_{counters['constraint']}", text=body)
                    constraints.append(node)
                    ordered_nodes.append(OrderedNode(symbol=node.symbol, node_type="CONSTRAINT", text=node.text))
                elif kind == "step":
                    counters["step"] += 1
                    node = StepNode(symbol=f"step_{counters['step']}", text=body)
                    steps.append(node)
                    ordered_nodes.append(OrderedNode(symbol=node.symbol, node_type="STEP", text=node.text))
                elif kind == "verify":
                    counters["verify"] += 1
                    node = VerificationNode(symbol=f"verify_{counters['verify']}", text=body)
                    verifications.append(node)
                    ordered_nodes.append(OrderedNode(symbol=node.symbol, node_type="VERIFY", text=node.text))
                elif kind == "close":
                    closure = ClosureNode(symbol="closure_1", text=body)
                    ordered_nodes.append(OrderedNode(symbol=closure.symbol, node_type="CLOSE", text=closure.text))
                break
        if not matched:
            counters["section"] += 1
            sections.append(SectionNode(symbol=f"section_{counters['section']}", text=line))

    return PromptNode(
        objective=objective,
        sections=tuple(sections),
        constraints=tuple(constraints),
        steps=tuple(steps),
        verifications=tuple(verifications),
        closure=closure,
        ordered_nodes=tuple(ordered_nodes),
    )


def parse_prompt_file(path: str | Path) -> PromptNode:
    p = Path(path)
    return parse_prompt_text(p.read_text(encoding="utf-8"))
