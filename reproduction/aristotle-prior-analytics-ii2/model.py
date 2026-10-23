"""Original finite teaching model for Prior Analytics II.2; Python stdlib only."""
from dataclasses import dataclass

NAMES = ('A', 'B', 'C')
MOODS = {
    'Barbara': (('A', 'B', 'A'), ('A', 'C', 'B'), ('A', 'C', 'A')),
    'Celarent': (('E', 'B', 'A'), ('A', 'C', 'B'), ('E', 'C', 'A')),
    'Darii': (('A', 'B', 'A'), ('I', 'C', 'B'), ('I', 'C', 'A')),
    'Ferio': (('E', 'B', 'A'), ('I', 'C', 'B'), ('O', 'C', 'A')),
}

@dataclass(frozen=True)
class Model:
    universe: frozenset
    A: frozenset
    B: frozenset
    C: frozenset

    def __post_init__(self):
        for name in ('universe',) + NAMES:
            value = getattr(self, name)
            if not isinstance(value, frozenset):
                raise TypeError(f'{name} must be a frozenset')
            if any(type(x) is not int for x in value):
                raise TypeError('Objects must be integers, not bools or other values')
        if not self.universe:
            raise ValueError('Universe must be nonempty')
        for name in NAMES:
            if not getattr(self, name) <= self.universe:
                raise ValueError(f'{name} lies outside universe')


def validate(model):
    if not isinstance(model, Model):
        raise TypeError('Expected Model')
    model.__post_init__()


def proposition(model, kind, subject, predicate):
    validate(model)
    if kind not in ('A', 'E', 'I', 'O'):
        raise ValueError('Unknown proposition kind')
    if subject not in NAMES or predicate not in NAMES:
        raise ValueError('Unknown term')
    s, p = getattr(model, subject), getattr(model, predicate)
    if kind == 'A':
        return s <= p
    if kind == 'E':
        return not bool(s & p)
    if kind == 'I':
        return bool(s & p)
    return bool(s - p)


def classify(model, kind, subject, predicate):
    """Modern explicit classification; 'wholly false' only for nonempty universals."""
    truth = proposition(model, kind, subject, predicate)
    s = getattr(model, subject)
    if kind in ('I', 'O'):
        return 'true' if truth else 'false'
    if not s:
        return 'vacuous_true'
    if truth:
        return 'true'
    opposite = 'E' if kind == 'A' else 'A'
    return 'wholly_false' if proposition(model, opposite, subject, predicate) else 'partly_false'


def evaluate(model, mood):
    validate(model)
    if mood not in MOODS:
        raise ValueError('Unknown mood')
    return tuple(proposition(model, *p) for p in MOODS[mood])


def signature(model, mood):
    return ''.join('T' if x else 'F' for x in evaluate(model, mood))


def type_models(nonempty_bc=False):
    """Each present unary membership type has one representative (0..7)."""
    if type(nonempty_bc) is not bool:
        raise TypeError('nonempty_bc must be bool')
    for mask in range(1, 256):
        u = frozenset(t for t in range(8) if mask & (1 << t))
        m = Model(u, frozenset(t for t in u if t & 4),
                  frozenset(t for t in u if t & 2),
                  frozenset(t for t in u if t & 1))
        if not nonempty_bc or (m.B and m.C):
            yield m


def make(A, B, C, universe=None):
    sets = [frozenset(x) for x in (A, B, C)]
    u = frozenset(universe) if universe is not None else frozenset().union(*sets)
    return Model(u, *sets)


def examples():
    return {
        'both_wholly_false_Barbara': (make({0}, {1}, {0}), 'Barbara'),
        'both_wholly_false_Celarent': (make({1}, {1}, {0}), 'Celarent'),
        'minor_wholly_false_Barbara': (make({0, 1}, {0}, {1}), 'Barbara'),
        'major_partly_false_Barbara': (make({0}, {0, 1}, {0}), 'Barbara'),
        'major_partly_false_Celarent': (make({1}, {0, 1}, {0}), 'Celarent'),
        'minor_partly_false_Barbara': (make({0, 1}, {0}, {0, 1}), 'Barbara'),
        'Darii_distinct_witnesses': (make({0}, {1}, {0, 1}), 'Darii'),
        'Ferio_distinct_witnesses': (make({1}, {1}, {0, 1}), 'Ferio'),
        'Darii_false_minor': (make({0, 1}, {0}, {1}), 'Darii'),
        'Ferio_false_minor': (make({2}, {0}, {1}), 'Ferio'),
        'empty_C_Barbara_exception': (make({0}, {1}, set()), 'Barbara'),
        'empty_C_Celarent_exception': (make({0}, {0}, set()), 'Celarent'),
    }
