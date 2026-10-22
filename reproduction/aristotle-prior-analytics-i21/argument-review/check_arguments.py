"""Independent set-based argument check. Does not import author's model."""
from itertools import product
import json, sys, platform

def require(condition, label):
    if not condition:
        raise RuntimeError(label)

def predicates(n, worlds):
    U = set(range(n))
    sets = tuple(tuple({x for x in U if mask & (1 << x)} for mask in row) for row in worlds)
    a, b, c = sets[0]
    changing = {x for x in U if any(x in row[0] for row in sets) and any(x not in row[0] for row in sets)}
    ever_not = {x for x in U if any(x not in row[0] for row in sets)}
    always = {x for x in U if all(x in row[0] for row in sets)}
    return a, b, c, changing, ever_not, always

rules = {k: 0 for k in ('universal_nonempty_transfer','universal_particular_transfer','particular_universal_transfer','weak_negative_transfer','necessary_restriction','strong_implies_weak','weak_necessary_duality')}
count = 0
comparisons = 0
for n, nw in ((1,1),(1,2),(1,3),(2,1),(2,2),(2,3)):
    for masks in product(range(1 << n), repeat=3*nw):
        worlds = tuple(tuple(masks[3*w:3*w+3]) for w in range(nw))
        a,b,c,v,neg,always = predicates(n, worlds)
        cases = (
            ('universal_nonempty_transfer', bool(c) and c <= v and c <= b, bool(b & v)),
            ('universal_particular_transfer', c <= v and bool(b & c), bool(b & v)),
            ('particular_universal_transfer', bool(c & v) and c <= b, bool(b & v)),
            ('weak_negative_transfer', bool(c & neg) and c <= b, bool(b & neg)),
            ('necessary_restriction', b <= always and c <= b, c <= always),
            ('strong_implies_weak', bool(b & v), bool(b & neg)),
            ('weak_necessary_duality', True, (not bool(b & neg)) == (b <= always)),
        )
        for name, premise, conclusion in cases:
            comparisons += 1
            if premise:
                rules[name] += 1
                require(conclusion, name + repr(worlds))
        count += 1

def variable(n, worlds, term):
    return {x for x in range(n) if any(row[term] & (1 << x) for row in worlds) and any(not row[term] & (1 << x) for row in worlds)}

# These exact prose configurations are intentionally independent of author examples.
prose = {}
a,b,c,v,neg,always = predicates(2, ((3,3,1),(2,3,1)))
require(c <= v and c <= b and bool(b & v) and bool(b & neg) and not bool(b-a), 'section6')
prose['section6_possible_not_actual_negative'] = True
_,_,c,v,_,_ = predicates(2, ((3,3,1),))
require(not v and not c <= v, 'section6_drop_counterfactual')
prose['section6_delete_alternative'] = True
a,b,c,v,neg,always = predicates(2, ((1,2,1),(1,1,1)))
v_b = variable(2, ((1,2,1),(1,1,1)), 1)
require(c <= a and c <= v_b and not b & a and not b & v, 'section7.1')
require(not b & variable(2, ((1,2,1),(1,1,1)), 2), 'section7.1_C_stable_no_conversion')
prose['section7_1_affirmative_failure'] = True
a,b,c,v,neg,always = predicates(2, ((2,2,1),(3,1,1)))
require(not a & c and c <= variable(2, ((2,2,1),(3,1,1)), 1) and not b & neg, 'section7.2')
prose['section7_2_background_failure'] = True
a,b,c,v,neg,always = predicates(2, ((2,1,1),(2,1,1)))
require(bool(b & neg) and not b & v and not b <= always, 'section7.3')
prose['section7_3_weak_not_strong_instantiation'] = True
a,b,c,v,neg,always = predicates(2, ((1,2,3),(1,1,3)))
require(bool(a & c) and bool(c & variable(2, ((1,2,3),(1,1,3)), 1)) and not bool(b & a) and not bool(b & v), 'section8')
prose['section8_different_witnesses'] = True
# Structural boundary models: missing nonemptiness, Box/N, and negative coincidence.
boundaries = {}
a,b,c,v,neg,always = predicates(1, ((1,1,0),))
require(c <= v and c <= b and not bool(b & v), 'empty_middle')
boundaries['nonempty_assumption_required'] = True
_,b,_,_,_,always = predicates(1, ((1,1,1),(0,0,1)))
require(not b <= always and all(B & ~A == 0 for A,B,C in ((1,1,1),(0,0,1))), 'N_Box')
boundaries['Box_not_N'] = True
print(json.dumps({'python':platform.python_version(),'optimization':sys.flags.optimize,'configurations':count,'implication_checks':comparisons,'rule_premise_counts':rules,'prose_configurations':prose,'boundary_configurations':boundaries,'status':'passed','scope':'Finite verification, not a general proof or unique ancient semantics.'}, ensure_ascii=False, indent=2))
