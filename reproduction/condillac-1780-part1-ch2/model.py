"""Modern teaching construction, not an algorithm attributed to Condillac.

Exact integer displacement constraints on a finite set of named objects.
Only the Python standard library is used. See MODEL.zh-CN.md for semantics.
"""
from __future__ import annotations

from collections import deque
from collections.abc import Mapping
from dataclasses import dataclass

Vector = tuple[int, ...]


def _names(value: object, label: str, *, nonempty: bool = False) -> None:
    if type(value) is not tuple:
        raise TypeError(f"{label} must be a tuple")
    if nonempty and not value:
        raise ValueError(f"{label} must not be empty")
    if any(type(x) is not str or not x or x.strip() != x for x in value):
        raise ValueError(f"{label} needs nonempty, unpadded string names")
    if len(value) != len(set(value)):
        raise ValueError(f"{label} must not contain duplicates")


def _vector(value: object, dimension: int) -> None:
    if type(value) is not tuple or len(value) != dimension:
        raise ValueError("offset must be a tuple of exactly dimension entries")
    if any(type(x) is not int for x in value):
        raise TypeError("offset entries must be integers; bools and floats are rejected")


def _name(value: object, universe: tuple[str, ...]) -> None:
    if type(value) is not str or value not in universe:
        raise ValueError(f"unknown object: {value!r}")


def _add(a: Vector, b: Vector) -> Vector:
    return tuple(x + y for x, y in zip(a, b))


def _subtract(a: Vector, b: Vector) -> Vector:
    return tuple(x - y for x, y in zip(a, b))


@dataclass(frozen=True)
class Relation:
    """The directed equation position[v] - position[u] = offset."""

    u: str
    v: str
    offset: Vector


@dataclass(frozen=True)
class ObservationBook:
    """Inventory is supplied by the exercise, not discovered by the solver.

    seen records distinct named objects. Relations are separate observations.
    Empty seen is valid. An empty inventory or nonpositive dimension is not.
    """

    inventory: tuple[str, ...]
    dimension: int
    seen: tuple[str, ...] = ()
    relations: tuple[Relation, ...] = ()

    def __post_init__(self) -> None:
        _names(self.inventory, "inventory", nonempty=True)
        if type(self.dimension) is not int or self.dimension <= 0:
            raise ValueError("dimension must be a positive integer, not a bool")
        _names(self.seen, "seen")
        if not set(self.seen) <= set(self.inventory):
            raise ValueError("seen must be a subset of inventory")
        if type(self.relations) is not tuple:
            raise TypeError("relations must be a tuple")
        for edge in self.relations:
            if type(edge) is not Relation:
                raise TypeError("relations must contain Relation instances")
            _name(edge.u, self.seen)
            _name(edge.v, self.seen)
            _vector(edge.offset, self.dimension)

    def observe_object(self, name: str) -> ObservationBook:
        _name(name, self.inventory)
        if name in self.seen:
            return self
        # Inventory order gives a deterministic representation.
        seen = tuple(x for x in self.inventory if x in self.seen or x == name)
        return ObservationBook(self.inventory, self.dimension, seen, self.relations)

    def observe_relation(self, u: str, v: str, offset: Vector) -> ObservationBook:
        _name(u, self.seen)
        _name(v, self.seen)
        _vector(offset, self.dimension)
        edge = Relation(u, v, offset)
        if edge in self.relations:
            return self
        return ObservationBook(self.inventory, self.dimension, self.seen,
                               self.relations + (edge,))


