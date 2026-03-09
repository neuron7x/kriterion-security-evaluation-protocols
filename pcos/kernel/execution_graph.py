from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionNode:
    node_id: str
    node_type: str


@dataclass(frozen=True)
class ExecutionGraph:
    nodes: list[ExecutionNode]

    @classmethod
    def from_plan(cls, plan: dict[str, object]) -> "ExecutionGraph":
        nodes: list[ExecutionNode] = []
        ordered = plan.get("ordered_execution", [])
        if isinstance(ordered, list) and ordered:
            for entry in ordered:
                if not isinstance(entry, dict):
                    continue
                nodes.append(ExecutionNode(node_id=str(entry.get("node_id", "missing")), node_type=str(entry.get("node_type", "UNKNOWN"))))
            return cls(nodes=nodes)

        for nid in plan.get("execution_order", []):
            nodes.append(ExecutionNode(node_id=str(nid), node_type="STEP"))
        for nid in plan.get("verification_points", []):
            nodes.append(ExecutionNode(node_id=str(nid), node_type="VERIFY"))
        nodes.append(ExecutionNode(node_id=str(plan.get("closure_node", "closure_missing")), node_type="CLOSE"))
        return cls(nodes=nodes)
