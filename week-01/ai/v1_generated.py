"""
Student marks processor.

Generated from the prompt:
    "Build a small program that processes a list of student marks and prints:
     average, highest, lowest, and pass rate."

Nothing else was specified, so the passing threshold, the input format, the
letter grades and the histogram below are choices the generator made on its own.
"""

import sys

PASS_MARK = 60          # not requested anywhere - picked by the generator
GRADE_SCALE = [(90, "A"), (80, "B"), (70, "C"), (60, "D"), (0, "F")]

DEFAULT_MARKS = "85, 23, 45, 90, 92"


def parse_marks(raw: str) -> list:
    """Turn a comma-separated string into a list of marks."""
    return [int(part.strip()) for part in raw.split(",")]


def letter_grade(mark: int) -> str:
    for threshold, letter in GRADE_SCALE:
        if mark >= threshold:
            return letter
    return "F"


def report(marks: list) -> None:
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
        print(f"  {mark:>3}  {letter_grade(mark)}  {'#' * (mark // 5)}")
    print("=" * 34)


def main() -> None:
    raw = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MARKS
    report(parse_marks(raw))


if __name__ == "__main__":
    main()
