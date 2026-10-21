"""Explicit modern teaching semantics; not Aristotle's unique modal semantics."""
from dataclasses import dataclass
from itertools import product

TERMS = ('A', 'B', 'C')
MODES = ('N+', 'N-', 'M+', 'M-', 'K')

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
        for world in self.worlds:
            if type(world) is not tuple or len(world) != 3:
                raise ValueError('each world must be a three-mask tuple')
            if any(type(v) is not int or not 0 <= v < (1 << self.n) for v in world):
                raise ValueError('masks must be bounded nonnegative integers')
        if type(self.actual) is not int or not 0 <= self.actual < len(self.worlds):
            raise ValueError('invalid actual index')

    def mask(self, term, world=None):
        if term not in TERMS:
            raise ValueError('unknown term')
        world = self.actual if world is None else world
        if type(world) is not int or not 0 <= world < len(self.worlds):
            raise ValueError('invalid world index')
        return self.worlds[world][TERMS.index(term)]

    def modal(self, predicate, subject, mode, quantity='all'):
        """Quantify actual subject objects, then worlds for the SAME object."""
        if mode not in MODES or quantity not in ('all', 'some'):
            raise ValueError('unknown mode or quantity')
        subject_mask = self.mask(subject)
        values = tuple(self.mask(predicate, w) for w in range(len(self.worlds)))
        answers = []
        for x in range(self.n):
            bit = 1 << x
            if subject_mask & bit:
                signs = tuple(bool(v & bit) for v in values)
                answer = {'N+': all(signs), 'N-': not any(signs),
                          'M+': any(signs), 'M-': not all(signs),
                          'K': any(signs) and not all(signs)}[mode]
                answers.append(answer)
        return all(answers) if quantity == 'all' else any(answers)

    def categorical(self, predicate, subject, quality):
        if quality not in ('A', 'E', 'I', 'O'):
            raise ValueError('unknown categorical quality')
        p, s = self.mask(predicate), self.mask(subject)
        return {'A': not bool(s & ~p), 'E': not bool(s & p),
                'I': bool(s & p), 'O': bool(s & ~p)}[quality]

    def symmetric_negative(self, predicate, subject):
        """E*: two local negative anchors; a stipulated conversion bridge."""
        return self.modal(predicate, subject, 'N-') and self.modal(subject, predicate, 'N-')

    def stable_positive(self, predicate, subject):
        """S+: all-world inclusion, NOT implied by local N+."""
        return all(not (self.mask(subject, w) & ~self.mask(predicate, w))
                   for w in range(len(self.worlds)))

    def jointly_possible(self, predicate, subject, positive=True):
        if type(positive) is not bool:
            raise ValueError('positive must be bool')
        s = self.mask(subject)
        return any(not (s & ~self.mask(predicate, w)) if positive
                   else not (s & self.mask(predicate, w))
                   for w in range(len(self.worlds)))

    def as_dict(self):
        return {'n': self.n, 'worlds': self.worlds, 'actual': self.actual}


def models(n, world_count=2):
    if type(n) is not int or n < 1 or type(world_count) is not int or world_count < 1:
        raise ValueError('positive integer sizes required')
    for flat in product(range(1 << n), repeat=3 * world_count):
        worlds = tuple(tuple(flat[i:i + 3]) for i in range(0, len(flat), 3))
        for actual in range(world_count):
            yield Model(n, worlds, actual)


def examples():
    return {
        'local_positive_not_possible': Model(2, ((1, 1, 2), (1, 3, 2))),
        'stable_positive_not_strong': Model(1, ((1, 0, 1), (1, 1, 1))),
        'stable_positive_not_actual': Model(1, ((0, 0, 1), (1, 1, 1))),
        'symmetric_negative_not_necessary': Model(3, ((1, 2, 4), (5, 6, 4))),
        'symmetric_negative_not_strong': Model(3, ((1, 2, 4), (1, 6, 4))),
        'one_way_negative_not_actual': Model(2, ((2, 1, 2), (2, 3, 2))),
        'negative_minor_positive_endpoint': Model(2, ((2, 1, 2), (3, 1, 2))),
        'negative_minor_negative_endpoint': Model(2, ((0, 1, 2), (1, 1, 2))),
        'particular_major_no_positive_endpoint': Model(2, ((1, 3, 2), (1, 1, 2))),
        'particular_major_positive_endpoint': Model(2, ((3, 3, 2), (3, 1, 2))),
        'pointwise_not_joint': Model(2, ((1, 3, 3), (2, 3, 3))),
        'different_witnesses': Model(2, ((1, 3, 3), (1, 3, 3))),
        'empty_subject': Model(1, ((1, 0, 0),)),
    }
