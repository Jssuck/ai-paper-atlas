"""Original, deliberately restricted teaching model for Prior Analytics I.33.
No natural-language interpretation or historical-semantics claim is made.
All(P, S) means every S is P; Some(P, S) means some S is P.
"""
from dataclasses import dataclass
from itertools import product


def _name(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('names must be nonblank strings')


@dataclass(frozen=True)
class Context:
    time: str = 'fixed-time'
    aspect: str = 'whole-object'

    def __post_init__(self):
        _name(self.time)
        _name(self.aspect)


@dataclass(frozen=True)
class Proposition:
    kind: str
    predicate: str
    subject: str
    context: Context = Context()

    def __post_init__(self):
        if self.kind not in ('All', 'Some', 'Member'):
            raise ValueError('unsupported quantifier or proposition kind')
        _name(self.predicate)
        _name(self.subject)
        if not isinstance(self.context, Context):
            raise ValueError('a typed Context is required')


def check_chain(major, minor, conclusion):
    """Syntactic certificate check, not a test of actual premise truth.

    Only All(A,B), All(B,C) => All(A,C) and
    All(A,B), Member(B,c) => Member(A,c) are accepted.
    Failure means unsupported by THIS checker, not logically invalid in general.
    """
    if not all(isinstance(p, Proposition) for p in (major, minor, conclusion)):
        return False, 'untyped-input'
    if not major.context == minor.context == conclusion.context:
        return False, 'context-mismatch'
    if major.kind != 'All':
        return False, 'major-not-universal'
    if minor.kind not in ('All', 'Member'):
        return False, 'unsupported-minor'
    if major.subject != minor.predicate:
        return False, 'middle-mismatch'
    if conclusion.kind != minor.kind:
        return False, 'conclusion-kind-mismatch'
    if conclusion.predicate != major.predicate or conclusion.subject != minor.subject:
        return False, 'conclusion-terms-mismatch'
    return True, 'verified-shape-only'


def powerset(n):
    return [frozenset(i for i in range(n) if mask & (1 << i))
            for mask in range(1 << n)]


def evaluate(prop, extensions, individuals):
    """One explicit extensional interpretation in the proposition's context.

    Caller supplies the interpretation for that context; this evaluator neither
    infers context alignment nor treats an individual name as a class name.
    Unknown names raise KeyError instead of silently becoming empty classes.
    """
    p = extensions[prop.predicate]
    if prop.kind == 'Member':
        return individuals[prop.subject] in p
    s = extensions[prop.subject]
    if prop.kind == 'All':
        return s <= p
    return bool(s & p)


def experiments(max_n=3):
    if not isinstance(max_n, int) or isinstance(max_n, bool) or not 0 <= max_n <= 5:
        raise ValueError('max_n must be an integer from 0 to 5')
    all_cases = all_premises = all_failures = 0
    weak_cases = weak_premises = weak_countermodels = 0
    member_cases = member_premises = member_failures = 0
    identity_cases = identity_failures = 0
    first_countermodel = None
    for n in range(max_n + 1):
        subsets = powerset(n)
        for a, b, c in product(subsets, repeat=3):
            all_cases += 1
            if b <= a and c <= b:
                all_premises += 1
                all_failures += not c <= a
            weak_cases += 1
            if a & b and c <= b:
                weak_premises += 1
                if not c <= a:
                    weak_countermodels += 1
                    if first_countermodel is None:
                        first_countermodel = {'n': n, 'A': sorted(a), 'B': sorted(b), 'C': sorted(c)}
        for a, b in product(subsets, repeat=2):
            for individual in range(n):
                member_cases += 1
                if b <= a and individual in b:
                    member_premises += 1
                    member_failures += individual not in a
        for p in subsets:
            for x, y in product(range(n), repeat=2):
                if x == y:
                    identity_cases += 1
                    identity_failures += ((x in p) != (y in p))
    return {
        'domain_sizes': list(range(max_n + 1)),
        'all_chain': {'assignments': all_cases, 'premise_models': all_premises, 'failures': all_failures},
        'some_major_all_minor': {'assignments': weak_cases, 'premise_models': weak_premises,
                                 'countermodels': weak_countermodels, 'first': first_countermodel},
        'member_chain': {'assignments': member_cases, 'premise_models': member_premises, 'failures': member_failures},
        'same_object_substitution': {'equal_identity_assignments': identity_cases, 'failures': identity_failures},
        'limit': 'finite extensional teaching checks, not a general proof or a reconstruction of the ancient examples'
    }


if __name__ == '__main__':
    import json
    print(json.dumps(experiments(), indent=2, ensure_ascii=False))
