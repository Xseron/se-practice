## Sequence diagram

```plantuml
@startuml registration_sequence
title Browse catalog and register for a course offering (R1–R5)
hide footbox
autonumber

actor "Student\n(signed in)" as S
boundary ":RegistrationUI" as UI
control ":RegistrationController" as Ctrl
entity "autumn2026 : Semester" as Sem
collections "offerings : CourseOffering" as Offs
entity "chosen : CourseOffering" as Off

note over S, Off
  Preconditions: the student is signed in, the chosen offering exists and
  its capacity is a positive whole number. "chosen" is one of the listed offerings.
  Example run: Lena Ortiz (ST-1001) browses Autumn 2026 and chooses SE-201 Section A.
end note

== Browse the catalog (R1, US-01) ==

S -> UI : viewCatalog("Autumn 2026")
activate UI
UI -> Ctrl : getCatalog("Autumn 2026")
activate Ctrl
Ctrl -> Sem : getOfferings()
activate Sem
Sem --> Ctrl : offerings
deactivate Sem

loop for each offering of the semester
  Ctrl -> Offs : catalogEntry()
  activate Offs
  Offs -> Offs : availablePlaces()\n= capacity - number of enrollments
  Offs --> Ctrl : course code, title, section, available places
  deactivate Offs
end

Ctrl --> UI : catalog entries
deactivate Ctrl
UI --> S : one entry per offering
deactivate UI

note over S, Ctrl
  AC-01: SE-201 "Software Requirements" A shows 2;
  MA-110 "Discrete Structures" A shows 0 (full but still listed, A6).
  Viewing reserves no place (A1, AC-02), so the number shown may be stale.
end note

== Request registration (R2–R5, US-02, US-03) ==

S -> UI : requestRegistration(chosen)
activate UI
UI -> Ctrl : register(student, chosen)
activate Ctrl

group atomic [final checks + creation, one operation per offering]
  Ctrl -> Off : enroll(student)
  activate Off

  note over Ctrl, Off
    One atomic operation per offering (A3): the duplicate check, the capacity
    recheck and the creation run with no other enroll() on this offering in between.
    AC-04: if Tomas and Mira compete for the last place, whichever runs second
    sees free = 0 and gets "course full". If one student submits twice, the second
    request sees alreadyEnrolled. The duplicate check takes precedence (A4).
    Rejections create nothing and leave the count unchanged (R5).
  end note

  Off -> Off : alreadyEnrolled := hasEnrollmentFor(student)
  Off -> Off : free := availablePlaces()

  alt alreadyEnrolled (R3, R5; AC-06)
    Off --> Ctrl : rejected("already enrolled")
  else not alreadyEnrolled and free = 0 (R2, R5; AC-05, AC-04 second request)
    Off --> Ctrl : rejected("course full")
  else not alreadyEnrolled and free > 0 (R2, R4; AC-03, AC-04 first request)
    create entity "e : Enrollment" as Enr
    Off -> Enr : «create»(student, chosen)
    Off -> Off : add e to enrollments\n(availablePlaces drops by 1)
    note right of Enr
      No stored counter (A2): creating e
      is the availability update.
      AC-03: 0 -> 1 enrollment, 1 place left.
    end note
    Off --> Ctrl : confirmed(e)
  end

  deactivate Off
end

Ctrl --> UI : outcome
deactivate Ctrl
UI --> S : confirmation, or reason\n"already enrolled" / "course full"
deactivate UI

@enduml
```

## Domain class diagram

