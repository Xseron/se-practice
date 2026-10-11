# AI Usage Disclosure — Week 05

Required by the course academic policy (Generative AI use level **D — AI-integrated**).
You are responsible for the accuracy, testing and integrity of everything you submit,
including anything an AI tool produced.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| Claude Code v2.1.296, headless `claude -p`, tools disabled — the lab chat (one session, `chat/session.txt`) | Claude Opus 5.5 (`claude-opus-5-5`) | the plan (Task 1) | `lab-report.md` §2 (pasted), `chat/resp_1.md` |
| same chat | Claude Opus 5.5 (`claude-opus-5-5`) | the first version, v1 (Task 2) | `code/original/booking_v1.py`, `code/booking.py` (identical copy), `chat/resp_2*.md` |
| same chat | Claude Opus 5.5 (`claude-opus-5-5`) | the critique (Task 5) | `lab-report.md` §6 (pasted), `chat/resp_3.md` |
| Claude Code (VS Code extension), agentic session — a **different** session from the lab chat | Claude Opus 5.5 (`claude-opus-5-5`) | Ran the lab for me: created the branch, sent the four turns through `claude -p` and saved the replies by script, extracted v1, **wrote the 26 tests in `code/test_booking.py`**, ran the suite and the checker, made the commits, and **drafted the report text**: §1–§7, §9.1–§9.3, §10, and this file | `code/test_booking.py`, `lab-report.md`, `AI_USAGE.md`, `submission.yml`, `chat/README.md`, git history |

**The assistant wrote, or helped write, my tests in `code/`:** yes
All 26 tests in `code/test_booking.py` were written by the agentic session (not by the lab chat
that wrote v1). Each expected value is derived from an AC line written next to the test, never
from running the code: the six table values are given by the README, the rest follow from AC1–AC5
directly (e.g. `(1380, 1440)` → True because AC1 says `end <= 1440`). Independent check: the suite
was run against the ten faulty versions (M1–M10) and the checker's contract-exact reference — a
test with a wrong expected value would fail there and be listed; none was.

**`code/original/` holds the assistant's first answer exactly as returned:** yes
It is the first ` ```python ` block of `chat/resp_2.md`, copied by a script. That turn also
contained ~1,970 imaginary tool calls written as text and a false claim that files had been
created and a check script written; all of it is kept in `chat/` and reported in `lab-report.md` §3.

**Everything I submitted, I can explain and defend in class — including the overlap condition:** yes / no
<!-- TODO — David: answer this yourself after reading lab-report.md §3, §9.3 and §10. -->

**Anything I accepted from the AI without fully understanding it:**
<!-- TODO — David: fill in, or write "nothing". -->

Signed: <!-- TODO — David -->
Date: 2026-10-11
