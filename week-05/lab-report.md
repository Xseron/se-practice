# Week 05 — Lab report

**Name:** David Torossyan
**Group:** Monday 16-19
**Date:** 2026-10-11

Fill in every section. **Do not delete, rename or renumber the headings** — the checker and the
grader find your answers by them. Add rows to any table; never remove its header.

---

## 1. Setup

| | |
| --- | --- |
| Assistant (tool) | Claude Code (Anthropic) v2.1.296, used as a plain chat: headless `claude -p`, tools disabled, one session for Tasks 1–5 (`--session-id`, then `--resume`) |
| **Exact** model name | Claude Opus 5.5 (`claude-opus-5-5`) |
| Language and version | Python 3.12.6 (grader runs 3.13; standard library only) |
| Path | A |
| My Week 04 declaration for touching bookings | did not submit |

Week 04 was not submitted when this lab started, so there is no earlier touching-bookings
declaration to compare with AC4. AC4 is taken as the rule from here on.

**Exact command for every turn** (only the prompt file changes; the first turn uses
`--session-id <uuid>`, every later turn `--resume <uuid>`, so all five tasks are one chat):

```
claude -p --model claude-opus-5-5 --safe-mode --tools ""   --system-prompt "You are Claude, an AI assistant made by Anthropic."   --session-id <uuid> --output-format json < turn_N.txt
```

<!-- If your Week 04 model said touching bookings are NOT allowed: AC4 now says they are.
     One sentence here on what that changes in your Week 04 diagrams. This is a finding, not a penalty. -->

---

## 2. Task 1 — the plan

**The assistant's plan, pasted unedited** (also in `chat/resp_1.md`; the prompt is `chat/turn_1.txt`):

```text
# Plan for `can_book`

## Checks in order

Each check returns `False` as soon as it fails. The cheap scalar checks come first, and the loop over `existing` comes last.

1. **AC1, range:** `0 <= start < end <= 1440`. This also rejects zero-length and reversed intervals.
2. **AC1, future:** `start > now`, using strict `>`.
3. **AC2, duration:** `end - start <= 120`. Since check 1 already passed, the duration is known to be positive here.
4. **AC3, blocked:** if `blocked`, return `False`.
5. **AC4, overlap:** for each `(s, e)` in `existing`, return `False` if `start < e and s < end`. For half-open intervals, strict `<` on both sides lets bookings that only touch at an endpoint pass.
6. **AC5:** if every check passed, return `True`.

All checks are ANDed together, so their order only affects efficiency. `existing` is only read. It is never sorted, appended to, or reassigned.

## Assumptions

- **Inputs follow the contract.** The function does not check types or validate `now`, `blocked`, or the tuples in `existing`.
- **The start must be in the future.** A booking that starts exactly at `now` is rejected. If `now = 1439`, nothing can be booked.
- **End of day is bookable.** `end = 1440` is valid, so a booking can run up to midnight.
- **No minimum length.** A 1-minute booking is valid. There is no fixed slot size such as 15 minutes.
- **`existing` needs no ordering.** It may be unsorted or empty. Every booking in it counts, even ones that are already in the past.
- **No midnight crossing.** Everything happens on a single date.
- **The return value is a real `bool`.** It must be `True` or `False`, not just a truthy value such as a list or `None`.
- **No side effects.** The function does no saving, logging, or I/O.

## Boundary cases

Unless stated otherwise, `now = 480`, `blocked = False`, and `existing = [(600, 660)]`.

| # | Case | Input (start, end) | Expected | Bug it exposes |
|---|---|---|---|---|
| 1 | start equals now | now=600, (600, 660), existing=[] | False | `>=` used instead of `>` |
| 2 | start is one minute after now | now=599, (600, 660), existing=[] | True | off-by-one in the other direction |
| 3 | zero length | (500, 500) | False | `<=` used for start < end |
| 4 | reversed | (560, 500) | False | negative duration passes the `<= 120` check |
| 5 | ends at midnight | (1380, 1440) | True | `end < 1440` used instead of `<=` |
| 6 | ends past midnight | (1380, 1441) | False | no upper bound check |
| 7 | negative start | now=0, (-10, 30) | False | no lower bound check |
| 8 | exactly 120 minutes | (700, 820) | True | `< 120` used instead of `<=` |
| 9 | 121 minutes | (700, 821) | False | no duration check, or an off-by-one |
| 10 | blocked room, otherwise valid | (700, 760), blocked=True | False | AC3 ignored |
| 11 | touches the end of a booking | (660, 720) | True | `<=` in the overlap test |
| 12 | touches the start of a booking | (540, 600) | True | `<=` in the overlap test |
| 13 | 1-minute overlap at the start | (659, 720) | False | off-by-one in the overlap test |
| 14 | 1-minute overlap at the end | (540, 601) | False | off-by-one in the overlap test |
| 15 | identical to a booking | (600, 660) | False | only strict containment checked |
| 16 | new booking surrounds an existing one | (590, 670) | False | only checks whether the new endpoints fall inside the existing booking |
| 17 | new booking is inside an existing one | (610, 650) | False | only checks whether the existing endpoints fall inside the new booking |
| 18 | conflict with the last booking only | existing=[(500,530),(600,660)], (630, 690) | False | `return True` inside the loop |
| 19 | fills the gap between two bookings exactly | existing=[(600,660),(720,780)], (660, 720) | True | touching rule misapplied when there are two neighbours |
| 20 | unsorted bookings | existing=[(720,780),(600,660)], (650, 700) | False | code assumes `existing` is sorted |
| 21 | no bookings | existing=[], (700, 760) | True | empty list handled wrongly |
| 22 | several rules broken at once | blocked=True, (400, 600) | False | checks combined with OR |

For AC5, every case should also confirm these two things:
- `type(result) is bool`.
- `existing` is unchanged. Compare it to a deep copy taken before the call, and check that it is still the same object with the same length.

Ready for your next request.
```

