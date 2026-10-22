"""Explicit definitional substitution: a modern teaching model, not an NLP system."""
from dataclasses import dataclass
from types import MappingProxyType


def name_check(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('names must be nonblank strings')


@dataclass(frozen=True)
class Atom:
    name: str
    def __post_init__(self):
        name_check(self.name)


@dataclass(frozen=True)
class Ref:
    name: str
    def __post_init__(self):
        name_check(self.name)


@dataclass(frozen=True)
class And:
    left: object
    right: object


@dataclass(frozen=True)
class Not:
    child: object


def term_check(term):
    if isinstance(term, (Atom, Ref)):
        name_check(term.name)
    elif isinstance(term, And):
        term_check(term.left)
        term_check(term.right)
    elif isinstance(term, Not):
        term_check(term.child)
    else:
        raise TypeError('expected Atom, Ref, And or Not')


class Definitions:
    """Explicit definitions; all references must exist and all definitions be acyclic."""
    def __init__(self, definitions):
        if not isinstance(definitions, dict):
            raise TypeError('definitions must be a dictionary')
        copied = dict(definitions)
        for name, term in copied.items():
            name_check(name)
            term_check(term)
        self.definitions = MappingProxyType(copied)
        # Validate unused definitions too, not just those reached by a later query.
        for name in copied:
            self.expand(Ref(name))

    def expand(self, term):
        term_check(term)
        def visit(t, stack):
            if isinstance(t, Atom):
                return t
            if isinstance(t, Ref):
                if t.name not in self.definitions:
                    raise KeyError('undefined reference: ' + t.name)
                if t.name in stack:
                    raise ValueError('cyclic definition: ' + t.name)
                return visit(self.definitions[t.name], stack + (t.name,))
            if isinstance(t, And):
                return And(visit(t.left, stack), visit(t.right, stack))
            return Not(visit(t.child, stack))
        return visit(term, ())

    def equivalent_by_definition(self, left, right):
        """Sufficient syntactic certificate, NOT complete semantic equivalence."""
        return self.expand(left) == self.expand(right)


class Model:
    """Finite extensional model with explicit domain-relative complement."""
    def __init__(self, domain, extensions):
        # Materialize once so generators work as expected.
        objects = tuple(domain)
        if any(type(x) is not int for x in objects):
            raise TypeError('domain objects must be integers, not booleans')
        self.domain = frozenset(objects)
        if not isinstance(extensions, dict):
            raise TypeError('extensions must be a dictionary')
        copied = {}
        for name, values in extensions.items():
            name_check(name)
            members = tuple(values)
            if any(type(x) is not int for x in members):
                raise TypeError('extension objects must be integers, not booleans')
            value = frozenset(members)
            if not value <= self.domain:
                raise ValueError('extension outside domain')
            copied[name] = value
        self.extensions = MappingProxyType(copied)

    def extension(self, term, definitions):
        if not isinstance(definitions, Definitions):
            raise TypeError('expected Definitions')
        expanded = definitions.expand(term)
        def evaluate(t):
            if isinstance(t, Atom):
                return self.extensions[t.name]  # Missing evidence is not false.
            if isinstance(t, And):
                # Evaluate BOTH sides, even if the first is empty.
                left = evaluate(t.left)
                right = evaluate(t.right)
                return left & right
            return self.domain - evaluate(t.child)
        return evaluate(expanded)

    def proposition(self, kind, subject, predicate, definitions):
        if kind not in ('A', 'E', 'I', 'O'):
            raise ValueError('kind must be A, E, I or O')
        s = self.extension(subject, definitions)
        p = self.extension(predicate, definitions)
        if kind == 'A':
            return s <= p
        if kind == 'E':
            return not bool(s & p)
        if kind == 'I':
            return bool(s & p)
        return bool(s - p)
