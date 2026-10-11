# Week 04 — Lab report: Modeling the System with UML

> The single worksheet for this lab. Fill in every section. **Do not delete, rename or renumber
> the headings** — the checker and the grader find your work by them. Replace every `<...>`
> placeholder; a row that still contains `<...>` counts as empty.

---

## 1. Setup

| Field | Value |
| --- | --- |
| Name | David Torossyan |
| Group | Monday 16-19 |
| AI assistant | Claude Code (Anthropic) v2.1.296, used as a plain chat: headless `claude -p`, tools disabled, neutral system prompt |
| Exact model | Claude Opus 5.5 (`claude-opus-5-5`) |
| Renderer | PlantUML web server (`https://www.plantuml.com/plantuml/png/…`) |
| Behaviour diagram | sequence |
| Stories used | the reference set from README §3 — Week 03 had not been completed when this lab started |

Tasks 1–3 were one chat (`--session-id`, then `--resume`); the critique was a new session. Every
prompt and reply is in `week-04/chat/`. Late submission: done on 2026-10-11, due 2026-10-04.

---

## 2. Prompts as sent

Paste every prompt **exactly as you sent it**, in the order you sent it, one code block each. The
AI's first replies are saved as files in `models/original/` — do not paste them here.

### 2.1 Task 1 — use-case prompt

```text
Using the supplied scenario and approved stories, generate PlantUML for a use-case diagram. Include Student and Administrator outside a named system boundary. Model their goals, show justified associations, and list assumptions. Use include or extend only with a clear reason.
```

### 2.2 Task 2 — class prompt

```text
Create a UML domain class diagram in PlantUML for Smart Campus. Start with Student, Room, and Booking. Add attributes, appropriate operations, and association multiplicities. Add other classes only when requirements justify them. Explain each relationship and list assumptions. Avoid unjustified inheritance or composition.
```

### 2.3 Task 3 — behaviour prompt (3A sequence or 3B activity)

```text
Generate PlantUML for Book room. Use Student, BookingService, and BookingRepository lifelines. Validate the supplied rules, then attempt the reservation. Show a successful confirmation and an unavailable-room alternative using alt. Label messages and replies. Explain new design components and all assumptions.
```

### 2.4 Focused correction prompts (if you sent any)

```text
none — every correction was made by hand in models/*.puml (change log §8)
```

### 2.5 Critique prompt

Sent in a new chat, after the approved stories and the three revised `.puml` files pasted above it
(full message: `chat/critique_prompt.txt`):

```text
Compare my diagrams with the requirements. Identify missing rules, inconsistent names, and unjustified elements. Cite each issue and propose a specific correction.
```

---

## 3. Task 1 — use-case review

**Assumptions the AI listed:** A1 users already identified, login outside the boundary · A2
Administrator is not a specialised Student · A3 the system itself issues the confirmation, no
secondary actor · A4 Block and Unblock are separate use cases · A5 Unblock only for a blocked room
(precondition) · A6 Review usage is read-only, content unspecified · A7 blocking stops new bookings
only, existing ones are an **open question** not shown in the diagram · A8 no admin cancelling of
other users' bookings · A9 no Time/Clock actor.

At least **two** findings. A finding names the element, the problem and the rule or story that
proves it is a problem.

