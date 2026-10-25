"""Original finite teaching reconstruction of Posterior Analytics I.17.
Set extension does not certify scientific explanation or an appropriate middle.
"""
from collections import Counter
from itertools import product
import json


def all_of(subject, predicate):
    return subject <= predicate


def none_of(subject, predicate):
    return subject.isdisjoint(predicate)


def status(kind, subject, predicate):
    if kind not in ('all', 'none'):
        raise ValueError('unknown proposition kind')
    truth = all_of(subject, predicate) if kind == 'all' else none_of(subject, predicate)
    contrary = none_of(subject, predicate) if kind == 'all' else all_of(subject, predicate)
    return 'true' if truth else ('wholly_false' if contrary else 'partly_false')


def propositions(form, a, b, c):
    table = {
        'Barbara': (('all', c, a), ('all', b, c), ('all', b, a)),
        'Celarent': (('none', c, a), ('all', b, c), ('none', b, a)),
        'Cesare': (('none', a, c), ('all', b, c), ('none', b, a)),
        'Camestres': (('all', a, c), ('none', b, c), ('none', b, a)),
    }
    return table[form]


def profile(form, a, b, c):
    return tuple(status(*p) for p in propositions(form, a, b, c))


def subsets(n, nonempty=False):
    if not isinstance(n, int) or n < 0:
        raise ValueError('n must be a nonnegative integer')
    return [frozenset(i for i in range(n) if mask & (1 << i))
            for mask in range(int(nonempty), 1 << n)]


def scenarios(a, b, c):
    """Structural teaching conditions, not a classifier of scientific middles."""
    return {
        'negative_fixed_true_chain': b <= c <= a,
        'positive_fixed_true_chain': b <= c and none_of(c, a),
        'negative_under_disjoint_minor': b <= a and c <= a and none_of(b, c),
        'negative_disjoint_major': b <= a and none_of(c, a),
        'positive_under_major': none_of(b, a) and c <= a,
        'positive_not_under_major': none_of(b, a) and not c <= a,
    }

SCENARIO_FORMS = {
    'negative_fixed_true_chain': 'Celarent',
    'positive_fixed_true_chain': 'Barbara',
    'negative_under_disjoint_minor': 'Celarent',
    'negative_disjoint_major': 'Celarent',
    'positive_under_major': 'Barbara',
    'positive_not_under_major': 'Barbara',
}


def enumerate_models(n=3):
    values = subsets(n)
    nonempty = subsets(n, True)
    validity = {}
    for form in ('Barbara', 'Celarent', 'Cesare', 'Camestres'):
        bad = 0
        for a, b, c in product(values, repeat=3):
            major, minor, conclusion = profile(form, a, b, c)
            if major == minor == 'true' and conclusion != 'true':
                bad += 1
        validity[form] = {'interpretations': len(values) ** 3, 'counterexamples': bad}
    groups = {name: {'count': 0, 'profiles': Counter(), 'witnesses': {}}
              for name in list(SCENARIO_FORMS) + ['second_figure_Cesare', 'second_figure_Camestres']}
    for a, b, c in product(nonempty, repeat=3):
        selected = [(name, SCENARIO_FORMS[name]) for name, yes in scenarios(a, b, c).items() if yes]
        if b <= a:
            selected += [('second_figure_' + form, form) for form in ('Cesare', 'Camestres')]
        for name, form in selected:
            p = profile(form, a, b, c)
            if p[2] == 'true':
                raise RuntimeError('a scenario did not give the required false conclusion')
            key = '/'.join(p[:2])
            g = groups[name]
            g['count'] += 1
            g['profiles'][key] += 1
            g['witnesses'].setdefault(key, {'A': sorted(a), 'B': sorted(b), 'C': sorted(c), 'form': form})
    for g in groups.values():
        g['profiles'] = dict(sorted(g['profiles'].items()))
    return {'universe': list(range(n)), 'nonempty_triples': len(nonempty) ** 3,
            'validity': validity, 'structural_scenarios': groups,
            'scope': 'Finite extensional teaching model; not scientific-middle certification or a general proof.'}


if __name__ == '__main__':
    print(json.dumps(enumerate_models(), ensure_ascii=False, indent=2, sort_keys=True))
