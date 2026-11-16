"""Run 10 real (uncached) agent runs and report the average cost."""
import os
os.environ["AI201_CACHE"] = "0"   # must be set before config is imported

import json
import time

from agent import run_agent
from runlog import LOG_PATH
from utils.data_loader import get_example_wardrobe

QUERIES = [
    "vintage graphic tee under $30",
    "90s track jacket in size M",
    "silk slip dress in midi length under $40",
    "platform sneakers size 8",
    "denim jacket under $50",
] * 2

for q in QUERIES:
    run_agent(q, get_example_wardrobe())
    time.sleep(9)   # stay under the 15 requests/minute limit

rows = [json.loads(l) for l in LOG_PATH.read_text(encoding="utf-8").splitlines()[-10:]]
n = len(rows)
print(f"\nruns: {n}, statuses: {sorted({r['status'] for r in rows})}")
print(f"avg ms:            {sum(r['ms'] for r in rows) / n:.0f}")
print(f"avg model calls:   {sum(r['model_calls'] for r in rows) / n:.1f}")
print(f"avg prompt tokens: {sum(r['prompt_tokens'] for r in rows) / n:.0f}")
print(f"avg output tokens: {sum(r['output_tokens'] for r in rows) / n:.0f}")