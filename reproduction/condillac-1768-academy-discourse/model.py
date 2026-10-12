"""Finite educational models. No historical or psychological claims are encoded.

Validation is explicit and remains active under python -O and -OO.
Only Python's standard library is used.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import re
from types import MappingProxyType
from typing import Mapping


class SchemaError(ValueError):
    """A finite model specification does not satisfy its declared schema."""


class UnknownInput(KeyError):
    """An input is outside the declared finite domain or training table."""


def _dict(value, context):
    if type(value) is not dict:
        raise SchemaError(f"{context} must be a dictionary")
    return value


def _keys(value, expected, context):
    _dict(value, context)
    if set(value) != set(expected):
        raise SchemaError(f"{context} keys must be exactly {sorted(expected)}")


def _text(value, context):
    if type(value) is not str or not value:
        raise SchemaError(f"{context} must be a nonempty string")
    return value


def _names(value, context, allow_empty=True):
    if type(value) is not list:
        raise SchemaError(f"{context} must be a list")
    for item in value:
        _text(item, context)
    if len(set(value)) != len(value):
        raise SchemaError(f"{context} contains duplicate names")
    if not allow_empty and not value:
        raise SchemaError(f"{context} must not be empty")
    return tuple(value)


def _total_map(value, domain, context):
    _dict(value, context)
    if set(value) != set(domain):
        raise SchemaError(f"{context} must cover exactly its declared domain")


def _require_member(value, domain):
    if type(value) is not str or value not in domain:
        raise UnknownInput(repr(value))


@dataclass(frozen=True)
class Evaluation:
    label: str
    predicate_tests: int


@dataclass(frozen=True)
class LookupEvaluation:
    label: str
    abstract_lookups: int = 1


@dataclass(frozen=True)
class _Leaf:
    label: str


@dataclass(frozen=True)
class _Branch:
    predicate: str
    no: str
    yes: str


class Tree:
    """A validated, immutable snapshot of a finite rooted binary tree.

    Each declared predicate is a total Boolean table on the finite domain.
    All nodes must be reachable; each non-root node has exactly one parent.
    The empty input domain is allowed. At least a root node is required.
    """
    __slots__ = ("_domain", "_root", "_nodes", "_predicates", "_sealed")

    def __setattr__(self, name, value):
        if getattr(self, "_sealed", False):
            raise AttributeError("Tree is immutable")
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        raise AttributeError("validated models are immutable")

    def __init__(self, spec):
        _keys(spec, {"domain", "root", "nodes", "predicates"}, "tree")
        domain = _names(spec["domain"], "domain")
        root = _text(spec["root"], "root")
        raw_nodes = _dict(spec["nodes"], "nodes")
        raw_predicates = _dict(spec["predicates"], "predicates")
        if not raw_nodes:
            raise SchemaError("nodes must not be empty")
        predicates = {}
        for name, table in raw_predicates.items():
            _text(name, "predicate name")
            _total_map(table, domain, f"predicate {name}")
            if any(type(value) is not bool for value in table.values()):
                raise SchemaError("predicate values must be Boolean, not truthy values")
            predicates[name] = MappingProxyType(dict(table))
        nodes = {}
        for name, node in raw_nodes.items():
            _text(name, "node name")
            _dict(node, f"node {name}")
            if set(node) == {"label"}:
                nodes[name] = _Leaf(_text(node["label"], "leaf label"))
            else:
                _keys(node, {"predicate", "false", "true"}, f"branch {name}")
                predicate = _text(node["predicate"], "branch predicate")
                if predicate not in predicates:
                    raise SchemaError(f"unknown predicate {predicate}")
                nodes[name] = _Branch(predicate, _text(node["false"], "false child"),
                                      _text(node["true"], "true child"))
        if root not in nodes:
            raise SchemaError("root must name a declared node")
        parents = Counter()
        for node in nodes.values():
            if isinstance(node, _Branch):
                for child in (node.no, node.yes):
                    if child not in nodes:
                        raise SchemaError(f"unknown child {child}")
                    parents[child] += 1
        if parents[root] != 0 or any(parents[name] != 1 for name in nodes if name != root):
            raise SchemaError("root must have no parent; each other node must have one")
        # Iterative graph walk also rejects disconnected cycles and unreachable nodes.
        seen, pending = set(), [root]
        while pending:
            name = pending.pop()
            if name in seen:
                raise SchemaError("nodes must form an acyclic tree")
            seen.add(name)
            node = nodes[name]
            if isinstance(node, _Branch):
                pending.extend((node.no, node.yes))
        if seen != set(nodes):
            raise SchemaError("every declared node must be reachable from the root")
        self._domain = domain
        self._root = root
        self._nodes = MappingProxyType(nodes)
        self._predicates = MappingProxyType(predicates)
        self._sealed = True

    @property
    def domain(self):
        return self._domain

    def evaluate(self, item):
        _require_member(item, self._domain)
        name, tests = self._root, 0
        while True:
            node = self._nodes[name]
            if isinstance(node, _Leaf):
                return Evaluation(node.label, tests)
            answer = self._predicates[node.predicate][item]
            tests += 1
            name = node.yes if answer else node.no

    def compile(self):
        """Enumerate the complete domain; this is not a training procedure."""
        return Lookup({item: self.evaluate(item).label for item in self._domain})

    def train_lookup(self, items):
        selected = _names(items, "training inputs")
        for item in selected:
            _require_member(item, self._domain)
        return Lookup({item: self.evaluate(item).label for item in selected})


class Lookup:
    """An immutable finite response table; one query costs one abstract lookup.

    This convention excludes validation, hashing, compilation, and hardware.
    It is not a claim of measured or worst-case constant CPU time.
    """
    __slots__ = ("_table", "_sealed")

    def __setattr__(self, name, value):
        if getattr(self, "_sealed", False):
            raise AttributeError("Lookup is immutable")
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        raise AttributeError("validated models are immutable")

    def __init__(self, table):
        _dict(table, "lookup table")
        for item, label in table.items():
            _text(item, "lookup input")
            _text(label, "lookup label")
        self._table = MappingProxyType(dict(table))
        self._sealed = True

    @property
    def table(self):
        return self._table

    def evaluate(self, item):
        _require_member(item, self._table)
        return LookupEvaluation(self._table[item])


def _weight(value):
    # No floats, booleans, infinities, or implicit rounding enter the model.
    if type(value) is int:
        result = Fraction(value)
    elif type(value) is str and re.fullmatch(r"[+-]?\d+(?:/[1-9]\d*)?", value):
        result = Fraction(value)
    else:
        raise SchemaError("weights must be integers or rational strings such as '2/3'")
    if result < 0:
        raise SchemaError("weights must be nonnegative")
    return result


@dataclass(frozen=True)
class OptimalDecoder:
    decoder: Mapping[str, str]
    error_mass: Fraction
    risk: Fraction


class RepresentationDomain:
    """A finite nonempty target population, labels, codes, and exact masses.

    Weights may be zero, but their sum must be positive. Missing weights
    select uniform unit masses. Risk always normalizes by total mass.
    """
    __slots__ = ("_objects", "_codes", "_labels", "_weights", "_mass", "_fibers", "_sealed")

    def __setattr__(self, name, value):
        if getattr(self, "_sealed", False):
            raise AttributeError("RepresentationDomain is immutable")
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        raise AttributeError("validated models are immutable")

    def __init__(self, spec):
        _dict(spec, "representation domain")
        required = {"objects", "codes", "labels"}
        if set(spec) not in (required, required | {"weights"}):
            raise SchemaError("representation keys must be objects, codes, labels, and optionally weights")
        objects = _names(spec["objects"], "objects", allow_empty=False)
        for key in ("codes", "labels"):
            _total_map(spec[key], objects, key)
            for value in spec[key].values():
                _text(value, key)
        weights = spec.get("weights", {item: 1 for item in objects})
        _total_map(weights, objects, "weights")
        weights = {item: _weight(weights[item]) for item in objects}
        mass = sum(weights.values(), Fraction(0))
        if mass == 0:
            raise SchemaError("total weight must be positive")
        fibers = {}
        for item in objects:
            fibers.setdefault(spec["codes"][item], []).append(item)
        self._objects = objects
        self._codes = MappingProxyType(dict(spec["codes"]))
        self._labels = MappingProxyType(dict(spec["labels"]))
        self._weights = MappingProxyType(weights)
        self._mass = mass
        self._fibers = MappingProxyType({code: tuple(items) for code, items in fibers.items()})
        self._sealed = True

    @property
    def objects(self):
        return self._objects

    @property
    def total_mass(self):
        return self._mass

    def sufficient(self, positive_support_only=False):
        if type(positive_support_only) is not bool:
            raise SchemaError("positive_support_only must be Boolean")
        return all(len({self._labels[item] for item in items
                        if not positive_support_only or self._weights[item] > 0}) <= 1
                   for items in self._fibers.values())

    def risk(self, decoder):
        if not isinstance(decoder, Mapping) or set(decoder) != set(self._fibers):
            raise SchemaError("decoder must map exactly the observed representation codes")
        for label in decoder.values():
            _text(label, "decoder label")
        errors = sum((self._weights[item] for item in self._objects
                      if decoder[self._codes[item]] != self._labels[item]), Fraction(0))
        return errors / self._mass

    def best_decoder(self):
        decoder, error_mass = {}, Fraction(0)
        for code, items in sorted(self._fibers.items()):
            masses = {}
            for item in items:
                label = self._labels[item]
                masses[label] = masses.get(label, Fraction(0)) + self._weights[item]
            winner = min(masses, key=lambda label: (-masses[label], label))
            decoder[code] = winner
            error_mass += sum(masses.values(), Fraction(0)) - masses[winner]
        return OptimalDecoder(MappingProxyType(decoder), error_mass, error_mass / self._mass)


@dataclass(frozen=True)
class Judgment:
    claim: str
    origin: str

    def __post_init__(self):
        _text(self.claim, "claim")
        _text(self.origin, "origin")


def copy_judgment(judgment, count):
    if type(judgment) is not Judgment:
        raise SchemaError("judgment must be a Judgment")
    if type(count) is not int or count < 0:
        raise SchemaError("copy count must be a nonnegative integer")
    return (judgment,) * count


def distinct_origins(judgments):
    if type(judgments) not in (tuple, list):
        raise SchemaError("judgments must be a list or tuple")
    if any(type(judgment) is not Judgment for judgment in judgments):
        raise SchemaError("all copied judgments must be Judgment values")
    return frozenset(judgment.origin for judgment in judgments)


@dataclass(frozen=True)
class Diffusion:
    judgment: Judgment
    snapshots: tuple[frozenset[str], ...]

    @property
    def holders(self):
        return self.snapshots[-1]

    @property
    def first_arrival(self):
        arrivals = {}
        for time, holders in enumerate(self.snapshots):
            for holder in sorted(holders):
                arrivals.setdefault(holder, time)
        return MappingProxyType(arrivals)

    @property
    def origins(self):
        return frozenset({self.judgment.origin}) if self.holders else frozenset()


def diffuse(spec, seeds, judgment):
    """Copy one fixed claim synchronously over a finite directed graph.

    Return S_0 through the last changing snapshot. A final repeated snapshot
    is omitted; an empty seed set therefore returns exactly (frozenset(),).
    """
    _keys(spec, {"nodes", "edges"}, "graph")
    nodes = _names(spec["nodes"], "graph nodes")
    if type(spec["edges"]) is not list:
        raise SchemaError("edges must be a list of two-element lists")
    edges = set()
    for edge in spec["edges"]:
        if type(edge) is not list or len(edge) != 2:
            raise SchemaError("each edge must be a two-element list")
        for node in edge:
            _text(node, "edge endpoint")
            if node not in nodes:
                raise SchemaError("edge endpoint must be a declared node")
        pair = tuple(edge)
        if pair in edges:
            raise SchemaError("duplicate edges are not allowed")
        edges.add(pair)
    seeds = _names(seeds, "seeds")
    if any(seed not in nodes for seed in seeds):
        raise SchemaError("every seed must be a declared node")
    if type(judgment) is not Judgment:
        raise SchemaError("judgment must be a Judgment")
    holders = frozenset(seeds)
    snapshots = [holders]
    while True:
        following = holders | frozenset(target for source, target in edges if source in holders)
        if following == holders:
            return Diffusion(judgment, tuple(snapshots))
        snapshots.append(following)
        holders = following
