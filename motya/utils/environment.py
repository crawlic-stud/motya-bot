import sys


def change_token(token: str) -> None:
    with open("motya/config.py", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith("TG_TOKEN"):
                lines[i] = f"TG_TOKEN = {token}\n"
    with open("motya/config.py", "w", encoding="utf-8") as f:
        f.writelines(lines)


def check_environment() -> bool:
    try:
        is_test = sys.argv[1]
    except IndexError:
        is_test = ""

    is_test = is_test == "test"

    if is_test:
        change_token("TEST_TOKEN")
    else:
        change_token("PROD_TOKEN")

    return is_test