| # | Element | Problem | Rule or story | Fix |
| --- | --- | --- | --- | --- |
| 1 | Every use-case name, e.g. "Book study room" with a second, small-font line "US-01, R1, R2, R3, R4" inside the name | Story IDs and rule numbers are written into the use-case *name*, so the name is no longer a goal phrase, and "Book study room" does not match the scenario's "book a room" | Scenario sentence "Students view room availability, book a room, and cancel their own bookings" | Names are plain goals ("Book room", "View room availability" …); story IDs moved to `'` comments and notes |
| 2 | `UC_Book` — R1–R4 only in a `legend`, no element on the use case | The rules Book room depends on are not attached to it, and R4 (confirmation) has no visible place at all | R4, US-01 | Note on Book room: R1, R3, R2 checked before creation, R4 as an *outcome* of Book room, not a separate goal |
| 3 | `UC_Block` — the AI's A7 "open question … not shown in the diagram" | README §3: an undecided question must be declared "the moment a diagram depends on it"; Block room depends on it | R3, US-04 | Declared A1 (existing bookings are kept) and put it in a note on Block room |
| 4 | Book room — touching bookings undecided | Same: R2's meaning for 10:00–12:00 / 12:00–13:00 is not stated anywhere | R2 | Declared A2 (touching allowed, half-open intervals) in the Book room note |
| 5 | Associations (6 lines) | Checked both directions: Student only to US-01/02/03 goals, Administrator only to US-04/05/06; nobody linked to a confirmation | scenario, US-01…US-06 | No association changed — none was wrong |

---

## 4. Task 2 — class diagram review

### 4.1 Relationships, read both ways

One row per association in your **revised** class diagram.

| Association | Read left → right | Read right → left | Multiplicities |
| --- | --- | --- | --- |
| Student — Booking | one student makes 0..* bookings | each booking is made by exactly 1 student | 1 / 0..* |
| Booking — Room | each booking is for exactly 1 room | one room has 0..* bookings | 0..* / 1 |
| Booking — Confirmation | each booking produces exactly 1 confirmation | each confirmation belongs to exactly 1 booking | 1 / 1 — holds because only a *successful* request creates a Booking (R4) |

### 4.2 Constraints the multiplicities cannot show

- R2: a note on `Booking` — "no two ACTIVE bookings of the same Room overlap", with the half-open
  interval [start, start + duration) so touching is allowed (A2).
- R1: in the same note on `Booking` (checked before a Booking is created).
- R3: note on `Room` — no new Booking while `blocked = true`; `isBlocked()` exposes it.
- R4: note on `Confirmation` — exactly one per successful booking.

### 4.3 Assumptions

- A1: blocking a room keeps its existing bookings; R3 stops only new ones (`blocking_a_booked_room: keep-bookings`).
- A2: a booking ending 14:00 and one starting 14:00 do not overlap — intervals are [start, start + duration) (`overlap_touching_bookings: allowed`).
- A3: a room is "free" for a slot (US-02, `Room.isFreeAt`) when it is not blocked **and** no ACTIVE booking overlaps the slot.
- A4: in the sequence, the blocked check, the overlap query and the save run as one atomic unit per room, so two concurrent requests cannot both pass R2.
- R1 settles "exactly two hours": at most 2 h, so 2 h is allowed.

### 4.4 Findings

| # | Element | Problem | Rule or story | Fix |
| --- | --- | --- | --- | --- |
| 1 | `note right of Room` holding R2 | R2 is about bookings, and README §4 puts it in a note on `Booking` | R2, README §4 | R2 (with the half-open interval) moved to a note on `Booking`; Room's note keeps R3 |
| 2 | `class Administrator { adminId, name, blockRoom(), unblockRoom(), reviewUsage() }` with dependencies to Room and Booking | No rule or story needs any stored state of an administrator; its three operations only delegate to `Room.block()/unblock()` — the AI says so itself ("They hand the work to Room"). It is the actor, already in the use-case diagram | US-04, US-05, US-06; CL6 "domain concepts only" | Removed the class and its two dependencies |
| 3 | `Room.book(student, start, duration) : Booking` | Puts the Book room control flow in the domain model, while Task 3 must use `BookingService` for it — the same behaviour would live in two places | US-01; consistency with §5 | Removed; `Room.isFreeAt()` stays as the US-02 query |
| 4 | `Room - blocked : Boolean` private, no reader | Nothing can ask whether a room is blocked, so R3 has no operation (found by the critique, §6 row 1) | R3 | Added `+ isBlocked() : Boolean` |
| 5 | `Student - name : String` | No story uses a student's name; registration is out of scope (critique §6 row 7) | Out-of-scope list | Removed |
| 6 | Multiplicities, read both ways (§4.1) | All three read correctly; `0..*` on both Booking ends | R2, R4 | Kept |

---

## 5. Task 3 — behaviour diagram review

**Option chosen and why:** 3A sequence — it is the diagram where "validated before anything is
created" and "nothing saved on failure" can be checked message by message.

**Design components added beyond the domain model:**
- `BookingService` «service» — the control object for Book room: checks R1 itself, asks the
  repository for the R3 and R2 facts, decides, creates the Booking with its Confirmation and
  replies to the Student.
- `BookingRepository` «repository» — persistence abstraction: answers `isRoomBlocked`,
  `findActiveOverlapping` and stores the booking with `save`; it is where the A4 atomic unit lives.
Neither is a domain class, so neither is in `class.puml`.

| # | Element | Problem | Rule or story | Fix |
| --- | --- | --- | --- | --- |
| 1 | `alt [not blocked and overlapping is empty]` … `else [blocked (R3) or overlapping not empty (R2)]` | Typed square brackets are read by PlantUML as a hyperlink and eat the first word. Rendered, the success guard reads **"blocked and overlapping is empty"** — the meaning is inverted — and the failure guard loses "blocked" (`img` of the original vs `models/img/sequence.png`) | README §4 convention; R3 | Guards without brackets: `alt R1 violated`, `alt room blocked (R3)`, `alt overlapping not empty (R2)`, `else slot free` |
| 2 | `break [R1 violated]` | Same bracket problem (renders as "violated"); and `break` hides that the rest is the *else* of a decision | README §4; R1 | One `alt R1 violated / else time slot valid`, with R3 and R2 nested inside the else |
| 3 | `isRoomBlocked` → `findActiveOverlapping` always both called, one combined failure branch | When the room is blocked the overlap query still runs, and the student gets one "ROOM_UNAVAILABLE" for two different rules | R3, R2 | Separate decisions in rule order R1 → R3 → R2, each with its own rejection; the overlap query runs only for an unblocked room |
| 4 | Failure branches | Checked: no `create`/`save` message in any failure branch; validation (`validateTimeSlot`) is the first message after the request | SQ3/SQ4, R1 | Kept — correct in the original |
| 5 | `note over BS, BR` "assumption A6" | Refers to the AI's own numbering, not to any assumption in this report | traceability | Renumbered to A4 (§4.3); after the critique the three calls are wrapped in `group atomic per room (A4)` | AI critique

---

## 6. AI critique

Run the critique prompt once, on all your revised diagrams together. At least **three** rows. A
critique is another claim to evaluate, not a verdict: reject what is wrong and say why.

| # | Issue the AI raised | Element it cited | Verdict | Why |
| --- | --- | --- | --- | --- |
| 1 | M1: R3 cannot be checked through the class model — `blocked` is private, no operation reads it | `Room - blocked : Boolean` | accept | True: the note states R3 but nothing exposes it. Added `+ isBlocked() : Boolean` |
| 2 | M2: "free" in US-02 not defined w.r.t. the blocked flag | `Room.isFreeAt`, `UC_View` | accept | Without it, availability could list blocked rooms that Book room then rejects. Declared A3 and added notes on Room and View room availability |
| 3 | M3: Unblock room has no note although US-05 traces to R3 | `UC_Unblock` | accept | Cheap and correct; note added |
| 4 | M4: A1, A2, A6 cited but not defined in the requirements | all three diagrams | accept in part | They are defined — in §4.3 of this report, which the critique could not see. But "A6" was the AI's own number from its sequence reply; renumbered to A4 so every cited ID exists in §4.3 |
| 5 | N1 (High): add `BookingService`, `RoomRepository`, `BookingRepository` classes to `class.puml`, and a `RoomRepository` + `room : Room` lifeline to the sequence | `class.puml`, `sequence.puml` | reject | `class.puml` is a *domain* class diagram: Service/Repository classes are exactly what README §5 Part 2 and CL6 exclude, and §5 is where design components are named. Task 3 fixes three lifelines; adding two more changes the prompt's design. The real point (a repository answering a room question) is recorded in §5 |
| 6 | N2: three conventions for a time interval | `findActiveOverlapping(roomId, start, start + duration)` | accept | Changed to `(roomId, start, duration)`, matching `isFreeAt` and `overlaps`; `(from, to)` stays for the US-06 reporting period |
| 7 | N3: `ALREADY_BOOKED` hides partial overlaps; U1: `Student.name` unused | `rejected(ALREADY_BOOKED)`, `Student.name` | accept | Renamed to `OVERLAPS_EXISTING_BOOKING` (one code per rule); `name` removed (no story uses it) |
| 8 | N4: returned `confirmation(code, bookingId, roomId, start, end)` does not match `Confirmation {code, issuedAt}` | sequence message 13 | accept | Reply is now `confirmation : Confirmation` |
| 9 | U2: the atomic unit is only asserted in a note | `note over BS, BR` | accept | Wrapped the three calls in `group atomic per room (A4)` |
| 10 | "Already consistent: … the check order R1 → R3 → R2 → R4 is identical" | — | accept, checked | I compared the Book room note with the sequence: same order |

---

## 7. Consistency table

One row for each of **R1–R4**, then one row for **every use case in your revised use-case
diagram**, spelled exactly as in the diagram, with the story ID it traces to.

| Requirement / story | Use case | Classes | Behaviour element |
| --- | --- | --- | --- |
| R1 | Book room | Booking.start, Booking.duration; note on Booking | `validateTimeSlot(start, duration)` + note; guard `R1 violated` |
| R2 | Book room, Cancel own booking | Booking.status (BookingStatus.ACTIVE), `Booking.overlaps()`; R2 note on Booking | `findActiveOverlapping(roomId, start, duration)`; guard `overlapping not empty (R2)` |
| R3 | Book room, Block room, Unblock room | Room.blocked, `Room.isBlocked()`, `block()`, `unblock()`; note on Room | `isRoomBlocked(roomId)`; guard `room blocked (R3)` |
| R4 | Book room | Confirmation, Booking — Confirmation 1 / 1; note on Confirmation | `create Booking … with its Confirmation`, reply `confirmation : Confirmation` |
| US-01 | Book room | Student, Booking, Room, Confirmation | the whole sequence: `bookRoom(...)` → `save(booking)` → `confirmation` |
| US-02 | View room availability | Room, `Room.isFreeAt()` (A3) | not in the sequence (Book room only) |
| US-03 | Cancel own booking | Student, `Student.activeBookings()`, `Booking.cancel()`, `isOwnedBy()`, BookingStatus.CANCELLED | not in the sequence |
| US-04 | Block room | Room.blocked, `Room.block()` | not in the sequence; its effect is the `room blocked (R3)` branch |
| US-05 | Unblock room | Room.blocked, `Room.unblock()` | not in the sequence |
| US-06 | Review room usage | `Room.bookingsBetween(from, to)` | not in the sequence |

---

## 8. Change log

At least **three** rows, and at least one for each required diagram (use case, class, your
behaviour diagram). "Before" is what the AI produced; "After" is what you submitted.

| # | Diagram | Before (AI's original) | After (your revision) | Reason |
| --- | --- | --- | --- | --- |
| 1 | use case | Names with IDs inside: "Book study room" with a second, small-font line "US-01, R1, R2, R3, R4" inside the name etc.; rules only in a legend | Plain goal names ("Book room", "View room availability", …); notes on Book room (R1–R4, A2), Block room (A1), Cancel own booking | §3 rows 1–4 |
| 2 | use case | No note on Unblock room or View room availability | Notes: Unblock → R3 again subject to R1, R2; View → "free" = A3 | critique M2, M3 (§6 rows 2–3) |
| 3 | class | `class Administrator` + two dependencies; `Room.book()`; `Student.name`; R2 in a note on Room; `blocked` unreadable | No Administrator class; no `Room.book()`; no `name`; R2 note on Booking; `+ isBlocked()`; A3 in Room's note | §4.4 rows 1–5; critique M1, U1 |
| 4 | sequence | `break [R1 violated]`, `alt [not blocked and overlapping is empty]` / `else [blocked (R3) or …]` — renders inverted | Bare guards, nested `alt` R1 → R3 → R2, one rejection per rule | §5 rows 1–3, README §4 |
| 5 | sequence | `findActiveOverlapping(roomId, start, start + duration)`, `rejected(ALREADY_BOOKED)`, `confirmation(code, bookingId, roomId, start, end)`, A6 note | `(roomId, start, duration)`, `OVERLAPS_EXISTING_BOOKING`, `confirmation : Confirmation`, `group atomic per room (A4)` | critique N2, N3, N4, U2; §5 row 5 |

---

## 9. Checker output

Paste the complete output of `python tests/check_models.py`, then explain **every FAIL you are
keeping**. The same IDs go in `submission.yml` under `checker.kept_fails`. A FAIL you report and explain costs you nothing. One you hide costs the whole criterion.

```text
$ python tests/check_models.py      # at commit 3a6ebc0
Week 04 structural check - shape only, never quality

