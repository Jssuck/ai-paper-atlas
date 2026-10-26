"""Exhaustive finite checks with a separately expressed truth-assignment oracle."""
import json
from itertools import product, combinations
from pathlib import Path
from model import conjunction_report, minimal_supports, independent_support, opposite_transfer


def subsets(xs):
    xs = list(xs)
    return [frozenset(xs[i] for i in range(len(xs)) if mask >> i & 1)
            for mask in range(1 << len(xs))]


def truth_entails(facts, rules, atom, universe):
    # Enumerate classical valuations, independently of forward chaining.
    for world in subsets(universe):
        if not facts <= world:
            continue
        if all(not set(ps) <= world or c in world for ps, c in rules):
            if atom not in world:
                return False
    return True


def run():
    sets = {'models':0,'both_predicated':0,'coextensive':0,'violations':0,'oracle_mismatches':0,
            'coextensive_with_two_unity_labels':0}
    for n in range(4):
        u = range(n)
        for h,p,q in product(subsets(u), repeat=3):
            r = conjunction_report(h,p,q)
            sets['models'] += 1
            sets['both_predicated'] += r['both_predicated']
            sets['coextensive'] += r['coextensive']
            sets['violations'] += r['both_predicated'] and not r['intersection_contains_subject']
            oracle = all(x in p and x in q for x in h)
            sets['oracle_mismatches'] += oracle != r['intersection_contains_subject']
            if r['coextensive']:
                for label in (False,True):
                    labeled = conjunction_report(h,p,q,label)
                    if labeled['unity_certified_by_sets']:
                        raise RuntimeError('set operations certified essence')
                    sets['coextensive_with_two_unity_labels'] += 1
    atoms = ('a','b','c')
    possible = [(frozenset([x]),y) for x in atoms for y in atoms if x != y]
    horn = {'systems':0,'atom_checks':0,'closure_mismatches':0,'support_mismatches':0}
    for indices in subsets(range(len(possible))):
        rules = [possible[i] for i in sorted(indices)]
        for facts in subsets(atoms):
            actual = minimal_supports(facts,rules)
            horn['systems'] += 1
            for a in atoms:
                horn['atom_checks'] += 1
                entailed = truth_entails(facts,rules,a,atoms)
                horn['closure_mismatches'] += bool(actual.get(a,set())) != entailed
                candidates = [s for s in subsets(sorted(facts)) if truth_entails(s,rules,a,atoms)]
                expected = {s for s in candidates if not any(t < s for t in candidates)}
                horn['support_mismatches'] += actual.get(a,set()) != expected
    transfer = {'valuations':0,'rule_satisfying':0,'all_four_premises':0,'violations_under_rule':0,
                'unbridged_counterexamples':0}
    for d,c,f,b,q in product((False,True), repeat=5):
        antecedent = opposite_transfer(d,c,f,b)
        satisfies = not antecedent or q
        transfer['valuations'] += 1
        transfer['rule_satisfying'] += satisfies
        transfer['all_four_premises'] += satisfies and antecedent
        transfer['violations_under_rule'] += satisfies and antecedent and not q
        transfer['unbridged_counterexamples'] += satisfies and d and c and f and not b and not q
    s = minimal_supports({'alias','observation'}, [(['alias'],'target'),(['observation'],'target')])
    examples = {'two_supports': sorted([sorted(x) for x in s['target']]),
                'has_support_avoiding_target_alias': independent_support(s,'target',{'target','alias'}),
                'unseeded_cycle': sorted(minimal_supports([], [(['a'],'b'),(['b'],'a')]).get('a',set()))}
    results = {'sets':sets,'horn':horn,'transfer':transfer,'examples':examples}
    if any((sets['violations'],sets['oracle_mismatches'],horn['closure_mismatches'],horn['support_mismatches'],transfer['violations_under_rule'])):
        raise RuntimeError('a verification mismatch occurred')
    return results

if __name__ == '__main__':
    result = json.dumps(run(),ensure_ascii=False,indent=2)
    Path('logs').mkdir(exist_ok=True)
    Path('logs/results.json').write_text(result+'\n',encoding='utf-8')
    print(result)
