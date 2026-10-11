# Review of the Smart Campus diagrams against the approved stories

## Summary

Coverage is good. All six stories map one-to-one to use cases, and nothing out of scope is modelled. R1–R4 appear in all three diagrams for US-01, so no rule is missing outright.

The real problems are between the class and sequence diagrams. They disagree about who enforces R2 and R3. The sequence also uses classes and operations that the class diagram doesn't contain. Fix N1 and M1 first, since they are linked. Then fix M2 and M4. The rest are low priority.

---

## Missing or incomplete rules

**M1. R3 cannot be checked through the class model (Medium)**
- **Where:** `class.puml`, `Room` has `- blocked : Boolean = false`. The attribute is private, and no operation reads it.
- **Problem:** Nothing outside `Room` can ask whether the room is blocked. So the note "no new Booking while blocked = true" has no operation that enforces it. The sequence works around this with `BookingRepository.isRoomBlocked`, which doesn't exist in the class diagram.
- **Fix:** Add `+ isBlocked() : Boolean` to `Room`. N1 then uses it.

**M2. "Free" in US-02 is not defined with respect to R3 (Medium)**
- **Where:** `class.puml`, `Room.isFreeAt(start, duration)`. Also `use-case.puml`, `UC_View`, which has no note.
- **Problem:** The diagrams don't say whether a blocked room counts as free. If `isFreeAt` checks only R2, "View room availability" will list blocked rooms. Book room will then reject them with `ROOM_BLOCKED`.
- **Fix:** Add this note on `Room`, or on `UC_View`: *"isFreeAt = not blocked AND no ACTIVE booking overlaps [start, start + duration)"*. This is an interpretation, because US-02 lists no rules in the approved set. Record it as a new assumption in `lab-report.md` rather than editing the story.

**M3. US-05 traces to R3, but Unblock room has no note (Low)**
- **Where:** `use-case.puml`, `UC_Unblock`. Only `UC_Block` mentions R3.
- **Fix:**
  ```plantuml
  note right of UC_Unblock
    US-05 / R3: once unblocked, new bookings are
    accepted again (still subject to R1, R2).
  end note
  ```

**M4. Assumptions A1, A2 and A6 are cited but not defined in the requirements (Medium, traceability)**
- **Where:** All three diagrams cite them: A1 on Block, A2 on the overlap notes, A6 on atomicity.
- **Problem:** The approved stories file defines only R1–R4. A reviewer reading the diagrams against that file can't tell what A1, A2 or A6 say.
- **Fix:**
  - Write each assumption out in `lab-report.md` and include it in the §7 consistency table next to the R rules.
  - If A3–A5 exist but aren't used in the diagrams, that's fine.
  - If they don't exist, renumber to A1–A3. I can't see your lab report, so I can't confirm which case applies.

---

## Inconsistent names and responsibilities

**N1. Class and sequence diagrams put R2 and R3 in different places (High)**
- **Where:**
  - In `class.puml`, R2 belongs to `Room.isFreeAt` and `Booking.overlaps`, and R3 belongs to `Room.blocked`.
  - In `sequence.puml`, R2 belongs to `BookingRepository.findActiveOverlapping`, and R3 belongs to `BookingRepository.isRoomBlocked`.
- **Problem:**
  - None of the sequence's participants or messages appears in the class diagram. That covers `BookingService`, `BookingRepository`, `bookRoom`, `validateTimeSlot`, `isRoomBlocked`, `findActiveOverlapping` and `save`.
  - Conversely, `isFreeAt` and `overlaps` are never called in the sequence.
  - A repository for bookings answering a question about rooms contradicts the class diagram, where `blocked` belongs to `Room`.
