"""
Student marks processor - version 2.

Follow-up prompt that produced this file:
    "The program crashes when the list contains text or empty values.
     Skip the entries that are not numbers, and print a clear message
     instead of statistics when the list has no usable marks at all."

Only the crash was reported, so only the crash was fixed: the invented pass
threshold of 60 and the missing 0-100 range check are still here.
"""

import sys

PASS_MARK = 60          # still the generator's own choice
GRADE_SCALE = [(90, "A"), (80, "B"), (70, "C"), (60, "D"), (0, "F")]

DEFAULT_MARKS = "85, 23, 45, 90, 92"


def parse_marks(raw: str) -> list:
    """Turn a comma-separated string into a list of marks, skipping junk."""
    marks = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            marks.append(int(part))
        except ValueError:
            continue
    return marks


def letter_grade(mark: int) -> str:
    for threshold, letter in GRADE_SCALE:
        if mark >= threshold:
            return letter
    return "F"


def report(marks: list) -> None:
    if not marks:
        print("No usable marks were found in the input - nothing to report.")
        return

    average = sum(marks) / len(marks)
    passed = [m for m in marks if m >= PASS_MARK]
    pass_rate = len(passed) / len(marks) * 100

    print("=" * 34)
    print("      STUDENT MARKS REPORT")
    print("=" * 34)
    print(f"Total marks : {len(marks)}")
    print(f"Average     : {average:.2f}")
    print(f"Highest     : {max(marks)}")
    print(f"Lowest      : {min(marks)}")
    print(f"Pass rate   : {pass_rate:.1f}%")
    print("-" * 34)
    print("Distribution:")
    for mark in marks:
        print(f"  {mark:>3}  {letter_grade(mark)}  {'#' * max(mark // 5, 0)}")
    print("=" * 34)


def main() -> None:
    raw = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MARKS
    report(parse_marks(raw))


if __name__ == "__main__":
    main()
