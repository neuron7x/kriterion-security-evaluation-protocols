from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionPlan:
    objective_node: str
    execution_order: list[str]
    verification_points: list[str]
    repair_nodes: list[str]
    closure_node: str
    ordered_execution: list[dict[str, str]]

    def to_dict(self) -> dict[str, object]:
        return {
            "objective_node": self.objective_node,
            "execution_order": self.execution_order,
            "verification_points": self.verification_points,
            "repair_nodes": self.repair_nodes,
            "closure_node": self.closure_node,
            "ordered_execution": self.ordered_execution,
        }