UC1  PASS  Student and Administrator declared
UC2  PASS  named system boundary: "Smart Campus Study Room Booking System"
UC3  PASS  all actors declared outside the boundary
UC4  PASS  all scenario goals present (6 use cases)
UC5  PASS  no actor is associated with a confirmation use case
UC6  PASS  actor responsibilities match the scenario
UC7  PASS  use cases are goals, not screens or components
UC8  PASS  every include / extend / generalization carries a ' why: comment (or there are none)
UC9  PASS  revised diagram differs from the AI's original
CL1  PASS  Student, Room and Booking present
CL2  PASS  Booking is associated with Student and with Room
CL3  PASS  every association has multiplicities at both ends
CL4  PASS  1 student / 1 room per booking, 0..* bookings per student and per room
CL5  PASS  every inheritance / composition / aggregation carries a ' why: comment (or there are none)
CL6  PASS  only domain concepts in the class diagram
CL7  PASS  attributes needed by R1-R3 are present
CL8  PASS  a note states R2 (no overlapping active bookings)
SQ1  PASS  Student, BookingService and BookingRepository lifelines present
SQ2  PASS  alt block with a guard on every branch (6 branches)
SQ3  PASS  validation happens before creation
SQ4  PASS  nothing is saved on a failure branch
SQ5  PASS  every message is labelled
SQ6  PASS  R1 (time range) is visible - checked or stated as a precondition
SQ7  PASS  R3 (blocked room) is visible
FI1  PASS  the AI's original output is kept for every diagram
FI2  PASS  a rendered image for every diagram
LR1  PASS  �1 setup filled (tool and model recorded)
LR2  PASS  5 prompts pasted in �2
LR3  PASS  5 use-case findings in �3
LR4  PASS  �4 relationships read both ways, 4 assumption(s) declared
LR5  PASS  5 behaviour-diagram findings in �5
LR6  PASS  10 critique issues with a verdict
LR7  PASS  5 change-log rows covering all three diagrams
CS1  PASS  6 approved stories
CS2  PASS  �7 traces R1-R4 into the diagrams
CS3  PASS  every use case traces to an approved story
CS4  PASS  every lifeline is a domain class or an explained design component

