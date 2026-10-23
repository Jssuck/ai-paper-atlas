"""Modern finite-set teaching model, not a reconstruction of unique ancient semantics."""
from dataclasses import dataclass
from itertools import combinations

@dataclass(frozen=True)
class Atom:
    name: str

@dataclass(frozen=True)
class And:
    parts: tuple

@dataclass(frozen=True)
class Or:
    parts: tuple

@dataclass(frozen=True)
class Not:
    part: object


def validate(formula):
    if isinstance(formula, Atom):
        if not isinstance(formula.name, str) or not formula.name:
            raise ValueError('atom name must be a nonempty string')
    elif isinstance(formula, (And, Or)):
        if not isinstance(formula.parts, tuple) or len(formula.parts) < 2:
            raise ValueError('connective requires at least two tuple members')
        for part in formula.parts:
            validate(part)
    elif isinstance(formula, Not):
        validate(formula.part)
    else:
        raise ValueError('unsupported formula')


def atoms(formula):
    validate(formula)
    if isinstance(formula, Atom):
        return frozenset((formula.name,))
    if isinstance(formula, Not):
        return atoms(formula.part)
    return frozenset().union(*(atoms(p) for p in formula.parts))


class Model:
    def __init__(self, universe, interpretation):
        self.universe = frozenset(universe)
        self.interpretation = {name: frozenset(values) for name, values in interpretation.items()}
        if any(not isinstance(n, str) or not n for n in self.interpretation):
            raise ValueError('invalid predicate name')
        if any(not v <= self.universe for v in self.interpretation.values()):
            raise ValueError('predicate outside universe')

    def extension(self, formula):
        # Validate the whole tree and all names before Boolean short circuit is possible.
        names = atoms(formula)
        if not names <= self.interpretation.keys():
            raise ValueError('uninterpreted predicate')
        return self._extension(formula)

    def _extension(self, formula):
        if isinstance(formula, Atom):
            return self.interpretation[formula.name]
        if isinstance(formula, Not):
            return self.universe - self._extension(formula.part)
        sets = [self._extension(p) for p in formula.parts]
        if isinstance(formula, And):
            return frozenset.intersection(*sets)
        return frozenset.union(*sets)

    def inclusion(self, subject, predicate):
        return self.extension(subject) <= self.extension(predicate)

    def counterexamples(self, subject, predicate):
        return self.extension(subject) - self.extension(predicate)

    def definition(self, subject, formula):
        return self.extension(subject) == self.extension(formula)


def conjunct_leaves(formula):
    """Flatten only positive top-level conjunction. Never project through Or or Not."""
    validate(formula)
    if isinstance(formula, And):
        return tuple(leaf for p in formula.parts for leaf in conjunct_leaves(p))
    return (formula,)


def project_component(formula, target):
    validate(target)
    if target not in conjunct_leaves(formula):
        raise ValueError('target is not an explicit top-level conjunct')
    return target


@dataclass(frozen=True)
class Certificate:
    subject: object
    predicate: object


def verify_certificate(model, certificate, subject, predicate):
    """Finite-model evidence: exact goal match plus truth in this model, not a proof."""
    validate(subject)
    validate(predicate)
    model.inclusion(subject, predicate)  # Validate requested names, even for a mismatch.
    validate(certificate.subject)
    validate(certificate.predicate)
    # Evaluate even mismatched certificates, so malformed names never pass silently.
    truth = model.inclusion(certificate.subject, certificate.predicate)
    return certificate.subject == subject and certificate.predicate == predicate and truth


def verify_components(model, subject, whole, certificates):
    """Check each conjunct explicitly; duplicate local evidence cannot fill missing goals."""
    model.inclusion(subject, whole)  # Invalid goals must not be hidden by empty evidence.
    leaves = conjunct_leaves(whole)
    certificates = tuple(certificates)
    for certificate in certificates:
        model.inclusion(certificate.subject, certificate.predicate)
    for leaf in leaves:
        if not any(verify_certificate(model, c, subject, leaf) for c in certificates):
            return False
    return True


def powerset(items):
    items = tuple(items)
    for n in range(len(items) + 1):
        for choice in combinations(items, n):
            yield frozenset(choice)
