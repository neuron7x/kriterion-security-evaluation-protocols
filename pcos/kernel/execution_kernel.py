from __future__ import annotations

import hashlib
import json
from pathlib import Path

from pcos.artifacts.trace import TraceEvent
from pcos.kernel.execution_graph import ExecutionGraph
from pcos.runtime.trace_graph import TraceGraph


class ExecutionKernel:
    def run(self, prompt_ir: dict[str, object], *, out_manifest: str | Path | None = None) -> dict[str, object]:
        plan = prompt_ir["execution_plan"]
        graph = ExecutionGraph.from_plan(plan)
        trace = TraceGraph()
        ir_hash = hashlib.sha256(json.dumps(prompt_ir, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

        verified = False
        for idx, node in enumerate(graph.nodes):
            status = "PASS"
            if node.node_type == "VERIFY":
                verified = True
            if node.node_type == "CLOSE" and not verified:
                status = "FAIL"
            trace.add(
                TraceEvent(
                    state=f"state_{idx}",
                    timestamp="deterministic-v1",
                    node_id=node.node_id,
                    input_hash=ir_hash,
                    candidate_id=f"cand_{idx}",
                    actions=[node.node_type],
                    status=status,
                )
            )
            if status == "FAIL":
                raise SystemExit("PCOS_KERNEL_FAIL_CLOSED: closure before verification")

        manifest = {
            "status": "PASS",
            "prompt_ir_hash": ir_hash,
            "execution_graph": [{"node_id": n.node_id, "node_type": n.node_type} for n in graph.nodes],
            "trace": trace.to_dict(),
            "verifier_result": {"status": "PASS", "verified": verified},
        }
        if out_manifest:
            Path(out_manifest).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return manifest
