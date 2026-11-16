"""Trials for criteria 2 and 4. Runs the real CLI in subprocesses."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

LOG = Path("runs.jsonl")
NEED = {"ts", "input", "output", "status", "item_id", "wardrobe_items",
        "model_calls", "prompt_tokens", "output_tokens", "ms"}

MIX = [  # criterion 2: 10 runs with mixed outcomes
    ("vintage graphic tee under $30", None),
    ("90s track jacket in size M", None),
    ("designer ballgown size XXS under $5", None),
    ("denim jacket under $50", "wrong_key"),
    ("platform sneakers size 8", None),
    ("flying saucer costume", None),
    ("silk slip dress in midi length under $40", None),
    ("denim jacket under $50", "wrong_key"),
    ("leather bomber", None),
    ("zzzz qqqq", None),
]
BLANK = [" ", "   ", "under $30", "under $50", "size M"]  # criterion 4


def log_lines():
    return LOG.read_text(encoding="utf-8").splitlines() if LOG.exists() else []


def ask(query, key=None):
    env = dict(os.environ, AI201_CACHE="0")
    if key:
        env["GEMINI_API_KEY"] = key
    p = subprocess.run([sys.executable, "app.py", "ask", query],
                       capture_output=True, text=True, env=env)
    return p.stdout + p.stderr


os.makedirs("results", exist_ok=True)

for trial in (1, 2, 3):
    print(f"\n=== TRIAL {trial} ===")

    # criterion 2
    before = len(log_lines())
    for q, key in MIX:
        ask(q, key)
        time.sleep(5)
    new = log_lines()[before:]
    rows = [json.loads(l) for l in new]
    ok2 = len(new) == 10 and all(NEED <= set(r) for r in rows)
    Path(f"results/capstone_c2_trial{trial}.jsonl").write_text("\n".join(new) + "\n", encoding="utf-8")
    print(f"criterion 2: {len(new)} new lines, all 10 keys in every line: {ok2}")
    print(f"             statuses: {[r['status'] for r in rows]}")

    # criterion 4
    before = len(log_lines())
    outs = [ask(q) for q in BLANK]
    rows = [json.loads(l) for l in log_lines()[before:]]
    passed = 0
    for q, out, r in zip(BLANK, outs, rows):
        good = r["model_calls"] == 0 and "matched ''" not in out and "describe" in out.lower()
        passed += good
        msg = next((l.strip() for l in out.splitlines()
                    if "matched" in l or "describe" in l.lower()), out.strip()[-120:])
        print(f"  {q!r:14} pass={good}  message: {msg}")
    print(f"criterion 4: {passed}/5 pass")
    Path(f"results/capstone_c4_trial{trial}.txt").write_text(
        "\n\n----\n\n".join(f"QUERY {q!r}\n{o}" for q, o in zip(BLANK, outs)), encoding="utf-8")