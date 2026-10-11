# Use-case diagram: Smart Campus study room booking

```plantuml
@startuml smart_campus_use_cases
title Smart Campus - Study Room Booking\nUse-case diagram

left to right direction
skinparam shadowing false

actor Student
actor Administrator

rectangle "Smart Campus Study Room Booking System" {
  usecase "View room availability\n<size:10>US-02</size>"            as UC_View
  usecase "Book study room\n<size:10>US-01 | R1, R2, R3, R4</size>"  as UC_Book
  usecase "Cancel own booking\n<size:10>US-03 | R2</size>"           as UC_Cancel
  usecase "Block room\n<size:10>US-04 | R3</size>"                   as UC_Block
  usecase "Unblock room\n<size:10>US-05 | R3</size>"                 as UC_Unblock
  usecase "Review room usage\n<size:10>US-06</size>"                 as UC_Review
}

' Student goals. Actor is written first so it is placed on the left.
Student -- UC_View
Student -- UC_Book
Student -- UC_Cancel

' Administrator goals. Use case is written first so the actor is placed on the right.
UC_Block   -- Administrator
UC_Unblock -- Administrator
UC_Review  -- Administrator

legend right
  <b>Business rules</b>
  R1  Future start; duration greater than 0 and at most 2 hours
  R2  Active bookings for the same room cannot overlap
  R3  A blocked room cannot accept a new booking
  R4  A successful booking produces a confirmation
endlegend
@enduml
```

I haven't rendered this here, so please check it in your PlantUML tool. The associations are plain lines, without arrowheads, because a UML actor association has no direction.

## Associations

| Actor | Use case | Story | Why this association |
|---|---|---|---|
| Student | View room availability | US-02 | The story's actor is a student. |
| Student | Book study room | US-01 | The story's actor is a student, and the student receives the confirmation (R4). |
| Student | Cancel own booking | US-03 | The story's actor is a student. Only the booking's owner cancels it. |
| Administrator | Block room | US-04 | The story's actor is an administrator. |
| Administrator | Unblock room | US-05 | The story's actor is an administrator. |
| Administrator | Review room usage | US-06 | The story's actor is an administrator. |

I left out some associations on purpose. No story lets an Administrator book, cancel or view availability, and no story lets a Student block, unblock or review usage.

## Why there is no «include» or «extend»

I looked for a clear reason to use each one and didn't find any:

| Candidate | Decision | Reason |
|---|---|---|
| Book «include» *Check booking rules* (R1–R3) | Rejected | The checks are internal steps of one use case, not a goal of any actor. Only Book uses them, so splitting them out would be functional decomposition. |
| Book «include» *Send confirmation* (R4) | Rejected | Only one use case needs it, and it happens on every successful booking. That makes it part of Book's success outcome, not a separate behaviour. |
| Book «extend» View availability (or the reverse) | Rejected | US-01 and US-02 are separate goals. A student can book without viewing first. "So that I can choose one before booking" explains the student's motive; it doesn't make one behaviour depend on the other. |
| Any use case «include» *Log in* | Rejected | Authentication isn't part of the scenario, and registration is explicitly out of scope. |

## Assumptions

1. **A1:** Users are already identified when they use the system, which is how "own" in US-03 can be enforced. Login and registration are outside the system boundary, so they aren't modelled.
2. **A2:** Administrator is not a specialised Student. There is no generalisation between them, because no story gives administrators any student goals.
3. **A3:** The system itself issues the confirmation (R4) to the Student. The scenario names no email or notification service, so there is no secondary actor. If your course expects one, you would add it to Book study room.
4. **A4:** Block and Unblock are two separate use cases rather than a single "Manage room status". They are separate stories (US-04 and US-05), and keeping them apart keeps the story IDs traceable.
5. **A5:** Unblock room only makes sense for a room that is currently blocked. That is a precondition, not a separate use case.
6. **A6:** Review room usage is read-only. The scenario doesn't say what the review contains, such as reports, periods or metrics, so I haven't modelled any detail.
7. **A7:** Blocking stops *new* bookings only (R3). The scenario doesn't say what happens to existing bookings for a blocked room. **This is an open question**, and it isn't shown in the diagram.
8. **A8:** No story lets an administrator cancel another user's booking, so that isn't modelled.
9. **A9:** Time passing, for example bookings that end and become inactive, isn't triggered by any actor, so there is no Time or Clock actor.

Ready for the next diagram.