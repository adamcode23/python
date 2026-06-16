def add(a, b):
    """Return the sum of a and b."""
    print(f"Adding {a} and {b}")
    return a + b


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


if __name__ == "__main__":
    test_add()
    print("All tests passed.")
