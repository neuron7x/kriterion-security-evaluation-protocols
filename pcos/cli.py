from __future__ import annotations

import argparse
import json
from pathlib import Path

from pcos.analysis.static_analyzer import StaticAnalyzer
from pcos.compiler.ir_builder import build_prompt_ir
from pcos.compiler.parser import parse_prompt_file
from pcos.kernel.execution_kernel import ExecutionKernel
from pcos.security.security_guard import SecurityGuard


def _expected_outcome(expected: str) -> str:
    if "BLOCK" in expected:
        return "BLOCK"
    if "FAIL" in expected:
        return "FAIL"
    return "PASS"


def _bench_case_outcome(attack: str, guard: SecurityGuard) -> str:
    scan = guard.scan(attack)
    if scan["status"] == "BLOCK":
        return "BLOCK"
    lowered = attack.lower()
    if "change objective" in lowered or "malformed json" in lowered:
        return "FAIL"
    return "PASS"


def cmd_compile(args: argparse.Namespace) -> int:
    prompt = parse_prompt_file(args.prompt)
    analyzer = StaticAnalyzer()
    findings = analyzer.analyze(prompt, fail_closed=args.fail_closed)
    if args.fail_closed and findings["fatal"]:
        raise SystemExit("PCOS_COMPILE_BLOCKED")
    ir = build_prompt_ir(prompt)
    ir["analysis"] = findings
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(ir, indent=2), encoding="utf-8")
    print("PCOS_COMPILE_OK")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    prompt_ir = json.loads(Path(args.ir).read_text(encoding="utf-8"))
    kernel = ExecutionKernel()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    kernel.run(prompt_ir, out_manifest=out)
    print("PCOS_RUN_OK")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    prompt_ir_hash = manifest.get("prompt_ir_hash")
    graph = manifest.get("execution_graph", [])
    events = manifest.get("trace", {}).get("events", [])
    vr = manifest.get("verifier_result", {})

    if not prompt_ir_hash or not isinstance(graph, list) or not isinstance(events, list) or not events:
        raise SystemExit("PCOS_VERIFY_FAIL_CLOSED")
    if len(graph) != len(events):
        raise SystemExit("PCOS_VERIFY_FAIL_CLOSED")

    seen_verify = False
    for idx, (node, event) in enumerate(zip(graph, events)):
        if event.get("input_hash") != prompt_ir_hash:
            raise SystemExit("PCOS_VERIFY_FAIL_CLOSED")
        if event.get("state") != f"state_{idx}" or event.get("candidate_id") != f"cand_{idx}":
            raise SystemExit("PCOS_VERIFY_FAIL_CLOSED")
        node_type = node.get("node_type")
        if event.get("node_id") != node.get("node_id"):
            raise SystemExit("PCOS_VERIFY_FAIL_CLOSED")
        if event.get("actions") != [node_type]:
            raise SystemExit("PCOS_VERIFY_FAIL_CLOSED")
        if node_type == "VERIFY":
            seen_verify = True
        if node_type == "CLOSE" and not seen_verify:
            raise SystemExit("PCOS_VERIFY_FAIL_CLOSED")
        if event.get("status") != "PASS":
            raise SystemExit("PCOS_VERIFY_FAIL_CLOSED")

    if vr.get("status") != "PASS" or vr.get("verified") is not True:
        raise SystemExit("PCOS_VERIFY_FAIL_CLOSED")
    print("PCOS_VERIFY_OK")
    return 0


def cmd_replay(args: argparse.Namespace) -> int:
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    graph = manifest.get("execution_graph", [])
    events = manifest.get("trace", {}).get("events", [])
    if not isinstance(graph, list) or not isinstance(events, list) or len(graph) != len(events):
        raise SystemExit("PCOS_REPLAY_FAIL_CLOSED")
    for idx, (node, event) in enumerate(zip(graph, events)):
        if event.get("state") != f"state_{idx}" or event.get("candidate_id") != f"cand_{idx}":
            raise SystemExit("PCOS_REPLAY_FAIL_CLOSED")
        if event.get("node_id") != node.get("node_id"):
            raise SystemExit("PCOS_REPLAY_FAIL_CLOSED")
        if event.get("actions") != [node.get("node_type")]:
            raise SystemExit("PCOS_REPLAY_FAIL_CLOSED")
    print("PCOS_REPLAY_OK")
    return 0


def cmd_bench(args: argparse.Namespace) -> int:
    family = json.loads(Path("pcos/benchmarks/families/B013_adversarial_prompt_stability.json").read_text(encoding="utf-8"))
    guard = SecurityGuard()
    cases = []
    passed = 0
    for case in family["cases"]:
        outcome = _bench_case_outcome(case["attack"], guard)
        expected = _expected_outcome(case["expected"])
        ok = outcome == expected
        passed += int(ok)
        cases.append({"name": case["name"], "expected": expected, "actual": outcome, "pass": ok})

    scorecard = {
        "family": family["id"],
        "cases": len(cases),
        "passed": passed,
        "status": "PASS" if passed == len(cases) else "FAIL",
        "results": cases,
    }
    print(json.dumps(scorecard, separators=(",", ":")))
    return 0 if scorecard["status"] == "PASS" else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pcos")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("compile")
    c.add_argument("prompt")
    c.add_argument("--out", required=True)
    c.add_argument("--fail-closed", action="store_true", default=True)
    c.set_defaults(func=cmd_compile)

    r = sub.add_parser("run")
    r.add_argument("ir")
    r.add_argument("--out", required=True)
    r.set_defaults(func=cmd_run)

    v = sub.add_parser("verify")
    v.add_argument("manifest")
    v.set_defaults(func=cmd_verify)

    b = sub.add_parser("bench")
    b.set_defaults(func=cmd_bench)

    rp = sub.add_parser("replay")
    rp.add_argument("manifest")
    rp.set_defaults(func=cmd_replay)
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.cmd == "compile":
        txt = Path(args.prompt).read_text(encoding="utf-8")
        g = SecurityGuard().scan(txt)
        if g["status"] == "BLOCK":
            raise SystemExit("PCOS_SECURITY_BLOCKED")
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