@dataclass(frozen=True)
class Reconstruction:
    book: ObservationBook
    consistent: bool
    components: tuple[tuple[str, ...], ...]
    coordinates: tuple[tuple[str, Vector], ...]
    conflicts: tuple[tuple[str, str, Vector, Vector], ...]

    @property
    def missing_objects(self) -> tuple[str, ...]:
        return tuple(x for x in self.book.inventory if x not in self.book.seen)

    @property
    def relative_complete(self) -> bool:
        return self.consistent and not self.missing_objects and len(self.components) == 1

    @property
    def translation_parameters(self) -> int | None:
        # The unsatisfiable case has no family of positions to parameterize.
        return self.book.dimension * len(self.components) if self.consistent else None

    def difference(self, u: str, v: str) -> Vector | None:
        """Return x_v-x_u if identified; None if absent or disconnected.

        Inconsistency raises rather than using vacuous logical consequence.
        """
        _name(u, self.book.inventory)
        _name(v, self.book.inventory)
        if not self.consistent:
            raise ValueError("inconsistent observations have no reconstructed positions")
        if not any(u in component and v in component for component in self.components):
            return None
        positions = dict(self.coordinates)
        return _subtract(positions[v], positions[u])

    def instantiate(self, shifts: Mapping[str, Vector]) -> dict[str, Vector]:
        """Translate every component independently; each root is its first name."""
        if not self.consistent:
            raise ValueError("cannot instantiate inconsistent observations")
        if not isinstance(shifts, Mapping):
            raise TypeError("shifts must be a mapping")
        roots = {component[0] for component in self.components}
        if set(shifts) != roots:
            raise ValueError("provide exactly one shift per component root")
        for shift in shifts.values():
            _vector(shift, self.book.dimension)
        positions = dict(self.coordinates)
        return {name: _add(positions[name], shifts[component[0]])
                for component in self.components for name in component}

    def summary(self) -> dict:
        possible = len(self.book.inventory) * (len(self.book.inventory) - 1) // 2
        direct = {frozenset((edge.u, edge.v)) for edge in self.book.relations
                  if edge.u != edge.v}
        identified = (sum(len(c) * (len(c) - 1) // 2 for c in self.components)
                      if self.consistent else None)
        return {
            "consistent": self.consistent,
            "observed_objects": len(self.book.seen),
            "inventory_objects": len(self.book.inventory),
            "missing_objects": list(self.missing_objects),
            "directly_observed_pairs": len(direct),
            "identifiable_pairs": identified,
            "all_inventory_pairs": possible,
            "components": [list(c) for c in self.components],
            "component_relative_positions": {k: list(v) for k, v in self.coordinates},
            "translation_parameters": self.translation_parameters,
            "relative_complete": self.relative_complete,
            "conflicts": [{"u": u, "v": v, "stated": list(s), "implied": list(i)}
                          for u, v, s, i in self.conflicts],
        }


def reconstruct(book: ObservationBook) -> Reconstruction:
    """Propagate offsets and check every equation, in canonical traversal order.

    No coordinates are returned when any equation is inconsistent. On a
    consistent graph, each connected component's first inventory object is
    placed at zero solely as a coordinate convention (a gauge choice).
    """
    if type(book) is not ObservationBook:
        raise TypeError("book must be an ObservationBook")
    rank = {name: i for i, name in enumerate(book.inventory)}
    adjacency = {name: [] for name in book.seen}
    for edge in book.relations:
        adjacency[edge.u].append((edge.v, edge.offset))
        adjacency[edge.v].append((edge.u, tuple(-x for x in edge.offset)))
    for neighbors in adjacency.values():
        neighbors.sort(key=lambda entry: (rank[entry[0]], entry[1]))
    positions: dict[str, Vector] = {}
    components = []
    for root in book.inventory:
        if root not in adjacency or root in positions:
            continue
        positions[root] = (0,) * book.dimension
        pending = deque([root])
        component = []
        while pending:
            u = pending.popleft()
            component.append(u)
            for v, offset in adjacency[u]:
                if v not in positions:
                    positions[v] = _add(positions[u], offset)
                    pending.append(v)
        components.append(tuple(sorted(component, key=rank.__getitem__)))
    conflicts = tuple(sorted({(e.u, e.v, e.offset, _subtract(positions[e.v], positions[e.u]))
                              for e in book.relations
                              if _subtract(positions[e.v], positions[e.u]) != e.offset}))
    consistent = not conflicts
    coordinates = (tuple((name, positions[name]) for name in book.inventory if name in positions)
                   if consistent else ())
    return Reconstruction(book, consistent, tuple(components), coordinates, conflicts)


def anchor_unresolved(book: ObservationBook, anchor: str) -> int:
    """Toy prefix score: seen objects not yet position-linked to an anchor.

    It is NOT elapsed time, cognitive load, or an empirical observation cost.
    """
    if type(book) is not ObservationBook:
        raise TypeError("book must be an ObservationBook")
    _name(anchor, book.seen)
    result = reconstruct(book)
    if not result.consistent:
        raise ValueError("prefix score is undefined for inconsistent data")
    return sum(result.difference(anchor, name) is None for name in book.seen)
