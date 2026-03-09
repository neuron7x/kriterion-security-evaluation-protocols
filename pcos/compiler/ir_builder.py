from __future__ import annotations

from pcos.compiler.ast import PromptNode
from pcos.runtime.execution_plan import ExecutionPlan


def build_prompt_ir(prompt: PromptNode) -> dict[str, object]:
    execution_order = [s.symbol for s in prompt.steps]
    verification_points = [v.symbol for v in prompt.verifications]
    repair_nodes = [s.symbol for s in prompt.steps if "repair" in s.text.lower()]
    closure_node = prompt.closure.symbol if prompt.closure else "closure_missing"
    ordered_execution = [
        {"node_id": node.symbol, "node_type": node.node_type}
        for node in prompt.ordered_nodes
        if node.node_type in {"STEP", "VERIFY", "CLOSE"}
    ]

    seen_verify = False
    for node in ordered_execution:
        if node["node_type"] == "VERIFY":
            seen_verify = True
        if node["node_type"] == "CLOSE" and not seen_verify:
            raise SystemExit("PCOS_IR_INVALID: closure must come after verification")

    plan = ExecutionPlan(
        objective_node="objective",
        execution_order=execution_order,
        verification_points=verification_points,
        repair_nodes=repair_nodes,
        closure_node=closure_node,
        ordered_execution=ordered_execution,
    )

    return {
        "ast": prompt.to_dict(),
        "execution_plan": plan.to_dict(),
    }
