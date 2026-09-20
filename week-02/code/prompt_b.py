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
