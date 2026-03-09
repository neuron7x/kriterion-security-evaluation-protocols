from __future__ import annotations

from dataclasses import dataclass, field

from pcos.artifacts.trace import TraceEvent


@dataclass
class TraceGraph:
    events: list[TraceEvent] = field(default_factory=list)

    def add(self, event: TraceEvent) -> None:
        self.events.append(event)

    def to_dict(self) -> dict[str, object]:
        return {"events": [e.to_dict() for e in self.events]}
