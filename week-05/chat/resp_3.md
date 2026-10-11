# Review of `can_book` against the contract and AC1–AC5

**I found no concrete issues.** Every acceptance criterion and contract line is implemented correctly, so I'm listing zero rather than inventing any. Keep in mind that I wrote this code, which can bias a self-review, and that the 22 boundary cases have not yet been confirmed by an actual test run.

## Check against each requirement

| Requirement | Line(s) | Verdict |
|---|---|---|
| **AC1:** `0 <= start < end <= 1440` | `if not (0 <= start < end <= MINUTES_PER_DAY):` | Correct. The chained comparison matches the criterion exactly, including `end == 1440` being allowed. It also rejects zero-length and reversed intervals. |
| **AC1:** `start > now` | `if start <= now:` | Correct. This is the exact negation for integers, so `start == now` is rejected. |
| **AC2:** duration at most 120 | `if end - start > MAX_DURATION:` | Correct. 120 passes and 121 fails. The duration is guaranteed positive because the AC1 check runs first. |
| **AC3:** room not blocked | `if blocked:` | Correct for a Boolean `blocked`, which the contract guarantees. |
| **AC4:** no overlap, touching allowed, intervals `[start, end)` | `if start < booked_start ...`, i.e. `if start < booked_end and booked_start < end:` | Correct. With strict `<` on both sides, adjacent bookings pass, while partial, identical, and containing overlaps all fail. The loop checks every booking and does not depend on order. |
| **AC5:** `True` only if AC1–AC4 all hold | `return True` | Correct. It is reached only after every check passes, and every other path returns `False`. |
| **AC5 / contract:** never alter `existing`, keep all inputs unchanged | `for booked_start, booked_end in existing:` | Correct. `existing` is only read. Nothing sorts it, appends to it, or reassigns it. The other inputs are immutable `int` and `bool` values. |
| **Contract:** return `True` or `False` | all `return` statements | Correct. Every return is a bool literal, never a truthy expression. |

## Not issues under this contract

These would only matter if the contract changed:

- **Malformed bookings:** a tuple in `existing` that isn't a pair would raise `ValueError` when unpacked. The contract guarantees valid `(start, end)` tuples.
- **One-shot iterators:** if `existing` were a generator, looping over it would consume it. The contract describes a collection of tuples.
- **Wrong input types:** inputs such as floats or `None` aren't checked. The contract guarantees integer times and a Boolean `blocked`.

## Remaining gap

The gap is evidence, not code. The boundary-case script has not produced a confirmed `22/22 passed`. Running it, or turning it into a `unittest` file, is the next step before treating AC1–AC5 as verified.