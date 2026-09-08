"""
Student marks processor - version 3.

Third prompt, this time carrying the requirements from Part 1 that the
one-line prompt never mentioned: what counts as a valid mark (a number
0-100 inclusive), that everything else is ignored rather than fatal, that
the pass threshold is 50, and the exact output format.

Run:  python v3_spec.py "88, 47, -5, 101, abc, 73, 50, , 100"
Test: python v3_spec.py test
"""

import sys

PASS_MARK = 50          # from the specification this time, not invented
MIN_MARK = 0
MAX_MARK = 100


def parse_marks(raw: str) -> list:
    """Keep only the entries that are numbers in [0, 100]; ignore the rest."""
    marks = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            value = float(part)
        except ValueError:
            continue
        if MIN_MARK <= value <= MAX_MARK:
            marks.append(int(value) if value.is_integer() else value)
    return marks


def report(marks: list) -> str:
    if not marks:
        return "No valid marks found (a valid mark is a number from 0 to 100)."

    average = sum(marks) / len(marks)
    pass_rate = sum(1 for m in marks if m >= PASS_MARK) / len(marks) * 100

    return "\n".join([
        f"Valid marks: {len(marks)}",
        f"Average    : {average:.2f}",
        f"Highest    : {max(marks)}",
        f"Lowest     : {min(marks)}",
        f"Pass rate  : {pass_rate:.1f}%",
    ])


CASES = [
    ("A", "85, 23, 45, 90, 92",
     "Valid marks: 5\nAverage    : 67.00\nHighest    : 92\nLowest     : 23\nPass rate  : 60.0%"),
    ("B", "88, 47, -5, 101, abc, 73, 50, , 100",
     "Valid marks: 5\nAverage    : 71.60\nHighest    : 100\nLowest     : 47\nPass rate  : 80.0%"),
    ("C", "10, 20, 30",
     "Valid marks: 3\nAverage    : 20.00\nHighest    : 30\nLowest     : 10\nPass rate  : 0.0%"),
    ("D", "abc, , xyz",
     "No valid marks found (a valid mark is a number from 0 to 100)."),
]


def run_tests() -> int:
    failed = 0
    for name, raw, expected in CASES:
        actual = report(parse_marks(raw))
        if actual == expected:
            print(f"case {name}: PASS")
        else:
            failed += 1
            print(f"case {name}: FAIL\n--- expected ---\n{expected}\n--- actual ---\n{actual}")
    print(f"\n{len(CASES) - failed}/{len(CASES)} passed")
    return failed


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        sys.exit(1 if run_tests() else 0)
    raw = sys.argv[1] if len(sys.argv) > 1 else input("Marks: ")
    print(report(parse_marks(raw)))


if __name__ == "__main__":
    main()
