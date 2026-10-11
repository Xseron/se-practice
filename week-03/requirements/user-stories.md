# User stories — Smart Campus study room booking

7 stories, reviewed against README section 1 (`lab-report.md` §3). Roles are **Student** or
**Administrator** only. Priorities were re-mapped from the assistant's MoSCoW labels
(Must → High, Should → Medium).

---

### US-01
**Story:** As a Student, I want to see which study rooms are free and at what times, so that I can choose a slot before I try to book.
**Priority:** High
**Assumption:** "Free" means no active booking overlaps the slot and the room is not blocked; a slot that starts exactly when another booking ends is shown as free (decision on R3 in `acceptance-criteria.md`).

### US-02
**Story:** As a Student, I want to reserve a free room for a time slot, so that I have a guaranteed place to study at that time.
**Priority:** High
**Assumption:** A booking of exactly two hours is allowed under R2; only bookings longer than two hours are rejected.

### US-03
**Story:** As a Student, I want to cancel a booking I made, so that the room is released for other students when I no longer need it.
**Priority:** Medium
**Assumption:** A student can cancel only their own booking, and the cancelled slot becomes free immediately.

### US-04
**Story:** As a Student, I want to receive a confirmation when my booking or cancellation succeeds, so that I know for certain whether the room is reserved for me.
**Priority:** Medium
**Assumption:** The system sends exactly one confirmation per successful booking or cancellation (UC-06) and no other messages, such as reminders.

### US-05
**Story:** As an Administrator, I want to block a room, so that students cannot book a room that is out of service.
**Priority:** High
**Assumption:** Blocking stops new bookings (R4) but does not cancel bookings that already exist for that room.

### US-06
**Story:** As an Administrator, I want to unblock a room, so that students can book it again once it is usable.
**Priority:** High
**Assumption:** An unblocked room can be booked immediately, subject to R1–R3 like any other room.

### US-07
**Story:** As an Administrator, I want to review how each room was used over a period I choose, so that I can see which rooms are in demand and which are underused.
**Priority:** Medium
**Assumption:** Usage is counted only from bookings that were not cancelled; it does not show whether students actually came, because attendance is out of scope.
