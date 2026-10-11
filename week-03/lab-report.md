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

Fresh chat. Prompt = README section 1, then the three selected stories (US-02, US-03, US-05 from my
revised set), then the Part 3 prompt verbatim: `chat/ac_prompt.txt`. Reply also in
`chat/ac_response.md`. The reply contains its own gherkin code fences, so it is fenced with `~~~~` here.

~~~~
# Acceptance Criteria: Smart Campus Study Room Booking

## Assumptions

### Decisions on the two open points

| ID | Question | Decision |
|---|---|---|
| **D1** | Does a booking that ends exactly when another begins overlap under R3? | **No.** A booking covers the time from its start up to, but not including, its end. So 12:00–14:00 and 14:00–15:00 in the same room are both allowed. |
| **D2** | Is exactly two hours allowed under R2? | **Yes.** A booking of up to and including 2:00 is accepted. Anything longer, even by one minute, is rejected. |

### General

- **A1** A time slot is a start and an end date-time chosen by the Student. The end must be after the start. The scenario defines no minimum length, slot size or opening hours, so none are enforced.
- **A2** "In the future" (R1) means the start time is strictly later than the current time when the request is processed. A start equal to the current time is rejected.
- **A3** All times are campus local time.
- **A4** The system knows whether a request comes from a Student or an Administrator, and which Student made each booking. How it knows is out of scope.
- **A5** Only active bookings count for R3. Cancelled bookings never cause an overlap.
- **A6** R3 applies per room only. The scenario gives no per-student limits, so a Student may hold several bookings, including at the same time in different rooms.
- **A7** If two requests compete for the same slot, the first one processed succeeds and the second is rejected under R3.
- **A8** "Rejected" always means:
  - no booking is created or changed;
  - availability is unchanged;
  - no confirmation (UC-06) is sent;
  - the system's response states which rule or condition caused the rejection.
- **A9** A confirmation (UC-06) is sent only after a successful booking or cancellation. The delivery channel is not specified.

### US-03: Cancel booking

- **A10** A Student can cancel only their own bookings, and only before the booking's start time.
- **A11** A cancelled slot becomes available to all Students immediately.

### US-05: Block room

- **A12** A block has no end date. The room stays blocked until an Administrator unblocks it (UC-04, a separate story).
- **A13** Blocking does not cancel or change existing bookings for that room, because R4 only prevents new bookings.
  - What should happen to those existing bookings is an open question for the product owner.
  - It is deliberately left open rather than invented here.
- **A14** A blocked room still appears in availability (UC-01), but it is reported as blocked with no bookable slots.

---

## US-02: Book room

*As a Student, I want to reserve a free room for a time slot, so that I have a guaranteed place to study at that time.*

**AC-02.1: Successful booking**
```gherkin
Given the current time is 2026-10-12 10:00
  And room R-101 is not blocked
  And room R-101 has no active booking between 2026-10-14 14:00 and 15:30
When the Student books room R-101 from 2026-10-14 14:00 to 15:30
Then the booking is created for that Student
  And availability no longer reports R-101 as free from 14:00 to 15:30 on 2026-10-14
  And the system sends the Student a booking confirmation (UC-06)
```

**AC-02.2: Start must be in the future (R1)**
```gherkin
Given the current time is 2026-10-12 10:00
  And room R-101 is not blocked and has no active bookings on 2026-10-12
When the Student books room R-101 from <start> to <end>
Then the request is <outcome>

Examples:
  | start            | end              | outcome                         |
  | 2026-10-12 09:00 | 2026-10-12 10:30 | rejected: start is in the past  |
  | 2026-10-12 10:00 | 2026-10-12 11:00 | rejected: start is not in the future (A2) |
  | 2026-10-12 10:01 | 2026-10-12 11:00 | accepted                        |
```

**AC-02.3: Maximum duration of two hours (R2)**
```gherkin
Given the current time is 2026-10-12 10:00
  And room R-101 is not blocked and has no active bookings on 2026-10-14
When the Student books room R-101 on 2026-10-14 from <start> to <end>
Then the request is <outcome>

Examples:
  | start | end   | outcome                                  |
  | 14:00 | 16:00 | accepted: exactly two hours (D2)         |
  | 14:00 | 16:01 | rejected: longer than two hours          |
  | 14:00 | 14:00 | rejected: end is not after start (A1)    |
  | 14:00 | 13:00 | rejected: end is not after start (A1)    |
```

