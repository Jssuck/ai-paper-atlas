"""Modern finite-world teaching semantics, not an edition of Aristotle's modal logic."""
from dataclasses import dataclass
from itertools import product

TERMS = ('P', 'S', 'M')
KINDS = ('A', 'E', 'I', 'O')

@dataclass(frozen=True)
class Model:
    n: int
    worlds: tuple

    def __post_init__(self):
        if type(self.n) is not int or self.n < 1:
            raise ValueError('domain size must be a positive integer')
        if type(self.worlds) is not tuple or not self.worlds:
            raise ValueError('worlds must be a nonempty tuple')
        for world in self.worlds:
            if type(world) is not tuple or len(world) != 3:
                raise ValueError('each world must be a tuple of three extension masks')
            if any(type(mask) is not int or not 0 <= mask < (1 << self.n) for mask in world):
                raise ValueError('extension mask outside domain')

    def validate_world(self, world):
        if type(world) is not int or not 0 <= world < len(self.worlds):
            raise ValueError('world index outside model')

    def extension(self, world, term):
        self.validate_world(world)
        if type(term) is not str or term not in TERMS:
            raise ValueError('unknown term')
        return self.worlds[world][TERMS.index(term)]


def validate_kind(kind):
    if type(kind) is not str or kind not in KINDS:
        raise ValueError('unknown proposition kind')


def categorical(model, world, kind, subject, predicate):
    validate_kind(kind)
    s, p = model.extension(world, subject), model.extension(world, predicate)
    return {'A': s & ~p == 0, 'E': s & p == 0,
            'I': s & p != 0, 'O': s & ~p != 0}[kind]


def necessary(model, kind, subject, predicate):
    validate_kind(kind)
    # Validate terms even before short-circuiting over worlds.
    model.extension(0, subject)
    model.extension(0, predicate)
    return all(categorical(model, w, kind, subject, predicate)
               for w in range(len(model.worlds)))


def rigid_witnesses(model, kind, subject, predicate):
    if kind not in ('I', 'O') or type(kind) is not str:
        raise ValueError('rigid witnesses are defined only for I and O')
    common = (1 << model.n) - 1
    for w in range(len(model.worlds)):
        s, p = model.extension(w, subject), model.extension(w, predicate)
        common &= s & (p if kind == 'I' else ~p)
    return tuple(i for i in range(model.n) if common & (1 << i))


def witnesses(model, world, kind, subject, predicate):
    if type(kind) is not str or kind not in ('I', 'O'):
        raise ValueError('witnesses are defined only for I and O')
    s, p = model.extension(world, subject), model.extension(world, predicate)
    mask = s & (p if kind == 'I' else ~p)
    return tuple(i for i in range(model.n) if mask & (1 << i))


# (name, figure, major kind, minor kind, conclusion kind, requires middle existence)
MOODS = (
    ('Barbara', 1, 'A', 'A', 'A', False),
    ('Celarent', 1, 'E', 'A', 'E', False),
    ('Darii', 1, 'A', 'I', 'I', False),
    ('Ferio', 1, 'E', 'I', 'O', False),
    ('Cesare', 2, 'E', 'A', 'E', False),
    ('Camestres', 2, 'A', 'E', 'E', False),
    ('Festino', 2, 'E', 'I', 'O', False),
    ('Baroco', 2, 'A', 'O', 'O', False),
    ('Darapti', 3, 'A', 'A', 'I', True),
    ('Disamis', 3, 'I', 'A', 'I', False),
    ('Datisi', 3, 'A', 'I', 'I', False),
    ('Felapton', 3, 'E', 'A', 'O', True),
    ('Bocardo', 3, 'O', 'A', 'O', False),
    ('Ferison', 3, 'E', 'I', 'O', False),
)


def mood_spec(name):
    if type(name) is not str:
        raise ValueError('unknown mood')
    for row in MOODS:
        if row[0] == name:
            return row
    raise ValueError('unknown mood')


def propositions(name):
    _, figure, major, minor, conclusion, _ = mood_spec(name)
    major_terms, minor_terms = {
        1: (('M', 'P'), ('S', 'M')),
        2: (('P', 'M'), ('S', 'M')),
        3: (('M', 'P'), ('M', 'S')),
    }[figure]
    return ((major, *major_terms), (minor, *minor_terms), (conclusion, 'S', 'P'))


def premises(model, name, require_middle=False):
    if type(require_middle) is not bool:
        raise ValueError('require_middle must be Boolean')
    major, minor, _ = propositions(name)
    # Validate both calls without allowing a false first premise to hide bad names.
    a, b = necessary(model, *major), necessary(model, *minor)
    existence = all(model.extension(w, 'M') != 0 for w in range(len(model.worlds)))
    return a and b and (existence or not require_middle)


def conclusion(model, name):
    return necessary(model, *propositions(name)[2])