- **Fix:** Keep your service/repository design, because A6 needs somewhere to live. Make the class diagram contain it.

  Add to `class.puml`:
  ```plantuml
  class BookingService <<service>> {
    + bookRoom(studentId : String, roomId : String, start : DateTime, duration : Duration) : Confirmation
    - validateTimeSlot(start : DateTime, duration : Duration) : Boolean
  }
  class RoomRepository <<repository>> {
    + findById(roomId : String) : Room
  }
  class BookingRepository <<repository>> {
    + findActiveOverlapping(roomId : String, start : DateTime, duration : Duration) : Booking[*]
    + save(booking : Booking) : String
  }
  BookingService ..> RoomRepository
  BookingService ..> BookingRepository
  BookingService ..> Booking : <<create>>
  ```

  In `sequence.puml`, replace the `isRoomBlocked` call so that R3 is answered by `Room`. Declare `RR` and `R` before `BR` so the A6 note still spans all of them.
  ```plantuml
  participant "RoomRepository" as RR <<repository>>
  participant "room : Room" as R
  ...
  BS -> RR : findById(roomId)
  RR --> BS : room
  BS -> R : isBlocked()
  R --> BS : blocked
  ```

  Then tie the remaining domain operations in:
  - Extend Booking's R2 note with *"findActiveOverlapping returns the ACTIVE bookings b of the room where b.overlaps(start, duration)"*.
  - Keep `Room.isFreeAt` as the US-02 operation, defined as in M2.

**N2. Three different conventions for a time interval (Low)**
- **Where:**
  - `isFreeAt(start, duration)` and `overlaps(start, duration)`
  - `bookingsBetween(from, to)`
  - `findActiveOverlapping(roomId, start, start + duration)`
- **Fix:** Use `(start, duration)` for every booking slot, including `findActiveOverlapping(roomId, start, duration)` as in N1. Keep `(from, to)` only for `bookingsBetween`. There it describes a reporting period for US-06, not a booking, so the difference is justified.

**N3. Rejection code `ALREADY_BOOKED` doesn't name R2 (Low)**
- **Where:** `sequence.puml`, `rejected(ALREADY_BOOKED)`.
- **Problem:** R2 is about overlap. A partial overlap, such as 10:30–11:30 against 10:00–11:00, is rejected too, which the name hides.
- **Fix:** Rename it to `rejected(OVERLAPS_EXISTING_BOOKING)`. Each code then maps to one rule: `INVALID_TIME_SLOT` to R1, `ROOM_BLOCKED` to R3, and `OVERLAPS_EXISTING_BOOKING` to R2.

**N4. The returned confirmation doesn't match the `Confirmation` class (Low)**
- **Where:** The sequence returns `confirmation(code, bookingId, roomId, start, end)`. The class is `Confirmation { code, issuedAt }`.
- **Problem:** Most of the returned fields belong to `Booking`, and `issuedAt` is missing. The message looks like a different type.
- **Fix:** Return the object with `BS --> Student : confirmation : Confirmation`, which matches `bookRoom(...) : Confirmation` in N1. The booking details are reachable through the Booking–Confirmation association.

---

## Unjustified elements

**U1. Class members that no story or diagram uses (Low)**
- `Student.name`: No story needs a student's name, and registration is out of scope. Remove it, or justify it with a trace comment, for example if names are shown in the US-06 usage review.
- `Student.activeBookings()`: Nothing calls it. If it exists so a student can pick which booking to cancel, add `' US-03`. Otherwise remove it.
- `Confirmation.issuedAt`: R4 only requires that a confirmation exists. It's harmless, but it isn't traced to any rule.
- `Booking.overlaps(...)`: It is currently unused. The N1 note justifies it, so keep it only if you add that note.

**U2. The A6 atomic unit is only asserted (Optional)**
- **Where:** `sequence.puml`, `note over BS, BR`.
- **Fix:** Wrap the blocked check, the overlap query and `save` in `group atomic per room (A6)` … `end`. Readers can then see exactly which calls the guarantee covers.

---

## Already consistent (keep as is)

- There are six stories and six use cases, with no extra use cases and no out-of-scope features.
- The check order R1 → R3 → R2 → R4 is identical in the Book room note and the sequence.
- R4 is modelled as an outcome of Book room, not as a separate use case. That is correct.
- `BookingStatus {ACTIVE, CANCELLED}` supports both R2 ("active bookings") and US-03.
- The half-open interval and touching rule (A2) are stated identically in the class and sequence notes.
- All multiplicities are sensible, including the 1–1 link between Booking and Confirmation, since only successful requests create a Booking.

Would you like me to apply these edits to the three `.puml` files?