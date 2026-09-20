```python
def analyze_marks(marks, pass_mark=50):
    """Return average, highest, lowest and pass_rate (%) for a list of marks (0-100)."""
    try:
        marks = list(marks)
    except TypeError:
        raise ValueError("marks must be a list of numbers") from None

    if not marks:
        raise ValueError("marks must not be empty")

    for m in marks:
        # bool is a subclass of int, so exclude it explicitly
        if isinstance(m, bool) or not isinstance(m, (int, float)):
            raise ValueError(f"non-numeric mark: {m!r}")
        # written this way so NaN (which fails every comparison) is also rejected
        if not (0 <= m <= 100):
            raise ValueError(f"mark out of range 0-100: {m!r}")

    passed = sum(1 for m in marks if m >= pass_mark)

    return {
        "average": sum(marks) / len(marks),
        "highest": max(marks),
        "lowest": min(marks),
        "pass_rate": passed / len(marks) * 100,
    }
```

Example:

```python
>>> analyze_marks([35, 50, 72.5, 90])
{'average': 61.875, 'highest': 90, 'lowest': 35, 'pass_rate': 75.0}
```

I have not run this code.

- **Validation first:** the function checks all input before computing anything, so bad input always raises `ValueError` and never returns a partial result. It raises for an empty list, for non-numeric values (including strings such as `"80"`, `None`, and `True`/`False`), and for anything outside 0–100, including `NaN` and infinity.
- **Pass rate:** `pass_rate` is a percentage from 0 to 100, and a mark equal to `pass_mark` counts as a pass (`>=`). If you want a fraction from 0 to 1 instead, remove the `* 100`.
- **Rounding:** values are not rounded, so the caller decides how to display them, for example `round(result["average"], 2)`.
- **Libraries:** it uses only built-ins (`sum`, `max`, `min`, `len`) and needs no imports.