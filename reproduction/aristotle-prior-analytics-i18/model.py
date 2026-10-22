"""Explicit modern actual-subject semantics; not a historical completeness claim."""
from dataclasses import dataclass
from itertools import product

TERMS = ('A', 'B', 'C')
FORMS = ('A', 'E', 'I', 'O')
MODES = ('actual', 'possible', 'necessary', 'contingent')

@dataclass(frozen=True)
class Model:
    n: int
    worlds: tuple
    actual: int = 0

    def __post_init__(self):
        if type(self.n) is not int or self.n < 1:
            raise ValueError('n must be a positive integer')
        if type(self.worlds) is not tuple or not self.worlds:
            raise ValueError('worlds must be a nonempty tuple')
        for row in self.worlds:
            if type(row) is not tuple or len(row) != 3:
                raise ValueError('each world has three masks')
            if any(type(v) is not int or not 0 <= v < 2**self.n for v in row):
                raise ValueError('masks must be bounded nonnegative integers')
        if type(self.actual) is not int or not 0 <= self.actual < len(self.worlds):
            raise ValueError('invalid actual world')

    def extension(self, term, world=None):
        if type(term) is not str or term not in TERMS:
            raise ValueError('invalid term')
        w = self.actual if world is None else world
        if type(w) is not int or not 0 <= w < len(self.worlds):
            raise ValueError('invalid world')
        mask = self.worlds[w][TERMS.index(term)]
        return frozenset(x for x in range(self.n) if mask & (1 << x))

    def categorical(self, predicate, subject, form, mode='actual'):
        if type(form) is not str or form not in FORMS:
            raise ValueError('invalid form')
        if type(mode) is not str or mode not in MODES:
            raise ValueError('invalid mode')
        subjects = self.extension(subject)
        extensions = [self.extension(predicate, w) for w in range(len(self.worlds))]
        answers = []
        for x in subjects:
            signs = [(x in p) == (form in ('A', 'I')) for p in extensions]
            value = {'actual': signs[self.actual], 'possible': any(signs),
                     'necessary': all(signs), 'contingent': any(signs) and not all(signs)}[mode]
            answers.append(value)
        return all(answers) if form in ('A', 'E') else any(answers)

    def persistent_exclusion(self, first, second):
        # Validate both even if short-circuit would find an early intersection.
        left = [self.extension(first, w) for w in range(len(self.worlds))]
        right = [self.extension(second, w) for w in range(len(self.worlds))]
        return all(x.isdisjoint(y) for x, y in zip(left, right))

    def rigid(self, term):
        actual = self.extension(term)
        return all(self.extension(term, w) == actual for w in range(len(self.worlds)))

    def jointly_possible(self, predicate, subject, positive=True):
        if type(positive) is not bool:
            raise ValueError('positive must be bool')
        s = self.extension(subject)
        ps = [self.extension(predicate, w) for w in range(len(self.worlds))]
        return any(s <= p if positive else s.isdisjoint(p) for p in ps)

    def as_dict(self):
        return {'n': self.n, 'worlds': self.worlds, 'actual': self.actual}


def models(n, world_count=2):
    if type(n) is not int or n < 1 or type(world_count) is not int or world_count < 1:
        raise ValueError('positive integer sizes required')
    for values in product(range(2**n), repeat=3*world_count):
        worlds = tuple(tuple(values[3*w:3*w+3]) for w in range(world_count))
        for actual in range(world_count):
            yield Model(n, worlds, actual)


def named_models():
    return {
        'missing_persistence': Model(1, ((0,1,1),(1,1,1))),
        'bridge_without_actual_conclusion': Model(1, ((0,1,1),(1,0,1))),
        'bridge_without_strict_conclusion': Model(2, ((0,2,1),(1,2,1))),
        'possible_negative_not_convertible': Model(1, ((0,1,1),(0,1,0))),
        'objectwise_not_joint': Model(2, ((1,2,3),(2,1,3))),
        'stable_overlap': Model(2, ((3,3,1),(0,3,1))),
        'stable_separation': Model(2, ((3,2,1),(0,2,1))),
        'empty_subject': Model(1, ((0,0,0),(1,0,0))),
    }
