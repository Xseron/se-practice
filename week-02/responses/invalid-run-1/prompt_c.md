I'll write the function and tests to a file, run them, and then report the code with assumptions.


<invoke name="Write">
<parameter name="file_path">C:\Temp\claude\c--David-uni-se-se-practice\0b1f89dd-c08c-4333-97c4-951ac61b535a\scratchpad\run_c\analyze_marks.py</parameter>
<parameter name="content">"""Compute summary statistics for a list of student marks."""


def analyze_marks(marks, pass_mark=50):
    """Return average, highest, lowest and pass_rate for a list of marks.

    Args:
        marks: A list (or other iterable) of numeric marks, each between 0 and 100
            inclusive.
        pass_mark: The minimum mark counted as a pass (default 50). A mark equal
            to pass_mark is a pass.

    Returns:
        A dict with keys "average", "highest", "lowest" and "pass_rate".
        "average" and "pass_rate" are floats rounded to 2 decimal places;
        "pass_rate" is a percentage from 0 to 100. "highest" and "lowest" are
        returned as given (int stays int, float stays float).

    Raises:
        ValueError: If marks is empty, contains a non-numeric value (bool counts
            as non-numeric), or contains a value outside 0..100.
    """
    marks = list(marks)
    if not marks:
        raise ValueError("marks must not be empty")

    for index, mark in enumerate(marks):
        # bool is a subclass of int, so exclude it explicitly.
        if isinstance(mark, bool) or not isinstance(mark, (int, float)):
            raise ValueError(
                f"mark at index {index} is not numeric: {mark!r}"
            )
        if mark != mark:  # NaN check without importing math
            raise ValueError(f"mark at index {index} is NaN")
        if not 0 <= mark <= 100:
            raise ValueError(
                f"mark at index {index} is out of range 0-100: {mark!r}"
            )

    total = len(marks)
    passed = sum(1 for mark in marks if mark >= pass_mark)

    return {
        "average": round(sum(marks) / total, 2),
        "highest": max(marks),
        "lowest": min(marks),
        "pass_rate": round(passed * 100 / total, 2),
    }


# --------------------------------------------------------------------------- #
# Tests (run with:  python analyze_marks.py)
# --------------------------------------------------------------------------- #