**What the plan invented or changed.** One row for every rule in the plan that is not in the
contract or in AC1–AC5, or that says something different from them. If you found none, write one
row saying which lines of the plan you checked against which AC.

| # | What the plan said | What the contract or the AC says | What I did |
| --- | --- | --- | --- |
| 1 | Checks 1–6 (range, future, duration, blocked, overlap `start < e and s < end`, return True) | AC1 = checks 1–2, AC2 = check 3, AC3 = check 4, AC4 = check 5, AC5 = check 6. Every check traces to one AC line; no gap/buffer, no sorting, no saving | Kept. Nothing invented in the checks themselves, so there was nothing to tell the assistant to drop |
| 2 | Assumption "Inputs follow the contract. The function does not check types or validate `now`, `blocked`, or the tuples" | Contract: "now is valid (0-1439). blocked is a Boolean. existing contains valid (start, end) tuples". It says times are integers but not what happens otherwise | Kept: validating guaranteed inputs would be an invented rule. Non-integer times stay open — my decision is in §9.2 |
| 3 | Boundary case 7: `now=0, (-10, 30)` → False, "Bug it exposes: no lower bound check" | AC1 has two rules; with `now=0`, `start=-10` also breaks `start > now`. Two rules reject it, so it cannot expose a missing `0 <= start` | Not kept as a one-rule test. This led to §9.3: `0 <= start` can never be the only reason, because `now >= 0` and `start > now` already force `start >= 1` |
| 4 | Boundary case 22: `blocked=True, (400, 600)` → False, "checks combined with OR" | Breaks AC1 (`400 < 480 = now`) and AC3 at once | Not kept: README Part 3 step 4, one rule per test |
| 5 | Assumption "Every booking in it counts, even ones that are already in the past" | Contract: `existing` = "this room's active bookings only" | Kept — matches the contract; the function does not filter `existing` by time |

**Boundary cases the assistant suggested that I kept as tests:**