SUMMARY pass=37 fail=0 error=0
A FAIL you report and explain in lab-report.md �9 costs you nothing. One you hide costs the criterion.
```

**FAILs I am keeping, and why:** none. Earlier runs had CL3 FAIL (a `Booking ..> BookingStatus` dependency read as an association without multiplicities; removed, the type is already on `status`) and SQ4 FAIL (the success guard `else no overlap` contains "overlap", so the checker took it for a failure branch; renamed to `else slot free`, the diagram is unchanged in meaning).

---

## 10. Conclusion (120–180 words)

The sequence diagram was the most wrong, in a way you can only see by rendering it. The AI wrote
guards in square brackets, `alt [not blocked and overlapping is empty]`. PlantUML treats the
bracket as a link and drops the first word, so the success branch is labelled "blocked and
overlapping is empty". Read as drawn, a blocked room gets booked. Anyone coding from the picture
instead of the source would have shipped R3 inverted.

In the class diagram, an Administrator class only passed calls through to Room. Room.book()
repeated the work of BookingService, so the same rule would have lived in two places.

The critique found two things I missed: `blocked` was private with no reader, so R3 could not be
enforced through the model, and "free" in US-02 ignored blocked rooms. Its main High item was
wrong. It asked me to put BookingService and two repositories into the domain class diagram,
which is exactly what a domain model must not contain.
