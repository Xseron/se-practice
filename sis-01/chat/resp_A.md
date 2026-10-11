# Draft (about 485 words)

**Applying fundamental engineering principles to a campus room-booking system**

The faculty's 40 study rooms are booked on paper sheets taped to each door, which causes double bookings and "reserved" rooms that stand empty. Two student developers must replace this with a system that is in use within one 12-week semester, runs on the faculty's existing server with the university's single sign-on (SSO), and needs no new software budget. Four engineering principles shape this work.

**Process.** An incremental process fits better than waterfall. Some booking rules were open at the start, such as whether touching bookings are allowed or whether exactly two hours is permitted. We assume some will only be settled once students and the administrator use the system. The first increment therefore delivers booking, and room blocking and usage reports follow. The trade-off is that incremental delivery needs users available for feedback during the semester, and early code may need rework when a rule changes. Waterfall offers a fixed plan, but would freeze rules before anyone knows them.

**Dependability.** The check that must never be wrong is the overlap check, and its errors sit at the boundaries: a booking starting exactly when another ends, exactly 120 minutes, the end of the day. We judge a lost or doubled booking in exam week to cost more than a slow page. So if the check cannot be completed, the system should reject the booking, trading occasional frustration for integrity. Correct logic is not enough: if two students submit at the same moment, both may pass the check before either is saved, so the database should enforce the rule too. Boundary tests apply whether a developer or an AI assistant wrote the code.

**Requirements management.** Every rule gets an ID and a testable acceptance criterion and is traced to its tests. If touching bookings are allowed, R3 might read: "A 10:00–12:00 booking for Room 12 is accepted when the only existing booking ends at 10:00." When a rule changes, the trace shows which code and tests change with it. The cost is bookkeeping for a two-person team, so a simple table is more realistic than a dedicated tool.

**Reuse.** Reusing SSO and an existing database avoids writing login and storage, which are hard to make secure and reliable, and keeps the project within budget. The trade-off is dependence: if SSO is down, nobody can book. AI-generated code is also reuse. Unlike a maintained library, though, it has no track record or maintainer, so it deserves at least the same review and testing as any third-party component.

**What AI can and cannot decide.** An AI assistant can quickly draft plans, code and test cases. In our labs, however, it also invented rules nobody asked for, such as "only an administrator can block" and "a started booking cannot be cancelled". Such rules look plausible, which makes them easy to miss. AI can therefore support drafting and checking, but choosing the rules, accepting the risks and signing off the release remain the engineers' decisions.

---

# Tutor notes

## Facts vs. assumptions

| Type | Items |
|---|---|
| **Given by your scenario** | 40 rooms, paper sheets, double and empty bookings, the three user groups, two developers, 12 weeks, existing server, SSO, no budget, the exam-week risk. |
| **Your own observation** | The AI invented two rules in your labs. This is real evidence, but it is a single anecdote. Keep the wording "in our labs" and don't generalise it to "AI always does this". |
| **Assumptions** | Rules only settle once users try the system. Users will be available for feedback mid-semester. The server can host the app. SSO integration is permitted. A suitable free database exists. |
| **Value judgements** | "A doubled booking costs more than a slow page." This is reasonable, but it is a priority you chose, not a fact. The draft says "we judge" for that reason. |

## Things I added beyond your ideas
Keep only what you can defend:
- **The concurrency point.** This is the biggest addition. Your exam-week risk may not come from wrong logic at all. Two simultaneous requests can both pass a correct check.
- **Fail-safe rejection.**
- **SSO as a single point of failure.**
- **AI code having no maintainer.**
- **The cost of traceability.**
- **The observation that the invented rules look plausible.** This one is sharp in your scenario. The administrator *does* block rooms, so "only an administrator can block" might become a real rule. The problem is that the AI decided it rather than a stakeholder.

## Claims to verify
1. **SSO access.** Does university IT allow a student-built app to use SSO, and how long does approval take? This could eat into your 12 weeks.
2. **Database enforcement.** Which existing database would you use, and can it enforce "no overlap" itself? For example, PostgreSQL has exclusion constraints. Check what your actual database supports.
3. **Your overlap condition.** With touching bookings allowed, a common formulation is `new.start < existing.end AND existing.start < new.end`. Test it against these cases: touching, identical times, one booking inside another, exactly 120 minutes, and closing time.
4. **"Only settled once real users try it."** Some rules could be settled by simply asking the administrator first. Consider softening this claim.
5. **Definitions.** Check how your course material defines "incremental" versus "iterative" or "agile", and how it phrases the four principles. If you cite a textbook, cite it from your own copy, not from memory.
6. **"AI drafts quickly."** Does it still save time once review is included? Your lab experience could answer this.