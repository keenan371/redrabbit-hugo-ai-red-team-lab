"""Local-only RedRabbit scan orchestrator. No network, shell, or external targets."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from hugo_integration.hugo_watchdog import HugoWatchdog
from redrabbit_agent.evaluator import evaluate
from redrabbit_agent.events import append_event, event

CATALOG_PATH = Path(__file__).with_name("test_catalog.json")


def load_catalog() -> list[dict]:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def run_safe_demo(mode: str, root: Path | str, test_id: str | None = None) -> dict:
    if mode not in {"baseline", "hardened"}:
        raise ValueError("mode must be baseline or hardened")
    root = Path(root)
    scan_id = f"scan-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}"
    event_path = root / "events" / f"{scan_id}.jsonl"
    hugo_log = root / "logs" / "hugo-decisions.jsonl"
    selected = [item for item in load_catalog() if test_id in {None, item["id"]}]
    if not selected:
        raise ValueError("unknown safe test id")

    append_event(event_path, event(scan_id, "scan_started", "system", {"mode": mode, "test_count": len(selected)}))
    hugo = HugoWatchdog(mode=mode, log_path=hugo_log)
    results = []
    for test in selected:
        append_event(event_path, event(scan_id, "redrabbit_test_sent", "redrabbit", {"test_id": test["id"], "category": test["category"]}))
        response = hugo.handle_message(test["prompt"])
        append_event(event_path, event(scan_id, "hugo_decision", "hugo", {"test_id": test["id"], "category": response["category"], "decision": response["decision"]}))
        finding = evaluate(test, response)
        results.append(finding)
        append_event(event_path, event(scan_id, "redrabbit_evaluation", "redrabbit", {"test_id": test["id"], "passed": finding["passed"], "actual_behavior": finding["actual_behavior"]}))

    summary = {"total": len(results), "passed": sum(item["passed"] for item in results), "failed": sum(not item["passed"] for item in results)}
    report = {"scan_id": scan_id, "mode": mode, "timestamp_utc": datetime.now(timezone.utc).isoformat(), "summary": summary, "results": results}
    append_event(event_path, event(scan_id, "scan_completed", "system", summary))
    result_path = root / "results" / f"{scan_id}.json"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(run_safe_demo("hardened", Path(__file__).parents[1]), indent=2))
