"""Finite teaching model inspired by Condillac, La Logique II.II.

This is a new mathematical abstraction, not a recovered historical algorithm.
Python standard library only; ordinary finite inputs are the API contract.
"""
from collections import Counter
from dataclasses import dataclass
from itertools import product
import json
from typing import Iterable, Mapping

Atom = tuple[str, str]
Message = tuple[str, ...]


def _strings(values: Iterable[str], label: str, *, nonempty: bool = False) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{label} must be an iterable of strings, not one string")
    result = tuple(values)
    if any(not isinstance(value, str) or (nonempty and not value) for value in result):
        raise ValueError(f"invalid string in {label}")
    return result


def pack(tokens: Iterable[str]) -> str:
    """Unambiguous framing; tokens may themselves contain delimiters or be empty."""
    return json.dumps(_strings(tokens, "tokens"), ensure_ascii=False, separators=(",", ":"))


def unpack(wire: str) -> tuple[str, ...]:
    if not isinstance(wire, str):
        raise ValueError("wire must be a JSON string")
    try:
        values = json.loads(wire)
    except json.JSONDecodeError as exc:
        raise ValueError("invalid JSON frame") from exc
    if not isinstance(values, list):
        raise ValueError("wire must encode a list")
    return _strings(values, "wire tokens")


@dataclass(frozen=True, init=False)
class Language:
    """Closed finite schema, context precedence, and a possibly colliding lexicon.

    Messages are tuples in schema insertion order. All stored fields are immutable
    snapshots. Orders enumerate all and only context-compatible permutations.
    """
    schema: tuple[tuple[str, tuple[str, ...]], ...]
    edges: frozenset[tuple[str, str]]
    lexicon: tuple[tuple[Atom, str], ...]
    orders: tuple[tuple[str, ...], ...]

    def __init__(self, schema: Mapping[str, Iterable[str]],
                 edges: Iterable[tuple[str, str]] = (),
                 lexicon: Mapping[Atom, str] | None = None):
        if not isinstance(schema, Mapping) or not schema:
            raise ValueError("schema must be a nonempty mapping")
        normalized = []
        for feature, raw_domain in schema.items():
            if not isinstance(feature, str) or not feature:
                raise ValueError("feature labels must be nonempty strings")
            domain = _strings(raw_domain, "domain", nonempty=True)
            if not domain or len(set(domain)) != len(domain):
                raise ValueError("domains must be nonempty and have no duplicates")
            normalized.append((feature, domain))
        snapshot = tuple(normalized)
        labels = tuple(feature for feature, _ in snapshot)
        edge_set = set()
        for edge in edges:
            if (not isinstance(edge, (tuple, list)) or len(edge) != 2
                    or any(not isinstance(x, str) for x in edge)):
                raise ValueError("each edge must have two string endpoints")
            a, b = edge
            if a not in labels or b not in labels or a == b:
                raise ValueError("edge endpoints must be distinct schema labels")
            edge_set.add((a, b))
        frozen_edges = frozenset(edge_set)
        orders = []

        def visit(prefix: tuple[str, ...]) -> None:
            if len(prefix) == len(labels):
                orders.append(prefix)
                return
            for feature in labels:
                if (feature not in prefix
                        and all(a in prefix for a, b in frozen_edges if b == feature)):
                    visit(prefix + (feature,))

        visit(())
        if not orders:
            raise ValueError("context must be acyclic")
        atoms = tuple((feature, value) for feature, domain in snapshot for value in domain)
        if lexicon is None:
            # JSON pairs also make default codewords injective for arbitrary labels.
            codes = {atom: pack(atom) for atom in atoms}
        else:
            if not isinstance(lexicon, Mapping) or set(lexicon) != set(atoms):
                raise ValueError("lexicon must cover exactly the schema atoms")
            if any(not isinstance(token, str) for token in lexicon.values()):
                raise ValueError("lexicon codewords must be strings")
            codes = dict(lexicon)
        object.__setattr__(self, "schema", snapshot)
        object.__setattr__(self, "edges", frozen_edges)
        object.__setattr__(self, "lexicon", tuple((atom, codes[atom]) for atom in atoms))
        object.__setattr__(self, "orders", tuple(orders))

    @property
    def labels(self) -> tuple[str, ...]:
        return tuple(feature for feature, _ in self.schema)

    @property
    def injective(self) -> bool:
        return len({token for _, token in self.lexicon}) == len(self.lexicon)

    def messages(self) -> tuple[Message, ...]:
        return tuple(product(*(domain for _, domain in self.schema)))

    def _message(self, message: Iterable[str]) -> Message:
        result = _strings(message, "message", nonempty=True)
        if len(result) != len(self.schema):
            raise ValueError("message must cover each feature exactly once")
        if any(value not in domain for value, (_, domain) in zip(result, self.schema)):
            raise ValueError("message value is outside its feature domain")
        return result

    def labeled(self, message: Iterable[str]) -> frozenset[Atom]:
        return frozenset(zip(self.labels, self._message(message)))

    def aggregate(self, message: Iterable[str]) -> tuple[tuple[str, int], ...]:
        """Deliberately forget feature labels but keep value multiplicities."""
        return tuple(sorted(Counter(self._message(message)).items()))

    def encode(self, message: Iterable[str], order: Iterable[str]) -> tuple[str, ...]:
        values = dict(zip(self.labels, self._message(message)))
        sequence = _strings(order, "order", nonempty=True)
        if sequence not in self.orders:
            raise ValueError("order must be a full context-compatible permutation")
        codes = dict(self.lexicon)
        return tuple(codes[(feature, values[feature])] for feature in sequence)

    def candidates(self, prefix: Iterable[str]) -> frozenset[Message]:
        observed = _strings(prefix, "prefix")
        return frozenset(message for message in self.messages()
                         if any(self.encode(message, order)[:len(observed)] == observed
                                for order in self.orders))

    def decode(self, wire: str) -> Message:
        tokens = unpack(wire)
        if len(tokens) != len(self.schema):
            raise ValueError("decode requires a complete frame")
        compatible = self.candidates(tokens)
        if len(compatible) != 1:
            raise ValueError("frame has no unique compatible message")
        return next(iter(compatible))


def version_space(hypotheses: Iterable[Iterable[str]],
                  examples: Iterable[tuple[int, str]]) -> frozenset[tuple[str, ...]]:
    """Filter a finite set of tables on common symbol indices 0,...,s-1."""
    tables = frozenset(_strings(table, "hypothesis") for table in hypotheses)
    if not tables or len({len(table) for table in tables}) != 1:
        raise ValueError("hypotheses must be nonempty tables of one common length")
    size = len(next(iter(tables)))
    if size == 0:
        raise ValueError("hypothesis tables must be nonempty")
    observations = []
    for example in examples:
        if not isinstance(example, (tuple, list)) or len(example) != 2:
            raise ValueError("examples must be index/value pairs")
        index, value = example
        if type(index) is not int or not 0 <= index < size or not isinstance(value, str):
            raise ValueError("example is outside the symbol/meaning vocabulary")
        observations.append((index, value))
    return frozenset(table for table in tables
                     if all(table[index] == value for index, value in observations))
