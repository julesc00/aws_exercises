lst_str = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]


def lower_strings(strings):
    """Return a list of strings in lower case."""
    string = str(next(iter(strings))).lower()
    return string


if __name__ == "__main__":
    for s in lst_str:
        print(lower_strings(s))
