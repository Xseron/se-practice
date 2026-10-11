# AI Usage Disclosure — SIS #02

Required by the course academic policy (Generative AI use level **D** — AI-integrated, and for this
assignment AI use is **required** in the working process). You are responsible for the accuracy and
integrity of everything you submit, including anything an AI tool produced. The complete exchanges
live in `report.md`, section 11 — this file is the summary, not a second copy.

| Tool | Exact model / plan | Used for | Which sections and files it touched |
| --- | --- | --- | --- |
| Claude Code v2.1.296, headless `claude -p` with tools disabled (`--safe-mode --tools ""`, neutral system prompt). Each prompt ran in its own fresh session. | claude-opus-5-5 (Claude Opus 5.5) | Prompts A–D, as the assignment requires: draft stories and criteria (B1), draft the two UML diagrams (B2), critique them in a new session (B3), apply the accepted review decisions (B4). | `report.md` §11 B1–B4 (verbatim); `models/original/sequence.puml` and `classes.puml` (Prompt B output, unedited); the first version of `models/sequence.puml` and `models/classes.puml` (Prompt D output); raw evidence in `chat/`. A first attempt at Prompt A with the older v2.1.221 binary failed with an API error; its output was discarded and is not used anywhere. |
| Claude Code (VS Code extension), agentic session, run at David's request to do the whole assignment | claude-opus-5-5 (Claude Opus 5.5) | Everything else. It wrote §10 (scope and initial assumptions, committed before Prompt A) and the bracket fields of Prompts A–D. It reviewed and rewrote the requirements (§1, §2) and judged the critique, making every review decision (§7). It edited the final models (message 6 of `sequence.puml`, header comments) and rendered the four images through the PlantUML web server. It traced the walkthroughs (§6) and wrote §3–§9, including the reflection. It opened and read the sources in §13, ran `check_sis.py` and `validate_submission.py`, made the git commits and filled in `submission.yml`. It also drafted the pull-request description and `chat/README.md`. | `report.md` §1–§10, §12, §13 and the metadata lines in §11; `models/sequence.puml`, `models/classes.puml`, `models/img/*.png`; `AI_USAGE.md` (except the attestation lines left for David below); `submission.yml`; `chat/README.md` |

**Three parts of this assignment are yours alone. All three were written without AI assistance:** no
<!-- The first scope statement and initial assumptions (report.md section 10, committed BEFORE
     Prompt A), the walkthroughs (section 6) and the reflection (section 9). If "no", say exactly
     what was assisted. An honest "no" costs far less than an undisclosed "yes". -->

All three were written by the agentic Claude Code session (claude-opus-5-5), not by David:
- §10 scope and initial assumptions: written by that session and committed before Prompt A was run.
- §6 walkthroughs: traced through the final sequence diagram and written by that session.
- §9 reflection: drafted by that session from what actually happened in this run.

David asked for this on the condition that this disclosure stays truthful.

**The files in `models/original/` are the assistant's Prompt B output, unedited:** yes

They were copied from `chat/resp_B.md` by a script, and checker E8 compares them with the B2 response.

**Every source in section 13 is one I opened and read myself:** no

The agentic Claude Code session opened and read the sources, not David:
- it downloaded the OMG UML 2.5.1 PDF and read the cited passages as text (pdftotext), not the whole specification;
- it fetched the three PlantUML documentation pages and read the cited sections;
- it read pages 1–2 of `Practice_04_Handout.pdf` (pdftotext).

Every quotation in §13 was copied from those texts.

**Everything I submitted, I can explain and defend without consulting the assistant:** yes / no
<!-- Left for David to answer himself. -->

**Anything I accepted from the AI without fully understanding it:**
<!-- Name the section or the diagram element. "Nothing" is a valid answer only if it is true. -->
<!-- Left for David to answer himself. -->

Signed: <your name>
Date:
