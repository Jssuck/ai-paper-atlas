"""II.21 teaching reconstruction, not a model of Aristotle's psychology."""
from dataclasses import dataclass
from itertools import product
import json

TERMS = ('A', 'B', 'C', 'D')


def validate_world(world):
    if not isinstance(world, dict) or set(world) != set(TERMS):
        raise ValueError('world must have exactly A, B, C, D')
    if any(not isinstance(v, frozenset) for v in world.values()):
        raise ValueError('extensions must be frozensets')
    if any(type(x) is not int or x < 0 for v in world.values() for x in v):
        raise ValueError('individuals must be nonnegative integers')


def premises(world):
    """p1: B subset A; p2: D subset B; p3: A disjoint C; p4: D subset C."""
    validate_world(world)
    a, b, c, d = (world[t] for t in TERMS)
    return (b <= a, d <= b, not a & c, d <= c)


def worlds(n):
    if type(n) is not int or not 1 <= n <= 3:
        raise ValueError('bounded census requires integer 1 <= n <= 3')
    subsets = tuple(frozenset(i for i in range(n) if mask & (1 << i))
                    for mask in range(1 << n))
    for extensions in product(subsets, repeat=4):
        yield dict(zip(TERMS, extensions))


def census(n):
    counts = dict(worlds=0, full_nonempty_D=0, full_empty_D=0,
                  missing_p4_nonempty_D=0, positive_route=0, negative_route=0)
    witness = None
    for w in worlds(n):
        counts['worlds'] += 1
        p1, p2, p3, p4 = premises(w)
        if p1 and p2 and w['D']:
            counts['positive_route'] += 1
            if not w['D'] <= w['A']:
                raise RuntimeError('positive route unsound')
        if p3 and p4 and w['D']:
            counts['negative_route'] += 1
            if w['D'] & w['A']:
                raise RuntimeError('negative route unsound')
        if all((p1,p2,p3,p4)):
            counts['full_nonempty_D' if w['D'] else 'full_empty_D'] += 1
        if p1 and p2 and p3 and w['D']:
            counts['missing_p4_nonempty_D'] += 1
            if witness is None:
                witness = {t: sorted(w[t]) for t in TERMS}
    return dict(n=n, counts=counts, missing_p4_witness=witness)


@dataclass(frozen=True)
class RecognitionState:
    """A fixed toy world: one object c is B and A; all B are A.

    Flags are possession/use records, not unrestricted modal operators.
    False opinion is explicitly NOT knowledge. exercise returns a new state;
    opinion is retained for conflict detection, not silently 'cured'.
    """
    universal_stored: bool
    recognition_stored: bool
    negative_opinion: bool
    exercised: bool = False

    def __post_init__(self):
        if any(type(x) is not bool for x in (
                self.universal_stored, self.recognition_stored,
                self.negative_opinion, self.exercised)):
            raise ValueError('state flags must be bool')
        if self.exercised and not self.available:
            raise ValueError('exercise requires both stored premises')

    @property
    def available(self):
        return self.universal_stored and self.recognition_stored

    @property
    def explicit_conflict(self):
        return self.exercised and self.negative_opinion

    def exercise(self):
        if not self.available:
            raise ValueError('cannot combine a missing premise')
        return RecognitionState(True, True, self.negative_opinion, True)


def acquire_verified(world, predicate, individual):
    """Only true recognized membership can enter the knowledge-side register."""
    validate_world(world)
    if predicate not in TERMS or type(individual) is not int or individual < 0:
        raise ValueError('invalid predicate or individual')
    if individual not in world[predicate]:
        raise ValueError('false recognition cannot count as knowledge')
    return (predicate, individual)


def recognition_census():
    rows = []
    for u, r, o in product((False, True), repeat=3):
        s = RecognitionState(u,r,o)
        after = s.exercise() if s.available else None
        rows.append(dict(universal_stored=u, recognition_stored=r,
                         negative_opinion=o, available=s.available,
                         exercised_before=s.exercised,
                         conflict_after=None if after is None else after.explicit_conflict))
    return rows


def main():
    print(json.dumps(dict(set_census=[census(n) for n in (1,2,3)],
                          recognition_states=recognition_census()),
                     ensure_ascii=False, sort_keys=True, indent=2))

if __name__ == '__main__':
    main()
