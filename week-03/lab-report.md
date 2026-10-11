# Lab report — Practice #03, Requirements Engineering with AI

Fill in every section. **Do not delete or renumber the headings** — the README points at them and a
missing heading reads as a missing section.

Name: David Torossyan
Student ID: TODO — David
GitHub username: Xseron

---

## 1. Setup

| | |
| --- | --- |
| AI assistant (tool) | Claude Code (Anthropic) v2.1.296, used as a plain chat: headless `claude -p`, tools disabled, neutral system prompt; one fresh session per prompt |
| Exact model name and version | Claude Opus 5.5 (`claude-opus-5-5`) |
| Date of the session | 2026-10-11 (late submission — the lab was due 2026-09-27) |
| Diagram renderer used | PlantUML web server (`https://www.plantuml.com/plantuml/png/…`) |

Exact command for every prompt (only the prompt file changes; each prompt is a new `--session-id`,
so each is a fresh chat):

```
claude -p --model claude-opus-5-5 --safe-mode --tools ""   --system-prompt "You are Claude, an AI assistant made by Anthropic."   --session-id <new uuid> --output-format json < turn.txt
```

Every prompt was sent with README section 1 (the scenario) pasted above it. The full prompts and
replies are in `week-03/chat/`.

One tool and one model for all three prompts. If you switched, say why here — it changes what your
findings mean.

---

## 2. Original AI output — user stories (Part 1)

Paste the **unedited** response to Prompt 1. Do not tidy it. If it is long, paste all of it anyway;
this is the baseline everything else is measured against.

The prompt (README section 1 pasted above it) is `chat/stories_prompt.txt`; the reply below is also
`chat/stories_response.md`, saved by a script before it was read.

```
# Smart Campus Study Room Booking: User Stories

## Actor goals

**Student**
- Find a room and a time that are actually free.
- Secure a room for a study session.
- Release a room they no longer need.
- Know for certain that a booking or cancellation went through.

**Administrator**
- Stop students from booking a room that is out of service.
- Return a room to service when it is usable again.
- Understand how the rooms are being used.

## User stories

Priorities use MoSCoW. **Must** means the system fails without it. **Should** means it is required but booking still works without it.

**US-01: View availability (UC-01) · Student · Must**
As a student, I want to see which study rooms are free and at what times, so that I can choose a slot before I try to book.
*Assumption:* A slot that starts exactly when another booking ends is free. Back-to-back bookings do not overlap under R3, so 10:00–12:00 and 12:00–14:00 in the same room can both exist.

**US-02: Book room (UC-02) · Student · Must**
As a student, I want to reserve a free room for a time slot, so that I have a guaranteed place to study at that time.
*Assumption:* A booking of exactly two hours is allowed under R2. Only bookings longer than two hours are rejected.

**US-03: Cancel booking (UC-03) · Student · Should**
As a student, I want to cancel a booking I made, so that the room is released for other students when I no longer need it.
*Assumption:* A cancelled slot becomes free immediately and can be booked by another student.

**US-04: Send confirmation (UC-06) · Student · Should**
As a student, I want to receive a confirmation when my booking or cancellation succeeds, so that I know for certain whether the room is reserved for me.
*Assumption:* The system sends exactly one confirmation per successful booking or cancellation. It sends no other messages, such as reminders.

**US-05: Block room (UC-04) · Administrator · Must**
As an administrator, I want to block a room, so that students cannot book a room that is out of service.
*Assumption:* Blocking stops new bookings (R4) but does not cancel bookings that already exist for that room.

**US-06: Unblock room (UC-04) · Administrator · Must**
As an administrator, I want to unblock a room, so that students can book it again once it is usable.
*Assumption:* An unblocked room can be booked immediately, subject to R1–R3 like any other room.

**US-07: Review usage (UC-05) · Administrator · Should**
As an administrator, I want to review how each room was used over a period I choose, so that I can see which rooms are in demand and which are underused.
*Assumption:* Usage is calculated only from bookings that were not cancelled. It does not reflect whether students actually showed up, because attendance is out of scope.

## Notes for your review

- **The two decisions** for your assumptions and `submission.yml`:
  - **R3:** back-to-back bookings are *not* an overlap.
  - **R2:** exactly two hours *is* allowed.
  
  I made these choices, but they're yours to own. Either answer is accepted, so change them if you prefer. I haven't written `submission.yml` because I don't know its required format.
- **A side effect of the R3 decision:** a student could book 10:00–12:00 and 12:00–14:00 in the same room, which gives them four hours in a row. No rule in the scenario forbids this, and I haven't added one. Decide whether you accept it or want to note it.
- **A side effect of the US-05 assumption:** a blocked room can still have earlier bookings in it. That is the literal reading of R4 ("cannot be *booked*"), but it is a real gap worth mentioning.
- **Scope:** the stories avoid payments, check-in, equipment, reminders, authentication, waiting lists and anything about screens or storage. Still, do your own pass against the out-of-scope list, since that check is the point of the exercise.
```

---

## 3. Story review (Part 2)

One row per change you made. "Kept unchanged" is a valid row and needs a reason too.