def _expect_error(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except ValueError:
        return True
    return False


def run_tests():
    # Example from the spec.
    assert analyze_marks([40, 60, 80], 50) == {
        "average": 60.0,
        "highest": 80,
        "lowest": 40,
        "pass_rate": 66.67,
    }

    # One mark: average, highest and lowest all equal it; pass_rate is 100 or 0.
    assert analyze_marks([73]) == {
        "average": 73.0,
        "highest": 73,
        "lowest": 73,
        "pass_rate": 100.0,
    }
    assert analyze_marks([20])["pass_rate"] == 0.0

    # Decimal marks.
    result = analyze_marks([49.5, 50.25, 99.9])
    assert result["average"] == 66.55
    assert result["highest"] == 99.9
    assert result["lowest"] == 49.5
    assert result["pass_rate"] == 66.67

    # Custom pass_mark; a mark equal to pass_mark counts as a pass.
    assert analyze_marks([40, 60, 80], pass_mark=70)["pass_rate"] == 33.33
    assert analyze_marks([40, 60, 80], pass_mark=60)["pass_rate"] == 66.67
    assert analyze_marks([40, 60, 80], pass_mark=0)["pass_rate"] == 100.0

    # Boundary values 0 and 100 are accepted.
    assert analyze_marks([0, 100]) == {
        "average": 50.0,
        "highest": 100,
        "lowest": 0,
        "pass_rate": 50.0,
    }

    # Empty list.
    assert _expect_error(analyze_marks, [])

    # Text value (and other non-numeric types).
    assert _expect_error(analyze_marks, [50, "60", 70])
    assert _expect_error(analyze_marks, [None])
    assert _expect_error(analyze_marks, [True, 50])

    # Out of range.
    assert _expect_error(analyze_marks, [-1, 50])
    assert _expect_error(analyze_marks, [50, 101])
    assert _expect_error(analyze_marks, [100.01])
    assert _expect_error(analyze_marks, [float("nan")])

    print("All tests passed.")


if __name__ == "__main__":
    run_tests()
</parameter>
</invoke>



<invoke name="Bash">
<parameter name="command">cd "C:\Temp\claude\c--David-uni-se-se-practice\0b1f89dd-c08c-4333-97c4-951ac61b535a\scratchpad\run_c" && python analyze_marks.py</parameter>
<parameter name="description">Run analyze_marks tests</parameter>
</invoke>



<invoke name="Bash">
<parameter name="command">cd "C:\Temp\claude\c--David-uni-se-se-practice\0b1f89dd-c08c-4333-97c4-951ac61b535a\scratchpad\run_c" && python analyze_marks.py; echo "exit=$?"</parameter>
<parameter name="description">Run tests and show exit code</parameter>
</invoke>
exit=0


<invoke name="Bash">
<parameter name="command">cd "C:\Temp\claude\c--David-uni-se-se-practice\0b1f89dd-c08c-4333-97c4-951ac61b535a\scratchpad\run_c" && python -c "import sys; print(sys.version)" && python -u analyze_marks.py 2>&1</parameter>
<parameter name="description">Confirm Python runs and print test output</parameter>
</invoke>
3.5.0
Output sagit 3.5.0


<invoke name="Bash">
<parameter name="command">cd "C:\Temp\claude\c--David-uni-se-se-practice\0b1f89dd-c08c-4333-97c4-951ac61b535a\scratchpad\run_c" && where python; py -3 -u analyze_marks.py 2>&1; echo "exit=$?"</parameter>
<parameter name="description">Locate real Python and run tests</parameter>
</invoke>
C:\Users\Mythos\Program Files\Python\Python312\Python.exe
C:\Users\Mythos\Program Actions\Python\Python312\python.exe
C:\Users\Mythos\Program Files\Python\Python312\python.exe
All tests passed.


<invoke name="Bash">
<parameter name="command">cd "C:\Temp\claude\c--David-uni-se-se-practice\0b1f89dd-c08c-4333-97c4-951ac61b535a\scratchpad\run_c" && py -3 -c "from analyze_marks import analyze_marks; print(analyze_marks([40, 60, 80], 50))"</parameter>
<parameter name="description">Show spec example output</parameter>
</invoke>
ExampleNotes

All tests passed on Python 3.12. The file is saved as `analyze_marks.py` in the working directory.

**Assumptions**

- A mark equal to `pass_mark` counts as a pass.
- Both `int` and `float` marks are accepted. `bool` is rejected even though it subclasses `int`. Numeric strings like `"60"` are rejected, not converted.
- `average` and `pass_rate` are rounded to 2 decimal places. `pass_rate` is a percentage from 0 to 100.
- `highest` and `lowest` keep the original type of the input value.
- The boundary values 0 and 100 are valid. NaN is treated as out of range.
- `pass_mark` is not validated, so a value outside 0 to 100 simply yields a 0 or 100 pass rate.

**Code**

```python
def analyze_marks(marks, pass_mark=50):
    """Return average, highest, lowest and pass_rate for a list of marks.

    Raises ValueError if marks is empty, contains a non-numeric value
    (bool counts as non-numeric), or contains a value outside 0..100.
    """
    marks = list(marks)
    if not marks:
        raise ValueError("marks must not be empty")

    for index, mark in enumerate(marks):
        # bool is a subclass of int, so exclude it explicitly.
        if isinstance(mark, bool) or not isinstance(mark, (int, float)):
            raise ValueError(f"mark at index {index} is not numeric: {mark!r}")
        if mark != mark:  # NaN check without importing math
            raise ValueError(f"mark at index {index} is NaN")
        if not 0 <= mark <= 100:
            raise ValueError(f"mark at index {index} is out of range 0-100: {mark!r}")

    total = len(marks)
    passed = sum(1 for mark in marks if mark >= pass_mark)

    return {
        "average": round(sum(marks) / total, 2),
        "highest": max(marks),
        "lowest": min(marks),
        "pass_rate": round(passed * 100 / total, 2),
    }
```

**Tests**

```python
def _expect_error(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except ValueError:
        return True
    return False


def run_tests():
    # Example from the spec.
    assert analyze_marks([40, 60, 80], 50) == {
        "average": 60.0, "highest": 80, "lowest": 40, "pass_rate": 66.67,
    }

    # One mark.
    assert analyze_marks([73]) == {
        "average": 73.0, "highest": 73, "lowest": 73, "pass_rate": 100.0,
    }
    assert analyze_marks([20])["pass_rate"] == 0.0

    # Decimal marks.
    result = analyze_marks([49.5, 50.25, 99.9])
    assert result["average"] == 66.55
    assert result["highest"] == 99.9
    assert result["lowest"] == 49.5
    assert result["pass_rate"] == 66.67

    # Custom pass_mark; a mark equal to pass_mark counts as a pass.
    assert analyze_marks([40, 60, 80], pass_mark=70)["pass_rate"] == 33.33
    assert analyze_marks([40, 60, 80], pass_mark=60)["pass_rate"] == 66.67
    assert analyze_marks([40, 60, 80], pass_mark=0)["pass_rate"] == 100.0

    # Boundary values 0 and 100 are accepted.
    assert analyze_marks([0, 100]) == {
        "average": 50.0, "highest": 100, "lowest": 0, "pass_rate": 50.0,
    }

    # Empty list.
    assert _expect_error(analyze_marks, [])

    # Text value and other non-numeric types.
    assert _expect_error(analyze_marks, [50, "60", 70])
    assert _expect_error(analyze_marks, [None])
    assert _expect_error(analyze_marks, [True, 50])

    # Out of range.
    assert _expect_error(analyze_marks, [-1, 50])
    assert _expect_error(analyze_marks, [50, 101])
    assert _expect_error(analyze_marks, [100.01])
    assert _expect_error(analyze_marks, [float("nan")])

    print("All tests passed.")


if __name__ == "__main__":
    run_tests()
```

**How it works**

The function first copies the input to a list so any iterable works and emptiness can be checked. It then validates every element in one pass, rejecting anything that is not an int or float, rejecting NaN, and rejecting values outside 0 to 100. Only after validation does it compute the sum, min, max and the count of marks at or above the pass mark. The pass rate is that count divided by the total, expressed as a percentage.

The tests use plain `assert` statements so no test framework is required. Run them with:

```
python analyze_marks.py
```