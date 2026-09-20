# analyze_marks.py
import unittest


def _is_number(value):
    """True for int/float, but not bool (bool is a subclass of int)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def analyze_marks(marks, pass_mark=50):
    """Return average, highest, lowest and pass_rate (%) for a list of marks.

    Raises ValueError for an empty list, non-numeric values, or values
    outside 0-100 (the same rules apply to pass_mark).
    """
    if not isinstance(marks, (list, tuple)):
        raise ValueError("marks must be a list or tuple of numbers")
    if len(marks) == 0:
        raise ValueError("marks must not be empty")
    if not _is_number(pass_mark) or not 0 <= pass_mark <= 100:
        raise ValueError(f"pass_mark must be a number from 0 to 100, got {pass_mark!r}")

    for index, mark in enumerate(marks):
        if not _is_number(mark):
            raise ValueError(f"mark at index {index} is not numeric: {mark!r}")
        if not 0 <= mark <= 100:  # also rejects NaN and +/-inf
            raise ValueError(f"mark at index {index} is outside 0-100: {mark!r}")

    count = len(marks)
    passed = sum(1 for mark in marks if mark >= pass_mark)

    return {
        "average": round(sum(marks) / count, 2),
        "highest": max(marks),
        "lowest": min(marks),
        "pass_rate": round(passed / count * 100, 2),
    }


class TestAnalyzeMarks(unittest.TestCase):
    def test_example_from_spec(self):
        self.assertEqual(
            analyze_marks([40, 60, 80], 50),
            {"average": 60, "highest": 80, "lowest": 40, "pass_rate": 66.67},
        )

    def test_one_mark_passing(self):
        self.assertEqual(
            analyze_marks([75]),
            {"average": 75, "highest": 75, "lowest": 75, "pass_rate": 100.0},
        )

    def test_one_mark_failing(self):
        self.assertEqual(analyze_marks([30])["pass_rate"], 0.0)

    def test_decimals(self):
        result = analyze_marks([55.5, 70.25, 49.75])
        self.assertAlmostEqual(result["average"], 58.5)
        self.assertEqual(result["highest"], 70.25)
        self.assertEqual(result["lowest"], 49.75)
        self.assertEqual(result["pass_rate"], 66.67)

    def test_custom_pass_mark(self):
        self.assertEqual(analyze_marks([40, 60, 80], pass_mark=70)["pass_rate"], 33.33)

    def test_pass_mark_is_inclusive(self):
        self.assertEqual(analyze_marks([40, 60, 80], pass_mark=40)["pass_rate"], 100.0)

    def test_boundary_marks_are_valid(self):
        result = analyze_marks([0, 100])
        self.assertEqual((result["lowest"], result["highest"]), (0, 100))

    def test_empty_list(self):
        with self.assertRaises(ValueError):
            analyze_marks([])

    def test_text_value(self):
        with self.assertRaises(ValueError):
            analyze_marks([50, "sixty", 70])

    def test_numeric_string_is_rejected(self):
        with self.assertRaises(ValueError):
            analyze_marks([50, "60", 70])

    def test_bool_is_rejected(self):
        with self.assertRaises(ValueError):
            analyze_marks([50, True])

    def test_mark_below_zero(self):
        with self.assertRaises(ValueError):
            analyze_marks([50, -1])

    def test_mark_above_100(self):
        with self.assertRaises(ValueError):
            analyze_marks([50, 100.5])

    def test_nan_is_rejected(self):
        with self.assertRaises(ValueError):
            analyze_marks([50, float("nan")])

    def test_invalid_pass_mark(self):
        for bad in (-1, 101, "50", None):
            with self.assertRaises(ValueError):
                analyze_marks([50, 60], pass_mark=bad)

    def test_input_not_mutated(self):
        marks = [80, 40, 60]
        analyze_marks(marks)
        self.assertEqual(marks, [80, 40, 60])


if __name__ == "__main__":
    unittest.main()