| Story (as generated) | What I did | Why | Final ID |
| --- | --- | --- | --- |
| All seven: priority given as MoSCoW ("Must"/"Should") | Re-mapped Must → High, Should → Medium | The template fixes High / Medium / Low; MoSCoW "Should" here meant "required but booking works without it", which is Medium, not Low | US-01 … US-07 |
| All seven: header "US-0n: <name> (UC-0n) · <role> · <priority>" | Rewrote into the fixed ID / Story / Priority / Assumption shape; the UC link moved to `traceability.md` | The checker and the traceability table read the fixed shape | US-01 … US-07 |
| US-01 View availability — assumption "A slot that starts exactly when another booking ends is free … 10:00–12:00 and 12:00–14:00 … can both exist" | Rewritten: what "free" means (no overlapping active booking **and** not blocked), touching = free, pointing to the decision in `acceptance-criteria.md` | The generated assumption silently decided open question 1 for me, and it left out R4: a blocked room must not be shown as free | US-01 |
| US-02 Book room — assumption "exactly two hours is allowed under R2" | Kept, and declared as **my** decision (§5) | The assistant decided open question 2 on its own; I checked it against R2 ("at most two hours") and agree, so it stays — but the decision is mine to declare | US-02 |
| US-03 Cancel booking — "cancel a booking I made"; assumption "becomes free immediately and can be booked by another student" | Assumption rewritten to say a student can cancel **only their own** booking | "a booking I made" is in the story but the assumption did not make ownership testable; "the student made" is the UC-03 note in README section 1 | US-03 |
| US-04 Send confirmation (role Student) | Kept unchanged | UC-06 is something the system does, but the story is the Student's goal of *knowing* the result — a valid stakeholder outcome. The diagram, not the story, is where "nobody triggers Send confirmation" matters (§7) | US-04 |
| US-05 Block room / US-06 Unblock room | Kept as two stories (not merged into UC-04's single name) | Each is one valuable outcome and fits one iteration; both trace to UC-04 | US-05, US-06 |
| US-05 assumption "does not cancel bookings that already exist" | Kept | R4 says a blocked room cannot be *booked*; it is silent on existing bookings, so the literal reading is the safest assumption — and it is one, so it stays visible | US-05 |
| US-07 Review usage | Kept unchanged | Administrator goal, period chosen by the user, explicitly excludes attendance (out-of-scope list) | US-07 |
| "Notes for your review": back-to-back bookings let one student hold 10:00–14:00 | No new rule added; recorded as a known consequence | No rule in section 1 limits bookings per student; adding one would widen the scenario | — |

**Did the assistant invent anything outside the scenario?** Name it against the out-of-scope list in
README section 1, or write "no, and here is how I checked".

No feature was invented. I checked every story and assumption against each item of the out-of-scope
list: no payment/fine, no check-in or QR (US-07 explicitly excludes attendance), no equipment or
maintenance, no notification beyond UC-06 (US-04 explicitly excludes reminders), no registration
or passwords, no waiting list, no screens or databases. What it *did* do beyond the scenario was
decide both open questions itself (US-01, US-02) — not scope creep, but a decision that was not
its to make.

**How many stories did you end with, and why that number?**

Seven. One per use case, except UC-04, which has two separate outcomes (block, unblock) that are
tested separately. Merging US-05 and US-06 would give a story with two goals; adding more would
mean inventing functions outside the six.

---

## 4. Original AI output — acceptance criteria (Part 3)

```
(paste here)
```

---

## 5. Criteria review (Part 3)

| Criterion (as generated) | Problem | What I changed it to | Final ID |
| --- | --- | --- | --- |
| | | | |

**The two open questions.** Write your decision and the reason. Either answer is accepted.

| Question | My decision | Why |
| --- | --- | --- |
| A booking ending exactly when another begins — overlap under R3? | allowed / not-allowed | |
| Is exactly two hours allowed under R2? | allowed / not-allowed | |

**Which invalid or boundary case did the assistant leave out?**

---

## 6. Original AI output — use-case diagram (Part 4)

```
(paste the PlantUML source exactly as generated)
```

Rendered diagram (image, or a link):

---

## 7. Diagram review (Part 4)

| Element | Problem | What I changed |
| --- | --- | --- |
| | | |

**Associations.** Which actor–use-case links did the assistant draw that a person does not actually
trigger? Name them.

**Did any screen, database or internal component appear as a use case or an actor?**

---

## 8. Traceability (Part 5)

Summarise what the table in `requirements/traceability.md` shows:

- Use cases with **no story** behind them:
- Stories with **no use case** they belong to:
- Criteria that test **no rule** from section 1:

**What does the largest gap tell you about the generated requirements?**

---

## 9. Checker runs

Paste the **real terminal output** of both runs. A table with nothing behind it does not count.

```
$ python tests/check_requirements.py
(paste)
```

```
$ python tests/validate_submission.py
(paste)
```

| | PASS | FAIL | ERROR |
| --- | --- | --- | --- |
| `check_requirements.py` | | | |

Commit these numbers were produced at (`git rev-parse --short HEAD`):

**Every FAIL, one line each: what it is and what you decided to do about it.** A FAIL you report and
explain costs you nothing.

**Did you run the checks by hand instead of with Python?** Say so here — it costs nothing, but it
has to be said.

---

## 10. Conclusion (150–200 words)

Answer all three:

1. Which part of the generated requirements was most wrong, and how would you have caught it without
   a checker?
2. What did the assistant get right that would have taken you noticeably longer by hand?
3. You are handing these requirements to someone who will implement them, and you will not be in the
   room. Which single one would you rewrite first, and why?

Be specific. "The AI was useful" is worth nothing; "UC-06 had no story behind it until I wrote
US-07, and the checker is what told me" is worth everything.
