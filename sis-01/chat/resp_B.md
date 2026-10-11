# Review of the draft against question 1.6 and your scenario

Concerns are grouped by section. Within each group, the most serious come first. Each one covers what is wrong, why it matters, how to check it, and a counterexample or alternative reading.

---

## A. Gaps against the question and scenario

**1. The "empty reserved rooms" problem is never addressed.**
- **Problem:** The scenario names two failures: double bookings and rooms reserved but left empty. Every section of the draft targets only double bookings.
- **Why it matters:** A marker comparing the draft with the scenario will see half the problem unsolved. An online system could also make no-shows *worse*, because booking from bed at midnight costs nothing.
- **Check:** For each section, ask what in it would reduce empty reserved rooms. Ask the administrator why rooms sit empty. People forgetting, booking speculatively and stale sheets each need different fixes.
- **Alternative:** No-shows may be a policy problem, solved by check-in, auto-release after 15 minutes or per-student limits. You could deliberately leave it out of version 1, but the draft must say so.

**2. The AI part of the question is not answered for each principle.**
- **Problem:** The question asks which of *these* decisions an AI can support. That means decisions about process, dependability, requirements and reuse. The draft answers in one general closing paragraph. AI appears briefly under dependability and reuse, not at all under process, and only implicitly under requirements.
- **Why it matters:** The second half of the question is half the marks. A generic list of "plans, code, test cases" and "rules, risks, release" could describe any project.
- **Check:** Draw a 4×2 grid: the four principles against "AI can support" and "humans must decide". Mark which cells the draft actually fills. Most of the process and reuse cells are empty.
- **Alternative:** Some decisions belong to neither the AI nor the engineers. See concern 3.

**3. "Choosing the rules … remain the engineers' decisions" puts authority in the wrong place.**
- **Problem:** Rules such as maximum duration, who may block rooms and whether a booking can be cancelled are faculty policy. The facilities administrator or the faculty owns them. The developers elicit, record and implement them. Your tutor note says the trouble with the AI's rule is that the AI chose it instead of a stakeholder. The draft's conclusion replaces the AI with the developers, which has the same flaw.
- **Why it matters:** This weakens your strongest argument. It also leaves "signing off the release" vague. Do two students approve their own work, or does the administrator accept it?
- **Check:** For each rule, ask who a student would complain to, and whether the administrator would accept that the developers set it.
- **Counterexample:** If a developer decides that "a started booking cannot be cancelled", they have done exactly what you criticise the AI for.
- **Alternative reading:** Engineers decide *technical* risk, such as failing closed and testing depth. Stakeholders decide *policy*. Drawing that line would sharpen the answer.

**4. The principles may be worded differently from your course.**
- **Problem:** Sommerville (ch. 1) is a common source for topic 1.6. If your course follows him, the fundamentals are a *managed and understood* process and *dependability and performance*.
  - The draft dismisses performance in passing ("a slow page").
  - Its process section picks a model but never says how the work will be managed: milestones, progress tracking, and what gets cut if week 8 slips.
- **Why it matters:** If the marking scheme follows that wording, you lose credit for points you could easily cover.
- **Check:** Compare with your course slides for 1.6, as tutor note 5 suggests.
- **Alternative:** If your course words the principles differently, this concern disappears.

---

## B. Process

**5. Incremental versus waterfall is a false choice, and waterfall is a strawman.**
- **Problem:** "Waterfall … would freeze rules before anyone knows them" assumes the rules can't be learned in advance. With 40 rooms and one administrator, a few interviews might settle most of them. Tutor note 4 already flags this, but the draft text hasn't changed. Other options also exist, such as a paper mock-up or throwaway prototype shown to the administrator in weeks 1–2 before a planned build.
- **Why it matters:** An argument that only beats a weak alternative looks unconsidered.
- **Check:** List the open rules and ask the administrator about them. Count how many truly need real usage to settle.
- **Counterexample:** The maximum duration probably already exists as a policy on the paper sheets, so it is not open at all.

**6. Deferring room blocking, and ignoring the move from paper, both create the risk you are trying to prevent.**
- **Problem:** The first increment is booking only, and blocking comes later. In exam week, rooms are likely to be blocked for exams. If blocking isn't built yet, students can book rooms that are unavailable. Separately, the draft never says what happens to the paper sheets at launch. If some people keep using paper while others use the system, there are two sources of truth. That causes double bookings no overlap check can see.
- **Why it matters:** The draft's process choice could produce the exam-week failure on its own, without any code defect.
- **Check:** Ask the administrator how often and when rooms are blocked. Place increment 2 on a timeline next to exam week. Decide who removes the sheets, and when.
- **Alternative:** If blocking is rare, the administrator could use a workaround, such as booking the room from an admin account. That would justify deferring it, but the draft needs to say so.

