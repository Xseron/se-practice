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