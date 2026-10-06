def read_int(prompt, minimum=None, maximum=None):
    while True:
        try:
            value = int(input(prompt).strip())
            if minimum is not None and value < minimum:
                raise ValueError
            if maximum is not None and value > maximum:
                raise ValueError
            return value
        except ValueError:
            limits = ""
            if minimum is not None:
                limits += f" >= {minimum}"
            if maximum is not None:
                limits += f" <= {maximum}"
            print(f"Please enter a valid integer{limits}.")


def read_float(prompt, minimum=None):
    while True:
        try:
            value = float(input(prompt).strip())
            if minimum is not None and value < minimum:
                raise ValueError
            return value
        except ValueError:
            print("Please enter a valid number.")


def read_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def pause():
    input("\nPress Enter to continue...")


def print_rows(rows, headers):
    if not rows:
        print("\nNo records found.")
        return

    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, value in enumerate(row):
            widths[i] = max(widths[i], len(str(value if value is not None else "")))

    separator = "+-" + "-+-".join("-" * w for w in widths) + "-+"
    print(separator)
    print("| " + " | ".join(str(h).ljust(widths[i]) for i, h in enumerate(headers)) + " |")
    print(separator)
    for row in rows:
        print("| " + " | ".join(
            str(value if value is not None else "").ljust(widths[i])
            for i, value in enumerate(row)
        ) + " |")
    print(separator)
