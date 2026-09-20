"""Statistics for a collection of marks (0-100)."""

import math


def analyze_marks(marks, pass_mark=50):
    """Return average, highest, lowest and pass_rate for the given marks.

    Raises ValueError if marks is empty, or if any value is not an int/float
    (bool, NaN and numeric strings are rejected), or lies outside 0..100.
    """
    # Materialise once so that every later step works on the same values.
    try:
        values = list(marks)
    except TypeError:
        raise ValueError("marks must be a list or tuple of numbers") from None

    if not values:
        raise ValueError("marks must not be empty")

    # Validate everything before computing anything.
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"mark must be an int or a float: {value!r}")
        if isinstance(value, float) and math.isnan(value):
            raise ValueError("mark must not be NaN")
        if not (0 <= value <= 100):
            raise ValueError(f"mark must be between 0 and 100: {value!r}")

    count = len(values)
    passed = sum(1 for value in values if value >= pass_mark)

    return {
        "average": round(math.fsum(values) / count, 2),
        "highest": max(values),
        "lowest": min(values),
        "pass_rate": round(passed * 100 / count, 2),
    }


if __name__ == "__main__":
    KEYS = {"average", "highest", "lowest", "pass_rate"}

    # Worked examples (the first one also covers the 66.67 rounding).
    assert analyze_marks([40, 60, 80], 50) == {
        "average": 60.0, "highest": 80, "lowest": 40, "pass_rate": 66.67}
    assert analyze_marks([49.9, 50, 70.25], 50) == {
        "average": 56.72, "highest": 70.25, "lowest": 49.9, "pass_rate": 66.67}

    # Exactly the four keys, nothing else.
    assert set(analyze_marks([40, 60, 80])) == KEYS
    assert len(analyze_marks([40, 60, 80])) == 4

    # One mark.
    assert analyze_marks([75]) == {
        "average": 75.0, "highest": 75, "lowest": 75, "pass_rate": 100.0}
    assert analyze_marks([10]) == {
        "average": 10.0, "highest": 10, "lowest": 10, "pass_rate": 0.0}

    # Decimals: average is rounded, highest/lowest are returned as given.
    result = analyze_marks([70.256, 33.333])
    assert result["average"] == 51.79
    assert result["highest"] == 70.256
    assert result["lowest"] == 33.333
    assert result["pass_rate"] == 50.0

    # Custom pass_mark.
    assert analyze_marks([40, 60, 80], 70)["pass_rate"] == 33.33
    assert analyze_marks([40, 60, 80], 30)["pass_rate"] == 100.0
    assert analyze_marks([40, 60, 80], 90)["pass_rate"] == 0.0
    assert analyze_marks([40, 60, 80], pass_mark=60)["pass_rate"] == 66.67

    # A mark exactly equal to pass_mark passes; just below does not.
    assert analyze_marks([50], 50)["pass_rate"] == 100.0
    assert analyze_marks([49.99], 50)["pass_rate"] == 0.0
    assert analyze_marks([72.5, 72.5], 72.5)["pass_rate"] == 100.0

    # 66.67 / 33.33 rounding, and pass_rate is a percentage, not a fraction.
    assert analyze_marks([10, 50, 90])["pass_rate"] == 66.67
    assert analyze_marks([10, 20, 90])["pass_rate"] == 33.33
    assert analyze_marks([10, 90])["pass_rate"] == 50.0

    # Boundaries 0 and 100 are valid; tuples are accepted.
    assert analyze_marks([0, 100]) == {
        "average": 50.0, "highest": 100, "lowest": 0, "pass_rate": 50.0}
    assert analyze_marks((40, 60, 80), 50) == analyze_marks([40, 60, 80], 50)

    # Invalid input: must raise ValueError and nothing else.
    bad_inputs = [
        [],                      # empty list
        (),                      # empty tuple
        [50, "abc"],             # text value
        [50, "60"],              # numeric string, must not be converted
        ["60"],
        [-1, 50],                # below 0
        [-0.01],
        [50, 101],               # above 100
        [100.01],
        [10, 20, 30, 40, 150],   # bad value at the very end
        [True, 50],              # bool
        [False],
        [float("nan"), 50],      # NaN
        [float("inf")],
        [float("-inf")],
        [None],
        [[50]],
        [50, 3 + 4j],
        None,                    # not iterable at all
    ]
    for bad in bad_inputs:
        raised = False
        try:
            analyze_marks(bad)
        except ValueError:
            raised = True
        assert raised, f"expected ValueError for {bad!r}"

    print("All tests passed.")
