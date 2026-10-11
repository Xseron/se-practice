# Review: registration sequence and domain models

## Verdict

Both models meet R1–R5 and all six acceptance criteria. All four validation cases follow the correct path, and no rule is broken. I found four genuine defects, all low severity: one traceability gap and three notation errors. None of them changes behaviour. Several further points are optional design choices.

## Validation cases

| Case | AC | Path through the models | Result |
|---|---|---|---|
| Available places | AC-03 (AC-01 and AC-02 for browsing) | `hasEnrollmentFor(Lena)` = false and `availablePlaces()` = 2 − 0 = 2, so the third branch runs. One `«create»` happens, the count goes from 0 to 1, 1 place is left, and `confirmed(e)` is returned. C1 holds (1 ≤ 2). When browsing, SE-201 shows 2 − 0 = 2. MA-110 shows 20 − 20 = 0 and is still listed because the loop has no filter. Browsing sends no message that changes state. | Pass |
| Exactly one place | AC-04 | A single request sees free = 1, takes the third branch, and the count goes from 1 to 2 with 0 places left. C1 still holds (2 ≤ 2). With two concurrent requests, the atomic region runs the two `enroll()` calls one after the other. The second sees free = 0 and gets "course full" with nothing created. The guards `free = 0` and `free > 0` split exactly at the boundary, so there is no off-by-one error. | Pass (concurrency is described in a note, which your brief allows) |
| Full after stale view | AC-05 | `register(student, chosen)` carries no place count from the catalog, so the stale "1" cannot affect the decision. `enroll()` recomputes free = 2 − 2 = 0. Mira is not enrolled, so she gets "course full", nothing is created and the count stays 2. | Pass |
| Duplicate | AC-06 | `hasEnrollmentFor(Lena)` = true, so the first branch returns "already enrolled" even though free = 1. Nothing is created, the count stays 1 and C3 holds. If the request is both a duplicate and for a full offering, the first branch still wins (A4). If the same student submits twice at once, the atomic region makes the second request see `alreadyEnrolled` (A3). | Pass |

**What is correct:**
- **Message order:**
  - Browsing never changes state (A1, AC-02).
  - The duplicate check, the capacity recheck, the decision and the creation all happen inside the atomic region.
  - The reply is sent only after the decision.
- **Guards:**
  - The three branches cover every case and never overlap, because C1 guarantees free ≥ 0.
  - Writing `not alreadyEnrolled` into the second and third guards enforces A4.
- **State changes:**
  - Only the success branch changes state, as R5 requires.
  - Availability is derived rather than stored, so creating `e` is the availability update (R4, A2).
- **Multiplicities:**
  - All four associations are 1 to 0..*.
  - The capacity limit is expressed in C1 rather than as a multiplicity, which is correct because capacity differs per offering.
- **OCL:**
  - C1 is valid.
  - In C3, `enrollments->isUnique(student)` uses the implicit iterator and the `student` role name, both of which exist.
- **Naming:**
  - The rejection reasons match R5 word for word.
  - The example data matches A7.
  - The role names used in the OCL exist in the diagram.

## Genuine defects

**D1. C4 relies on an assumption you have not approved.**
- **Rule and element:** No rule requires it; the closest is R1 / AC-01. The element is the CourseOffering note, "C4 Offering identity (assumption)".
- **Impact:** Every other constraint traces to R1–R5 or A1–A7. C4 cites an unnumbered assumption that is not on your approved list, so it is an untraced rule added to the model. No AC depends on it.
- **Fix:** Either delete C4, or submit it for approval as A8 ("an offering is identified by course, semester and section, so catalog entries can be told apart") and cite A8. If you keep it, state it formally:
  ```
  context Semester
  inv: offerings->forAll(a, b | a <> b and a.course = b.course
                               implies a.section <> b.section)
  ```
  This needs the role name `offerings` (see O3). Without it, the OCL default name `courseOffering` applies.

**D2. The guards contain traceability tags.**
- **Rule and element:** R2, R3, R5 and A4; the three `alt`/`else` branches in the sequence diagram.
- **Impact:** PlantUML puts the whole label inside the guard brackets. For example, `[alreadyEnrolled (R3, R5; AC-06)]` reads like an operation call with arguments, and `free = 0 (R2, …)` reads like `0(...)`. The conditions themselves are correct, but the guards are no longer clean boolean expressions.
- **Fix:** Keep only the boolean condition in each guard and move the mapping into the existing atomic note:
  ```
  alt alreadyEnrolled
  else not alreadyEnrolled and free = 0
  else not alreadyEnrolled and free > 0
  ```
  Add this line to the note: *"Branch 1 → R3, R5 (AC-06); 2 → R2, R5 (AC-05, AC-04 second request); 3 → R2, R4 (AC-03, AC-04 first request)."*

