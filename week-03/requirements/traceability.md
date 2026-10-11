# Traceability — use cases → stories → criteria

One row per use case. All six rows stay, even the ones with nothing behind them: an empty cell is a
finding you report, not a failure you hide. Use real IDs, comma-separated; write `none` where there
is nothing.

| Use case | Stories (US-nn) | Criteria (AC-nn) | Gap? |
| --- | --- | --- | --- |
| UC-01 View availability | US-01 | none | yes — no criteria: US-01 was not one of the three selected stories |
| UC-02 Book room | US-02 | AC-01, AC-02, AC-03, AC-04, AC-05, AC-07 | no |
| UC-03 Cancel booking | US-03 | AC-06, AC-07, AC-08, AC-09 | no |
| UC-04 Block or unblock room | US-05, US-06 | AC-10, AC-11, AC-12 | partly — "unblock" (US-06) has no criteria |
| UC-05 Review usage | US-07 | none | yes — no criteria: US-07 was not selected |
| UC-06 Send confirmation | US-04 | AC-01, AC-06 (and the "no confirmation" outcome in AC-09) | partly — no criteria of its own; only tested through Book and Cancel |

**Stories that belong to no use case:** none

**What the gaps tell you:** every use case has a story, but only three stories have criteria, so View availability, Review usage and unblocking are untested. Send confirmation can only be tested as an outcome of another use case, which supports drawing it as an `<<include>>` with no actor.