def exposition(model, name):
    """Return a locally checked witness for each world; no cross-world identity claim."""
    if name not in ('Baroco', 'Bocardo') or type(name) is not str:
        raise ValueError('exposition supports only Baroco and Bocardo')
    if not premises(model, name):
        raise ValueError('necessary premises are not both true')
    premise = propositions(name)[1 if name == 'Baroco' else 0]
    chosen = []
    for w in range(len(model.worlds)):
        candidates = witnesses(model, w, *premise)
        if not candidates:
            raise RuntimeError('necessary particular has no local witness')
        i = candidates[0]
        s, p = model.extension(w, 'S'), model.extension(w, 'P')
        if not (s & (1 << i)) or p & (1 << i):
            raise RuntimeError('exposition does not establish conclusion')
        chosen.append(i)
    return tuple(chosen)


def two_world_models(n=2):
    if type(n) is not int or not 1 <= n <= 3:
        raise ValueError('enumeration bound is one to three individuals')
    for values in product(range(1 << n), repeat=6):
        yield Model(n, (values[:3], values[3:]))


def as_data(model):
    return {'domain_size': model.n, 'term_order': list(TERMS),
            'worlds': [list(w) for w in model.worlds]}


def run_report():
    rows = {row[0]: {'premise_models_free': 0, 'failures_free': 0,
                     'premise_models_middle_nonempty': 0,
                     'failures_middle_nonempty': 0, 'first_failure_free': None}
            for row in MOODS}
    witness_gap = {'I': 0, 'O': 0}
    rigid_implication_failures = 0
    exposition_world_checks = 0
    stable_exposition_checks = 0
    model_count = 0
    for model in two_world_models():
        model_count += 1
        for name, *_ in MOODS:
            row = rows[name]
            if premises(model, name):
                row['premise_models_free'] += 1
                if not conclusion(model, name):
                    row['failures_free'] += 1
                    if row['first_failure_free'] is None:
                        row['first_failure_free'] = as_data(model)
                if name in ('Baroco', 'Bocardo'):
                    exposition_world_checks += len(exposition(model, name))
                    particular = propositions(name)[1 if name == 'Baroco' else 0]
                    stable = rigid_witnesses(model, *particular)
                    if stable:
                        stable_exposition_checks += 1
                        if not set(stable) <= set(rigid_witnesses(model, 'O', 'S', 'P')):
                            raise RuntimeError('stable witness route failed')
            if premises(model, name, require_middle=True):
                row['premise_models_middle_nonempty'] += 1
                row['failures_middle_nonempty'] += not conclusion(model, name)
        for kind in ('I', 'O'):
            n = necessary(model, kind, 'S', 'P')
            r = bool(rigid_witnesses(model, kind, 'S', 'P'))
            witness_gap[kind] += n and not r
            rigid_implication_failures += r and not n
    # Ordered masks are P, S, M; members are 0 and 1.
    switched_i = Model(2, ((1, 3, 0), (2, 3, 0)))
    switched_o = Model(2, ((2, 3, 0), (1, 3, 0)))
    baroco = Model(2, ((0, 1, 2), (0, 2, 1)))
    bocardo = Model(2, ((2, 3, 1), (1, 3, 2)))
    mixed_major = Model(1, ((1, 1, 1), (0, 1, 0)))
    mixed_minor = Model(1, ((1, 1, 1), (0, 1, 1)))
    bad_o = Model(2, ((1, 3, 0), (1, 3, 0)))
    return {
        'semantics': 'Modern constant-domain, world-varying predicates; necessary means all listed worlds; no unique historical-semantics claim.',
        'models': model_count, 'individuals': 2, 'worlds': 2,
        'ordered_models_include_duplicate_worlds': True,
        'mood_results': rows, 'necessary_without_rigid_witness': witness_gap,
        'rigid_implies_necessary_failures': rigid_implication_failures,
        'exposition_world_checks': exposition_world_checks,
        'stable_exposition_model_checks': stable_exposition_checks,
        'examples': {
            'switching_I': as_data(switched_i), 'switching_O': as_data(switched_o),
            'Baroco': {'model': as_data(baroco), 'per_world_witnesses': list(exposition(baroco, 'Baroco'))},
            'Bocardo': {'model': as_data(bocardo), 'per_world_witnesses': list(exposition(bocardo, 'Bocardo'))},
            'necessary_major_current_minor_not_necessary_conclusion': as_data(mixed_major),
            'current_major_necessary_minor_not_necessary_conclusion': as_data(mixed_minor),
            'O_conversion_failure': as_data(bad_o),
        },
        'limits': ['Finite checks do not prove general validity.',
                   'Mixed-modal examples diagnose this modern semantics; they do not refute Aristotle I.9.',
                   'No contingent syllogism calculus or complete historical modal interpretation is implemented.'],
    }

if __name__ == '__main__':
    import json
    print(json.dumps(run_report(), ensure_ascii=False, indent=2))
