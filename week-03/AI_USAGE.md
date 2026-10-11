# AI Usage Disclosure — Week 03

Required by the course academic policy (Generative AI use level **D** — AI-integrated).
AI use is expected in this lab. You remain responsible for the accuracy, testing and integrity of
everything you submit, including everything an AI tool produced.

| Tool | Exact model + version | Used for | Which files it touched |
| --- | --- | --- | --- |
| Claude Code v2.1.296, headless `claude -p`, tools disabled, fresh session | Claude Opus 5.5 (`claude-opus-5-5`) | Prompt 1 — user stories | `requirements/user-stories.md`, `chat/stories_*` |
| same, new fresh session | Claude Opus 5.5 (`claude-opus-5-5`) | Prompt 2 — acceptance criteria | `requirements/acceptance-criteria.md`, `chat/ac_*` |
| same, new fresh session | Claude Opus 5.5 (`claude-opus-5-5`) | Prompt 3 — use-case diagram | `requirements/use-cases.puml`, `chat/uc_*` |

**One tool and one model for all three prompts:** yes

**Did you use AI for anything beyond the three verbatim prompts** — rewriting your review, writing
the traceability table, drafting the conclusion? Name it. This is allowed and disclosed, not hidden.

Yes. A separate agentic Claude Code session in VS Code (same model, `claude-opus-5-5`) ran the
whole lab for me. It created the branch, sent the three prompts through `claude -p` and saved
the replies by script, and chose which three stories got criteria (US-02, US-03, US-05). It also
wrote the review: the revised stories, the revised criteria, the revised diagram, the traceability
table, the review tables and answers in `lab-report.md` §3, §5, §7, §8, the conclusion (§10), this
file and `submission.yml`. It ran both checkers and made the commits. This was done on 2026-10-11,
after the deadline, so the submission is late.

**Everything I submitted, I can explain and defend in class:** yes

**Anything I accepted from the AI without fully understanding it:**
nothing

Signed: David Torossyan
Date: 2026-10-11
