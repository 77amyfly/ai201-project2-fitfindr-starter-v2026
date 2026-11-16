# Running FitFinder

**Python:** 3.13.15 (tested). 3.11 and 3.12 should also work. Do not use 3.14:
some pinned packages don't support it yet, and `python3` on a recent Mac may
point to it. Check with `python3.13 --version` before you start.

**Environment:** macOS. Dependencies are pinned in `requirements.txt`. There
are no local model files. The model is called through the Gemini API, so you
need internet access and your own `GEMINI_API_KEY`.

## From a clean checkout

```bash
git clone clone https://github.com/77amyfly/ai201-project2-fitfindr-starter-v2026 fitfinder-test
cd fitfinder-test
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env             # then paste your GEMINI_API_KEY into .env
python test.py                   # should pass before you go on
python app.py ask 'vintage graphic tee under $30'
```

If `python3.13` is not found, install it with `brew install python@3.13`.

Use single quotes around the query. The search tool (an MCP server) starts
automatically on every run, so there is nothing else to launch.

## What a run records

Every run appends one JSON line to `runs.jsonl`: timestamp, input, output,
status (`ok`, `no_results` or `error`), item id, wardrobe size, model calls,
prompt and output tokens, and milliseconds. Failed runs are recorded too.

The original starter instructions are kept in `STARTER_GUIDE.md`.