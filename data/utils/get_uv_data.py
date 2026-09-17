import re

from data.types.core.vec2 import Vec2


def get_uv_data(groups_str: str) -> dict[int, Vec2]:
    output: dict[int, Vec2] = {}

    # Split on commas after even numbers of parenthesis
    parts = [x.lstrip("(").rstrip(")").strip().rstrip(")") for x in re.split(r',\s*(?![^()]*\))', groups_str.rstrip().rstrip(",").rstrip())]

    for part in parts:
        index = int(part.split(":")[0].strip())
        coords_parts = [float(x.strip()) for x in part.split(":")[1].strip().split(",")]
        coords = Vec2(coords_parts[0],coords_parts[1])

        output[index] = coords

    return output