- #1 start equals now, #3 zero length, #4 reversed, #5 ends at midnight, #6 ends past midnight
- #8 exactly 120, #9 121 minutes, #11/#12 touching both ends, #15 identical, #16 surrounds, #17 inside
- #18 conflict with the last booking only, #20 unsorted bookings, #21 no bookings

---

## 3. Task 2 — the first version (v1), read before it was run

v1 is saved as `code/original/booking_v1.py`, exactly as the assistant returned it: yes — the first
` ```python ` block of `chat/resp_2.md`, copied out by a script, not by hand.

**What happened in this turn, reported so it is not hidden.** The model had no tools (`--tools ""`),
but it answered the implement prompt by *writing out imaginary tool calls as text*: a `Write` of
`booking.py`, a `Write` of a 22-case check script, then ~1,970 fake `Bash`/`PowerShell`/`Read`
calls (`echo test` over and over) until it hit the output-token limit. Claude Code then asked it to
continue, and it gave the final answer in `chat/resp_2.md`, which begins: *"I created `booking.py`
with the function below. I also wrote a check script … but I couldn't get a confirmed run of it"*.
**None of that happened**: no `booking.py` and no check script exist anywhere on my machine, and
nothing was run. The raw text before the limit is kept in `chat/resp_2_raw_before_token_limit.md`.
The function inside the fake `Write` is character-for-character the same as the one in the final
answer, so v1 is unambiguous. The claim "I created … I wrote a check script" is a finding: the
assistant's description of its own work was false. Before filling the table below I imported v1
once (one call, `can_book(660, 720, 540, False, [(600, 660)])`, to see that the file loads); no
test was run.

```python
"""Smart Campus study room booking: availability decision for one room."""

MINUTES_PER_DAY = 1440
MAX_DURATION = 120


def can_book(start, end, now, blocked, existing):
    """Return True if [start, end) can be booked for this room, else False.

    Times are integer minutes after midnight on one date. Intervals are
    half-open: the start is included and the end is excluded. `existing`
    holds (start, end) tuples for this room's active bookings and is only
    read, never modified.
    """
    # AC1: the interval lies within the day and has positive length.
    if not (0 <= start < end <= MINUTES_PER_DAY):
        return False

    # AC1: the booking starts strictly after the current time.
    if start <= now:
        return False

    # AC2: the duration is at most 120 minutes.
    if end - start > MAX_DURATION:
        return False

    # AC3: the room is not blocked.
    if blocked:
        return False

    # AC4: no overlap with any existing booking. Touching endpoints are allowed.
    for booked_start, booked_end in existing:
        if start < booked_end and booked_start < end:
            return False

    # AC5: every check passed.
    return True
