# Revised UML sources: registration sequence and domain model

## models/original/sequence.puml

```plantuml
@startuml registration_sequence
title Browse catalog and register for a course offering (R1–R5)
hide footbox
autonumber

actor "Student" as S
boundary ":RegistrationUI" as UI
control ":RegistrationController" as Ctrl
collections "offerings : CourseOffering" as Offs
entity "offering : CourseOffering" as Offering
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
Ctrl -> Offs : getOfferings("Autumn 2026")
activate Offs
Offs --> Ctrl : offerings
deactivate Offs

loop for each offering of the semester
  Ctrl -> Offering : catalogEntry()
  activate Offering
  Offering -> Offering : availablePlaces() := capacity - number of enrollments
  Offering --> Ctrl : course code, title, section, available places
  deactivate Offering
end

Ctrl --> UI : catalog entries
deactivate Ctrl
UI --> S : one entry per offering
deactivate UI

note over S, Ctrl
  AC-01: SE-201 "Software Requirements" Section A shows 2;
  MA-110 "Discrete Structures" Section A shows 0 (full but still listed, A6).
  Viewing reserves no place (A1, AC-02), so the number shown may be stale.
end note

...other students may register meanwhile; the catalog view reserved nothing (A1)...

== Request registration (R2–R5, US-02, US-03) ==

S -> UI : requestRegistration(chosen)
activate UI
UI -> Ctrl : register(student, chosen)
activate Ctrl

critical atomic: final checks + creation, one operation per offering
  Ctrl -> Off : enroll(student)
  activate Off

  note over Ctrl, Off
    One atomic operation per offering (A3): the duplicate check, the capacity
    recheck and the creation run with no other enroll() on this offering in between.
    Guards are checked in this order; the duplicate check comes first (A4):
    "already enrolled": R3, R5; AC-06.
    "not enrolled and course full (free = 0)": R2, R5; AC-05, AC-04 second request.
    "not enrolled and places left (free > 0)": R2, R4; AC-03, AC-04 first request.
    AC-04: if Tomas and Mira compete for the last place, whichever runs second
    sees free = 0 and gets "course full". If one student submits twice, the second
    request sees alreadyEnrolled.
    Rejections create nothing and leave the count unchanged (R5).
  end note

  Off -> Off : alreadyEnrolled := hasEnrollmentFor(student)
  Off -> Off : free := availablePlaces()

  alt already enrolled
    Off --> Ctrl : rejected("already enrolled")
  else not enrolled and course full (free = 0)
    Off --> Ctrl : rejected("course full")
  else not enrolled and places left (free > 0)
    create entity "e : Enrollment" as Enr
    Off -> Enr : «create»(student, chosen)
    Off -> Off : update availability: enrollment count + 1, availablePlaces - 1
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

## models/original/classes.puml

```plantuml
@startuml registration_domain
title Domain model: course registration (R1–R5)
hide circle
hide empty methods
skinparam classAttributeIconSize 0

class Student {
  studentId : String {id}
  name : String
}

class Course {
  code : String {id}
  title : String
}

class CourseOffering {
  semester : String
  section : String
  capacity : Integer {capacity > 0}
  /availablePlaces : Integer
  enroll(student : Student)
}

class Enrollment

Course "1" -- "0..*" CourseOffering : is scheduled as >
CourseOffering "1" -- "0..*" Enrollment : receives >
Student "1" -- "0..*" Enrollment : holds >

note left of CourseOffering
  Catalog (R1) is a view of the offerings of one semester,
  selected by the semester value: course code, title,
  section and /availablePlaces.
  It is derived on request, not stored, and reserves nothing (A1).
  Full offerings stay listed with 0 places (A6).
end note

note right of CourseOffering
  <b>C1 Capacity (R2)</b>
  context CourseOffering
  inv: capacity > 0
  inv: enrollment->size() <= capacity

  <b>C2 Derived availability (R1, R4, A2)</b>
  context CourseOffering::availablePlaces : Integer
  derive: capacity - enrollment->size()
  With C1: 0 <= availablePlaces <= capacity