**7. The timing is undefined, and "usage reports" have no source.**
- **Problem:** The draft never says when version 1 goes live relative to exam week. If it launches in week 11 and exams start in week 13, the first heavy use comes almost immediately, with no feedback cycle in between. "Usage reports" appear nowhere in the scenario, and no stakeholder is named who wants them.
- **Why it matters:** Incremental delivery only helps if increments reach users early. Every unrequested feature competes for 12 weeks of two people's time.
- **Check:** Sketch a week-by-week plan with release points and exam week marked.
- **Alternative:** Reports *could* be justified by the empty-room problem, for example by showing no-show rates. If that is your reason, connect them to concern 1.

---

## C. Dependability

**8. "Its errors sit at the boundaries" overclaims and mixes different rules.**
- **Problem:** "Exactly 120 minutes" is a duration rule, and "end of the day" is an opening-hours rule. Neither is part of the overlap check. The scenario also never says there is a 2-hour limit, yet the draft assumes one twice. Overlap errors also come from other sources:
  - leaving the room out of the comparison;
  - counting cancelled bookings, or not counting them;
  - leaving administrator blocks out of the check;
  - simultaneous requests, which the draft raises two sentences later, contradicting its own claim.
- **Why it matters:** If you test only boundaries, you will feel safe while a common bug survives.
- **Check:** Write overlap functions with one planted bug each, and see which ones your boundary tests catch.
- **Counterexample:** A check of the form "conflict if the new start falls inside an existing booking, or the new end falls inside it" misses a 09:00–13:00 booking that fully contains a 10:00–12:00 one. That is a containment bug, not a boundary bug, and it accepts exactly the double booking in your risk.

**9. The value judgement doesn't match the decision it justifies, and availability is ignored.**
- **Problem:** "A doubled booking costs more than a slow page" is used to justify rejecting bookings when the check can't complete. But the cost of rejecting is a *refused valid booking or an unusable system*, not a slow page. "Cannot be completed" is also vague. If the database is down, the booking can't be saved anyway, so the rule adds nothing. Rejecting also does nothing to prevent the "lost" bookings the sentence mentions.
- **Why it matters:** Dependability covers availability as well as integrity. If the system refuses everything during an exam-week outage, students go back to paper or squatting, which brings back double bookings outside the system.
- **Check:** List concrete failures (database down, SSO down, timeout, server restart) and decide the behaviour for each one.
- **Alternative:** A study room is not safety-critical. A double booking means two groups at one door, which is today's normal situation. Accepting the booking and flagging the conflict to the administrator is a defensible choice. The draft needs to argue why it is worse.

**10. Nothing covers detecting or recovering from a double booking.**
- **Problem:** Your risk says a faulty check *accepts* two bookings. The draft only discusses prevention.
- **Why it matters:** Dependability includes detection and recovery. Examples are a nightly query for overlapping rows, a conflict view for the administrator, notifying both students, and a rule for who keeps the room.
- **Check:** Ask yourself: if this happens on the Monday of exam week, who finds out, how, and what do they do?
- **Counterexample:** If you add a database constraint after overlapping rows already exist, creating it fails. Prevention alone also does not clean up existing bad data.

**11. Simultaneous bookings are presented as rare, and the database fix is vague.**
- **Problem:** "If two students submit at the same moment" sounds like an edge case. But popular slots in exam week, or bookings that open at a fixed time, make simultaneous requests normal. "The database should enforce the rule too" doesn't say how.
- **Why it matters:** Some common approaches do not actually work:
  - A unique constraint on (room, start time) only catches identical start times, not partial overlaps.
  - A check-then-insert inside a transaction can still race at default isolation levels.
- **Check:** Write a small script that sends two overlapping inserts at once and see whether both succeed. If you use PostgreSQL, an exclusion constraint on room plus time range needs the `btree_gist` extension. Check that you have permission to enable it on the faculty server.

**12. Maintainability and privacy are missing.**
- **Problem:** The scenario says the two students "build and maintain" the system, but students graduate. AI-generated code that nobody fully understands makes handover harder. Bookings tied to SSO identities also record who is in which room and when, which is personal data.
- **Check:** Ask the faculty who maintains the system next year. Check the university's data-protection rules.
- **Alternative:** If your course scope covers version 1 only, one sentence acknowledging this is enough.

---

## D. Requirements management