```plantuml
@startuml registration_domain
title Domain model: course registration (R1–R5)
hide circle
hide empty methods
skinparam classAttributeIconSize 0

class Student {
  studentId : String {unique}
  name : String
}

class Course {
  code : String {unique}
  title : String
}

class Semester {
  name : String {unique}
}

class CourseOffering {
  section : String
  capacity : Integer {capacity > 0}
  /availablePlaces : Integer
}

class Enrollment {
  registeredAt : DateTime
}

Course "1" -- "0..*" CourseOffering : is scheduled as >
Semester "1" -- "0..*" CourseOffering : offers >
CourseOffering "offering\n1" -- "enrollments\n0..*" Enrollment
Student "student\n1" -right- "enrollments\n0..*" Enrollment

note right of Semester
  Catalog (R1) is a view of one Semester's offerings:
  course code, title, section and /availablePlaces.
  It is derived on request, not stored, and reserves nothing (A1).
  Full offerings stay listed with 0 places (A6).
end note

note right of CourseOffering
  <b>C1 Capacity (R2)</b>
  context CourseOffering
  inv: capacity > 0
  inv: enrollments->size() <= capacity

  <b>C2 Derived availability (R1, R4, A2)</b>
  /availablePlaces = capacity - enrollments->size()
  so 0 <= availablePlaces <= capacity

  <b>C4 Offering identity (assumption)</b>
  (course, semester, section) is unique
end note

note bottom of Enrollment
  <b>C3 Uniqueness (R3)</b>
  context CourseOffering
  inv: enrollments->isUnique(student)
  At most one Enrollment per (Student, CourseOffering) pair.
  Nothing is required across sections of one course (A5).

  C1 and C3 are checked, and the Enrollment is created,
  in one atomic operation per offering (see the sequence
  diagram), so concurrent requests cannot violate them.
end note

@enduml
```

## Constraints

- **C1 Capacity (R2):** `capacity > 0`, and an offering never has more Enrollments than its capacity.
- **C2 Derived availability (A2):** `availablePlaces = capacity − number of Enrollments`. It always stays between 0 and capacity. It is never stored, so creating an Enrollment is the update R4 asks for.
- **C3 Uniqueness (R3):** a student has at most one Enrollment per offering. A repeat request is rejected with "already enrolled".
- **Enforcement:** both C1 and C3 are guaranteed by the atomic `enroll()` on the offering. Every Enrollment links exactly one Student and one CourseOffering (the 1-multiplicities, R4).

## Assumptions and modelling decisions

Beyond your approved A1–A7, I made these choices:

1. **The atomic operation belongs to `CourseOffering.enroll()`.** The offering owns its capacity and its Enrollments, so it is the natural boundary for "one operation per offering" (A3). How the operation is made atomic (locks, transactions) is left out, as you specified.
2. **There are three branches with mutually exclusive guards.** Both values are read inside the atomic group. The guards include "not alreadyEnrolled", so a repeat request for a full offering gets "already enrolled" (A4).
3. **The reply is outside the atomic group.** Only the checks and the creation are atomic. The single `outcome` reply carries the confirmation or the reason, and how it is delivered is out of scope.
4. **Concurrency is shown as a note, not a second actor.** Using one generic Student keeps the diagram readable. AC-04 and the double-submit case are explained in the atomic note. A `par` fragment with Tomas and Mira would be an alternative if your course expects one.
5. **Catalog is not a class.** It is the derived view of one Semester's offerings and holds no state. Course code and title come through the offering's link to its Course.
6. **Enrollment is a class of its own, not a UML association class.** This makes C3 an explicit constraint rather than leaving it implied by association-class semantics.
7. **Some attributes are not required by R1–R5:** `Student.name`, `Enrollment.registeredAt` and the C4 identity of (course, semester, section). I added them because they are useful for identification and confirmation, but you can drop them.
8. **The domain model has no operations.** `enroll()`, `availablePlaces()` and `hasEnrollmentFor()` in the sequence diagram are responsibilities given to CourseOffering at design level.

## Technical lifelines

- **`:RegistrationUI` (boundary):** the interface the student uses. It forwards requests and shows the catalog and the outcome. It contains no business rules.
- **`:RegistrationController` (control):** coordinates the use case. It identifies the signed-in student and the chosen offering, gets the semester's offerings, hands the atomic `enroll()` to the offering and passes the result back. It holds no business state and performs no checks itself, so R2–R5 stay in the domain.

Neither appears in the class diagram because they are not domain concepts. For a black-box view, both can be merged into a single `:RegistrationSystem` lifeline. The other lifelines (Semester, the `offerings` multi-object, the chosen CourseOffering and the created Enrollment) are domain objects.

I haven't rendered the diagrams here; the syntax is standard PlantUML (`create`, `group`, `collections`, creole notes).