end note

note bottom of Enrollment
  <b>C3 Uniqueness (R3)</b>
  context CourseOffering
  inv: enrollment->isUnique(student)
  At most one Enrollment per (Student, CourseOffering) pair.
  Nothing is required across sections of one course (A5).

  C1 and C3 are checked, and the Enrollment is created,
  in one atomic operation per offering (A3), so concurrent
  requests cannot violate them.
end note

@enduml
```

## Change log

**Sequence diagram**
- **M3:** The actor is now "Student", the same name as the class. "Signed in" stays in the precondition note.
- **M1:** I removed the Semester lifeline. The controller now sends `getOfferings("Autumn 2026")` to the offerings collection. The collection only answers that selection.
- **D3:**
  - `catalogEntry()` now goes to a new lifeline "offering : CourseOffering", with no `[i]` selector.
  - Its self-call is on one line, so no label line starts with "=". This fixes the heading problem you saw in the render.
- **O9:** The AC-01 note now says "Section A". I applied this to MA-110 as well as SE-201, because AC-01 uses that wording for both.
- **O2:** I added a delay (`...`) between the browse section and the request section. It says other students may register meanwhile and the catalog view reserved nothing (A1).
- **O1:** `group atomic [...]` is now `critical atomic: final checks + creation, one operation per offering`. The atomic note is kept.
- **D2:**
  - The three guards are plain conditions, in the order you gave.
  - Their rule and AC tags moved into the atomic note, one line per guard.
  - The A4 precedence sentence now introduces those lines.
- **O5 (rejected, relabel only):** The self-message after the create now reads "update availability: enrollment count + 1, availablePlaces - 1".

**Class diagram**
- **M1:** I removed the Semester class and its "offers >" association. CourseOffering gets `semester : String`.
- **D4:** `{unique}` is replaced by `{id}` on `Student.studentId` and `Course.code`.
- **O6:** I removed `Enrollment.registeredAt`.
- **O8:** I added only `enroll(student : Student)` to CourseOffering.
- **D1:** I deleted C4.
- **O9:**
  - C2 is in OCL derive form.
  - I moved its bound line out of the OCL into a prose line ("With C1: …") so it does not read as part of the derive expression.
  - The labels now run C1, C2, C3 in reading order.
  - The Enrollment note cites A3.
- **M2:**
  - Every multiplicity is a plain "1" or "0..*".
  - The associations are named "receives >" (CourseOffering to Enrollment) and "holds >" (Student to Enrollment).
  - I dropped `-right-`.
  - The OCL uses the default end names `enrollment` and `student`.

**Kept unchanged by decision:**
- The browse flow.
- `enroll()` on "chosen" as the atomic boundary.
- Reading alreadyEnrolled and free inside the critical region.
- The three replies from the offering and the single outcome reply outside the region.
- Derived availability, C1, C3, and the A2/AC-03 note at the create.

O3, O4 and O7 led to no edits. Scope, R1–R5, A1–A7, AC-01–AC-06 and the C1–C3 IDs are all preserved.

## Flags
1. **Catalog note (my interpretation of M1):** The old Semester note still carries R1, A1 and A6 content. So I moved it to CourseOffering instead of deleting it with the class. Delete it if you meant it to go with Semester.
2. **Critical label shown in brackets:** PlantUML normally prints the text after `critical` in brackets, as it did with the guards. It may therefore look like a guard, although it is only a label. Please check the render.
3. **Empty Enrollment compartment:** After O6, Enrollment has no attributes. Since only `hide empty methods` is set, PlantUML will draw an empty attribute compartment. This is valid UML; `hide empty members` would remove it, but I have not applied that.
4. **Not rendered or saved:** I have not rendered these blocks or written them to disk. Please re-render to confirm the D2 and D3 fixes.