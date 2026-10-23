"""Real finite checks; counts are not a proof over arbitrary domains."""
import json
from model import Statement as S, models, examples


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run():
    counts = dict(models=0, A_conversion_cases=0, E_conversion_cases=0,
                  I_conversion_cases=0, A_restriction_cases=0,
                  E_restriction_cases=0, O_nonconversion_countermodels=0,
                  particular_subclass_countermodels=0, A_empty_countermodels=0)
    first = {}
    for n in range(4):
        for m in models(n, ('S', 'P', 'D')):
            counts['models'] += 1
            h = lambda mood, x, y: m.holds(S(mood, x, y))
            if h('A', 'S', 'P') and m.extension('S'):
                counts['A_conversion_cases'] += 1
                require(h('I', 'P', 'S'), 'A conversion failed')
            if h('E', 'S', 'P'):
                counts['E_conversion_cases'] += 1
                require(h('E', 'P', 'S'), 'E conversion failed')
            if h('I', 'S', 'P'):
                counts['I_conversion_cases'] += 1
                require(h('I', 'P', 'S'), 'I conversion failed')
            if h('A', 'D', 'S') and h('A', 'S', 'P'):
                counts['A_restriction_cases'] += 1
                require(h('A', 'D', 'P'), 'A restriction failed')
            if h('A', 'D', 'S') and h('E', 'S', 'P'):
                counts['E_restriction_cases'] += 1
                require(h('E', 'D', 'P'), 'E restriction failed')
            conditions = {
                'O_nonconversion_countermodels': h('O', 'S', 'P') and not h('O', 'P', 'S'),
                'particular_subclass_countermodels': h('I', 'S', 'P') and h('A', 'D', 'S') and bool(m.extension('D')) and not h('I', 'D', 'P'),
                'A_empty_countermodels': h('A', 'S', 'P') and not h('I', 'P', 'S')}
            for key, condition in conditions.items():
                if condition:
                    counts[key] += 1
                    first.setdefault(key, {'n': n, 'terms': {k: sorted(v) for k, v in m.terms.items()}})
    deps = {key: sorted(proof.dependencies()) for key, proof in examples().items()}
    require(len(deps['second_original']) == 2, 'original dependency missing')
    require('p2:C subset A' not in deps['second_submiddle'], 'irrelevant original premise was added')
    require('d2:some C is B' not in deps['particular_submiddle'], 'irrelevant witness was added')
    return {'scope': 'all three named subsets of n=0,1,2,3',
            'counts': counts, 'first_countermodels': first, 'dependencies': deps,
            'failures': 0}


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2))