**AC-02.4: No overlapping bookings in the same room (R3)**
```gherkin
Given the current time is 2026-10-12 10:00
  And rooms R-101 and R-102 are not blocked
  And room R-101 has an active booking by another Student on 2026-10-14 from 14:00 to 15:00
When the Student books <room> on 2026-10-14 from <start> to <end>
Then the request is <outcome>

Examples:
  | room  | start | end   | outcome                                             |
  | R-101 | 14:00 | 15:00 | rejected: same slot                                 |
  | R-101 | 14:30 | 16:00 | rejected: partial overlap                           |
  | R-101 | 13:30 | 15:30 | rejected: new booking contains existing one         |
  | R-101 | 12:00 | 14:00 | accepted: ends when existing begins (D1)            |
  | R-101 | 15:00 | 16:00 | accepted: starts when existing ends (D1)            |
  | R-102 | 14:00 | 15:00 | accepted: different room (A6)                       |
```

**AC-02.5: Blocked room cannot be booked (R4)**
```gherkin
Given the current time is 2026-10-12 10:00
  And room R-101 is blocked
  And room R-101 has no active booking on 2026-10-14
When the Student books room R-101 from 2026-10-14 14:00 to 15:00
Then the request is rejected because the room is blocked
```

---

## US-03: Cancel booking

*As a Student, I want to cancel a booking I made, so that the room is released for other students when I no longer need it.*

**AC-03.1: Successful cancellation**
```gherkin
Given the current time is 2026-10-12 10:00
  And Student A has an active booking for R-101 on 2026-10-14 from 14:00 to 15:00
When Student A cancels that booking
Then the booking is cancelled
  And availability reports R-101 as free from 14:00 to 15:00 on 2026-10-14
  And the system sends Student A a cancellation confirmation (UC-06)
```

**AC-03.2: Released slot can be booked by another Student**
```gherkin
Given the current time is 2026-10-12 10:00
  And room R-101 is not blocked
  And Student A's booking for R-101 on 2026-10-14 from 14:00 to 15:00 has been cancelled
When Student B books R-101 on 2026-10-14 from 14:00 to 15:00
Then the booking is created for Student B (A5)
```

**AC-03.3: Cannot cancel another Student's booking**
```gherkin
Given Student B has an active booking for R-101 on 2026-10-14 from 14:00 to 15:00
When Student A tries to cancel that booking
Then the request is rejected because the booking belongs to another Student
  And Student B's booking remains active
```

**AC-03.4: Cannot cancel a booking that has started or ended (A10)**
```gherkin
Given Student A has an active booking for R-101 on 2026-10-14 from 14:00 to 15:00
  And the current time is <now>
When Student A cancels that booking
Then the request is <outcome>

Examples:
  | now              | outcome                              |
  | 2026-10-14 13:59 | accepted: booking is cancelled       |
  | 2026-10-14 14:00 | rejected: booking has already started |
  | 2026-10-14 15:30 | rejected: booking has already ended   |
```

**AC-03.5: Booking already cancelled**
```gherkin
Given the current time is 2026-10-12 10:00
  And Student A's booking for R-101 on 2026-10-14 from 14:00 to 15:00 is already cancelled
When Student A cancels that booking again
Then the request is rejected because the booking is already cancelled
  And no second cancellation confirmation is sent
```

---

## US-05: Block room

*As an Administrator, I want to block a room, so that students cannot book a room that is out of service.*

**AC-05.1: Successful block**
```gherkin
Given room R-101 is not blocked
When the Administrator blocks R-101
Then R-101 is blocked
  And availability reports R-101 as blocked with no bookable slots (A14)
  And any later Student request to book R-101 is rejected under R4 (see AC-02.5)
```

**AC-05.2: Existing bookings are not changed by blocking (A13)**
```gherkin
Given room R-101 is not blocked
  And Student A has an active booking for R-101 on 2026-10-14 from 14:00 to 15:00
When the Administrator blocks R-101
Then R-101 is blocked
  And Student A's booking remains active and unchanged
  And no cancellation confirmation is sent to Student A
```

**AC-05.3: Room is already blocked**
```gherkin
Given room R-101 is already blocked
When the Administrator blocks R-101
Then R-101 remains blocked and nothing else changes
  And the system responds that R-101 was already blocked
```

**AC-05.4: Only an Administrator can block a room**
```gherkin
Given room R-101 is not blocked
When a Student tries to block R-101
Then the request is rejected because only an Administrator can block rooms
  And R-101 remains not blocked and can still be booked
```

---

## Rule coverage

