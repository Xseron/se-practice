# The three exchanges for SIS 01 — raw evidence

Claude Code v2.1.296 (the binary bundled with the VS Code extension; the `claude` on PATH, v2.1.221,
refused the model with "API Error 400 … version 2.1.280 or newer is required", so that first attempt
produced no response). Every prompt ran as a fresh headless session:

```
claude -p --model claude-opus-5-5 --safe-mode --tools "" --no-session-persistence \
  --system-prompt "You are a helpful assistant." --output-format json < turn_X.txt > resp_X.json
```

`turn_X.txt` is exactly what was sent; `resp_X.json` is the raw JSON reply; `resp_X.md` is its
`result` field, saved by a script before anything was read or edited. All three ran on 2026-10-11.

- `turn_A` / `resp_A` — Prompt A, report.md §8 B1
- `turn_B` / `resp_B` — Prompt B, §8 B2 (the full Prompt A response pasted in)
- `turn_C` / `resp_C` — Prompt C, §8 B3 (`c_decisions.txt` and `c_evidence.txt` are the two fields
  pasted into it, kept separately for readability)

The prompts, the decisions and the evidence notes were written by the agentic Claude Code session
described in `../AI_USAGE.md`, not by David.
