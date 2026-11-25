import json
import math
from collections import Counter

from argo_probe_json.exceptions import JsonException


def check_equality(value, target):
    return value == target


def check_target_in_value(value, target):
    return target in value


def _split_list_items(inner):
    items = []
    current = ""
    quote = None

    for char in inner:
        if quote is not None:
            current += char
            if char == quote:
                quote = None

        elif char in ("\"", "'"):
            quote = char
            current += char

        elif char == ",":
            items.append(current)
            current = ""

        else:
            current += char

    items.append(current)
    return items


def parse_target_value(target):
    """Parse the target value.

    A list-like target, e.g. '["value3", "value5"]' or '[value3, value5]',
    is parsed into a list of values; any other target is returned as is.
    """
    stripped = target.strip()

    if not (stripped.startswith("[") and stripped.endswith("]")):
        return target

    target_list = []
    for item in _split_list_items(stripped[1:-1]):
        item = item.strip()

        if not item:
            continue

        if len(item) > 1 and item[0] == item[-1] and item[0] in "\"'":
            target_list.append(item[1:-1])
            continue

        try:
            target_list.append(json.loads(item))

        except ValueError:
            target_list.append(item)

    return target_list


def check_list_equality(value, target):
    """Compare two lists ignoring the order of the elements."""
    return Counter(map(str, value)) == Counter(map(str, target))


def get_range(range_string):
    try:
        if range_string.strip().startswith(":"):
            floor = 0.
            ceil = float(range_string.strip()[1:])

        elif range_string.strip().endswith(":"):
            floor = float(range_string.strip()[:-1])
            ceil = math.inf

        elif ":" not in range_string:
            floor = 0.
            ceil = float(range_string)

        else:
            range_list = range_string.split(":")
            floor = float(range_list[0].strip())
            ceil = float(range_list[1].strip())

    except ValueError:
        raise JsonException(f"Range '{range_string}' not defined properly!")

    return floor, ceil


def value_in_range(value, range_tuple):
    floor, ceil = range_tuple

    try:
        return floor <= float(value) <= ceil

    except (ValueError, TypeError):
        raise JsonException(f"Value '{value}' is not a number!")
