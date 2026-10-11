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