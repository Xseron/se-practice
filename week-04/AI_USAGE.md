# AI Usage Disclosure — Week 04

Required by the course academic policy (Generative AI use level **D** — AI-integrated). You are
responsible for the accuracy of everything you submit, including every diagram an AI drafted.

| Tool | Exact model | Used for | Which files it touched |
| --- | --- | --- | --- |
| Claude Code v2.1.296, headless `claude -p`, tools disabled (chat 1) | Claude Opus 5.5 (`claude-opus-5-5`) | Task 1 — use-case draft | `models/original/use-case.puml`, `chat/resp_1.md` |
| same chat 1 | Claude Opus 5.5 (`claude-opus-5-5`) | Task 2 — class draft | `models/original/class.puml`, `chat/resp_2.md` |
| same chat 1 | Claude Opus 5.5 (`claude-opus-5-5`) | Task 3A — sequence draft | `models/original/sequence.puml`, `chat/resp_3.md` |
| same tool, new session (chat 2) | Claude Opus 5.5 (`claude-opus-5-5`) | Critique of the revised diagrams | `lab-report.md` §6, `chat/critique_response.md` |
| Claude Code (VS Code extension), agentic session, separate from both chats | Claude Opus 5.5 (`claude-opus-5-5`) | Ran the lab for me: branch, sending the prompts and saving the replies by script, extracting the `.puml` originals, **writing the revised diagrams**, rendering, running the checkers, the commits, and **drafting the whole worksheet** | `models/*.puml`, `models/img/`, `lab-report.md`, `AI_USAGE.md`, `submission.yml`, `chat/README.md` |

**The files in `models/original/` are the AI's first replies, unedited:** yes
<!-- Each is the first plantuml block of the reply, copied by a script. -->

**I can explain every element of the revised diagrams in `models/`:** yes — the corrections themselves were written by the agentic session in the table above

**Did an AI write any part of `lab-report.md` other than the critique it produced?** yes
Sections 1–10 were drafted by the agentic session: findings, the both-ways readings, assumptions
A1–A4, the critique verdicts, the consistency table, the change log, the checker paste and the
conclusion.
What I changed afterwards: nothing.

**Anything I accepted from the AI without fully understanding it:**
nothing

Signed: David Torossyan
Date: 2026-10-11
