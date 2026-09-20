# Lab report — Practice #02: The Prompt Is an Engineering Input

**Name:** David Torossyan
**Group:** Monday 16-19
**Date:** 2026-09-20

> Fill in every section. **Do not delete or renumber the headings** — the grading pass reads them
> by number. If something did not happen, write "did not happen" and why; an empty section and a
> fabricated one are graded the same way.

---

## 1. The frozen experiment

| | |
| --- | --- |
| AI assistant | Claude Code (Anthropic), v2.1.278, used as a plain chat: headless `claude -p`, one process per prompt |
| Exact model name | Claude Fable 5.1 (`claude-fable-5-1`) |
| Implementation language | Python 3.12.6 |
| Date of the runs | 2026-09-20 |

**Non-Python students only** — paste your substituted Prompt B text here, so the substitution can
be checked:

```
n/a — used Python
```

**Confirmations:**

- Each prompt was sent in a **fresh chat**: yes — every prompt was a separate `claude -p` process with `--no-session-persistence`, started in its own empty directory
- No follow-up questions were asked before Part 7: yes — print mode is one message in, one message out
- Every output was saved **before** any editing: yes — the full responses are in `responses/prompt_*.md`; `code/prompt_*.py` is the first fenced `python` block of each response, copied out by a script, not by hand

**Exact command, identical for all four prompts** (only the prompt file changes):

```
claude -p --model claude-fable-5-1 --safe-mode --tools "" \
  --system-prompt "You are Claude, an AI assistant made by Anthropic." \
  --no-session-persistence --output-format json < prompt_X.txt
```

`--safe-mode` switches off my CLAUDE.md, plugins, hooks and memory, so nothing from my machine
reaches the model except the prompt.

