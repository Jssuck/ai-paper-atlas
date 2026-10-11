"""Wholly invented teaching objects. These values are not empirical plant data."""
from model import Item


def garden() -> tuple[Item, ...]:
    rows = (
        ("a1", "apple", False, 4.5),
        ("a2", "apple", True, 7.0),
        ("p1", "pear", True, 7.0),
        ("c1", "cherry", False, 4.0),
        ("h1", "peach", False, 3.5),
        ("o1", "none", True, 8.0),
        ("s1", "none", False, 2.0),
        ("g1", "none", False, 0.5),
    )
    return tuple(
        Item(oid,
             {"fruit_kind": fruit, "shade_ready": shade, "height": height,
              "visible_green": True},
             {"harvest": "collect" if fruit != "none" else "skip",
              "sort_fruit": fruit,
              "shade": "use" if shade else "skip"})
        for oid, fruit, shade, height in rows
    )
