import re


def get_groups(groups_str: str) -> list[list[int]]:
    output: list[list[int]] = list()

    # Split on commas after even numbers of parenthesis
    parts = [x.lstrip("(").rstrip(")").strip() for x in re.split(r',\s*(?![^()]*\))', groups_str)]

    for part in parts:
        output.append(list([int(x.strip()) for x in part.split(",")]))

    return output