**D3. The loop sends its messages to the collection, not to each offering.**
- **Rule and element:** R1 and A2; the `loop` block, the `collections "offerings : CourseOffering"` lifeline, `catalogEntry()` and the self-call `availablePlaces()`.
- **Impact:** In UML, a message to a collection lifeline goes to the collection object itself. The diagram therefore says the collection computes "capacity − number of enrollments". C2 and A2 define that value per offering, and the 2-versus-0 result in AC-01 depends on exactly that.
- **Fix:** Add a lifeline for the element and remove the `collections` lifeline. `offerings` remains only as the reply to `getOfferings()`.
  ```
  entity "offerings[i] : CourseOffering" as Oi
  loop for each offering of the semester
    Ctrl -> Oi : catalogEntry()
    activate Oi
    Oi -> Oi : availablePlaces()\n= capacity - number of enrollments
    Oi --> Ctrl : course code, title, section, available places
    deactivate Oi
  end
  ```

**D4. `{unique}` is used to mean "key".**
- **Rule and element:** R1 and the catalog lookup; `Student.studentId`, `Course.code` and `Semester.name`.
- **Impact:** In UML, `{unique}` applies only to multi-valued elements: it means no duplicate values within one object's collection. On a single-valued attribute it says nothing. The intended rule, that no two semesters share a name, is therefore never stated. `getCatalog("Autumn 2026")` depends on that rule.
- **Fix:** Use `{id}` (for example `name : String {id}`), or write OCL such as `context Semester inv: Semester.allInstances()->isUnique(name)`.

## Optional design choices

- **O1 – Atomic fragment (R2, A3).** You could replace `group atomic […]` with `critical […]`. That is UML's standard operator for a region that nothing else may interleave with, and PlantUML supports it. Your brief accepts the note, so this is optional.
- **O2 – Stale view (R2, A1, AC-05).** You could add `... other students may register; the catalog view reserves nothing (A1) ...` between the two sections. That would show the stale interval in the flow itself, not only in a note.
- **O3 – Role names (R1).** The sequence diagram already uses `getOfferings()` and `offerings`, but the Course and Semester associations have no role names. Code and title belong to Course, so the reply from `catalogEntry()` really means `course.code, course.title, …`. You could add the role names `course`, `semester` and `offerings`. OCL default names work without them, so this is optional.
- **O4 – Semester lookup (R1).** The controller receives the string "Autumn 2026" but then messages `autumn2026` without any step that finds that object. You could add `Ctrl -> Ctrl : autumn2026 := findSemester("Autumn 2026")`. Leaving it out is an acceptable shortcut in an instance-level diagram.
- **O5 – Create and add (R4).** `«create»(student, chosen)` already links `e` to both the student and the offering. The extra step "add e to enrollments" shows only the offering's side, so it could be read as a second, one-sided state change. You could remove it and move "availablePlaces drops by 1" into the note.
- **O6 – `registeredAt` (no rule).** No rule or AC requires this attribute, and the `«create»` message never sets it. Remove it, or keep it and pass it in `«create»`.
- **O7 – Association class (R3).** Modelling Enrollment as an association class between Student and CourseOffering would enforce R3 through the structure itself. Your current class plus C3 is equally correct and easier to read, so I would keep it.
- **O8 – Operations (R2, A3).** The domain model shows none of the operations the sequence diagram uses, such as `enroll` and `hasEnrollmentFor`. That is normal for a domain model. Add `enroll(student)` to CourseOffering only if the assignment expects a design class diagram.
- **O9 – Small fixes:**
  - The constraint labels run C1, C2, C4, C3; renumber them in order.
  - `capacity > 0` appears three times; keep the formal statement and the precondition.
  - Write C2 as `context CourseOffering::availablePlaces : Integer derive: capacity - enrollments->size()`.
  - In the Enrollment note, cite A3 instead of "see the sequence diagram".
  - In the AC-01 note, write "SE-201 Section A" rather than "SE-201 … A".

I reviewed the PlantUML source without rendering it. The point in D2 about how guards are displayed is based on PlantUML's standard behaviour of wrapping `alt` and `else` labels in brackets.