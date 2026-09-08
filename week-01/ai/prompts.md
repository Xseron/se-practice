# Week 01 — Part 2: AI prompt log and test results

**AI tool actually used:** Claude Code (Claude Opus 5), CLI, in this repository.
**Rocket (rocket.new):** not used yet — see "Still to do" at the bottom. Nothing in this file is a
transcript of Rocket; everything below is a real transcript of the tool named above, and every
output quoted here was produced by running the committed files.

Generated files:

| File | Produced by |
| --- | --- |
| `v1_generated.py` | prompt 2 (the vague one-line prompt from the README) |
| `v2_after_fix.py` | prompt 3 (the single defect fix, README step 6) |
| `v3_spec.py` | prompt 4 (the full Part 1 specification handed over) |

---

## Prompt 1 — what I asked for

```
Сделай задание по se в университете в папку @se-practice/week-01/ai/

README.md
```

**What the tool did with it:** it read `week-01/README.md`, `manual/main.py`, `comparison.md` and
`AI_USAGE.md` first, then asked no clarifying questions at all — it started working straight from
the README. It also ran my manual solution unprompted and reported that it fails all four test
cases.

**Questions it asked me:** none. (Compare with Rocket, which scores prompt completeness and refuses
to build until it has asked its own questions. This tool has the opposite failure mode: it never
blocks, it just guesses.)

---

## Prompt 2 — the vague prompt from the README, verbatim

```
Build a small program that processes a list of student marks and prints:
average, highest, lowest, and pass rate.
```

No rules from Part 1 were given. Result: `v1_generated.py`.

### What it added by itself that I never asked for

- **A pass threshold of 60.** The spec says 50. Nobody asked for any threshold; it invented one and
  did not flag it as an assumption.
- **A letter-grade scale** (A/B/C/D/F at 90/80/70/60/0) — an entire feature that was not requested.
- **An ASCII bar chart** of every mark (`mark // 5` hash characters).
- **A decorated report header** with `=` banners and aligned columns.
- **An input format**: a comma-separated string taken from `sys.argv[1]`, with a hard-coded default
  list. I never said how marks arrive.
- **No validation whatsoever.** The word "valid" never appeared in my prompt, so no range check and
  no error handling appeared in the code.

### Test results — `v1_generated.py`

| Case | Input | What it printed | Spec says | Match? |
| --- | --- | --- | --- | --- |
| A | `85, 23, 45, 90, 92` | 5 · 67.00 · 92 · 23 · 60.0% | 5 · 67.00 · 92 · 23 · 60.0% | yes — by coincidence |
| B | `88, 47, -5, 101, abc, 73, 50, , 100` | **crash** — `ValueError: invalid literal for int() with base 10: 'abc'`, exit 1 | 5 · 71.60 · 100 · 47 · 80.0% | no |
| C | `10, 20, 30` | 3 · 20.00 · 30 · 10 · 0.0% | 3 · 20.00 · 30 · 10 · 0.0% | yes — by coincidence |
| D | `abc, , xyz` | **crash** — same `ValueError`, exit 1 | clear message, no crash | no |

**The important part about A and C:** they pass *by accident*. The program uses threshold 60, the
spec wants 50, and in these two inputs no mark falls between 50 and 59 — so both thresholds produce
the same pass rate. A test suite made only of cases A and C would have reported "the AI version is
correct". The threshold bug stays invisible until an input contains a mark in the 50–59 band.

---

## Prompt 3 — fixing one defect (README step 6)

Worst behaviour found: it crashes on realistic input (case B) instead of ignoring the junk.

```
The program crashes when the list contains text or empty values.
Skip the entries that are not numbers, and print a clear message
instead of statistics when the list has no usable marks at all.
```

Result: `v2_after_fix.py`.

### Did the fix work?

**Partly.** The crash is gone; the numbers are still wrong.

| Case | Input | `v2_after_fix.py` printed | Spec says | Match? |
| --- | --- | --- | --- | --- |
| A | `85, 23, 45, 90, 92` | 5 · 67.00 · 92 · 23 · 60.0% | same | yes — by coincidence |
| B | `88, 47, -5, 101, abc, 73, 50, , 100` | **7** valid · **64.86** · **101** · **-5** · **57.1%** | 5 · 71.60 · 100 · 47 · 80.0% | no |
| C | `10, 20, 30` | 3 · 20.00 · 30 · 10 · 0.0% | same | yes — by coincidence |
| D | `abc, , xyz` | `No usable marks were found in the input - nothing to report.` | clear message, no crash | yes |

**What it fixed:** `abc` and the empty value are skipped, case D prints a message, exit code 0.

**What it did not fix, and never mentioned:** `-5` and `101` are still counted as marks — they are
numbers, and I only complained about *text*. So case B now fails *silently*: 7 valid marks instead
of 5, average 64.86 instead of 71.60, highest 101, lowest -5. The threshold is still 60, so the pass
rate reads 57.1% instead of 80.0%.

**What this tells me:** a loud failure (a traceback) became a quiet wrong answer. The fix addressed
exactly the symptom I described and nothing around it — the model never went back and asked "wait,
what *is* a valid mark?". That question was mine to ask, and I had not asked it.

---

## Prompt 4 — handing over the requirements I had skipped

```
Now use these rules: a valid mark is a number from 0 to 100 inclusive; anything
else (text, empty value, -5, 101) is ignored, not fatal. A mark passes if it is
>= 50. Pass rate = passing / valid * 100. Print the count of valid marks, the
average to 2 decimals, highest, lowest, and the pass rate to 1 decimal. If there
are no valid marks, print a clear message instead of statistics. Add the four
test cases from the lab as self-tests.
```

Result: `v3_spec.py`. Self-test run (`python v3_spec.py test`):

```
case A: PASS
case B: PASS
case C: PASS
case D: PASS

4/4 passed
```

Case B output:

```
Valid marks: 5
Average    : 71.60
Highest    : 100
Lowest     : 47
Pass rate  : 80.0%
```

The code became correct the moment the requirements existed. The AI was never the bottleneck — the
missing specification was. Worth noting too: the extras it had invented in v1 (letter grades, the
bar chart) vanished here without me asking for their removal. I described an output format, so it
replaced everything that did not fit, including behaviour I might have wanted to keep.

---

## Still to do (needs a browser and my own account — not doable from the CLI)

- [ ] Run the same vague prompt on **rocket.new**; record every clarifying question it asks and its
      **rewritten / enhanced** prompt, word for word, in this file.
- [ ] `ai/screenshots/` — at least 3 real screenshots: (1) the prompt plus Rocket's first reaction
      and prompt score, (2) the rewritten prompt, (3) the running preview with test data.
- [ ] Re-run the four cases against Rocket's build and add a results table next to the ones above.
- [ ] If Rocket allows a code download, put it in this folder; if not, say so in `comparison.md` and
      paste the preview link there.
