"""Original bounded AEIO teaching model for Prior Analytics I.24.

A domain has one representative per occupied three-predicate Boolean region.
This finite implementation is not the historical author's unique semantics.
"""
from fractions import Fraction
from itertools import product

FORMS = ('A', 'E', 'I', 'O')
TERMS = ('S', 'P', 'M')
POLICIES = ('allow_empty_terms', 'all_terms_nonempty')


def validate_mask(mask):
    if type(mask) is not int or not 1 <= mask <= 255:
        raise ValueError('mask must be an integer from 1 through 255; bool excluded')
    return mask


def validate_term(term):
    if type(term) is not str or term not in TERMS:
        raise ValueError('term must be S, P or M')
    return term


def validate_form(form):
    if type(form) is not str or form not in FORMS:
        raise ValueError('form must be uppercase A, E, I or O')
    return form


def validate_policy(policy):
    if type(policy) is not str or policy not in POLICIES:
        raise ValueError('unknown empty-term policy')
    return policy


def extension(mask, term):
    validate_mask(mask)
    validate_term(term)
    bit = TERMS.index(term)
    return frozenset(i for i in range(8) if mask & (1 << i) and i & (1 << bit))


def domain(mask):
    validate_mask(mask)
    return frozenset(i for i in range(8) if mask & (1 << i))


def proposition(mask, form, subject, predicate):
    validate_form(form)
    s, p = extension(mask, subject), extension(mask, predicate)
    if form == 'A':
        return s <= p
    if form == 'E':
        return not (s & p)
    if form == 'I':
        return bool(s & p)
    return bool(s - p)


def eligible(mask, policy='allow_empty_terms'):
    validate_mask(mask)
    validate_policy(policy)
    return policy == 'allow_empty_terms' or all(extension(mask, t) for t in TERMS)


def models(policy='allow_empty_terms'):
    validate_policy(policy)
    return tuple(m for m in range(1, 256) if eligible(m, policy))


def premises(figure):
    if type(figure) is not int or figure not in (1, 2, 3):
        raise ValueError('figure must be integer 1, 2 or 3; bool excluded')
    return {1: (('M', 'P'), ('S', 'M')),
            2: (('P', 'M'), ('S', 'M')),
            3: (('M', 'P'), ('M', 'S'))}[figure]


def validate_mood(mood):
    if type(mood) is not str or len(mood) != 3:
        raise ValueError('mood must be an uppercase three-letter string')
    for form in mood:
        validate_form(form)
    return mood


def evaluate(mask, figure, mood):
    validate_mask(mask)
    validate_mood(mood)
    major, minor = premises(figure)
    return (proposition(mask, mood[0], *major),
            proposition(mask, mood[1], *minor),
            proposition(mask, mood[2], 'S', 'P'))


def classify(figure, mood, policy='allow_empty_terms'):
    premises(figure)
    validate_mood(mood)
    validate_policy(policy)
    satisfying = []
    failures = []
    for mask in models(policy):
        a, b, c = evaluate(mask, figure, mood)
        if a and b:
            satisfying.append(mask)
            if not c:
                failures.append(mask)
    return {'figure': figure, 'mood': mood, 'policy': policy,
            'premise_models': len(satisfying), 'countermodel_count': len(failures),
            'valid': not failures, 'first_countermodel': failures[0] if failures else None}


def census(policy='allow_empty_terms'):
    validate_policy(policy)
    return [classify(f, ''.join(m), policy) for f in (1, 2, 3)
            for m in product(FORMS, repeat=3)]


def equal_remainders(whole_left, whole_right, part_left, part_right):
    """Check a supplied exact arithmetic instance, not a geometric construction.

    Only exact int/Fraction inputs, nonnegative wholes/parts, parts <= wholes.
    Return validity of implication, plus whether equalities were assumed true.
    """
    values = (whole_left, whole_right, part_left, part_right)
    if any(type(v) not in (int, Fraction) for v in values):
        raise ValueError('use exact int or Fraction, not float or bool')
    a, b, c, d = map(Fraction, values)
    if min(a, b, c, d) < 0 or c > a or d > b:
        raise ValueError('nonnegative parts must not exceed their wholes')
    assumptions = a == b and c == d
    conclusion = a - c == b - d
    return {'assumptions': assumptions, 'conclusion': conclusion,
            'implication': not assumptions or conclusion,
            'remainders': (a-c, b-d)}
