"""Finite modern teaching semantics, not Aristotle's proof calculus."""
from dataclasses import dataclass


def _label(value):
    if not isinstance(value, str) or not value or not value.strip():
        raise ValueError('label must be a nonblank string')
    return value


@dataclass(frozen=True)
class Space:
    atoms: tuple

    def __post_init__(self):
        atoms = tuple(self.atoms)
        for atom in atoms:
            _label(atom)
        if len(set(atoms)) != len(atoms) or len(atoms) > 8:
            raise ValueError('use at most eight distinct atoms')
        object.__setattr__(self, 'atoms', atoms)

    @property
    def rows(self):
        return 1 << len(self.atoms)

    def assignment(self, row):
        if type(row) is not int or not 0 <= row < self.rows:
            raise ValueError('row must be an integer in this space')
        return {
            atom: bool(row & (1 << (len(self.atoms) - 1 - i)))
            for i, atom in enumerate(self.atoms)
        }

    def atom(self, name):
        _label(name)
        if name not in self.atoms:
            raise ValueError('undeclared atom')
        return Formula(self, frozenset(r for r in range(self.rows) if self.assignment(r)[name]))


@dataclass(frozen=True)
class Formula:
    space: Space
    true_rows: frozenset

    def __post_init__(self):
        if not isinstance(self.space, Space):
            raise TypeError('space must be Space')
        supplied = tuple(self.true_rows)
        if any(type(r) is not int or not 0 <= r < self.space.rows for r in supplied):
            raise ValueError('invalid truth row')
        object.__setattr__(self, 'true_rows', frozenset(supplied))

    def negated(self):
        return Formula(self.space, frozenset(range(self.space.rows)) - self.true_rows)

    def implies(self, other):
        _formula(other, self.space)
        return Formula(self.space, self.negated().true_rows | other.true_rows)


def _formula(formula, space=None):
    if not isinstance(formula, Formula):
        raise TypeError('expected Formula')
    if space is not None and formula.space != space:
        raise ValueError('different atom spaces')
    return formula


def common_rows(premises, space):
    if not isinstance(space, Space):
        raise TypeError('expected Space')
    premises = tuple(premises)
    # Validate all entries before intersection, including after an empty formula.
    for premise in premises:
        _formula(premise, space)
    result = frozenset(range(space.rows))
    for premise in premises:
        result &= premise.true_rows
    return result


def counterexample(premises, conclusion):
    _formula(conclusion)
    bad = common_rows(premises, conclusion.space) - conclusion.true_rows
    return None if not bad else conclusion.space.assignment(min(bad))


def entails(premises, conclusion):
    return counterexample(premises, conclusion) is None


@dataclass(frozen=True)
class Assumption:
    label: str
    formula: Formula

    def __post_init__(self):
        _label(self.label)
        _formula(self.formula)


@dataclass(frozen=True)
class ReductioCertificate:
    background: tuple
    temporary: Assumption
    conclusion: Formula

    def __post_init__(self):
        object.__setattr__(self, 'background', tuple(self.background))
        if not isinstance(self.temporary, Assumption):
            raise TypeError('temporary must be Assumption')
        _formula(self.conclusion, self.temporary.formula.space)
        labels = []
        for premise in self.background:
            if not isinstance(premise, Assumption):
                raise TypeError('background must contain Assumptions')
            _formula(premise.formula, self.conclusion.space)
            labels.append(premise.label)
        if len(set(labels)) != len(labels) or self.temporary.label in labels:
            raise ValueError('assumption labels must be distinct across scopes')


def verify_reductio(certificate):
    """Finite semantic check, not a syntactic proof of the inner contradiction."""
    if not isinstance(certificate, ReductioCertificate):
        raise TypeError('expected ReductioCertificate')
    if certificate.conclusion != certificate.temporary.formula.negated():
        return False
    context = tuple(a.formula for a in certificate.background) + (certificate.temporary.formula,)
    return not common_rows(context, certificate.conclusion.space)


def is_even_square_equivalent(n):
    if type(n) is not int:
        raise TypeError('n must be an integer, not bool')
    return (n * n % 2 == 0) == (n % 2 == 0)
