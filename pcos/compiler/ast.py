from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SectionNode:
    symbol: str
    text: str


@dataclass(frozen=True)
class ConstraintNode:
    symbol: str
    text: str


@dataclass(frozen=True)
class StepNode:
    symbol: str
    text: str


@dataclass(frozen=True)
class VerificationNode:
    symbol: str
    text: str


@dataclass(frozen=True)
class ClosureNode:
    symbol: str
    text: str


@dataclass(frozen=True)
class OrderedNode:
    symbol: str
    node_type: str
    text: str


@dataclass(frozen=True)
class PromptNode:
    objective: str
    sections: tuple[SectionNode, ...] = field(default_factory=tuple)
    constraints: tuple[ConstraintNode, ...] = field(default_factory=tuple)
    steps: tuple[StepNode, ...] = field(default_factory=tuple)
    verifications: tuple[VerificationNode, ...] = field(default_factory=tuple)
    closure: ClosureNode | None = None
    ordered_nodes: tuple[OrderedNode, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "objective": self.objective,
            "sections": [s.__dict__ for s in self.sections],
            "constraints": [c.__dict__ for c in self.constraints],
            "steps": [s.__dict__ for s in self.steps],
            "verifications": [v.__dict__ for v in self.verifications],
            "closure": None if self.closure is None else self.closure.__dict__,
            "ordered_nodes": [n.__dict__ for n in self.ordered_nodes],
        }