| Rule / decision | Covered by |
|---|---|
| R1: start in the future | AC-02.2 |
| R2: at most two hours | AC-02.3 |
| R3: no overlap | AC-02.4, AC-03.2 |
| R4: blocked room cannot be booked | AC-02.5, AC-05.1 |
| D1: adjacent bookings allowed | AC-02.4 (rows 4 and 5) |
| D2: exactly two hours allowed | AC-02.3 (row 1) |

**For `submission.yml`:** I don't know your file's field names, so I haven't guessed any. Declare these two decisions:
- **D1:** a booking ending exactly when another begins is **not** an overlap.
- **D2:** exactly two hours **is** allowed.

**Worth flagging in your review:** A10 (cancel only before the start time) and A13 (blocking keeps existing bookings) are team decisions where the scenario is silent. They are not given rules. If your instructor expects these to be raised as questions rather than decided, list them under open questions instead.
~~~~

---

## 5. Criteria review (Part 3)

| Criterion (as generated) | Problem | What I changed it to | Final ID |
| --- | --- | --- | --- |
| AC-02.1 Successful booking (14:00–15:30, empty room) | Happy path that tests neither open decision | Success case is now 14:00–16:00 next to an existing 12:00–14:00: exactly two hours *and* touching, both accepted | AC-01 |
| AC-02.2 R1 as a 3-row Examples table | One criterion with three results; README: "one action triggers one observable result" | Kept only the boundary row (start = now → rejected, R1) | AC-02 |
| AC-02.3 R2 Examples incl. "14:00–14:00 / 14:00–13:00 rejected: end is not after start (A1)" | Mixes R2 with a different validation (A1) under the R2 heading; four results | R2 boundary 14:00–16:01 rejected; "exactly two hours" moved into AC-01; end-after-start kept as an assumption | AC-03 |
| AC-02.4 R3 Examples (same slot, partial, contains, touching ×2, other room) | Six results in one; and the **inside** case (new booking within an existing one) is missing | One R3 rejection with the missing case: 14:15–14:45 inside 14:00–15:00 | AC-04 |
| AC-02.5 Blocked room (R4) | Fine | Kept, wording aligned | AC-05 |
| AC-03.1 Successful cancellation (two Thens: availability + confirmation) | Availability clause duplicates AC-07, which tests it observably | Kept without the availability clause | AC-06 |
| AC-03.2 Released slot can be booked by another Student | Fine | Kept | AC-07 |
| AC-03.3 Cannot cancel another Student's booking | Fine | Kept | AC-08 |
| AC-03.4 Cannot cancel a booking that has started or ended (A10) | **Invented rule.** No line of README section 1 limits cancellation by time; the assistant itself calls A10 a "team decision where the scenario is silent" | Removed; not replaced | — |
| AC-03.5 Booking already cancelled | Fine | Kept | AC-09 |
| AC-05.1 Successful block (+ "reported as blocked with no bookable slots (A14)") | A14 describes how availability is *displayed*, close to a screen detail | Kept the block and the R4 consequence, dropped the display clause | AC-10 |
| AC-05.2 Existing bookings not changed by blocking | Fine; makes the blocking assumption testable | Kept | AC-11 |
| AC-05.3 Room already blocked | Fine | Kept | AC-12 |
| AC-05.4 Only an Administrator can block a room | **Out of scope**: an access-control rule that rests on authentication, which README section 1 excludes | Removed | — |
| Assumptions A3 "All times are campus local time", A7 "first request processed wins" | Not needed by any remaining criterion | Dropped | — |

**The two open questions.** Write your decision and the reason. Either answer is accepted.

| Question | My decision | Why |
| --- | --- | --- |
| A booking ending exactly when another begins — overlap under R3? | allowed | A booking covers [start, end): 12:00–14:00 and 14:00–15:00 share no minute, so there is nothing for R3 to forbid. Tested in AC-01 |
| Is exactly two hours allowed under R2? | allowed | "at most two hours" includes two hours; 2 h 1 min is rejected. Tested in AC-01 and AC-03 |

**Which invalid or boundary case did the assistant leave out?**

The **inside** overlap: a new booking that lies entirely within an existing one (14:15–14:45 vs
14:00–15:00). Its R3 table had same slot, partial and contains, but an implementation that only
checks whether the *existing* booking's endpoints fall inside the new one passes all three and
fails this one. It is now AC-04.

---

## 6. Original AI output — use-case diagram (Part 4)

Fresh chat: README section 1, then the Part 4 prompt verbatim (`chat/uc_prompt.txt`). The full
reply, with its explanation, is `chat/uc_response.md`.

