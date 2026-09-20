# AI Usage Disclosure — Week 02

Required by the course academic policy (Generative AI use level **D** — AI-integrated).
AI use is **the subject** of this lab, not a shortcut in it. You remain responsible for the
accuracy, testing and integrity of everything you submit, including everything an AI produced.

## 1. The tool under test

| | |
| --- | --- |
| Assistant | Claude Code (Anthropic) v2.1.278, headless `claude -p`, tools disabled, `--safe-mode`, neutral one-line system prompt — exact command in `lab-report.md` section 1 |
| Exact model name | Claude Fable 5.1 (`claude-fable-5-1`) |
| Plan (free / paid) | TODO — David: fill in |
| Dates of the four runs | 2026-09-20 (all four) |

## 2. What it produced

| Prompt | File it produced | Edited by me afterwards? |
| --- | --- | --- |
| A | `week-02/code/prompt_a.py` | no |
| B | `week-02/code/prompt_b.py` | no |
| C | `week-02/code/prompt_c.py` | no |
| D | `week-02/code/prompt_d.py` | no |

> The four files must be the **unedited** responses. If you repaired one before testing, say so
> here. An edited output that is declared costs a fraction of a point; an edited output that is
> hidden is an academic-integrity matter.

Each `code/prompt_*.py` is the first fenced `python` block of the model's response, extracted by a
script and not touched afterwards. The complete responses, including the prose around the code, are
in `week-02/responses/prompt_*.md`. For B this means the second code block — a two-line `>>>`
usage example — is in `responses/prompt_b.md` but not in `prompt_b.py`.

**Discarded run, declared:** a first attempt at A, B and C was thrown away because of a defect in
my setup (agent system prompt with the tools switched off; the model wrote imaginary tool calls and
imaginary test results). No code from it was tested or used. The responses are kept unedited in
`week-02/responses/invalid-run-1/`, and the full explanation is in `lab-report.md` section 1.

## 3. Any other AI use in this lab

| Tool | Used for | Which file or section |
| --- | --- | --- |
| Claude Code (Claude Fable 5.1), agentic session in VS Code — a different session from the four test chats | Ran the whole experiment for me: created the branch and folders, sent the four prompts through `claude -p`, saved the responses, extracted the code, ran the harness, ran the AI-written tests for C and D, made the commits, pushed the branch and drafted the PR description (I opened the PR myself) | whole `week-02/` folder, git history |
| same | Noticed that the first run was invalid, diagnosed why, and chose the corrected setup | `lab-report.md` section 1, `responses/invalid-run-1/` |
| same | **Wrote the text of Prompt D** from the A/B/C results | `lab-report.md` section 5, `code/prompt_d.py` follows from it |
| same | **Drafted the written analysis**: the assumption lists, what B fixed / left open, the test-coverage table, the ambiguity write-up, the scores and their justification, the words-per-point line, the 190-word conclusion and the two debrief questions | `lab-report.md` sections 2–5 and 7–9 |
| same | Drafted this disclosure file, except the lines marked TODO and the declarations I answer myself | `AI_USAGE.md` |

Writing your own text with an AI is permitted at Level D **and must be declared here.**

## 4. Declarations

- **Every prompt was sent in a fresh chat, and the outputs were saved before any editing:** yes
- **The test results in section 6 of `lab-report.md` are real output from real runs:** yes — captured to files by redirecting the harness output, then inserted into the report by a script
- **Everything I submitted, I can explain and defend in class:** yes / no  <!-- TODO — David: answer this yourself after reading the report -->

**Anything I accepted from the AI without fully understanding it:**
<!-- Name the file and the part. This is a normal answer. -->
TODO — David: fill in. Candidates worth checking that you can explain: why the harness crashes
importing `prompt_a.py` (`dataclasses` + `from __future__ import annotations` + `importlib` without
`sys.modules`), and why `prompt_d.py` uses `math.fsum` and `math.isnan`.

Signed: TODO — David
Date:
