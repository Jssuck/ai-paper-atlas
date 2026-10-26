"""Finite teaching models for Posterior Analytics II.12, not causal discovery."""
from fractions import Fraction
from itertools import product
import json

NODES = ('stones', 'foundation', 'house')
EDGES = tuple((a, b) for a in NODES for b in NODES if a != b)
HOUSE_RULES = (('house', 'foundation'), ('foundation', 'stones'))

def closure(seed, rules):
    """Edge (a,b) means: presence of a requires presence of b, not a causes b."""
    known = set(seed)
    if not known <= set(NODES) or any(a not in NODES or b not in NODES for a,b in rules):
        raise ValueError('Unknown event name')
    while True:
        new = known | {b for a,b in rules if a in known}
        if new == known:
            return frozenset(known)
        known = new

def truth_oracle(seed, rules):
    """Intersect satisfying valuations; no use of the closure algorithm."""
    worlds = []
    for bits in product((False, True), repeat=len(NODES)):
        world = {x for x, bit in zip(NODES, bits) if bit}
        if set(seed) <= world and all(a not in world or b in world for a,b in rules):
            worlds.append(world)
    return frozenset.intersection(*(frozenset(w) for w in worlds))

def valid_trace(times, rules=HOUSE_RULES):
    """None means absent from this whole finite trace, not unknown in reality.
    If an event occurs, its required predecessor must occur strictly earlier.
    """
    if set(times) != set(NODES):
        raise ValueError('All three event names required')
    if any(t is not None and (type(t) is not int or t < 0) for t in times.values()):
        raise ValueError('Times must be nonnegative integers or None')
    if any(a not in NODES or b not in NODES for a,b in rules):
        raise ValueError('Unknown event name')
    return all(times[a] is None or (times[b] is not None and times[b] < times[a]) for a,b in rules)

def completed(times, now):
    return frozenset(x for x,t in times.items() if t is not None and t <= now)

def midpoint(a, b):
    a,b = Fraction(a),Fraction(b)
    if not a < b:
        raise ValueError('Require a < b')
    return (a+b)/2

def cycle_tokens(steps):
    if type(steps) is not int or steps < 0:
        raise ValueError('Nonnegative integer steps required')
    kinds = ('wet_ground','vapour','cloud','rain')
    return [(i,kinds[i%4]) for i in range(steps+1)]

def majority(sub, pred):
    """Modern finite strict-majority surrogate, not Aristotle's semantics."""
    return bool(sub) and 2*len(sub & pred) > len(sub)

def experiments():
    graph_instances = mismatch = 0
    for mask in range(1 << len(EDGES)):
        rules = tuple(edge for i,edge in enumerate(EDGES) if mask >> i & 1)
        for bits in product((False,True),repeat=3):
            seed = {x for x,bit in zip(NODES,bits) if bit}
            graph_instances += 1
            mismatch += closure(seed,rules) != truth_oracle(seed,rules)
    trace_count = valid_count = house_count = backward_errors = 0
    for values in product((None,0,1,2),repeat=3):
        times = dict(zip(NODES,values)); trace_count += 1
        if not valid_trace(times): continue
        valid_count += 1
        if times['house'] is not None: house_count += 1
        for now in range(3):
            done = completed(times,now)
            backward_errors += not closure(done,HOUSE_RULES) <= done
    triples = universal_premises = universal_errors = majority_premises = majority_errors = 0
    for n in range(4):
        subsets = [{i for i in range(n) if mask >> i & 1} for mask in range(1<<n)]
        for c,b,a in product(subsets,repeat=3):
            triples += 1
            if c <= b and b <= a:
                universal_premises += 1; universal_errors += not c <= a
            if majority(c,b) and majority(b,a):
                majority_premises += 1; majority_errors += not majority(c,a)
    pairs = [(Fraction(i,3),Fraction(j,3)) for i in range(-3,4) for j in range(i+1,4)]
    midpoint_errors = sum(not a < midpoint(a,b) < b for a,b in pairs)
    return {'graph_instances':graph_instances,'oracle_mismatches':mismatch,
            'traces':trace_count,'valid_traces':valid_count,'house_traces':house_count,
            'completed_backward_errors':backward_errors,'subset_triples':triples,
            'universal_premises':universal_premises,'universal_errors':universal_errors,
            'majority_premises':majority_premises,'majority_counterexamples':majority_errors,
            'midpoint_pairs':len(pairs),'midpoint_errors':midpoint_errors,
            'cycle_tokens':cycle_tokens(8)}

if __name__ == '__main__':
    print(json.dumps(experiments(),ensure_ascii=False,indent=2))
