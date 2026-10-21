"""Independent finite semantic audit. Standard library; no bare assertions."""
import hashlib
import itertools as it
import json
from fractions import Fraction as F
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import boole_model as m

COUNTS = {}

def check(condition, label):
    COUNTS[label] = COUNTS.get(label, 0) + 1
    if not condition:
        raise RuntimeError('audit failed: ' + label)

def subsets(n):
    return [frozenset(i for i in range(n) if mask & (1 << i)) for mask in range(1 << n)]

def assignments(n):
    return list(it.product((0, 1), repeat=n))

def direct_solutions(table, fixed, size):
    result = set()
    for z in subsets(size):
        valid = True
        for i in range(size):
            key = tuple(int(i in c) for c in fixed) + (int(i in z),)
            if table[key] != 0:
                valid = False
                break
        if valid:
            result.add(z)
    return frozenset(result)

# Four-variable constituent partition and independent exact expansion values.
for point in assignments(4):
    for atom in assignments(4):
        check(m.constituent(atom, point) == int(atom == point), 'constituent_bits')

# All 625 rational-valued binary tables in this explicitly chosen alphabet.
values = (F(-2, 3), F(-1), F(0), F(1, 5), F(2))
for entries in it.product(values, repeat=4):
    table = dict(zip(assignments(2), entries))
    for p in assignments(2):
        check(m.expansion_at(table, p) == table[p], 'rational_expansion')
    for x in subsets(2):
        expected = direct_solutions(table, (x,), 2)
        check(m.solve_last_class(table, range(2), (x,)) == expected, 'rational_all_solutions')

# Every Boolean-valued ternary residual table; values 0 and 1 encode all forbidden masks.
for entries in it.product((0, 1), repeat=8):
    table = dict(zip(assignments(3), entries))
    for x, y in it.product(subsets(2), repeat=2):
        check(m.solve_last_class(table, range(2), (x, y)) == direct_solutions(table, (x, y), 2),
              'ternary_all_solutions')

# Independent direct set semantics on four objects, including free subregions.
u = frozenset(range(4)); ss = subsets(4)
ship_table = {a: a[0]*a[1] - a[1]*a[2] - a[0]*(1-a[2]) for a in assignments(3)}
for x, y in it.product(ss, repeat=2):
    expected = frozenset(z for z in ss if (x & y) == ((y & z) | (x-z)))
    check(m.solve_last_class(ship_table, u, (x,y)) == expected, 'ship_four_object_solutions')
    # One common free selector already expresses every choice on both disjoint free zones.
    generated = frozenset(m.ship_parametrization(u,x,y,w,w) for w in ss)
    check(generated == expected, 'ship_free_subregions')
    for z in ss:
        check(m.equation_holds(ship_table,u,(x,y,z)) == ((x&y)==((y&z)|(x-z))), 'ship_equation_holds')
for v, y in it.product(ss, repeat=2):
    expected = frozenset(u-x for x in ss if y == (v&x))
    if y <= v:
        generated = frozenset(m.complement_parametrization(u,v,y,w) for w in ss)
        check(generated == expected, 'fixed_selector_solutions')
    else:
        try:
            m.complement_parametrization(u,v,y,frozenset())
        except ValueError:
            check(not expected, 'incompatible_selector_rejected')
        else:
            raise RuntimeError('missing fixed selector constraint')

# Three-object existential projection, a distinct larger domain than author test.
u3 = frozenset(range(3)); s3 = subsets(3)
for v, vp, x, z in it.product(s3, repeat=4):
    projection = any(x == (v&y) and z == (vp&(u3-y)) for y in s3)
    retained = x <= v and z <= vp and all(
        int(i in v)*int(i in z) == int(i in vp)*(int(i in v)-int(i in x)) for i in u3)
    check(projection == retained, 'projection_three_objects')

# Some requires a nonempty common selected class; do not import author equality predicate.
for x,y in it.product(s3,repeat=2):
    candidates = [v&y for v,vp in it.product(s3,repeat=2) if (v&y)==(vp&x)]
    check(bool(candidates), 'bare_particular_always_satisfiable')
    check(any(candidates) == bool(x&y), 'particular_nonempty_equivalence')

# Mutation probes: verify that chosen independent fixtures detect three wrong implementations.
def detects(change, probe):
    old = getattr(m, change[0])
    try:
        setattr(m, change[0], change[1])
        return not probe()
    finally:
        setattr(m, change[0], old)
mutants = {
    'free_endpoint_collapsed': detects(('endpoint_choices',lambda a,b: (0,) if a==0 else ((1,) if b==0 else ())),
        lambda: m.solve_last_class({(0,):0,(1,):0},{0,1},())==frozenset(subsets(2))),
    'forbidden_zero_inverted': detects(('forbidden_constituents',lambda t: frozenset(k for k,v in t.items() if v==0)),
        lambda: m.equation_holds({(0,):0,(1,):1},{0},(frozenset(),))),
    'atom_indicator_reversed': detects(('constituent',lambda a,p:int(a!=p)),
        lambda: m.expansion_at({(0,):0,(1,):1},(1,))==1),
}
check(all(mutants.values()), 'mutants_detected')

# Preserve and verify frozen author evidence; do not overwrite its logs.
manifest = json.loads((ROOT/'logs/run-manifest.json').read_text())
for rel, digest in manifest['source_sha256'].items():
    check(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest, 'author_source_hash')
for run in manifest['runs']:
    for command in run['commands']:
        check(command['exit_code']==0, 'author_exit_code')
        check(hashlib.sha256((ROOT/command['log']).read_bytes()).hexdigest()==command['sha256'], 'author_log_hash')
check(len({(ROOT/f'logs/{mode}-demo.json').read_bytes() for mode in ('normal','optimized','double_optimized')})==1,
      'author_demo_bytes_identical')
print(json.dumps({'status':'passed','counts':COUNTS,'mutants_detected':mutants,
                  'scope':'finite explicit input families; not a proof of all historical logic'},indent=2,sort_keys=True))
