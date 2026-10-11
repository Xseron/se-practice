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