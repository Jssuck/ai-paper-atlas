"""Original, bounded teaching model for Prior Analytics I.37; not an NLP parser."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Atom:
    name: str
    category: str
    aspect: str

    def __post_init__(self):
        for value in (self.name, self.category, self.aspect):
            if not isinstance(value, str) or not value.strip():
                raise ValueError('atom labels must be nonempty strings')


@dataclass(frozen=True)
class And:
    left: object
    right: object


@dataclass(frozen=True)
class Not:
    child: object


class Model:
    def __init__(self, domain, extensions):
        self.domain = frozenset(domain)
        self.extensions = {}
        for atom, members in extensions.items():
            if not isinstance(atom, Atom):
                raise TypeError('extension keys must be Atom values')
            members = frozenset(members)
            if not members <= self.domain:
                raise ValueError('extension outside domain')
            self.extensions[atom] = members

    def extension(self, expression):
        if isinstance(expression, Atom):
            # Missing evidence is not a negative fact.
            return self.extensions[expression]
        if isinstance(expression, And):
            return self.extension(expression.left) & self.extension(expression.right)
        if isinstance(expression, Not):
            return self.domain - self.extension(expression.child)
        raise TypeError('unsupported expression; no natural-language parsing')

    def includes(self, subject, predicate):
        return self.extension(subject) <= self.extension(predicate)

    def some(self, expression):
        return bool(self.extension(expression))


def chain_certificate(first, second, conclusion):
    """Recognize exactly two explicit inclusion edges and their composite.

    This checks shape only, NOT truth of premises. A False result only says
    this particular certificate is not recognized. No labels are erased.
    """
    edges = (first, second, conclusion)
    if any(not isinstance(e, tuple) or len(e) != 2 or
           any(not isinstance(t, Atom) for t in e) for e in edges):
        raise TypeError('each edge must be a pair of Atom values')
    c, b = first
    other_b, a = second
    return b == other_b and conclusion == (c, a)
