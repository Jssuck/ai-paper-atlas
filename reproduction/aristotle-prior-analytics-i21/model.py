"""I.21 teaching semantics. Model core reused from our I.20 code.
Not a reconstruction of unique ancient semantics.
"""
from dataclasses import dataclass
from itertools import product

@dataclass(frozen=True)
class Model:
    n: int
    worlds: tuple  # each world is an (A, B, C) tuple of bit masks

    def __post_init__(self):
        if type(self.n) is not int or self.n < 1:
            raise ValueError('n must be a positive integer')
        if type(self.worlds) is not tuple or not self.worlds:
            raise ValueError('worlds must be a nonempty tuple')
        for world in self.worlds:
            if type(world) is not tuple or len(world) != 3:
                raise ValueError('each world must be an (A,B,C) tuple')
            if any(type(mask) is not int or not 0 <= mask < (1 << self.n) for mask in world):
                raise ValueError('term masks must be integers within the universe')

    def extension(self, term, world=0):
        if type(term) is not str or term not in ('A','B','C'):
            raise ValueError('unknown term')
        if type(world) is not int or not 0 <= world < len(self.worlds):
            raise ValueError('unknown world')
        return self.worlds[world][('A','B','C').index(term)]

    def varying(self, term):
        masks = [self.extension(term, w) for w in range(len(self.worlds))]
        union, intersection = 0, (1 << self.n)-1
        for mask in masks:
            union |= mask
            intersection &= mask
        return union & ~intersection

    def holds(self, mode, quantity, predicate, subject):
        if type(mode) is not str or mode not in ('D','P','N','C','BOX'):
            raise ValueError('unknown mode')
        if type(quantity) is not str or quantity not in ('a','e','i','o'):
            raise ValueError('unknown quantity')
        self.extension(predicate)
        subjects = self.extension(subject)
        positive = quantity in ('a','i')
        universal = quantity in ('a','e')
        full = (1 << self.n)-1
        if mode == 'BOX':
            return all(self._quantify(self.extension(predicate,w) if positive else full ^ self.extension(predicate,w), self.extension(subject,w), universal) for w in range(len(self.worlds)))
        masks = [self.extension(predicate,w) if positive else full ^ self.extension(predicate,w) for w in range(len(self.worlds))]
        if mode == 'D':
            good = masks[0]
        elif mode == 'C':
            good = self.varying(predicate)
        elif mode == 'P':
            good = 0
            for mask in masks:
                good |= mask
        else:
            good = full
            for mask in masks:
                good &= mask
        return self._quantify(good, subjects, universal)

    @staticmethod
    def _quantify(good, subjects, universal):
        return subjects & ~good == 0 if universal else bool(subjects & good)

    def as_dict(self):
        return {'n':self.n, 'worlds':[{t:[i for i in range(self.n) if self.extension(t,w) & (1<<i)] for t in 'ABC'} for w in range(len(self.worlds))]}

def models(n, world_count):
    if type(n) is not int or n < 1 or type(world_count) is not int or world_count < 1:
        raise ValueError('positive integer dimensions required')
    for masks in product(range(1 << n), repeat=3*world_count):
        yield Model(n, tuple(tuple(masks[3*w:3*w+3]) for w in range(world_count)))

def examples():
    return {
        'witness_transfer_success': Model(2, ((1,3,1),(2,3,1))),
        'affirmative_actual_subject_failure': Model(2, ((1,2,1),(1,3,1))),
        'negative_background_failure': Model(2, ((2,2,1),(2,3,1))),
        'weak_not_strong': Model(2, ((2,3,1),(2,3,1))),
        'different_particular_witnesses': Model(2, ((1,1,3),(1,3,3))),
        'contingent_conclusion_not_actual': Model(2, ((2,1,1),(3,1,1))),
        'empty_middle': Model(1, ((1,1,0),(1,0,0))),
        'worldwise_not_anchored_necessity': Model(1, ((1,1,1),(0,0,1))),
    }
