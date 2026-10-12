"""Original teaching models, not a reconstruction of Condillac's mathematics.

Only the Python standard library is needed. Runtime validation never uses assert.
The finite-world operations are exponential and intended for small examples.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable, Mapping, Sequence

World = dict[str, bool]


def _name(value: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError("Names must be nonempty strings")


def _names(values: Iterable[str]) -> tuple[str, ...]:
    result = tuple(values)
    for value in result:
        _name(value)
    if len(result) != len(set(result)):
        raise ValueError("Names must be distinct")
    return result


def _world(world: Mapping[str, bool]) -> World:
    result = dict(world)
    for key, value in result.items():
        _name(key)
        if type(value) is not bool:
            raise TypeError("World values must be bool, not truthy objects or integers")
    return result


class Expr:
    """Base for the five supported immutable Boolean expression nodes."""


@dataclass(frozen=True)
class Const(Expr):
    value: bool

    def __post_init__(self) -> None:
        if type(self.value) is not bool:
            raise TypeError("A constant must be bool")


@dataclass(frozen=True)
class Var(Expr):
    name: str

    def __post_init__(self) -> None:
        _name(self.name)


@dataclass(frozen=True)
class Not(Expr):
    arg: Expr

    def __post_init__(self) -> None:
        variables(self.arg)


@dataclass(frozen=True)
class And(Expr):
    left: Expr
    right: Expr

    def __post_init__(self) -> None:
        variables(self.left)
        variables(self.right)


@dataclass(frozen=True)
class Or(Expr):
    left: Expr
    right: Expr

    def __post_init__(self) -> None:
        variables(self.left)
        variables(self.right)


def variables(expr: Expr) -> frozenset[str]:
    """Return free names; reject unsupported expression nodes."""
    if type(expr) is Const:
        return frozenset()
    if type(expr) is Var:
        return frozenset((expr.name,))
    if type(expr) is Not:
        return variables(expr.arg)
    if type(expr) in (And, Or):
        return variables(expr.left) | variables(expr.right)
    raise TypeError("Expected Const, Var, Not, And, or Or")


def evaluate(expr: Expr, world: Mapping[str, bool]) -> bool:
    """Evaluate after validating all names, including short-circuited branches."""
    names = variables(expr)
    values = _world(world)
    missing = names - values.keys()
    if missing:
        raise ValueError(f"Unbound names: {sorted(missing)}")

    def visit(node: Expr) -> bool:
        if type(node) is Const:
            return node.value
        if type(node) is Var:
            return values[node.name]
        if type(node) is Not:
            return not visit(node.arg)
        if type(node) is And:
            return visit(node.left) and visit(node.right)
        if type(node) is Or:
            return visit(node.left) or visit(node.right)
        raise TypeError("Unsupported expression")

    return visit(expr)


def enumerate_worlds(names: Iterable[str]) -> tuple[World, ...]:
    """Enumerate 2**n worlds in input-name order; no names gives one empty world."""
    ordered = _names(names)
    return tuple(dict(zip(ordered, bits)) for bits in product((False, True), repeat=len(ordered)))


@dataclass(frozen=True)
class Definition:
    name: str
    expression: Expr

    def __post_init__(self) -> None:
        _name(self.name)
        variables(self.expression)


@dataclass(frozen=True)
class DefinitionSystem:
    """Fresh, total, acyclic explicit definitions over a fixed primitive vocabulary.

    Definitions may be supplied in any order. Ties in the topological order
    retain input order. Unknown dependencies, old-name reuse and cycles fail.
    """
    primitives: tuple[str, ...]
    definitions: tuple[Definition, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "primitives", _names(self.primitives))
        object.__setattr__(self, "definitions", tuple(self.definitions))
        if any(type(d) is not Definition for d in self.definitions):
            raise TypeError("Expected Definition objects")
        defined = _names(d.name for d in self.definitions)
        if set(defined) & set(self.primitives):
            raise ValueError("Definitions must introduce fresh names")
        allowed = set(self.primitives) | set(defined)
        for definition in self.definitions:
            unknown = variables(definition.expression) - allowed
            if unknown:
                raise ValueError(f"Unknown dependency: {sorted(unknown)}")
        self.topological_definitions()

    def topological_definitions(self) -> tuple[Definition, ...]:
        known = set(self.primitives)
        remaining = list(self.definitions)
        ordered = []
        while remaining:
            ready = next((d for d in remaining if variables(d.expression) <= known), None)
            if ready is None:
                raise ValueError("Cyclic definitions are not explicit acyclic definitions")
            remaining.remove(ready)
            ordered.append(ready)
            known.add(ready.name)
        return tuple(ordered)

    def expand(self, primitive_world: Mapping[str, bool]) -> World:
        result = _world(primitive_world)
        if set(result) != set(self.primitives):
            raise ValueError("An input world must assign exactly the primitive names")
        for definition in self.topological_definitions():
            result[definition.name] = evaluate(definition.expression, result)
        return result

    def worlds(self) -> tuple[World, ...]:
        return tuple(self.expand(w) for w in enumerate_worlds(self.primitives))


def satisfying_extensions(base: Mapping[str, bool], equations: Iterable[Definition]) -> tuple[World, ...]:
    """Brute-force equation oracle, deliberately allowing cycles and old-name LHSs.

    A Definition here denotes an equation name = expression, not permission to
    overwrite the base world. Each previously unassigned LHS name is enumerated.
    """
    base = _world(base)
    equations = tuple(equations)
    if any(type(d) is not Definition for d in equations):
        raise TypeError("Expected Definition objects")
    left_names = _names(d.name for d in equations)
    allowed = set(base) | set(left_names)
    for equation in equations:
        unknown = variables(equation.expression) - allowed
        if unknown:
            raise ValueError(f"Unknown dependency: {sorted(unknown)}")
    new_names = tuple(name for name in left_names if name not in base)
    answers = []
    for assignment in enumerate_worlds(new_names):
        candidate = {**base, **assignment}
        if all(candidate[d.name] == evaluate(d.expression, candidate) for d in equations):
            answers.append(candidate)
    return tuple(answers)


def _same_vocabulary(worlds: Iterable[Mapping[str, bool]]) -> tuple[World, ...]:
    rows = tuple(_world(w) for w in worlds)
    if rows and any(set(w) != set(rows[0]) for w in rows):
        raise ValueError("All worlds must have the same vocabulary")
    return rows


def filter_evidence(worlds: Iterable[Mapping[str, bool]], evidence: Expr) -> tuple[World, ...]:
    """Retain exactly worlds satisfying evidence; does not introduce definitions."""
    variables(evidence)
    return tuple(w for w in _same_vocabulary(worlds) if evaluate(evidence, w))


def entails(worlds: Iterable[Mapping[str, bool]], proposition: Expr) -> bool:
    """Classical universal consequence; True on the empty set (vacuously)."""
    variables(proposition)
    rows = _same_vocabulary(worlds)
    values = tuple(evaluate(proposition, w) for w in rows)
    return all(values)


@dataclass(frozen=True)
class ObservationAnalysis:
    definable: bool
    # Successful tables contain only observed signatures; absence is not False.
    table: tuple[tuple[tuple[bool, ...], bool], ...]
    witness: tuple[World, World] | None


def analyze_observations(
    worlds: Iterable[Mapping[str, bool]], features: Sequence[Expr], target: Expr
) -> ObservationAnalysis:
    """Check factorization through the Boolean observation map on these worlds.

    A failure returns a same-feature/opposite-target witness. Empty worlds give
    a successful empty table. Zero features give the single signature () when
    at least one world exists.
    """
    rows = _same_vocabulary(worlds)
    features = tuple(features)
    for expr in (*features, target):
        variables(expr)
    # Validate every expression at every supplied world before looking for a witness.
    records = tuple((tuple(evaluate(f, w) for f in features), evaluate(target, w), w) for w in rows)
    representatives: dict[tuple[bool, ...], tuple[bool, World]] = {}
    for signature, value, world in records:
        if signature in representatives:
            previous, old_world = representatives[signature]
            if previous != value:
                return ObservationAnalysis(False, (), (dict(old_world), dict(world)))
        else:
            representatives[signature] = (value, world)
    table = tuple((key, representatives[key][0]) for key in sorted(representatives))
    return ObservationAnalysis(True, table, None)


def observed_formula(analysis: ObservationAnalysis, feature_names: Iterable[str]) -> Expr:
    """Build a DNF over synthetic coordinate names from a supplied target table.

    Names are distinct within the coordinate vocabulary. Bind each to its
    feature value; spelling shared with an original name does not identify them.
    This checks representation of given target values, not label learning.
    Unobserved signatures are set to False by convention, not by evidence.
    Empty conjunction = True; empty disjunction = False.
    """
    if type(analysis) is not ObservationAnalysis or type(analysis.definable) is not bool:
        raise TypeError("Expected ObservationAnalysis with a bool definable field")
    names = _names(feature_names)
    if not analysis.definable or analysis.witness is not None:
        raise ValueError("No observation-only formula exists for a conflicting table")
    result: Expr = Const(False)
    seen = set()
    for signature, target in analysis.table:
        if len(signature) != len(names) or any(type(bit) is not bool for bit in signature) or type(target) is not bool:
            raise ValueError("Malformed observation table")
        if signature in seen:
            raise ValueError("Duplicate observation signature")
        seen.add(signature)
        if target:
            term: Expr = Const(True)
            for name, bit in zip(names, signature):
                term = And(term, Var(name) if bit else Not(Var(name)))
            result = Or(result, term)
    return result


@dataclass(frozen=True)
class Rule:
    premises: frozenset[str]
    conclusion: str

    def __post_init__(self) -> None:
        _name(self.conclusion)
        premises = frozenset(self.premises)
        for premise in premises:
            _name(premise)
        object.__setattr__(self, "premises", premises)


def _rule_inputs(seeds: Iterable[str], rules: Iterable[Rule]) -> tuple[set[str], tuple[Rule, ...]]:
    known = set(seeds)
    for item in known:
        _name(item)
    rules = tuple(rules)
    if any(type(rule) is not Rule for rule in rules):
        raise TypeError("Expected Rule objects")
    return known, rules


def forward_closure(seeds: Iterable[str], rules: Iterable[Rule]) -> frozenset[str]:
    """Least superset of seeds closed under the declared finite Horn rules."""
    known, rules = _rule_inputs(seeds, rules)
    while True:
        additions = {r.conclusion for r in rules if r.premises <= known} - known
        if not additions:
            return frozenset(known)
        known.update(additions)


def plan_learning(seeds: Iterable[str], rules: Iterable[Rule]) -> tuple[str, ...]:
    """Produce a valid acquisition order for all derivable non-seed names.

    Repeatedly use the first enabled rule with a new conclusion. Rules may
    contain cycles; only the part enabled by seeds/empty-premise rules is learnt.
    """
    known, rules = _rule_inputs(seeds, rules)
    order = []
    while True:
        next_rule = next((r for r in rules if r.conclusion not in known and r.premises <= known), None)
        if next_rule is None:
            return tuple(order)
        known.add(next_rule.conclusion)
        order.append(next_rule.conclusion)


@dataclass(frozen=True)
class OrderReport:
    valid: bool
    known: frozenset[str]
    failure_index: int | None = None
    reason: str | None = None
    missing_alternatives: tuple[frozenset[str], ...] = ()


def verify_order(seeds: Iterable[str], rules: Iterable[Rule], order: Iterable[str]) -> OrderReport:
    """Check each step against prior knowledge; a valid prefix need not be complete.

    A conclusion needs at least one rule whose entire premise set is known.
    Duplicate/already-known steps fail. Indices are zero-based.
    """
    known, rules = _rule_inputs(seeds, rules)
    order = tuple(order)
    for conclusion in order:
        _name(conclusion)
    for index, conclusion in enumerate(order):
        if conclusion in known:
            return OrderReport(False, frozenset(known), index, "already known")
        candidates = tuple(r for r in rules if r.conclusion == conclusion)
        if not any(r.premises <= known for r in candidates):
            missing = tuple(r.premises - known for r in candidates)
            return OrderReport(False, frozenset(known), index, "no enabled rule", missing)
        known.add(conclusion)
    return OrderReport(True, frozenset(known))