**13. The trace is inconsistent and only runs one way.**
- **Problem:** Rules are "traced to its tests", yet the next sentence says the trace shows "which code" changes. Nothing links rules to code. More importantly, the trace only runs *forward*, from rules to tests. Tracing *backward*, from each rule to its source (e.g. "administrator, interview, week 2"), is exactly what would catch AI-invented rules. A rule in the code with no source is an invented rule. The draft misses this link to its own best evidence.
- **Check:** Draft the table with a "source" column, then see whether "only an administrator can block" would be flagged.
- **Alternative:** Linking rule IDs in commit messages gives you the rule-to-code trace almost for free.

**14. The R3 example tests one side only, and change control is missing.**
- **Problem:** R3 covers a new booking that starts when an existing one ends. It doesn't cover the mirror case, a new booking that ends when an existing one starts, or any case that should be rejected. "Touching" is also used before it is defined. Requirements management also covers *who approves a change*, which matters when the draft expects rules to change mid-semester.
- **Why it matters:** A bug that is wrong on only one side passes R3, so R3 is weak as the draft's showcase of "testable".
- **Check:** Write the mirror case and one rejection case, then run them against the planted bugs from concern 8.

---

## E. Reuse

**15. SSO is a requirement, not a reuse choice, and the biggest reuse question is missing.**
- **Problem:** The scenario requires SSO, so presenting it as a reuse decision with a trade-off is weak, because there was no alternative. The real reuse decisions are which framework, calendar component and database to use. Above all: should you deploy an existing open-source room-booking system, such as MRBS, or extend the university's timetabling system instead of building one? Several other points also need tightening:
  - "Keeps the project within budget" is inaccurate. Writing your own login costs *time*, not money, so the constraint it protects is the 12 weeks.
  - "An existing database" is an assumption. The scenario only mentions an existing server.
  - "No budget for new software" could mean "can't buy" or "can't install". These lead to different decisions.
  - "If SSO is down, nobody can book" may be overstated, since sessions that are already logged in may continue.
- **Check:** Ask faculty IT what is installed on the server and whether free software may be added. Look for existing booking systems that support your university's SSO protocol. Note their licences, since "free" can still carry obligations.
- **Counterexample:** If an existing tool fits, building at all is the wrong decision. If it doesn't, explaining why makes the case for building much stronger.

**16. "AI-generated code is also reuse" can be challenged.**
- **Problem:** Once you accept the code, it is arguably *your* code, not a reused component. "It has no maintainer" then misses the point: the maintainer is you, and that is the real burden. "At least the same review" also doesn't say what that review involves.
- **Check:** Look up how your course defines reuse. It is often about components and systems, not generated code.
- **Alternative:** A different framing could be reuse of code of *unknown origin*, which raises licensing and copying risks rather than maintenance risks.

---

## F. The AI section

**17. "Rules nobody asked for" is partly contradicted by your own scenario.**
- **Problem:** The scenario says the administrator blocks rooms. So "an administrator can block" was asked for. Only the word "*only*" was invented. The tutor note spots this, but the draft text still says "nobody asked for".
- **Why it matters:** A reader who knows the scenario can dismiss your example in one sentence.
- **Check:** Reread the prompt you used in the lab. Did it say who blocks rooms, or who can cancel?
- **Alternative reading:** The AI filled gaps in an underspecified prompt. That is evidence for *requirements management* rather than proof that the AI is unreliable. That framing may actually be stronger.

**18. "AI can support checking" is unsupported, and correlated errors are ignored.**
- **Problem:** The risk says the faulty check may come from an AI. If the same AI also writes the tests from the same understanding, the tests will confirm the bug. For example, both may treat a booking's end time as part of the booking, which blocks touching bookings. "Quickly" is also unsupported once review time is counted (tutor note 6).
- **Why it matters:** This is the central weakness in your risk scenario, and the draft treats tests as an independent safeguard without saying where their independence comes from.
- **Check:** In the lab, give the AI the containment-bug function from concern 8, ask for tests, and see whether they catch it. Then compare with tests written from the requirements table.
- **Alternative:** An AI reviewing *human* code, or tests derived from requirements rather than from the code, could provide real independence. Independence is the property to argue for.

---

## Where to start

The highest-value fixes are:

1. **Empty rooms** (concern 1).
2. **Per-principle AI decisions with stakeholder ownership** (concerns 2 and 3).
3. **The containment counterexample and detection/recovery** (concerns 8 and 10).
4. **Backward traceability as the defence against invented rules** (concern 13).

These address the question directly and strengthen the evidence you already have.