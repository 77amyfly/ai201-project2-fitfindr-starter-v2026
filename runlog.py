"""Structured run log: one JSON object per line in runs.jsonl."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path(__file__).parent / "runs.jsonl"


def log_run(record: dict) -> None:
    record = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), **record}
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as exc:  # a logging problem must not crash a run, but must be seen
        print(f"[runlog] could not write log: {exc}", file=sys.stderr)