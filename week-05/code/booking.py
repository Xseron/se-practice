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
