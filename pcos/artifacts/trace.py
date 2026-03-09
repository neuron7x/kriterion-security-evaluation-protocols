from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TraceEvent:
    state: str
    timestamp: str
    node_id: str
    input_hash: str
    candidate_id: str
    actions: list[str]
    status: str

    def to_dict(self) -> dict[str, object]:
        return {
            "state": self.state,
            "timestamp": self.timestamp,
            "node_id": self.node_id,
            "input_hash": self.input_hash,
            "candidate_id": self.candidate_id,
            "actions": self.actions,
            "status": self.status,
        }
