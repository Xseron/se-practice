# Week 01 — Manual vs AI: Comparison

**Name:** David Torossyan 
**Group:** Monday 16-19
**Date:** 08.09.2026

---

## 1. Facts

| | Manual (Part 1) | Rocket (Part 2) |
| --- | --- | --- |
| Language / stack used | python | python |
| Time to first version that ran | 5min | 1min |
| Time to all 4 test cases passing | 30 min | 5 min |
| Number of attempts / prompts needed | 1 | 1 |
| Lines of code you actually wrote | all | none |
| Did it handle invalid marks (case B)? | yes | yes |
| Did it handle an empty list (case D)? | yes | yes |
| Did it use the ≥ 50 pass threshold? | yes | yes |
| Output format matches the spec? | yes | yes |
| Can you explain every line of it? | yes | no |

## 2. Test results

| Case | Input | Manual output | Rocket output | Spec says | Match? |
| --- | --- | --- | --- | --- | --- |
| A | `85, 23, 45, 90, 92` | pass | pass | avg 67.00 · high 92 · low 23 · pass 60.0% | |
| B | `88, 47, -5, 101, abc, 73, 50, , 100` | pass | pass | avg 71.60 · high 100 · low 47 · pass 80.0% | |
| C | `10, 20, 30` | pass | pass | avg 20.00 · high 30 · low 10 · pass 0.0% | |
| D | `abc, , xyz` | pass | pass | clear message, no crash | |

## 3. What the AI added that I never asked for

<!-- Tech stack, UI, extra features, a pass threshold it invented, styling, etc. -->

-
- A **pass threshold of 60** — invented silently, never marked as an assumption, and wrong for KBTU
- A **letter-grade scale** (A/B/C/D/F at 90/80/70/60/0) — a whole feature nobody requested
- An **ASCII bar chart** of every mark and a decorated `=====` report banner
- A **choice of stack and input format**: Python, comma-separated string from `sys.argv[1]`, with a
  hard-coded default list. My prompt never said how marks arrive
- Then the opposite problem in v3: once I specified an output format, it **deleted** the letter
  grades and the histogram without asking, including behaviour I might have wanted to keep

## 4. What the AI got wrong or silently skipped

<!-- Be concrete: input, expected, actual. -->

- **No validation at all in v1.** Input `88, 47, -5, 101, abc, 73, 50, , 100` → expected 5 valid
  marks, got a traceback (`ValueError: invalid literal for int() with base 10: 'abc'`, exit 1). The
  word "valid" was not in my prompt, so the concept did not exist in the code
- **Out-of-range marks counted as real in v2.** Same input → expected 5 · 71.60 · 100 · 47 · 80.0%,
  got 7 · 64.86 · **101** · **-5** · 57.1%. No warning, exit code 0
- **Wrong pass threshold, invisible on my test data.** 60 instead of 50 in v1 and v2, hidden by the
  fact that cases A and C have no marks between 50 and 59
- **It never asked a single clarifying question.** It read the README and started generating. Rocket
  at least scores prompt completeness and interrogates you first; this tool just guesses and the
  guesses look confident

## 5. The defect I asked Rocket to fix

**Prompt I used:**

```
The program crashes when the list contains text or empty values.
Skip the entries that are not numbers, and print a clear message
instead of statistics when the list has no usable marks at all
```

**Result:** partly fixed — and it made the program *more* dangerous. The crash is gone (case D now
prints a message, exit 0), but `-5` and `101` are numbers, so they survived the filter: case B went
from a loud traceback to a quiet wrong answer, 7 valid marks and a 57.1% pass rate that looks
completely plausible on screen

**What this tells me:** the model fixed exactly the symptom I described and did not look one step
further. It never asked "what actually counts as a valid mark?" — and that is the question the whole
task turns on. A traceback tells you something is broken; a wrong number does not

---

## 6. Reflection (200–300 words)

Answer all four, in your own words:

1. Which parts of the work did the AI genuinely speed up?

in easy tasks

2. Where did the AI cost you time, or give you something that looked right but was not?

it maked my code too much 

3. Which of these two artefacts would you be willing to put your name on, and why?

manual, its beautiful

4. What must a human engineer still be responsible for after this experiment?

yes

<!-- Write your reflection below this line -->


The AI genuinely saved time on everything that was mechanical. v1 ran on the first try in under a
minute — parsing, formatting, `max`/`min`, the printing layout, all correct and readable. My own
first version took five minutes and did not work at all, because `split()` without an argument left
commas glued to the numbers. On typing speed it is not a fair contest.

Where it cost me time was verification. Cases A and C passed with the wrong pass threshold of 60,
purely because neither input has a mark between 50 and 59. That is the thing that scared me: the
program looked correct, and it was only correct by accident on the data I happened to try. I found
it by reading the source, not by running it. The v2 fix was worse in a way — I reported a crash, it
removed the crash, and case B started returning 57.1% instead of 80.0% with a clean exit code.

I would put my name on the manual version, and on `v3_spec.py` only because I read every line of it
and wrote the tests it passes. The difference is not who typed it; it is whether I can say why each
rule is there.

What stays with me: the AI never once asked what a valid mark is. All three defects — no range
check, the invented threshold, the half-fix — come from requirements I did not state. The engineer
still owns the specification, the test cases that cover the boundaries (50, 0, 100, 101), and the
decision that the output is actually right. The AI writes code; it does not know what "correct"
means here.
