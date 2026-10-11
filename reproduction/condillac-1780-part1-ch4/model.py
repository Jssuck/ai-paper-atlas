"""Modern finite classification models, not an algorithm authored by Condillac.

Python 3.10+, standard library only. Dataset attributes and target decisions are
stipulated inputs: this module neither learns them nor discovers natural kinds.
"""
from dataclasses import dataclass
from enum import Enum
from itertools import combinations
import math
from typing import Iterable, Mapping, Sequence

Atom = str | bool | int | float | None
Partition = tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class Item:
    object_id: str
    attributes: Mapping[str, Atom]
    targets: Mapping[str, str]


def _atom_key(value: Atom) -> tuple[str, Atom]:
    # Preserve True versus 1. None is an observed missing-value marker, not false.
    if type(value) not in (str, bool, int, float, type(None)):
        raise ValueError("Attributes must be scalar strings, booleans, numbers, or None")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Nonfinite attributes are not supported")
    return type(value).__name__, value


def validate_items(items: Sequence[Item]) -> None:
    if not isinstance(items, Sequence) or isinstance(items, (str, bytes)):
        raise ValueError("Items must be a reusable Sequence[Item], not a generator")
    seen: set[str] = set()
    for item in items:
        if not isinstance(item, Item):
            raise ValueError("Each input object must be an Item")
        if not isinstance(item.attributes, Mapping) or not isinstance(item.targets, Mapping):
            raise ValueError("Item attributes and targets must be mappings")
        if not isinstance(item.object_id, str) or not item.object_id:
            raise ValueError("Each object needs a nonempty string ID")
        if item.object_id in seen:
            raise ValueError("Duplicate object ID: " + item.object_id)
        seen.add(item.object_id)
        for key, value in item.attributes.items():
            if not isinstance(key, str) or not key:
                raise ValueError("Attribute names must be nonempty strings")
            _atom_key(value)
        for key, value in item.targets.items():
            if not isinstance(key, str) or not key:
                raise ValueError("Task names must be nonempty strings")
            if type(value) is not str or not value:
                raise ValueError("Task outputs must be known nonempty built-in strings")


def normalize_partition(blocks: Iterable[Iterable[str]]) -> Partition:
    if isinstance(blocks, (str, bytes)):
        raise ValueError("A partition must be a collection of blocks")
    result: list[tuple[str, ...]] = []
    seen: set[str] = set()
    for block in blocks:
        if isinstance(block, (str, bytes)):
            raise ValueError("A block must be a collection of object IDs")
        members = list(block)
        if not members:
            raise ValueError("Empty blocks are not allowed")
        for member in members:
            if not isinstance(member, str) or not member:
                raise ValueError("Object IDs must be nonempty strings")
            if member in seen:
                raise ValueError("An object may occur in only one block")
            seen.add(member)
        result.append(tuple(sorted(members)))
    return tuple(sorted(result))


def _domain(partition: Partition) -> set[str]:
    return {member for block in partition for member in block}


def _fields(names: Iterable[str]) -> tuple[str, ...]:
    if isinstance(names, (str, bytes)):
        raise ValueError("Pass a collection of field names, not a single string")
    names = tuple(names)
    if any(not isinstance(name, str) or not name for name in names):
        raise ValueError("Field names must be nonempty strings")
    return tuple(sorted(set(names)))


def _partition(items: Sequence[Item], names: Iterable[str], source: str) -> Partition:
    validate_items(items)
    fields = _fields(names)
    groups: dict[tuple, list[str]] = {}
    for item in items:
        values = item.targets if source == "targets" else item.attributes
        missing = set(fields) - values.keys()
        if missing:
            raise ValueError(f"Missing {source} for {item.object_id}: {sorted(missing)}")
        key = tuple(_atom_key(values[field]) for field in fields)
        groups.setdefault(key, []).append(item.object_id)
    return normalize_partition(groups.values())


def task_partition(items: Sequence[Item], needs: Iterable[str]) -> Partition:
    """Group by stipulated, known task outputs (the ideal target partition)."""
    return _partition(items, needs, "targets")


