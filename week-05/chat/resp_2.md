I created `booking.py` with the function below. I also wrote a check script for the 22 boundary cases in the scratchpad, but I couldn't get a confirmed run of it, so the function is **not yet verified by execution**.

## `booking.py`

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

## What each condition does

1. **`0 <= start < end <= 1440` (AC1, range)**
   - Keeps the booking within the day. `end = 1440` is allowed, so a booking can run until midnight.
   - The strict `start < end` rejects zero-length bookings like `(500, 500)`.
   - It also rejects reversed ones like `(560, 500)`. Without it, a reversed booking would have a negative duration and slip through the 120-minute check.
2. **`start <= now` → `False` (AC1, future)**
   - This is the negation of the required `start > now`, so a booking that starts exactly at `now` is rejected.
3. **`end - start > 120` → `False` (AC2)**
   - Exactly 120 minutes is allowed and 121 is rejected.
   - By this point check 1 has passed, so the duration is guaranteed to be positive.
4. **`if blocked` → `False` (AC3)**
   - A blocked room fails no matter what the times are.
5. **`start < booked_end and booked_start < end` → `False` (AC4)**
   - This is the standard overlap test for half-open intervals.
   - Both comparisons are strict, so `(660, 720)` next to `(600, 660)` doesn't count as an overlap.
   - The test catches every real overlap: partial at either end, identical, the new booking inside an existing one, and an existing one inside the new booking.
   - Every booking is checked and order doesn't matter. The function only returns `True` after the loop has finished.
6. **`return True` (AC5)**
   - This line is reached only if all checks pass.
   - Every return is the literal `True` or `False`, so the result is always a real `bool`.
   - `existing` is only iterated over. It is never sorted, appended to, or reassigned, so the caller's list is unchanged.

## Scope

- **Included:** only what the contract and AC1–AC5 require. It uses no imports, does no saving, confirmation, or logging, and does no type validation.
- **Constants:** `MINUTES_PER_DAY` and `MAX_DURATION` are named so the limits are easy to read. They don't change the behaviour.

## Verifying

The check script is `check_booking.py` in the scratchpad directory. It runs all 22 boundary cases from the plan. For each case it also asserts that `type(result) is bool` and that `existing` is unchanged (same contents, same object, same length).

To run it:

```powershell
python -I <scratchpad>\check_booking.py <folder containing booking.py>
```

It prints `22/22 passed` on success, or the case number of any failure.

If you like, I can turn those cases into a proper `unittest` file next to `booking.py`.