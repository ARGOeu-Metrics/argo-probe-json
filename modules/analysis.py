import math

from argo_probe_json.exceptions import JsonException


def check_equality(value, target):
    return value == target


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

    except ValueError:
        raise JsonException(f"Value '{value}' is not a number!")
