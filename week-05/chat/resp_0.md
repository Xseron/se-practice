Understood. I'll use only this scenario, contract, and acceptance criteria.

**`can_book(start, end, now, blocked, existing)`**
- **AC1:** `0 <= start < end <= 1440` and `start > now`
- **AC2:** `end - start <= 120`
- **AC3:** `blocked` is `False`
- **AC4:** For each `(s, e)` in `existing`, no overlap under half-open `[start, end)`. Touching endpoints are allowed.
- **AC5:** Return `True` only if AC1–AC4 all hold, otherwise `False`. Never change `existing` or any other input.

What's your first request?