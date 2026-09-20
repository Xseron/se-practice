Here's a self-contained script that uses only the standard library. I haven't run it here. It reads marks from a CSV file, or uses built-in sample data if you don't give it one, and prints a report.

```python
"""Student marks analyzer.

Usage:
    python marks.py              # runs on built-in sample data
    python marks.py marks.csv    # runs on your CSV

CSV format (first column = student name, remaining columns = subjects):
    Name,Math,Physics,English
    Alice,92,88,79
    Bob,45,38,61
"""
from __future__ import annotations

import csv
import statistics
import sys
from collections import Counter
from dataclasses import dataclass

MAX_MARK = 100
PASS_MARK = 40
GRADE_BOUNDARIES = [(90, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D"), (40, "E")]


def grade_for(score: float) -> str:
    for boundary, letter in GRADE_BOUNDARIES:
        if score >= boundary:
            return letter
    return "F"


@dataclass
class Student:
    name: str
    marks: dict[str, float]

    @property
    def total(self) -> float:
        return sum(self.marks.values())

    @property
    def average(self) -> float:
        return self.total / len(self.marks) if self.marks else 0.0

    @property
    def grade(self) -> str:
        return grade_for(self.average)

    @property
    def failed_subjects(self) -> list[str]:
        return [subj for subj, mark in self.marks.items() if mark < PASS_MARK]


def load_csv(path: str) -> list[Student]:
    students: list[Student] = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or len(reader.fieldnames) < 2:
            raise ValueError("CSV needs a name column plus at least one subject column")
        name_col, *subjects = reader.fieldnames

        for line_no, row in enumerate(reader, start=2):
            name = (row[name_col] or "").strip()
            if not name:
                continue
            marks: dict[str, float] = {}
            for subject in subjects:
                raw = (row[subject] or "").strip()
                if not raw:          # blank cell = mark missing, skip it
                    continue
                try:
                    mark = float(raw)
                except ValueError:
                    raise ValueError(
                        f"Line {line_no}: invalid mark {raw!r} for {subject}"
                    ) from None
                if not 0 <= mark <= MAX_MARK:
                    raise ValueError(
                        f"Line {line_no}: mark {mark} for {subject} is outside 0-{MAX_MARK}"
                    )
                marks[subject] = mark
            students.append(Student(name, marks))
    return students


def rank_students(students: list[Student]) -> list[tuple[int, Student]]:
    """Rank by average, highest first. Tied students share a rank (1, 2, 2, 4)."""
    ordered = sorted(students, key=lambda s: s.average, reverse=True)
    ranked: list[tuple[int, Student]] = []
    for i, student in enumerate(ordered):
        if i > 0 and student.average == ordered[i - 1].average:
            rank = ranked[-1][0]
        else:
            rank = i + 1
        ranked.append((rank, student))
    return ranked


def subject_stats(students: list[Student]) -> dict[str, dict]:
    subjects: list[str] = []
    for s in students:
        for subj in s.marks:
            if subj not in subjects:
                subjects.append(subj)

    stats: dict[str, dict] = {}
    for subj in subjects:
        entries = [(s.marks[subj], s.name) for s in students if subj in s.marks]
        values = [mark for mark, _ in entries]
        top = max(entries, key=lambda e: e[0])
        low = min(entries, key=lambda e: e[0])
        stats[subj] = {
            "count": len(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "stdev": statistics.stdev(values) if len(values) > 1 else 0.0,
            "highest": top,
            "lowest": low,
            "pass_rate": 100 * sum(v >= PASS_MARK for v in values) / len(values),
        }
    return stats


def print_report(students: list[Student]) -> None:
    if not students:
        print("No student data found.")
        return

    line = "-" * 62

    print("\nSTUDENT RANKING")
    print(line)
    print(f"{'Rank':<6}{'Name':<20}{'Total':>8}{'Average':>10}{'Grade':>8}")
    print(line)
    for rank, s in rank_students(students):
        print(f"{rank:<6}{s.name:<20}{s.total:>8.1f}{s.average:>10.2f}{s.grade:>8}")

    print("\nSUBJECT STATISTICS")
    print(line)
    for subj, st in subject_stats(students).items():
        print(f"{subj}  (n={st['count']})")
        print(f"   mean {st['mean']:.2f} | median {st['median']:.1f} | "
              f"std dev {st['stdev']:.2f} | pass rate {st['pass_rate']:.0f}%")
        print(f"   highest: {st['highest'][0]:.0f} ({st['highest'][1]})   "
              f"lowest: {st['lowest'][0]:.0f} ({st['lowest'][1]})")

    print("\nGRADE DISTRIBUTION")
    print(line)
    counts = Counter(s.grade for s in students)
    for _, letter in GRADE_BOUNDARIES + [(0, "F")]:
        n = counts.get(letter, 0)
        print(f"{letter:<4}{'#' * n} {n}")

    print("\nSTUDENTS WITH FAILED SUBJECTS")
    print(line)
    failing = [s for s in students if s.failed_subjects]
    if failing:
        for s in failing:
            detail = ", ".join(f"{subj} ({s.marks[subj]:.0f})" for subj in s.failed_subjects)
            print(f"{s.name}: {detail}")
    else:
        print("None - everyone passed every subject.")

    averages = [s.average for s in students]
    print("\nCLASS SUMMARY")
    print(line)
    print(f"Students: {len(students)}")
    print(f"Class average: {statistics.mean(averages):.2f}")
    print(f"Best average:  {max(averages):.2f}")
    print(f"Worst average: {min(averages):.2f}")


SAMPLE_DATA = [
    Student("Alice",   {"Math": 92, "Physics": 88, "English": 79}),
    Student("Bob",     {"Math": 45, "Physics": 38, "English": 61}),
    Student("Charlie", {"Math": 73, "Physics": 67, "English": 85}),
    Student("Diana",   {"Math": 98, "Physics": 95, "English": 91}),
    Student("Ethan",   {"Math": 32, "Physics": 41, "English": 36}),
    Student("Fatima",  {"Math": 81, "Physics": 77, "English": 88}),
]


def main() -> None:
    if len(sys.argv) > 1:
        try:
            students = load_csv(sys.argv[1])
        except (OSError, ValueError) as exc:
            sys.exit(f"Error: {exc}")
    else:
        students = SAMPLE_DATA
    print_report(students)


if __name__ == "__main__":
    main()
```

The report shows:
- **Ranking:** each student's total, average and letter grade, with tied students sharing a rank.
- **Subject statistics:** mean, median, standard deviation and pass rate, plus who scored highest and lowest.
- **Grade distribution:** a simple text histogram.
- **Failed subjects:** which students scored below the pass mark, and in what.
- **Class summary:** overall average and the best and worst student averages.

The constants `PASS_MARK`, `MAX_MARK` and `GRADE_BOUNDARIES` at the top set the grading scheme. A blank cell in the CSV counts as a missing mark and is left out of that student's average, not counted as zero. A non-numeric or out-of-range mark stops the script with an error that names the line.

If you have specific requirements, such as a fixed input format, weighted subjects or charts, tell me and I'll adapt it.