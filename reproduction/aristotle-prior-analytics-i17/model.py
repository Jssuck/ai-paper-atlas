"""Modern finite teaching reconstruction, not an ancient semantic attribution.

Quantification over the actual subject extension precedes modal quantification.
Every object has a fixed identity in a nonempty constant domain. Every listed
world is accessible, including the distinguished actual world.
"""
from dataclasses import dataclass
from itertools import product

TERMS = ('A', 'B', 'C')
FORMS = ('A', 'E', 'I', 'O')
MODALITIES = ('actual', 'necessary', 'possible', 'contingent')


@dataclass(frozen=True)
class Model:
    n: int
    worlds: tuple
    actual: int = 0

    def __post_init__(self):
        if type(self.n) is not int or self.n <= 0:
            raise ValueError('domain size must be a positive integer')
        if type(self.worlds) is not tuple or not self.worlds:
            raise ValueError('worlds must be a nonempty tuple')
        for row in self.worlds:
            if type(row) is not tuple or len(row) != len(TERMS):
                raise ValueError('each world must be a tuple of three masks')
            if any(type(mask) is not int or not 0 <= mask < 2 ** self.n for mask in row):
                raise ValueError('predicate masks must be bounded nonnegative integers')
        if type(self.actual) is not int or not 0 <= self.actual < len(self.worlds):
            raise ValueError('actual world index out of range')

    def extension(self, term, world=None):
        if type(term) is not str or term not in TERMS:
            raise ValueError('unknown term')
        index = self.actual if world is None else world
        if type(index) is not int or not 0 <= index < len(self.worlds):
            raise ValueError('world index out of range')
        mask = self.worlds[index][TERMS.index(term)]
        return frozenset(x for x in range(self.n) if mask & (1 << x))

    def profile(self, predicate, obj):
        if type(obj) is not int or not 0 <= obj < self.n:
            raise ValueError('object index out of range')
        return tuple(obj in self.extension(predicate, w) for w in range(len(self.worlds)))

    def categorical(self, predicate, subject, form='A', modality='actual'):
        if type(form) is not str or form not in FORMS:
            raise ValueError('unknown categorical form')
        if type(modality) is not str or modality not in MODALITIES:
            raise ValueError('unknown modality')
        subjects = self.extension(subject)
        self.extension(predicate)  # Reject bad predicates even with empty subject.
        answers = []
        positive = form in ('A', 'I')
        for obj in subjects:
            signs = self.profile(predicate, obj)
            signed = signs if positive else tuple(not v for v in signs)
            if modality == 'actual':
                answer = signed[self.actual]
            elif modality == 'necessary':
                answer = all(signed)
            elif modality == 'possible':
                answer = any(signed)
            else:
                answer = any(signed) and not all(signed)
            answers.append(answer)
        return all(answers) if form in ('A', 'E') else any(answers)

    def noncontingency_witnesses(self, predicate, subject):
        self.extension(predicate)
        positive, negative = [], []
        for obj in sorted(self.extension(subject)):
            signs = self.profile(predicate, obj)
            if all(signs):
                positive.append(obj)
            elif not any(signs):
                negative.append(obj)
        return {'necessary_positive': positive, 'necessary_negative': negative}

    def jointly_possible(self, predicate, subject, positive=True):
        """One common world for all actual subject objects; NOT objectwise M."""
        if type(positive) is not bool:
            raise ValueError('positive must be bool')
        s = self.extension(subject)
        possibilities = [self.extension(predicate, w) for w in range(len(self.worlds))]
        return any(s <= p if positive else s.isdisjoint(p) for p in possibilities)

    def as_dict(self):
        return {'n': self.n, 'worlds': self.worlds, 'actual': self.actual}


def models(n, world_count=2):
    if type(n) is not int or n < 1 or type(world_count) is not int or world_count < 1:
        raise ValueError('domain and world counts must be positive integers')
    for flat in product(range(2 ** n), repeat=3 * world_count):
        rows = tuple(tuple(flat[k:k + 3]) for k in range(0, len(flat), 3))
        for actual in range(world_count):
            yield Model(n, rows, actual)


def examples():
    return {
        'disjoint': Model(2, ((3, 1, 2), (0, 1, 2))),
        'identical': Model(2, ((3, 1, 1), (0, 1, 1))),
        'conversion_failure': Model(2, ((3, 1, 2), (2, 1, 2))),
        'necessary_positive': Model(1, ((1, 1, 1), (1, 1, 1))),
        'necessary_negative': Model(1, ((0, 1, 1), (0, 1, 1))),
        'mixed_fixed': Model(2, ((1, 3, 3), (1, 3, 3))),
        'alternating_witnesses': Model(2, ((1, 3, 3), (2, 3, 3))),
    }