**One discarded attempt, reported here so it is not hidden.** My first attempt at A, B and C used
the same command *without* `--system-prompt`. Claude Code's default system prompt tells the model
it is a coding agent with tools, but `--tools ""` had removed the tools. The model answered by
writing imaginary tool calls as plain text: A claimed it had saved `student_marks.py` and that its
assertions printed `ALL OK`; C showed "All tests passed." from a Python at `C:\Users\Mythos\...`,
a path that does not exist on my machine; B contained no code at all. I checked the three run
directories — no file had been written, so none of that happened. That is a defect of my setup, not
a result about the prompts, so I discarded all three, fixed the setup, froze it, and re-ran A, B
and C under the command above; D was only ever run under the final command. I decided to discard
before running the harness on anything, and I never ran the harness on the discarded C code, so the
choice was not made by looking at verdicts. The discarded responses are kept unedited in
`responses/invalid-run-1/`. (A second, earlier failure produced no model output at all: my
globally installed CLI v2.1.221 refused the model with an API 400 "version 2.1.251 or newer is
required", so I used the v2.1.278 binary that ships with the VS Code extension.)

---

## 2. Prompt A — minimal

**Prompt sent** (should be exactly one sentence):

```
Write Python code to analyze student marks.
```

**Assumptions the AI made that I never gave it** — list them, one per line. A data format, a pass
threshold, a rounding rule, an input method, an invented feature all count.

1. Input method: a CSV file given on the command line (`python marks.py marks.csv`), with built-in sample data for six invented students if no file is given.
2. Data format: one row per student, first column the name, every other column a subject — so "marks" became a students × subjects table, not a list of numbers.
3. Pass threshold: `PASS_MARK = 40`, not 50.
4. A letter-grade scheme nobody asked for: A+ ≥ 90, A ≥ 80, B ≥ 70, C ≥ 60, D ≥ 50, E ≥ 40, else F.
5. Output is a printed text report (ranking table, grade histogram made of `#`), not a returned value.
6. Invented statistics: median, standard deviation, ranking with shared ranks for ties, per-subject top and bottom student.
7. A blank CSV cell means "mark missing" and is skipped instead of being an error or a zero.
8. Rounding: 2 decimals for averages, 0 decimals for pass rate — only in the printed text.
9. Invalid marks raise `ValueError` inside `load_csv`, but `main()` catches it and turns it into `sys.exit("Error: ...")`.

**Questions it should have asked and did not:**

1. What is the input — a plain list of numbers, or a file / table of students and subjects?
2. Which results do you need, and should they be returned (in what structure) or printed?
3. What is the pass mark, and does a mark equal to it pass?
4. What should happen with empty or invalid input?

It asked none of them first. It did end with "If you have specific requirements, such as a fixed
input format, weighted subjects or charts, tell me and I'll adapt it" — after 195 lines of code.

**Is the function named `analyze_marks` with the required signature?** no — there is no such
function. The file defines `grade_for`, `load_csv`, `rank_students`, `subject_stats`,
`print_report`, `main` and a `Student` dataclass. The closest thing, `subject_stats(students)`,
takes `Student` objects and has the pass mark hard-coded.

**First impression before testing** (one sentence — you will compare this with section 6 later):
It looks like the most impressive answer of the four — it runs and prints a tidy report — and it is useless for this task, because nothing in it can be called as `analyze_marks(marks, pass_mark)`.

---

## 3. Prompt B — structured context

**Prompt sent** (paste it in full, including any substitutions):

```
You are a Python developer. Implement analyze_marks(marks, pass_mark=50). Return
average, highest, lowest, and pass_rate in a dictionary. Accept marks from 0 to 100;
raise ValueError for an empty list, non-numeric values, or out-of-range values. Use
no external libraries. Return code plus a short explanation.
```

**What B fixed compared to A:**

1. The function exists with the exact name and signature, and `pass_mark` defaults to 50 — the harness could import and call it (A: no such function).
2. It returns a dictionary with exactly the four named keys instead of printing a report.
3. All three invalid inputs raise `ValueError` deliberately, before anything is computed (cases 4, 5, 6 PASS). `"60"` is rejected, not converted.
4. The scope collapsed from 195 lines (CSV, dataclass, grades, histogram) to 26 lines with no imports.

**What B still leaves open:**

1. **Rounding.** B says nothing about it, and the model chose *not* to round: case 1 returns `pass_rate=66.66666666666666`. It is a PASS only because the harness tolerates 0.01.
2. Whether `pass_rate` is a percentage or a 0–1 fraction, and whether a mark equal to `pass_mark` passes — the model guessed percentage and `>=`, and said so, but only *after* the code.
3. No tests were asked for, so none were written: the answer has one illustrative `>>>` example and the sentence "I have not run this code."
4. Edge types are left to the model: it decided on its own to reject `bool` and NaN and to accept any iterable.

---

## 4. Prompt C — examples and tests

**What I appended to Prompt B:**

```
Example: analyze_marks([40, 60, 80], 50) → average 60, highest 80, lowest 40,
pass_rate 66.67. Include tests for: one mark, decimals, custom pass_mark, empty list,
text value, and marks below 0 or above 100. State any remaining assumptions before
the code.
```

**Tests the AI wrote for itself** — how many, and which situations do they cover?

16 `unittest` test methods, in the same file as the function, guarded by `if __name__ == "__main__":`.

| Situation | Covered by the AI's tests? |
| --- | --- |
| one mark | yes — `test_one_mark_passing` (`[75]`), `test_one_mark_failing` (`[30]`) |
| decimals | yes — `test_decimals` (`[55.5, 70.25, 49.75]`) |
| custom pass_mark | yes — `test_custom_pass_mark` (70 → 33.33), `test_pass_mark_is_inclusive` (40 → 100.0) |
| empty list | yes — `test_empty_list` |
| text value | yes — `test_text_value` (`"sixty"`), `test_numeric_string_is_rejected` (`"60"`) |
| below 0 / above 100 | yes — `test_mark_below_zero` (−1), `test_mark_above_100` (100.5) |

Not asked for, added anyway: the spec example, 0 and 100 as valid boundaries, `bool`, NaN, invalid
`pass_mark`, and "input list is not mutated".

**Do the AI's own tests pass against the AI's own code?** yes — I ran `python code/prompt_c.py`:
`Ran 16 tests in 0.000s — OK`. The model itself had not run them; its answer says "I traced the
expected values by hand but have not executed the file in this session."

**Do they agree with the harness in section 6?** yes — 16/16 of its own tests and 6/6 harness cases.
There is no disagreement this time, but that is luck of the spec, not proof: its tests check its
own assumptions (for example, that `pass_mark=101` must raise), which the harness never asks about.
The clearest warning is in the discarded first attempt (section 1), where the model printed
"All tests passed." without having any way to run a test.

**Assumptions C stated explicitly before the code:**

Eight, numbered, before the code: (1) a pass is inclusive, `mark >= pass_mark`; (2) `average` and
`pass_rate` are rounded to 2 decimals, `pass_rate` is a percentage 0–100, `highest`/`lowest`
returned as given; (3) numeric means `int` or `float`, `bool` rejected, numeric strings rejected
not converted; (4) NaN and infinity rejected; (5) 0 and 100 are valid; (6) `pass_mark` must itself
be a number from 0 to 100 or `ValueError`; (7) `marks` must be a list or tuple, anything else is
`ValueError`; (8) "no external libraries" allows the standard library, so tests use `unittest`.

---

## 5. Prompt D — my combined prompt

**The complete prompt I wrote** (one message, sent to a fresh chat):

```
You are a Python developer. Write one Python 3 file using only the standard library.

Implement exactly this function:

    analyze_marks(marks, pass_mark=50)

It returns a dictionary with exactly these four keys: "average", "highest", "lowest", "pass_rate".
- average: the mean of the marks, rounded to 2 decimal places.
- highest, lowest: the largest and smallest mark, returned as given, not rounded.
- pass_rate: the percentage (0 to 100, not a 0 to 1 fraction) of marks that pass, rounded to 2 decimal places. A mark passes when mark >= pass_mark, so a mark equal to pass_mark passes.

Validation: check all input before computing anything, and raise ValueError (never another exception type, never a partial result) when:
- marks is empty;
- any value is not an int or a float. A numeric string such as "60" is an error and must not be converted. bool and NaN are errors too;
- any value is below 0 or above 100. 0 and 100 themselves are valid.
Do not add other error conditions: pass_mark is trusted as given, and marks may be a list or a tuple.

Worked examples:
analyze_marks([40, 60, 80], 50) returns {"average": 60.0, "highest": 80, "lowest": 40, "pass_rate": 66.67}
analyze_marks([49.9, 50, 70.25], 50) returns {"average": 56.72, "highest": 70.25, "lowest": 49.9, "pass_rate": 66.67}

Tests: put them in the same file under if __name__ == "__main__": using plain assert statements. Cover: one mark, decimals, custom pass_mark, a mark exactly equal to pass_mark, the 66.67 rounding, empty list, text value, numeric string, a mark below 0, a mark above 100. Importing the file must execute nothing and print nothing.

Scope: only this function and its tests. No CLI, no input(), no file or CSV reading, no classes, no letter grades, no extra statistics, no extra dictionary keys.

Answer format: first a short list of any assumptions you still had to make, then one Python code block containing the whole file, then at most three sentences of explanation.
```

**What I deliberately added that A, B and C did not have:**

1. An explicit rounding rule — `average` and `pass_rate` to 2 decimals, `highest`/`lowest` untouched, `pass_rate` a percentage — because B returned `66.66666666666666` and C only guessed rounding from the example.
2. The boundary rule in words (`mark >= pass_mark`, "a mark equal to pass_mark passes") plus a second worked example, `[49.9, 50, 70.25]`, that exercises the boundary, decimals and average rounding (56.72) at once. B and C got `>=` right, but only by guessing.
3. Decisions for every type edge the models had been deciding for me: `"60"` is an error and is not converted, `bool` and NaN are errors, 0 and 100 are valid.
4. A "do not add" list. From A: no CLI, `input()`, CSV, classes, grades, extra statistics, extra keys. From C: no extra error conditions — `pass_mark` is trusted, list or tuple accepted.
5. "Importing the file must execute nothing and print nothing", with the tests under `if __name__ == "__main__":` — because the harness imports the file, and Prompt A died at import.
6. An answer format: assumptions first, one code block, at most three sentences of explanation.

**The ambiguity I found in the specification, and how I resolved it inside Prompt D:**

**Rounding.** The task says the function returns `pass_rate`, and the example shows `66.67`, but
nowhere does the specification say "round to 2 decimal places". 2 of 3 marks passing is
66.666…%, so `66.67` is either the required return value or just how the example was printed — and
the same question applies to `average`. The models split on it: B returned
`pass_rate=66.66666666666666` and wrote "values are not rounded, so the caller decides how to
display them"; C saw the example and rounded to `66.67`. Both are PASS only because the harness
compares with a tolerance of 0.01, which hides the difference. A caller doing
`result["pass_rate"] == 66.67` would get `False` from B and `True` from C.

My resolution in Prompt D, in these words: "average: the mean of the marks, rounded to 2 decimal
places", "highest, lowest: … returned as given, not rounded", "pass_rate: the percentage (0 to 100,
not a 0 to 1 fraction) of marks that pass, rounded to 2 decimal places". D returned `66.67`.

---

## 6. Test results — the evidence

Six cases × four prompts. Verdicts are **PASS**, **FAIL** or **ERROR** only.

| # | Call | Required | A | B | C | D |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `analyze_marks([40, 60, 80], 50)` | avg 60 · high 80 · low 40 · rate 66.67 | ERROR | PASS | PASS | PASS |
| 2 | `analyze_marks([100], 50)` | avg 100 · high 100 · low 100 · rate 100 | ERROR | PASS | PASS | PASS |
| 3 | `analyze_marks([49.5, 50], 50)` | avg 49.75 · high 50 · low 49.5 · rate 50 | ERROR | PASS | PASS | PASS |
| 4 | `analyze_marks([], 50)` | raises ValueError | ERROR | PASS | PASS | PASS |
| 5 | `analyze_marks([40, "60"], 50)` | raises ValueError | ERROR | PASS | PASS | PASS |
| 6 | `analyze_marks([-1, 50, 101], 50)` | raises ValueError | ERROR | PASS | PASS | PASS |
| | **Totals** | | 0/6 | 6/6 | 6/6 | 6/6 |

**For every FAIL and ERROR above, one line: what was returned or raised instead.**

| Prompt | Case | What actually happened |
| --- | --- | --- |
| A | 1–6 | The harness stopped before case 1: `code\prompt_a.py could not be imported: AttributeError: 'NoneType' object has no attribute '__dict__'`. No case was called, so all six are ERROR. |
| A | 1–6 | Why it crashed: the file uses `@dataclass` together with `from __future__ import annotations`, and the harness loads it with `importlib` without registering the module in `sys.modules`, which `dataclasses` needs. Run directly (`python code/prompt_a.py`) the file works and prints its report. |
| A | 1–6 | It would be ERROR without the crash too: `grep analyze_marks code/prompt_a.py` finds nothing, so the harness's "defines no callable named 'analyze_marks'" branch would have fired instead. |

Not a FAIL, but the only place the three passing prompts differ in a returned value — case 1,
`pass_rate`: B `66.66666666666666`, C `66.67`, D `66.67`.

### Pasted terminal output — all four runs

> This is the part that makes the table above count. Paste the **whole** output, unedited,
> including the header lines. A table with nothing behind it is not accepted.

Run from `week-02/` with `PYTHONIOENCODING=utf-8` so that the `—` and `·` characters the harness
prints survive the Windows console.

**Prompt A**

```
ERROR: code\prompt_a.py could not be imported: AttributeError: 'NoneType' object has no attribute '__dict__'
The file must define analyze_marks and must not crash on import.
```

**Prompt B**

```
========================================================================
analyze_marks harness — code/prompt_b.py
tolerance for numeric comparison: 0.01
========================================================================
SIGNATURE: ok
------------------------------------------------------------------------
case 1  PASS   analyze_marks([40, 60, 80], 50)
          expect: average=60.0, highest=80, lowest=40, pass_rate=66.67
          got   : average=60.0, highest=80, lowest=40, pass_rate=66.66666666666666
------------------------------------------------------------------------
case 2  PASS   analyze_marks([100], 50)
          expect: average=100.0, highest=100, lowest=100, pass_rate=100.0
          got   : average=100.0, highest=100, lowest=100, pass_rate=100.0
------------------------------------------------------------------------
case 3  PASS   analyze_marks([49.5, 50], 50)
          expect: average=49.75, highest=50, lowest=49.5, pass_rate=50.0
          got   : average=49.75, highest=50, lowest=49.5, pass_rate=50.0
------------------------------------------------------------------------
case 4  PASS   analyze_marks([], 50)
          expect: ValueError
          got   : raised ValueError: marks must not be empty
------------------------------------------------------------------------
case 5  PASS   analyze_marks([40, '60'], 50)
          expect: ValueError
          got   : raised ValueError: non-numeric mark: '60'
------------------------------------------------------------------------
case 6  PASS   analyze_marks([-1, 50, 101], 50)
          expect: ValueError
          got   : raised ValueError: mark out of range 0-100: -1
------------------------------------------------------------------------
RESULT  6 PASS · 0 FAIL · 0 ERROR   (code/prompt_b.py)
========================================================================
```

**Prompt C**

```
========================================================================
analyze_marks harness — code/prompt_c.py
tolerance for numeric comparison: 0.01
========================================================================
SIGNATURE: ok
------------------------------------------------------------------------
case 1  PASS   analyze_marks([40, 60, 80], 50)
          expect: average=60.0, highest=80, lowest=40, pass_rate=66.67
          got   : average=60.0, highest=80, lowest=40, pass_rate=66.67
------------------------------------------------------------------------
case 2  PASS   analyze_marks([100], 50)
          expect: average=100.0, highest=100, lowest=100, pass_rate=100.0
          got   : average=100.0, highest=100, lowest=100, pass_rate=100.0
------------------------------------------------------------------------
case 3  PASS   analyze_marks([49.5, 50], 50)
          expect: average=49.75, highest=50, lowest=49.5, pass_rate=50.0
          got   : average=49.75, highest=50, lowest=49.5, pass_rate=50.0
------------------------------------------------------------------------
case 4  PASS   analyze_marks([], 50)
          expect: ValueError
          got   : raised ValueError: marks must not be empty
------------------------------------------------------------------------
case 5  PASS   analyze_marks([40, '60'], 50)
          expect: ValueError
          got   : raised ValueError: mark at index 1 is not numeric: '60'
------------------------------------------------------------------------
case 6  PASS   analyze_marks([-1, 50, 101], 50)
          expect: ValueError
          got   : raised ValueError: mark at index 0 is outside 0-100: -1
------------------------------------------------------------------------
RESULT  6 PASS · 0 FAIL · 0 ERROR   (code/prompt_c.py)
========================================================================
```

**Prompt D**

```
========================================================================
analyze_marks harness — code/prompt_d.py
tolerance for numeric comparison: 0.01
========================================================================
SIGNATURE: ok
------------------------------------------------------------------------
case 1  PASS   analyze_marks([40, 60, 80], 50)
          expect: average=60.0, highest=80, lowest=40, pass_rate=66.67
          got   : average=60.0, highest=80, lowest=40, pass_rate=66.67
------------------------------------------------------------------------
case 2  PASS   analyze_marks([100], 50)
          expect: average=100.0, highest=100, lowest=100, pass_rate=100.0
          got   : average=100.0, highest=100, lowest=100, pass_rate=100.0
------------------------------------------------------------------------
case 3  PASS   analyze_marks([49.5, 50], 50)
          expect: average=49.75, highest=50, lowest=49.5, pass_rate=50.0
          got   : average=49.75, highest=50, lowest=49.5, pass_rate=50.0
------------------------------------------------------------------------
case 4  PASS   analyze_marks([], 50)
          expect: ValueError
          got   : raised ValueError: marks must not be empty
------------------------------------------------------------------------
case 5  PASS   analyze_marks([40, '60'], 50)
          expect: ValueError
          got   : raised ValueError: mark must be an int or a float: '60'
------------------------------------------------------------------------
case 6  PASS   analyze_marks([-1, 50, 101], 50)
          expect: ValueError
          got   : raised ValueError: mark must be between 0 and 100: -1
------------------------------------------------------------------------
RESULT  6 PASS · 0 FAIL · 0 ERROR   (code/prompt_d.py)
========================================================================
```

---

## 7. Scoring

0–2 per criterion, using the rubric in `README.md` Part 7.

| Criterion | A | B | C | D |
| --- | --- | --- | --- | --- |
| Correctness (cases passed) | 0 | 2 | 2 | 2 |
| Requirement coverage | 0 | 2 | 2 | 2 |
| Verifiability (tests) | 0 | 0 | 2 | 2 |
| Assumptions stated | 1 | 1 | 2 | 2 |
| Noise (2 = none) | 0 | 2 | 1 | 2 |
| **Total / 10** | 1 | 7 | 9 | 10 |

Why each score that is not obvious from section 6:

- **Assumptions — A 1, B 1.** Both name some assumptions, but *after* the code: A's closing paragraph (constants, blank cells), B's bullets (percentage, `>=`, no rounding). C and D list them before the code, as asked.
- **Verifiability — B 0.** One `>>>` example that the model says it did not run is not a test. C: 16 `unittest` tests, all pass, cover cases 4–6. D: 23 `assert` statements, one of them looping over 19 invalid inputs (41 checks); `python code/prompt_d.py` prints `All tests passed.`
- **Noise — C 1.** C invented behaviour: `ValueError` when `pass_mark` is outside 0–100, and `ValueError` for any `marks` that is not a list or tuple. Neither is in the specification.
- **Noise — D 2, with a reservation.** Only the function and its tests, no extra keys or error rules. But it ignored "marks may be a list or a tuple" and accepts any iterable, and its test list is much longer than the ten situations I named. I kept the 2 because the rubric's noise is unrequested *scope*, and there is none.

**Prompt length, in words:** A 7 · B 44 · C 83 · D 323 (counted with `wc -w`)

**Words added per point gained** — B over A, C over B, D over C. One line on what that ratio says:

B over A: 37 words for 6 points ≈ 6 words per point · C over B: 39 words for 2 points ≈ 20 words per point · D over C: 240 words for 1 point = 240 words per point. The first 44 words did almost all the work; after that every point cost roughly ten times more words than the one before, and the last 240 words changed no test verdict at all.

---

## 8. Conclusion — 150–200 words

Answer in this order: (1) which prompt scored best, and whether it is the one you would actually
use at work; (2) which single addition bought the most correctness, naming the exact case that
changed verdict; (3) what was pure noise; (4) the ambiguity and your resolution.

Name test cases and real returned values. "More detailed prompts work better" scores zero.

```
By score Prompt D wins with 10/10, then C 9, B 7, A 1. At work I would still send C: D cost 240 more words for one rubric point and changed no test verdict.

The single addition that bought the most correctness was B's exact signature and key names. Prompt A returned a 195-line CSV report script with PASS_MARK = 40 and no function called analyze_marks; the harness stopped at import, so cases 1-6 are all ERROR. With B the same six cases are all PASS. Nothing added after B changed a verdict: B, C and D are all 6/6.

Pure noise: C invented a ValueError for a pass_mark outside 0-100 and rejected any input that was not a list or tuple. D tested complex numbers, None and infinity, which I never listed.

The ambiguity is rounding. The specification shows pass_rate 66.67 but never says "round". B returned 66.66666666666666 for case 1 and passed only because the harness tolerates 0.01; C guessed rounding from the example. In D I wrote it out: average and pass_rate rounded to 2 decimals, pass_rate a percentage, highest and lowest untouched. D returned 66.67.
```

**Word count:** 190 (counted with `wc -w`)

---

## 9. Two questions for the debrief

Written before class, answered in class.

1. B returned `pass_rate=66.66666666666666` and still got PASS on case 1 because the harness tolerates 0.01. Is the tolerance part of the specification? If it is not, was B actually correct — and who decides: the prose, the example, or the test?
2. B, C and D were all 6/6 with this model, so the six cases could not separate a 44-word prompt from a 323-word one. How do we know when a test suite is too weak to measure the thing we are changing — and would a weaker model have shown the differences that Fable 5.1 hid?
