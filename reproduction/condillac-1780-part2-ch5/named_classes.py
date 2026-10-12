"""Modern finite extensional teaching model, not a historical reconstruction."""
from collections import deque
from dataclasses import dataclass


class InvalidGraph(ValueError):
    """The entire asserted graph failed its extensional validity gate."""


@dataclass(frozen=True, slots=True)
class ClassSystem:
    objects: tuple[str, ...]
    labels: tuple[str, ...]
    extensions: tuple[frozenset[str], ...]
    edges: tuple[tuple[str, str], ...] = ()

    def __post_init__(self):
        for name, values in (("objects", self.objects), ("labels", self.labels)):
            if type(values) is not tuple:
                raise TypeError(f"{name} must be a tuple")
            if any(type(x) is not str or not x for x in values):
                raise ValueError(f"{name} must contain nonempty strings")
            if len(set(values)) != len(values):
                raise ValueError(f"duplicate {name}")
        if not self.labels:
            raise ValueError("at least one label is required")
        if type(self.extensions) is not tuple or len(self.extensions) != len(self.labels):
            raise ValueError("one extension per label is required")
        for extension in self.extensions:
            if type(extension) is not frozenset:
                raise TypeError("extensions must be frozensets")
            if any(type(x) is not str for x in extension) or not extension <= set(self.objects):
                raise ValueError("extension contains an object outside the universe")
        if type(self.edges) is not tuple:
            raise TypeError("edges must be a tuple")
        for edge in self.edges:
            if type(edge) is not tuple or len(edge) != 2:
                raise ValueError("each edge must be a pair")
            if any(type(x) is not str or x not in self.labels for x in edge):
                raise ValueError("edge endpoint is not a label")
        if len(set(self.edges)) != len(self.edges):
            raise ValueError("duplicate edges")

    def extension(self, label):
        if type(label) is not str or label not in self.labels:
            raise ValueError("unknown label")
        return self.extensions[self.labels.index(label)]

    def includes(self, source, target):
        """Whether E(source) is a subset of E(target), within declared U."""
        left, right = self.extension(source), self.extension(target)
        return left <= right

    def witness(self, source, target):
        """First counterexample in the declared object order, else None."""
        left, right = self.extension(source), self.extension(target)
        return next((x for x in self.objects if x in left and x not in right), None)

    def violations(self):
        """Invalid edges with witnesses, retaining declared edge order."""
        return tuple((a, b, self.witness(a, b)) for a, b in self.edges
                     if not self.includes(a, b))

    def find_path(self, source, target):
        """Raw graph reachability, independent of extensional validity."""
        self.extension(source)
        self.extension(target)
        if source == target:
            return (source,)
        adjacent = {label: [] for label in self.labels}
        for a, b in self.edges:
            adjacent[a].append(b)
        previous = {source: None}
        queue = deque([source])
        while queue:
            current = queue.popleft()
            for following in adjacent[current]:
                if following in previous:
                    continue
                previous[following] = current
                if following == target:
                    path = [target]
                    while previous[path[-1]] is not None:
                        path.append(previous[path[-1]])
                    return tuple(reversed(path))
                queue.append(following)
        return None

    def prove(self, source, target):
        """Return graph proof only after checking every asserted edge."""
        self.extension(source)
        self.extension(target)
        invalid = self.violations()
        if invalid:
            raise InvalidGraph(f"invalid asserted edges: {invalid!r}")
        return self.find_path(source, target)

    def same_extension(self, first, second):
        return self.extension(first) == self.extension(second)

    def components(self):
        """SCCs in declared label order; no semantic merging is performed."""
        remaining = set(self.labels)
        groups = []
        for a in self.labels:
            if a not in remaining:
                continue
            group = tuple(b for b in self.labels if b in remaining
                          and self.find_path(a, b) is not None
                          and self.find_path(b, a) is not None)
            groups.append(group)
            remaining.difference_update(group)
        return tuple(groups)

    def rename(self, new_labels):
        """Positionwise bijection, jointly transported across edges and E."""
        if type(new_labels) is not tuple or len(new_labels) != len(self.labels):
            raise ValueError("rename must supply exactly one new label per old label")
        if any(type(x) is not str or not x for x in new_labels):
            raise ValueError("new labels must be nonempty strings")
        if len(set(new_labels)) != len(new_labels):
            raise ValueError("renaming must be bijective")
        mapping = dict(zip(self.labels, new_labels))
        return ClassSystem(self.objects, new_labels, self.extensions,
                           tuple((mapping[a], mapping[b]) for a, b in self.edges))


def prototype_accepts(system, source, target, prototype):
    """Deliberately inadequate one-object test, NOT universal inference."""
    left, right = system.extension(source), system.extension(target)
    if type(prototype) is not str or prototype not in left:
        raise ValueError("prototype must belong to the source extension")
    return prototype in right
