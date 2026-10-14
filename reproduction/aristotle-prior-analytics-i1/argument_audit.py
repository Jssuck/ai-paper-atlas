"""Independent checks of the article's mathematical claims.

Written by the argument auditor. Imports no author production/test module.
The general infinite-domain theorem still requires the proof in the article.
"""
from itertools import combinations, product
import json


def subsets(xs, include_empty=False):
    xs = tuple(xs)
    for size in range(0 if include_empty else 1, len(xs) + 1):
        yield from combinations(xs, size)


def models(k):
    types = tuple(product((False, True), repeat=k))
    for support in subsets(types):
        # Use the type tuple itself as an object, as in the theorem.
        yield tuple(frozenset(x for x in support if x[i]) for i in range(k))


def val(kind, s, p):
    return {'A': s <= p, 'E': s.isdisjoint(p),
            'I': bool(s & p), 'O': bool(s - p)}[kind]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def consequence(k, premises, conclusion, required=()):
    admissible = satisfying = failures = 0
    smallest = None
    for support in subsets(tuple(product((False, True), repeat=k))):
        exts = tuple(frozenset(x for x in support if x[i]) for i in range(k))
        if not all(exts[i] for i in required):
            continue
        admissible += 1
        if all(val(t, exts[s], exts[p]) for t, s, p in premises):
            satisfying += 1
            if not val(conclusion[0], exts[conclusion[1]], exts[conclusion[2]]):
                failures += 1
                if smallest is None:
                    smallest = len(support)
    return {'admissible_supports': admissible, 'premise_satisfying_supports': satisfying,
            'counterexample_supports': failures, 'holds': failures == 0,
            'minimum_counterexample_objects': smallest}


def main():
    counts = {}
    rule_checks = 0
    complement_checks = 0
    for k in (1, 2, 3):
        counts[str(k)] = {}
        all_models = list(models(k))
        require(len(all_models) == 2**(2**k) - 1, 'support count')
        for req in subsets(range(k), include_empty=True):
            counts[str(k)][','.join(map(str, req)) or 'none'] = sum(
                all(m[i] for i in req) for m in all_models)
        for exts in all_models:
            for s, p in product(exts, repeat=2):
                require(val('A', s, p) == (not val('O', s, p)), 'A/O complement')
                require(val('E', s, p) == (not val('I', s, p)), 'E/I complement')
                require(val('E', s, p) == val('E', p, s), 'E symmetry')
                complement_checks += 2
                rule_checks += 1
            for s, m, p in product(exts, repeat=3):
                forms = (
                    (val('A', s, m) and val('A', m, p), val('A', s, p)),
                    (val('A', s, m) and val('E', m, p), val('E', s, p)),
                    (val('I', s, m) and val('A', m, p), val('I', s, p)),
                    (val('O', s, p) and val('A', s, m), val('O', m, p)),
                    (val('O', s, m) and val('A', p, m), val('O', s, p)),
                    (val('I', s, m) and val('E', m, p), val('O', s, p)),
                )
                for antecedent, consequent in forms:
                    require(not antecedent or consequent, 'inference form')
                    rule_checks += 1
    examples = {}
    def example(name, actual, expected):
        require(actual == expected, name)
        examples[name] = actual
    example('same_singleton_I_A_O', [val(t, {1}, {1}) for t in 'IAO'], [True, True, False])
    example('disjoint_singletons_O_I', [val(t, {1}, {2}) for t in 'OI'], [True, False])
    example('empty_S_AEIO', [val(t, set(), {1}) for t in 'AEIO'], [True, True, False, False])
    example('A_direction', [val('A', {1}, {1,2}), val('A', {1,2}, {1})], [True, False])
    example('main_false_start', [val('A', {1}, {2}), val('A', {2}, {2}), val('A', {1}, {2})], [False, True, False])
    example('hidden_assumption', [val('A', {1}, {1}), val('A', {1}, {2}), val('A', {1}, {2})], [True, False, False])
    example('O_direction_and_E_distinction', [val('O', {1,2}, {1}), val('O', {1}, {1,2}), val('E', {1,2}, {1})], [True, False, False])
    cases = {
        'A_transitivity': (3, [('A',0,1),('A',1,2)], ('A',0,2), ()),
        'E_conversion_then_down': (3, [('A',0,1),('E',2,1)], ('E',0,2), ()),
        'A_converse': (2, [('A',0,1)], ('A',1,0), ()),
        'O_converse': (2, [('O',0,1)], ('O',1,0), ()),
        'missing_bridge': (3, [('A',0,1)], ('A',0,2), ()),
        'A_not_I': (2, [('A',0,1)], ('I',0,1), ()),
        'A_with_nonempty_S_gives_I': (2, [('A',0,1)], ('I',0,1), (0,)),
        'report_converging_A_invalid': (3, [('A',0,1),('A',2,1)], ('A',0,2), ()),
        'I_up': (3, [('I',0,1),('A',1,2)], ('I',0,2), ()),
        'O_from_I_E': (3, [('I',0,1),('E',1,2)], ('O',0,2), ()),
        'main_A_O_inconsistent': (2, [('A',0,1),('O',0,1)], ('I',0,1), ()),
        'report_E_I_inconsistent': (2, [('E',0,0),('I',0,0)], ('A',0,1), ()),
    }
    results = {name: consequence(*args) for name,args in cases.items()}
    expected = {
        'A_transitivity': (255,15,0,True,None),
        'E_conversion_then_down': (255,15,0,True,None),
        'A_converse': (15,7,4,False,1),
        'O_converse': (15,8,4,False,1),
        'missing_bridge': (255,63,32,False,1),
        'A_not_I': (15,7,3,False,1),
        'A_with_nonempty_S_gives_I': (12,4,0,True,None),
        'report_converging_A_invalid': (255,31,16,False,1),
        'I_up': (255,32,0,True,None),
        'O_from_I_E': (255,32,0,True,None),
        'main_A_O_inconsistent': (15,0,0,True,None),
        'report_E_I_inconsistent': (15,0,0,True,None),
    }
    keys = ('admissible_supports','premise_satisfying_supports',
            'counterexample_supports','holds','minimum_counterexample_objects')
    for name, target in expected.items():
        require(tuple(results[name][key] for key in keys) == target, name)
    require(counts['2']['0,1'] == 10 and counts['3']['0,1,2'] == 218, 'all nonempty counts')
    require(results['A_transitivity']['premise_satisfying_supports'] == 15, 'A chain count')
    require(results['E_conversion_then_down']['premise_satisfying_supports'] == 15, 'E chain count')
    require(results['A_with_nonempty_S_gives_I']['premise_satisfying_supports'] == 4, 'nonempty count')
    require(results['report_converging_A_invalid']['premise_satisfying_supports'] == 31, 'invalid convergence count')
    require(results['I_up']['premise_satisfying_supports'] == 32, 'I up count')
    require(results['O_from_I_E']['premise_satisfying_supports'] == 32, 'O from I/E count')
    result = {'passed': True, 'independence': 'No import from author modules or author test suite',
              'support_policy_counts': counts, 'implication_checks_including_repeated_terms': rule_checks,
              'complement_checks': complement_checks, 'explicit_main_examples': examples,
              'consequence_cases': results}
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
