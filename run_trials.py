"""Capstone trials for criteria 3 and 5: 3 trials x 10 runs, cache off, 9s apart."""
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

os.makedirs("results", exist_ok=True)

for trial in (1, 2, 3):
    for q in QUERIES:
        run_agent(q, get_example_wardrobe())
        time.sleep(9)

    rows = [json.loads(l) for l in LOG_PATH.read_text(encoding="utf-8").splitlines()[-10:]]
    with open(f"results/capstone_trial{trial}.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    fast = sum(r["ms"] <= 4000 for r in rows)
    ok5 = sum(r["model_calls"] == 2 and r["prompt_tokens"] + r["output_tokens"] <= 1000 for r in rows)
    print(f"\n=== TRIAL {trial} ===")
    print(f"criterion 3: {fast}/10 runs <= 4000 ms   (ms: {sorted(r['ms'] for r in rows)})")
    print(f"criterion 5: {ok5}/10 runs pass          (tokens: {[r['prompt_tokens'] + r['output_tokens'] for r in rows]}, calls: {[r['model_calls'] for r in rows]})")
    