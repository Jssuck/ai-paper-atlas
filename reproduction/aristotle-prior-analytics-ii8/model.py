"""Original teaching reconstruction for Prior Analytics II.8; Python stdlib only.

Each inhabited unary A/B/C type is represented once. Types are 0..7,
with bit 0=A, bit 1=B, bit 2=C. This is a finite diagnostic, not by itself
an infinite-model proof or a complete interpretation of Aristotle.
"""
from dataclasses import dataclass
import json

KINDS = ('U', 'E', 'I', 'O')
TERMS = ('A', 'B', 'C')
NEGATION = {'U': 'O', 'O': 'U', 'E': 'I', 'I': 'E'}
CONTRARY = {'U': 'E', 'E': 'U', 'I': 'O', 'O': 'I'}


def validate_statement(statement):
    if not isinstance(statement, tuple) or len(statement) != 3:
        raise ValueError('statement must be a (kind, predicate, subject) tuple')
    if statement[0] not in KINDS or any(t not in TERMS for t in statement[1:]):
        raise ValueError('unknown kind or term')
    return statement


def validate_model(model):
    if not isinstance(model, frozenset) or not model:
        raise ValueError('model must be a nonempty frozenset of inhabited type IDs')
    if any(type(x) is not int or x < 0 or x > 7 for x in model):
        raise ValueError('type IDs must be integers 0..7 (not booleans)')
    return model


def extension(model, term):
    validate_model(model)
    if term not in TERMS:
        raise ValueError('unknown term')
    bit = 1 << TERMS.index(term)
    return frozenset(t for t in model if t & bit)


def holds(model, statement):
    validate_model(model)
    kind, pred, subj = validate_statement(statement)
    p, s = extension(model, pred), extension(model, subj)
    return {'U': s <= p, 'E': not (s & p), 'I': bool(s & p), 'O': bool(s - p)}[kind]


def conjunction(model, statements):
    # Materialize and validate ALL statements before short-circuit evaluation.
    statements = tuple(statements)
    validate_model(model)
    for statement in statements:
        validate_statement(statement)
    return all(holds(model, statement) for statement in statements)


def opposite(statement, mode):
    kind, pred, subj = validate_statement(statement)
    if mode not in ('contradictory', 'contrary'):
        raise ValueError('unknown opposition mode')
    return ((NEGATION if mode == 'contradictory' else CONTRARY)[kind], pred, subj)


def models(policy='empty_terms_allowed'):
    if policy not in ('empty_terms_allowed', 'C_nonempty', 'all_terms_nonempty'):
        raise ValueError('unknown existence policy')
    for mask in range(1, 256):
        model = frozenset(t for t in range(8) if mask & (1 << t))
        if policy == 'C_nonempty' and not extension(model, 'C'):
            continue
        if policy == 'all_terms_nonempty' and not all(extension(model, t) for t in TERMS):
            continue
        yield model


@dataclass(frozen=True)
class Mood:
    name: str
    major: tuple
    minor: tuple
    conclusion: tuple


MOODS = (
    Mood('Barbara', ('U','A','B'), ('U','B','C'), ('U','A','C')),
    Mood('Celarent', ('E','A','B'), ('U','B','C'), ('E','A','C')),
    Mood('Darii', ('U','A','B'), ('I','B','C'), ('I','A','C')),
    Mood('Ferio', ('E','A','B'), ('I','B','C'), ('O','A','C')),
)
# Two entries in each pair: keep major, keep minor. None means no stated
# categorical consequence about the dropped premise's ordered term pair.
RESULTS = {
    ('Barbara','contradictory'): (('O','B','C'), ('O','A','B')),
    ('Barbara','contrary'): (('E','B','C'), ('O','A','B')),
    ('Celarent','contradictory'): (('O','B','C'), ('I','A','B')),
    ('Celarent','contrary'): (('E','B','C'), ('I','A','B')),
    ('Darii','contradictory'): (('E','B','C'), ('O','A','B')),
    ('Darii','contrary'): (('O','B','C'), None),
    ('Ferio','contradictory'): (('E','B','C'), ('I','A','B')),
    ('Ferio','contrary'): (('O','B','C'), None),
}


def witness(model):
    return {'inhabited_types': sorted(model), **{t: sorted(extension(model,t)) for t in TERMS}}


def analyse(mood, mode, keep, policy):
    if mood not in MOODS or keep not in ('major','minor'):
        raise ValueError('unknown mood or retained premise')
    replacement = opposite(mood.conclusion, mode)
    retained = getattr(mood, keep)
    dropped = mood.minor if keep == 'major' else mood.major
    stated = RESULTS[mood.name, mode][0 if keep == 'major' else 1]
    assumptions = (replacement, retained)
    eligible = [m for m in models(policy) if conjunction(m, assumptions)]
    # Nonvacuity is reported separately; all our rows have satisfying models.
    target = opposite(dropped, 'contradictory')
    bad = [m for m in eligible if not holds(m, target)]
    result_bad = None if stated is None else [m for m in eligible if not holds(m, stated)]
    categorical = [(k, dropped[1], dropped[2]) for k in KINDS]
    entailed = [s for s in categorical if all(holds(m,s) for m in eligible)]
    return {
        'mood': mood.name, 'mode': mode, 'keep': keep, 'policy': policy,
        'assumptions': assumptions, 'dropped_premise': dropped,
        'refutation_target': target, 'stated_result': stated,
        'satisfying_models': len(eligible), 'entailed_ordered_pair_results': entailed,
        'stated_result_counterexamples': None if result_bad is None else len(result_bad),
        'refutation_counterexamples': len(bad),
        'first_refutation_countermodel': witness(bad[0]) if bad else None,
        'first_stated_result_countermodel': witness(result_bad[0]) if result_bad else None,
    }


def report():
    policies = ('empty_terms_allowed','C_nonempty','all_terms_nonempty')
    return {'scope': 'II.8 modern unary set diagnostic; no original PDFs or translation',
            'model_counts': {p: sum(1 for _ in models(p)) for p in policies},
            'rows': [analyse(m,mode,keep,p) for p in policies for m in MOODS
                     for mode in ('contradictory','contrary') for keep in ('major','minor')]}


if __name__ == '__main__':
    print(json.dumps(report(), ensure_ascii=False, indent=2, sort_keys=True))
