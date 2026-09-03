"""RedRabbit event construction and JSONL persistence for actual local scans."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def event(scan_id: str, event_type: str, actor: str, details: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "scan_id": scan_id,
        "event_type": event_type,
        "actor": actor,
        "details": details,
    }


def append_event(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")