def observation_partition(items: Sequence[Item], observed: Iterable[str]) -> Partition:
    """Group indistinguishable reports; equal unknown markers do not prove equality."""
    return _partition(items, observed, "attributes")


def is_refinement(finer: Partition, coarser: Partition) -> bool:
    finer, coarser = normalize_partition(finer), normalize_partition(coarser)
    if _domain(finer) != _domain(coarser):
        raise ValueError("Partitions must have the same object domain")
    coarse_class = {item: n for n, block in enumerate(coarser) for item in block}
    return all(len({coarse_class[item] for item in block}) == 1 for block in finer)


def common_refinement(left: Partition, right: Partition) -> Partition:
    left, right = normalize_partition(left), normalize_partition(right)
    if _domain(left) != _domain(right):
        raise ValueError("Partitions must have the same object domain")
    return normalize_partition(
        overlap for a in left for b in right if (overlap := set(a) & set(b))
    )


def is_sufficient(items: Sequence[Item], partition: Partition, needs: Iterable[str]) -> bool:
    """Independently check constancy of requested outputs in every class."""
    validate_items(items)
    fields = _fields(needs)
    partition = normalize_partition(partition)
    by_id = {item.object_id: item for item in items}
    if _domain(partition) != set(by_id):
        raise ValueError("Partition domain does not match the supplied objects")
    for item in items:
        if set(fields) - item.targets.keys():
            raise ValueError("A requested task output is missing")
    return all(
        len({tuple(by_id[oid].targets[field] for field in fields) for oid in block}) == 1
        for block in partition
    )


def observation_conflicts(items: Sequence[Item], observed: Iterable[str],
                         needs: Iterable[str]) -> list[dict[str, object]]:
    """Return explicit pairs proving non-identifiability from these reports."""
    observations = observation_partition(items, observed)
    fields = _fields(needs)
    task_partition(items, fields)  # Validate requested targets even on no conflicts.
    by_id = {item.object_id: item for item in items}
    witnesses = []
    for block in observations:
        for left, right in combinations(block, 2):
            different = [name for name in fields
                         if by_id[left].targets[name] != by_id[right].targets[name]]
            if different:
                witnesses.append({"objects": [left, right], "different_needs": different})
    return witnesses


class Truth(Enum):
    FALSE = "false"
    TRUE = "true"
    UNKNOWN = "unknown"

    def __bool__(self) -> bool:
        raise TypeError("Three-valued evidence needs an explicit TRUE/FALSE/UNKNOWN branch")


def observed_truth(value: bool | None) -> Truth:
    if value is None:
        return Truth.UNKNOWN
    if type(value) is not bool:
        raise ValueError("Use a boolean observation or None")
    return Truth.TRUE if value else Truth.FALSE


def boundary_name(height: float | None, low: float = 4.0,
                  high: float = 6.0) -> str:
    """Toy naming convention, not botany: the closed middle band uses 'plant'."""
    def finite_number(value):
        return type(value) is int or (type(value) is float and math.isfinite(value))

    if not finite_number(low) or not finite_number(high) or low >= high:
        raise ValueError("Finite numeric thresholds with low < high are required")
    if height is None:
        return "plant"
    if not finite_number(height) or height < 0:
        raise ValueError("Height must be finite, numeric and nonnegative, or None")
    if height < low:
        return "shrub"
    if height > high:
        return "tree"
    return "plant"


def claims_are_accurate(truth: Mapping[str, Atom], claims: Mapping[str, Atom]) -> bool:
    """Check claims against known fields; two missing reports do not verify a fact."""
    for mapping in (truth, claims):
        if not isinstance(mapping, Mapping):
            raise ValueError("References and claims must be mappings")
        for key, value in mapping.items():
            if not isinstance(key, str) or not key:
                raise ValueError("Claim field names must be nonempty strings")
            _atom_key(value)
    return all(key in truth and value is not None and truth[key] is not None
               and _atom_key(value) == _atom_key(truth[key])
               for key, value in claims.items())
