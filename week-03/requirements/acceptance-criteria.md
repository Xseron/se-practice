# Acceptance criteria — three selected stories

Assumptions first, then the criteria. Each block names the story it belongs to. Reviewed from the
assistant's output (`lab-report.md` §4–§5): one action and one observable result per criterion,
every rule R1–R4 has its own rejection case, and nothing about screens, databases or classes.

---

## Assumptions

These settle the two questions the scenario leaves open.

- **Overlap:** a booking that ends exactly when another begins is **allowed** under R3 (not an overlap), because a booking covers its start up to, but not including, its end — 12:00–14:00 and 14:00–15:00 share no minute.
- **Duration:** a booking of exactly two hours is **allowed** under R2, because R2 says "at most two hours"; one minute more is rejected.
- **Future start (R1):** the start must be strictly later than the current time; a start equal to the current time is rejected.
- **Time slot:** the end must be after the start. The scenario defines no slot size or opening hours, so none are enforced.
- **Active bookings:** only active (not cancelled) bookings count for R3.
- **Rejected** means: no booking is created or changed, and no confirmation (UC-06) is sent.
- **Blocking (R4):** blocking stops new bookings only; existing bookings for that room are kept. What should happen to them is an open question for the product owner.
- **Identity:** the system knows which Student made each booking. How it knows is out of scope (authentication is excluded in README section 1).
- Room numbers and dates below are fictional examples.

---

## US-02 — Book room

### AC-01
- **Given** the current time is 2026-10-12 10:00, room R-101 is not blocked, and R-101 has one active booking on 2026-10-14 from 12:00 to 14:00
- **When** the Student books R-101 on 2026-10-14 from 14:00 to 16:00
- **Then** the booking is created for that Student and the Student receives a booking confirmation (UC-06)

### AC-02
- **Given** the current time is 2026-10-12 10:00 and room R-101 is not blocked and has no bookings that day
- **When** the Student books R-101 on 2026-10-12 from 10:00 to 11:00
- **Then** the request is rejected because the start is not in the future (R1), and no booking is created

### AC-03
- **Given** the current time is 2026-10-12 10:00 and room R-101 is not blocked and has no bookings on 2026-10-14
- **When** the Student books R-101 on 2026-10-14 from 14:00 to 16:01
- **Then** the request is rejected because the booking is longer than two hours (R2), and no booking is created

### AC-04
- **Given** the current time is 2026-10-12 10:00, room R-101 is not blocked, and R-101 has an active booking on 2026-10-14 from 14:00 to 15:00
- **When** the Student books R-101 on 2026-10-14 from 14:15 to 14:45
- **Then** the request is rejected because it overlaps an existing booking of the same room (R3), and no booking is created

### AC-05
- **Given** the current time is 2026-10-12 10:00, room R-101 is blocked, and R-101 has no bookings on 2026-10-14
- **When** the Student books R-101 on 2026-10-14 from 14:00 to 15:00
- **Then** the request is rejected because the room is blocked (R4), and no booking is created

---

## US-03 — Cancel booking

### AC-06
- **Given** the current time is 2026-10-12 10:00 and Student A has an active booking for R-101 on 2026-10-14 from 14:00 to 15:00
- **When** Student A cancels that booking
- **Then** the booking is cancelled and Student A receives a cancellation confirmation (UC-06)

### AC-07
- **Given** Student A's booking for R-101 on 2026-10-14 from 14:00 to 15:00 has been cancelled, R-101 is not blocked, and the current time is 2026-10-12 10:00
- **When** Student B books R-101 on 2026-10-14 from 14:00 to 15:00
- **Then** the booking is created for Student B, because a cancelled booking does not count for R3

### AC-08
- **Given** Student B has an active booking for R-101 on 2026-10-14 from 14:00 to 15:00
- **When** Student A tries to cancel that booking
- **Then** the request is rejected because the booking belongs to another Student, and Student B's booking stays active

### AC-09
- **Given** Student A's booking for R-101 on 2026-10-14 from 14:00 to 15:00 is already cancelled
- **When** Student A cancels that booking again
- **Then** the request is rejected because the booking is already cancelled, and no second confirmation is sent

---

## US-05 — Block room

### AC-10
- **Given** room R-101 is not blocked
- **When** the Administrator blocks R-101
- **Then** R-101 is blocked, and a later request by a Student to book R-101 is rejected under R4, as in the blocked-room criterion of US-02

### AC-11
- **Given** room R-101 is not blocked and Student A has an active booking for R-101 on 2026-10-14 from 14:00 to 15:00
- **When** the Administrator blocks R-101
- **Then** R-101 is blocked and Student A's booking stays active and unchanged

### AC-12
- **Given** room R-101 is already blocked
- **When** the Administrator blocks R-101 again
- **Then** R-101 stays blocked, nothing else changes, and the Administrator is told the room was already blocked
