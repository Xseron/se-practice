# Course Registration: User Stories and Acceptance Criteria

## Fictional Test Data

| Element | Values |
|---|---|
| Students | Lena Ortiz (ST-1001), Tomas Reyes (ST-1002), both signed in |
| Semester | Autumn 2026 |
| Courses | SE-201 "Software Requirements", MA-110 "Discrete Structures" |
| Offerings | SE-201 Section A (capacity 30), SE-201 Section B (capacity 25), MA-110 Section A (capacity 20) |

**Terms:** *Enrollment count* means the number of Enrollments for one offering. *Available places* means capacity minus enrollment count (A3).

## Review of Your Assumptions

| ID | Assumption | Analyst comment |
|---|---|---|
| A1 | No waiting list; full means rejected, nothing queued | Matches the exclusions and R5. |
| A2 | Catalog view reserves nothing; the shown number may be stale | Matches the scenario. This is why R2 requires a recheck. |
| A3 | Available places = capacity − Enrollments | Consistent with R1, R2 and R4. Because cancellation is excluded, every Enrollment counts. |
| A4 | Two students racing for the last place; only one wins | Matches R2. **I suggest extending it** to cover the duplicate check too. One student sending the same request twice at once could otherwise get two Enrollments, which would break R3. |

## User Stories and Acceptance Criteria

### US-01: Browse the course catalog
**As a** student, **I want** to see the offerings of one semester with their available places, **so that** I can choose an offering to register for.

**AC-01: Catalog shows required fields per offering** (R1)
- **Given** semester Autumn 2026 has the offerings SE-201 Section A, SE-201 Section B and MA-110 Section A
- **When** Lena views the catalog for Autumn 2026
- **Then** each offering is listed as a separate entry showing its course code, course title, offering (section) and available places
- **And** SE-201 Section A and SE-201 Section B appear as two entries for the same course

**AC-02: Available places are derived, and viewing reserves nothing** (R1; supports A2, A3)
- **Given** SE-201 Section A has capacity 30 and 28 Enrollments
- **When** Lena views the catalog
- **Then** SE-201 Section A shows 2 available places
- **And** the enrollment count remains 28 and no place is held for Lena

### US-02: Register for an offering with a free place
**As a** student, **I want** to request registration for a chosen offering, **so that** I receive a confirmed place in it.

**AC-03: Successful registration** (R2, R4)
- **Given** SE-201 Section A has capacity 30 and 28 Enrollments, and Lena has no Enrollment in it
- **When** Lena requests registration for SE-201 Section A
- **Then** current availability is rechecked at the time of the request
- **And** exactly one Enrollment linking Lena and SE-201 Section A is created
- **And** the enrollment count becomes 29 and available places become 1
- **And** Lena receives a confirmation

**AC-04: Competing requests for the last place** (R2, R4, R5; A4)
- **Given** SE-201 Section B has capacity 25 and 24 Enrollments, and neither Lena nor Tomas has an Enrollment in it
- **When** Lena and Tomas request registration for SE-201 Section B at almost the same moment
- **Then** exactly one request succeeds and creates one Enrollment, and that student receives a confirmation
- **And** the other request is rejected with "course full" and creates no Enrollment
- **And** the final enrollment count is 25, never 26

### US-03: Understand why registration was rejected
**As a** student, **I want** a clear reason when my registration is rejected, **so that** I know nothing was recorded and why.

**AC-05: Offering became full after the catalog was viewed** (R2, R5; A1, A2)
- **Given** Tomas saw 1 available place for MA-110 Section A in the catalog
- **And** that place was then taken, so MA-110 Section A now has capacity 20 and 20 Enrollments
- **And** Tomas has no Enrollment in MA-110 Section A
- **When** Tomas requests registration for MA-110 Section A
- **Then** the request is rejected with the reason "course full"
- **And** no Enrollment is created, the enrollment count remains 20, and the request is not queued

**AC-06: Repeat request for the same offering** (R3, R5)
- **Given** Lena already has an Enrollment in SE-201 Section A, which has capacity 30 and 29 Enrollments
- **When** Lena requests registration for SE-201 Section A again
- **Then** the request is rejected with the reason "already enrolled"
- **And** no Enrollment is created, the enrollment count remains 29, and Lena still has exactly one Enrollment in SE-201 Section A

*AC-06 deliberately leaves free places, so "already enrolled" is the only reason that applies (see U-01).*

## Atomic Operation Note

**RegisterForOffering(student, offering)** is a single indivisible operation:

1. **Duplicate check:** if the student already has an Enrollment in this offering, reject with "already enrolled".
2. **Capacity check:** if the enrollment count is greater than or equal to capacity, reject with "course full".
3. **Create** one Enrollment linking the student and the offering. Available places therefore drop by 1.
4. **Return** a confirmation.

Either all steps take effect or none do. Requests for the same offering are handled one after another, so each request's checks see every earlier successful Enrollment. Two invariants must always hold:
- **Capacity:** for every offering, the enrollment count is at most its capacity.
- **No duplicates:** for every student and offering pair, there is at most one Enrollment.

The order of steps 1 and 2 is not fixed by the rules (see U-01).

## Traceability

| Rule | Acceptance criteria |
|---|---|
| R1 Catalog | AC-01, AC-02 |
| R2 Capacity | AC-03, AC-04, AC-05 |
| R3 Duplicates | AC-06 |
| R4 Success | AC-03, AC-04 |
| R5 Rejection | AC-04, AC-05, AC-06 |

## Uncertainties (to confirm with stakeholders)

| ID | Question | Why it matters |
|---|---|---|
| U-01 | If a student is already enrolled **and** the offering is full, which reason is shown? | R5 defines both reasons but no precedence. This decides the check order in the atomic operation. |
| U-02 | May a student enroll in two different offerings of the **same course** (e.g., SE-201 Sections A and B)? | R3 only forbids repeats of the same offering. The rules are silent here, so no policy was assumed. |
| U-03 | If the same student sends two simultaneous requests, should the second always get "already enrolled"? | This depends on extending A4 to the duplicate check (see the assumption review). |
| U-04 | Is "available places" stored or always calculated? | R4 says "update availability". If it is calculated (A3), the update is implicit. If it is stored, it must change in the same atomic step. |
| U-05 | Are full offerings listed with 0 available places, or hidden? | R1 does not say. |
| U-06 | How is the one semester chosen: does the student pick it, or is there a default? | R1 says only "for one semester". |
| U-07 | What must the confirmation contain, and how is it delivered? | R4 requires a confirmation but does not define it. |
| U-08 | Are "course full" and "already enrolled" exact message texts or just meanings? | This affects how testers verify AC-04 to AC-06. |
| U-09 | What does the student see if registration fails for a reason outside R5, such as a technical error? | Not covered by R1–R5. Atomicity only guarantees that no partial Enrollment is created. |