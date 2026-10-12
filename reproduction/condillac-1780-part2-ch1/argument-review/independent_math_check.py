"""Independent finite checks; not a proof or a psychological experiment."""
from itertools import combinations, product
import argparse
import hashlib
from pathlib import Path
import importlib.util
import json
import random
import sys
sys.dont_write_bytecode = True

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--model', type=Path, default=Path(__file__).resolve().parents[1] / 'model.py')
args = parser.parse_args()
TARGET = args.model.resolve()
spec = importlib.util.spec_from_file_location('audited_model', TARGET)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

def check(condition):
    if not condition:
        raise AssertionError("Independent mathematical check failed")


def subsets(v):
    v = tuple(sorted(v))
    return [frozenset(c) for n in range(len(v)+1) for c in combinations(v,n)]

def independent_fixed_sets(v, rules, a, w):
    u = v-w
    fixed = []
    for s in subsets(u):
        supported = {x for x in a if x not in w}
        for body, head in rules:
            if all(x in s for x in body) and head not in w:
                supported.add(head)
        if s == supported:
            fixed.append(s)
    check(fixed)
    least = frozenset.intersection(*fixed)
    greatest = frozenset.union(*fixed)
    check(least in fixed and greatest in fixed)
    return least, greatest

contexts=0

def check_system(v, rules):
    global contexts
    obj=m.HornSystem(v, tuple(m.Rule(b,h) for b,h in rules))
    cache={}
    for a,w in product(subsets(v), repeat=2):
        expected=independent_fixed_sets(v,rules,a,w)
        actual=tuple(obj.fixed_point(kind,a,w) for kind in ('least','greatest'))
        check(tuple(x.result for x in actual)==expected)
        check(all(x.changes<=len(v-w) for x in actual))
        check(all(x.result<=v-w for x in actual))
        check(all(x.states[i] < x.states[i+1] for x in actual[:1] for i in range(x.changes)))
        check(all(x.states[i] > x.states[i+1] for x in actual[1:] for i in range(x.changes)))
        cache[a,w]=expected
        contexts+=1
    for (a,w),points in cache.items():
        for x in v:
            more_a=cache[a|{x},w]
            more_w=cache[a,w|{x}]
            check(all(s<=t for s,t in zip(points,more_a)))
            check(all(s>=t for s,t in zip(points,more_w)))

# Every positive nonempty-body rule system on 0, 1, and 2 labels.
exhaustive_systems=0
for n in range(3):
    v=frozenset('abc'[:n])
    possible=[(b,h) for b in subsets(v) if b for h in sorted(v)]
    for bits in product((False,True),repeat=len(possible)):
        check_system(v,[r for bit,r in zip(bits,possible) if bit])
        exhaustive_systems+=1

# All unary-rule systems on 3 labels, all anchor/exclusion sets.
v=frozenset('abc')
possible=[(frozenset({b}),h) for b in sorted(v) for h in sorted(v)]
for bits in product((False,True), repeat=len(possible)):
    check_system(v,[r for bit,r in zip(bits,possible) if bit])

# Seeded higher-arity sample, 4 labels, all anchor/exclusion sets.
rng=random.Random(1780)
v=frozenset('abcd')
possible=[(b,h) for b in subsets(v) if b for h in sorted(v)]
for _ in range(40):
    check_system(v, rng.sample(possible, rng.randrange(0,15)))

# Every initial set and every sequence of three compatibility sets on 3 labels.
h=frozenset('abc')
evidence_cases=0
for initial,e1,e2,e3 in product(subsets(h),repeat=4):
    trace=m.filter_evidence(h,[e1,e2,e3],initial)
    check(trace==(initial,initial&e1,initial&e1&e2,initial&e1&e2&e3))
    check(trace[-1]==m.filter_evidence(h,[e3,e2,e1],initial)[-1])
    for truth in h:
        check((truth in trace[-1]) == (truth in initial and all(truth in e for e in [e1,e2,e3])))
        check((trace[-1]=={truth}) == (truth in initial and all(truth in e for e in [e1,e2,e3]) and all(other not in initial or any(other not in e for e in [e1,e2,e3]) for other in h-{truth})))
    evidence_cases+=1
check(m.filter_evidence([],[])==(frozenset(),))
print(json.dumps({'status':'PASS','optimization':sys.flags.optimize,'model_sha256':hashlib.sha256(TARGET.read_bytes()).hexdigest(),'exhaustive_rule_systems_n_le_2':exhaustive_systems,'exhaustive_unary_systems_n_3':512,'seeded_hyperrule_systems_n_4':40,'total_horn_contexts':contexts,'three_observation_evidence_cases':evidence_cases,'seed':1780,'scope':'finite implementation checks only; general proofs must be read independently'},indent=2))