```
@startuml SmartCampus_StudyRoomBooking
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false

actor "Student" as Student
actor "Administrator" as Admin

rectangle "Smart Campus - Study Room Booking" {
  usecase "View availability\n(UC-01)" as UC01
  usecase "Book room\n(UC-02)" as UC02
  usecase "Cancel booking\n(UC-03)" as UC03
  usecase "Block or unblock room\n(UC-04)" as UC04
  usecase "Review usage\n(UC-05)" as UC05
  usecase "Send confirmation\n(UC-06)" as UC06

  UC02 ..> UC06 : <<include>>
  UC03 ..> UC06 : <<include>>
}

' Student (primary actor, left side)
Student -- UC01
Student -- UC02
Student -- UC03

' Administrator (primary actor, right side)
UC04 -- Admin
UC05 -- Admin

note bottom of UC02
  Constrained by business rules R1-R4:
  R1 start in the future
  R2 at most two hours
  R3 no overlap for the same room
  R4 blocked room cannot be booked
end note
@enduml
```

Rendered diagram (image, or a link): original `img/use-cases-original.png`, revised
`img/use-cases.png`, both rendered with the PlantUML web server.

---

## 7. Diagram review (Part 4)

| Element | Problem | What I changed |
| --- | --- | --- |
| Use-case names `"View availability\n(UC-01)"` … `"Send confirmation\n(UC-06)"` | The ID is part of the rendered name, so the name is no longer the business goal from section 1, and the traceability table spells them without IDs | Names exactly as in section 1; IDs kept in the aliases `UC01` … `UC06` |
| `UC02 ..> UC06 : <<include>>`, `UC03 ..> UC06 : <<include>>` | Justified in the reply's prose, but nothing in the diagram source says why | A `' why:` comment above each include, citing UC-06 "confirms a booking or a cancellation" |
| `note bottom of UC02` quoting R1–R4 | Correct, but it deliberately leaves both open questions unsettled, and the diagram depends on them | Note now states both decisions: start = now rejected, exactly 2 h allowed, touching allowed |
| Associations | Checked every one against section 1: Student → View / Book / Cancel; Administrator → Block-or-unblock / Review; nobody → Send confirmation | None changed (see below) |

**Associations.** Which actor–use-case links did the assistant draw that a person does not actually
trigger? Name them.

None in this draft. I checked the two the README warns about: *Send confirmation* has no actor
(the system performs it inside Book and Cancel, via `<<include>>`), and *Review usage* is linked to
the Administrator only, a person who does trigger it ("watch how they are used"). The assistant
also did **not** link the Administrator to View availability, which section 1 does not give them.
I report "no wrong association" as observed rather than inventing one.

**Did any screen, database or internal component appear as a use case or an actor?**

No: two actors, six use cases, no "System" actor; PU-2 and PU-5 confirm it.

---

## 8. Traceability (Part 5)

Summarise what the table in `requirements/traceability.md` shows:

- Use cases with **no story** behind them: none; every UC-01…UC-06 has at least one (US-01…US-07).
- Stories with **no use case** they belong to: none.
- Criteria that test **no rule** from section 1: AC-08 and AC-09 (ownership and double cancel,
  from US-03, not from R1–R4), AC-11 and AC-12 (what blocking does *not* do). They test the
  stories and my assumptions, not a numbered rule.

**What does the largest gap tell you about the generated requirements?**

UC-01 View availability and UC-05 Review usage have stories but no criteria, and "unblock" has
none either. Three selected stories cannot cover seven, and the assistant spent its criteria on
the booking rules it was told about (R1–R4) and on rules it invented (cancel-before-start,
admin-only). The parts the prompt did not name are the parts left untested.

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

The acceptance criteria were the most wrong part. The assistant added two rules that are not in
section 1: AC-03.4, "cannot cancel a booking that has started", and AC-05.4, "only an
Administrator can block". AC-05.4 also depends on authentication, which is out of scope. The
checker cannot catch either one, because both are well-formed Given/When/Then. I caught them by
asking, for every criterion, which line of section 1 it comes from. Neither has an answer.

The assistant got the boundary tables right. Its R1–R3 Examples gave me the start-equals-now,
two-hours-one-minute and touching cases in seconds. Deriving them by hand would have taken much
longer. It also kept Send confirmation free of actors without being told.

If I had to hand one item to an implementer, I would rewrite the assumption on blocking first
(US-05, AC-11). R4 says only that a blocked room cannot be *booked*. Nobody has decided what
happens to the bookings it already has. An implementer could go either way, and AC-11 is the
only criterion that stops a silent mass cancellation.