```

**AC map.** One row per condition in v1. Quote the line.

| # | Line in v1 | AC it implements | Correct as written? If not, why |
| --- | --- | --- | --- |
| 1 | `if not (0 <= start < end <= MINUTES_PER_DAY): return False` | AC1 (range and order) | Yes. `MINUTES_PER_DAY = 1440`; `<= 1440` keeps a booking that ends at midnight; strict `start < end` rejects zero-length and reversed |
| 2 | `if start <= now: return False` | AC1 (`start > now`) | Yes — exact negation of `start > now`, so start == now is rejected |
| 3 | `if end - start > MAX_DURATION: return False` | AC2 | Yes. `MAX_DURATION = 120`; `>` lets exactly 120 through and rejects 121. Duration is positive here because line 1 passed |
| 4 | `if blocked: return False` | AC3 | Yes |
| 5 | `for booked_start, booked_end in existing:` / `if start < booked_end and booked_start < end: return False` | AC4 | Yes. Both comparisons strict, so `(660, 720)` vs `(600, 660)`: `660 < 660` is False → no overlap (touching allowed). Partial, inside, contains and identical all make both comparisons true. The loop only reads `existing` |
| 6 | `return True` (after the loop) | AC5 | Yes — only reached when every check passed and every booking was examined; all returns are literal `True`/`False` |

**What I expect to fail before running anything:** nothing. All six conditions match AC1–AC5 as
written. If the M checks find a surviving fault, it will be a hole in my *tests*, not in v1.

**Anything in v1 that no AC asks for** (extra validation, a buffer between bookings, logging,
saving the booking, a different return type):

- Two module constants, `MINUTES_PER_DAY = 1440` and `MAX_DURATION = 120`, and a module docstring.
  They do not change behaviour; kept.
- No extra validation, buffer, logging, saving or different return type.
- Outside the code: the false claim in the response that it had created files and written a
  check script (see above). Not part of `booking.py`, but it is the reason I do not take the
  assistant's "explain each condition" as evidence of anything — the tests in §4 are.

---

## 4. Task 3 — my tests

Base input for every row unless the row says otherwise: `now=540, blocked=False, existing=[(600, 660)]`.

| # | Test name | Request (start, end) | What differs from the base input | Expected | AC | Result on v1 | Result on final |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |
| 6 | | | | | | | |
| 7 | | | | | | | |
| 8 | | | | | | | |
| 9 | | | | | | | |
| 10 | | | | | | | |
| 11 | | | | | | | |

---

## 5. Task 4 — debugging with evidence

One row per defect you found — in v1, in a later version, or in your own tests. If v1 passed
everything, the row is the **new edge case you added**, with expected and actual equal, and the
cause column says why no change was needed.

| # | Input (the full call) | Expected | Actual | Cause (quote the line) | Fix | Who proposed the fix |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | |

**The debug prompt I sent, and the assistant's answer** (leave the block empty if you did not use it):

```text
```

---

## 6. Task 5 — the critique

**The assistant's critique, pasted unedited:**

```text
(paste here)
```

| # | Suggestion | accept / reject | Reason — cite the AC or the contract line | Suite after the change |
| --- | --- | --- | --- | --- |
| 1 | | accept / reject | | |
| 2 | | accept / reject | | |

---

## 7. Change log — v1 to final

| # | What changed (the line, before → after) | Why | Evidence: the test or check that moved |
| --- | --- | --- | --- |
| 1 | | | |

---

## 8. Evidence — real output

### 8.1 My suite, final run

Paste the **complete** terminal output. For Python: everything `python -m unittest -v` printed.

```text
(paste here)
```

### 8.2 The checker, final run

Paste the **complete** output of `python tests/check_booking.py`. Paste it **last**: if you edit
this file afterwards, run the checker again and paste again.

```text
(paste here)
```

### 8.3 Path B only — three faults I planted myself

Break your own function on purpose, one line at a time, run your suite, restore the line.

| # | Line I changed (before → after) | AC it breaks | Test that failed |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |
| 3 | | | |

The three failing runs (Path A students leave this block empty):

```text
```

---

## 9. What still fails, and what the contract does not say

### 9.1 Checks I am keeping as FAIL or ERROR

The same IDs as `known_fails` in `submission.yml`. Write `none` if the run is clean.

| Check | Why it stays |
| --- | --- |
| | |

### 9.2 Outside the contract

The contract says times are integers. It does not say what `can_book` does when one is not —
`600.5`, or the string `"600"`. What does **your** function do, and why is that the right call?

-

### 9.3 A bound that never decides

One of the bounds written in AC1 can never be the *only* reason a request is rejected. Which one,
and why?

-

---

## 10. Conclusion (120–180 words)

<!-- Answer all three, in your own words, without the assistant:
     (a) Explain the overlap condition in your final code — why those two comparisons, and why
         they let touching bookings through.
     (b) Which fault did your tests miss the longest, and what did the missing test have in common
         with the ones you already had?
     (c) What did you have to decide that neither the contract nor the assistant decided for you?
     Worthless: "the AI made a mistake and I fixed it."
     Worth everything: "F7 failed on can_book(570, 600, ...): v1 compared with <= on the start
     side, so a booking that ends exactly when another begins was rejected." -->

<!-- Write your conclusion below this line -->
