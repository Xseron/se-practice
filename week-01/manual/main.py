NO_MARKS = "No valid marks"


def table(valid, average, highest, lowest, pass_rate):
    return f"""| Output | Format |
| --- | --- |
| Number of valid marks | {valid} |
| Average | {average} |
| Highest | {highest} |
| Lowest | {lowest} |
| Pass rate | {pass_rate} |"""

def main(inp_str: str):
    inp = list(filter(lambda x: x >= 0 and x <= 100, map(int, filter(lambda x: x.lstrip("-").isdigit(), map(str.strip, inp_str.split(","))))))

    if not inp:
        return NO_MARKS

    return table(len(inp), "{:.2f}".format(sum(inp)/len(inp)), max(inp), min(inp), "{:.1f}%".format(len(list(filter(lambda x: x >= 50, inp)))/len(inp) * 100))


def check(got: str, expected: str):
    assert got == expected, "\n--- got ---\n" + got + "\n--- expected ---\n" + expected


def testA():
    check(main("85, 23, 45, 90, 92"), table("5", "67.00", "92", "23", "60.0%"))


def testB():
    check(main("88, 47, -5, 101, abc, 73, 50, , 100"), table("5", "71.60", "100", "47", "80.0%"))


def testC():
    check(main("10, 20, 30"), table("3", "20.00", "30", "10", "0.0%"))


def testD():
    check(main("abc, , xyz"), NO_MARKS)


def run_tests():
    failed = 0
    for t in (testA, testB, testC, testD):
        try:
            t()
            print(t.__name__ + ": PASS")
        except AssertionError as e:
            failed += 1
            print(t.__name__ + ": FAIL " + str(e))
        except Exception as e:
            failed += 1
            print(t.__name__ + ": CRASH " + type(e).__name__ + ": " + str(e))
    print("\n" + str(4 - failed) + "/4 passed")
    return failed


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        sys.exit(1 if run_tests() else 0)
    print(main(input()))
