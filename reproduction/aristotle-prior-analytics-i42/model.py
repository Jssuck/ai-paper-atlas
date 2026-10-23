"""Original I.42 teaching model: categorical moods and local figure labels."""
from dataclasses import dataclass
from itertools import product

KINDS = ('A', 'E', 'I', 'O')
PATTERNS = {1: (('M', 'P'), ('S', 'M')),
            2: (('P', 'M'), ('S', 'M')),
            3: (('M', 'P'), ('M', 'S'))}


def figure_number(value):
    if type(value) is not int or value not in PATTERNS:
        raise ValueError('figure must be an integer in 1, 2, 3')
    return value


def kind(value):
    if not isinstance(value, str) or value not in KINDS:
        raise ValueError('kind must be A, E, I, or O')
    return value


def frozen_ids(values):
    items = tuple(values)
    if any(type(x) is not int or x < 0 for x in items):
        raise ValueError('object ids must be nonnegative integers, not booleans')
    return frozenset(items)


@dataclass(frozen=True)
class Model:
    domain: frozenset
    s: frozenset
    m: frozenset
    p: frozenset

    def __post_init__(self):
        for name in ('domain', 's', 'm', 'p'):
            object.__setattr__(self, name, frozen_ids(getattr(self, name)))
        if not self.domain:
            raise ValueError('domain must be nonempty')
        if any(not getattr(self, name) <= self.domain for name in ('s', 'm', 'p')):
            raise ValueError('term extension lies outside domain')

    def extension(self, term):
        if term not in ('S', 'M', 'P'):
            raise ValueError('term must be S, M, or P')
        return getattr(self, term.lower())

    def satisfies(self, quality, subject, predicate):
        quality = kind(quality)
        a, b = self.extension(subject), self.extension(predicate)
        return {'A': a <= b, 'E': not (a & b),
                'I': bool(a & b), 'O': bool(a - b)}[quality]

    def all_terms_nonempty(self):
        return bool(self.s and self.m and self.p)


def canonical_models(nonempty_terms=False):
    """One object per occupied nonzero S/M/P type; 000 only if all empty."""
    if type(nonempty_terms) is not bool:
        raise ValueError('nonempty_terms must be bool')
    for support in range(128):
        objects = {t for t in range(1, 8) if support & (1 << (t - 1))}
        model = Model(objects or {0}, {t for t in objects if t & 4},
                      {t for t in objects if t & 2}, {t for t in objects if t & 1})
        if not nonempty_terms or model.all_terms_nonempty():
            yield model


def validate_mood(mood):
    if not isinstance(mood, str) or len(mood) != 3:
        raise ValueError('mood must have three A/E/I/O characters')
    for q in mood:
        kind(q)
    return mood


def evaluate(model, figure, mood):
    figure = figure_number(figure)
    mood = validate_mood(mood)
    major, minor = PATTERNS[figure]
    return (model.satisfies(mood[0], *major),
            model.satisfies(mood[1], *minor),
            model.satisfies(mood[2], 'S', 'P'))


def countermodel(figure, mood, nonempty_terms=False):
    figure_number(figure)
    validate_mood(mood)
    for model in canonical_models(nonempty_terms):
        major, minor, conclusion = evaluate(model, figure, mood)
        if major and minor and not conclusion:
            return model
    return None


def valid_moods(nonempty_terms=False):
    return {f: [a+b+c for a, b, c in product(KINDS, repeat=3)
                if countermodel(f, a+b+c, nonempty_terms) is None]
            for f in PATTERNS}


def candidate_figures(conclusion_kind, nonempty_terms=False):
    quality = kind(conclusion_kind)
    return tuple(f for f, moods in valid_moods(nonempty_terms).items()
                 if any(m[-1] == quality for m in moods))


def classify_step(major, minor, conclusion):
    """Triples are (kind, subject, predicate); labels are syntactic, not proofs."""
    for prop in (major, minor, conclusion):
        if not isinstance(prop, tuple) or len(prop) != 3:
            raise ValueError('propositions must be triples')
        kind(prop[0])
        if any(not isinstance(t, str) or not t for t in prop[1:]):
            raise ValueError('term names must be nonempty strings')
    s, p = conclusion[1:]
    names = set(major[1:] + minor[1:] + conclusion[1:])
    if s == p or len(names) != 3:
        raise ValueError('exactly three distinct term names required')
    m, = names - {s, p}
    mapping = {'S': s, 'P': p, 'M': m}
    for f, (a, b) in PATTERNS.items():
        if major[1:] == tuple(mapping[t] for t in a) and minor[1:] == tuple(mapping[t] for t in b):
            return f
    return None


def mixed_proof():
    first = (('A', 'M', 'P'), ('A', 'S', 'M'), ('A', 'S', 'P'))
    second = (('E', 'Q', 'P'), ('A', 'S', 'P'), ('E', 'S', 'Q'))
    return [dict(figure=classify_step(*step), major=step[0], minor=step[1], conclusion=step[2])
            for step in (first, second)]
