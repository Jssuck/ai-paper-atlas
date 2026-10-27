"""Independent I.10 audit. Run beside copied author sources, no network.

Independent rational midpoint/intersection oracles do not call the author's
generator or arithmetic when computing their expected values. This remains a
finite implementation audit, not a proof of Euclid's general proposition.
"""
import ast
import contextlib
import hashlib
import io
import json
import math
import random
import sys
from dataclasses import replace
from fractions import Fraction as R
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent
sys.path.insert(0, str(SOURCE))
from geometry import (Q3, point, construct, accepted, check_certificate, sub,
                      intersect_open_ray_segment, equal_angles, inside)

counts = {}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def expect_value_error(call, label):
    try:
        call()
    except ValueError:
        return
    raise RuntimeError('expected ValueError: ' + label)


def p(native):
    return point(*native)


def native_add(x, y):
    return tuple(a+b for a, b in zip(x, y))


def native_scale(k, x):
    return tuple(k*a for a in x)


rng = random.Random(1010)
def rational():
    return R(rng.randrange(-30, 31), rng.randrange(1, 18))


# Expected midpoint coordinates use Fraction only, never geometry.scale/add.
for _ in range(256):
    a, b = (rational(), rational()), (rational(), rational())
    if a == b:
        raise RuntimeError('unexpected duplicate seeded input')
    expected = tuple((x+y)/2 for x, y in zip(a, b))
    certificates = []
    for branch in (1, -1):
        cert = construct(p(a), p(b), branch)
        require(accepted(p(a), p(b), cert), 'valid rational certificate rejected')
        require(cert.d == p(expected), 'independent midpoint oracle mismatch')
        require(cert.s == Q3(R(1,2)) and cert.t == Q3(R(1,2)), 'parameter mismatch')
        require(sub(cert.f, cert.c) == tuple(x+y for x,y in zip(sub(p(a),cert.c), sub(p(b),cert.c))),
                'F-C is not u+v')
        certificates.append(cert)
    require(certificates[0].c == certificates[1].f, 'branch-swap mismatch')
counts['new_rational_certificates'] = 512

# General ray intersections: t intentionally varies instead of being fixed 1/2.
for i in range(1, 121):
    a = (rational(), rational())
    edge = (R(i, 17), R(i+3, 23))
    b = native_add(a, edge)
    direction = (-edge[1] + R(2)*edge[0], edge[0] + R(2)*edge[1])
    t, s = R((i % 11)+1, 13), R(i+1, 7)
    target = native_add(a, native_scale(t, edge))
    origin = native_add(target, native_scale(-s, direction))
    actual, actual_s, actual_t = intersect_open_ray_segment(p(origin), p(direction), p(a), p(b))
    require(actual == p(target) and actual_s == Q3(s) and actual_t == Q3(t),
            'independent non-midpoint intersection mismatch')
counts['general_non_midpoint_intersections'] = 120

# Independent exact sign oracle uses rational bounds on sqrt(3), derived by
# integer square root. It neither reproduces Q3.sign's branching nor uses floats.
den = 10**250
lower_numerator = math.isqrt(3*den*den)
lower, upper = R(lower_numerator, den), R(lower_numerator+1, den)
sign_inputs = [(R(a,7), R(b,11)) for a in range(-20,21) for b in range(-20,21)]
a,b = 2,1
for _ in range(100):
    sign_inputs.extend([(R(a), R(-b)), (R(-a), R(b))])
    a,b = 2*a+3*b, a+2*b
for a,b in sign_inputs:
    lo, hi = sorted((a+b*lower, a+b*upper))
    expected = 0 if a == b == 0 else 1 if lo > 0 else -1 if hi < 0 else None
    require(expected is not None, 'sign oracle interval is inconclusive')
    require(Q3(a,b).sign() == expected, 'exact sign disagreement')
counts['independent_interval_sign_cases'] = len(sign_inputs)

# Field multiplication and division via explicit Fraction coefficient oracles.
for _ in range(200):
    a,b,c,d = (rational() for _ in range(4))
    x,y = Q3(a,b),Q3(c,d)
    expected_product = Q3(a*c+3*b*d, a*d+b*c)
    require(x*y == expected_product, 'product mismatch')
    if c != 0 or d != 0:
        n = c*c-3*d*d
        expected_division = Q3((a*c-3*b*d)/n, (b*c-a*d)/n)
        require(x/y == expected_division, 'division mismatch')
counts['independent_field_pairs'] = 200

A,B = point(0,0),point(6,0)
cert = construct(A,B)
negatives = {
    'off_line_equidistant_3_4': replace(cert,d=point(3,4)),
    'reverse_branch_label_only': replace(cert,branch=-1),
    'wrong_C_with_correct_D': replace(cert,c=point(2,5)),
    'same_side_F_equals_C': replace(cert,f=cert.c),
    'wrong_F': replace(cert,f=point(4,-5)),
    'wrong_D': replace(cert,d=point(R(5,2),0)),
    'negative_s': replace(cert,s=-cert.s),
    'wrong_t': replace(cert,t=Q3(R(2,3))),
    'endpoint_A': replace(cert,d=A,t=Q3(0)),
    'endpoint_B': replace(cert,d=B,t=Q3(1)),
    'outside_segment': replace(cert,d=point(9,0),t=Q3(R(3,2))),
    'bool_branch': replace(cert,branch=True),
    'float_parameter': replace(cert,s=0.5),
    'missing_certificate': None,
    'mapping_not_certificate': {},
}
failures = {}
for label,bad in negatives.items():
    facts = check_certificate(A,B,bad)
    require(not all(facts.values()), 'negative accepted: '+label)
    failures[label] = [name for name,value in facts.items() if not value]
require(check_certificate(A,B,negatives['off_line_equidistant_3_4'])['conclusion_AD_equals_DB'],
        'off-line counterexample lost equal-distance premise')
require(not accepted(A,point(12,0),cert), 'certificate accepted for wrong trusted input')
counts['new_negative_certificates'] = len(negatives)+1

# Supplementary angles have equal squared cosines but are not equal angles.
require(not equal_angles(point(1,0), point(-1,0), point(1,1)), 'supplementary angles accepted')
require(equal_angles(point(-3,-1),point(3,-1),point(0,1)), 'reverse ray should be equiangular')
require(not inside(point(-3,-1),point(3,-1),point(0,1)), 'reverse ray classified internal')
require(not equal_angles(point(1,0),point(0,1),point(0,0)), 'zero direction accepted')
counts['angle_sign_direction_checks'] = 4

for label, origin, direction in [
    ('parallel_external',point(3,2),point(-6,0)),
    ('opposite_ray',point(3,2),point(0,1)),
    ('zero_direction',point(3,2),point(0,0)),
    ('endpoint',point(0,2),point(0,-1)),
    ('outside',point(7,2),point(0,-1)),
    ('at_origin',point(3,0),point(0,-1)),
]:
    expect_value_error(lambda: intersect_open_ray_segment(origin,direction,A,B),label)
expect_value_error(lambda: construct(A,A), 'coincident input')
expect_value_error(lambda: construct(point(Q3(0,1),0),B), 'irrational coordinate')
counts['explicit_rejection_paths'] = 8

assert_locations = []
for source in sorted(SOURCE.glob('*.py')):
    for node in ast.walk(ast.parse(source.read_text())):
        if isinstance(node,ast.Assert):
            assert_locations.append(f'{source.name}:{node.lineno}')
notebook = json.loads((SOURCE/'teaching.zh-CN.ipynb').read_text())
code_cells = [c for c in notebook['cells'] if c['cell_type']=='code']
for i,cell in enumerate(code_cells):
    if any(isinstance(node,ast.Assert) for node in ast.walk(ast.parse(''.join(cell['source'])))):
        assert_locations.append(f'notebook-code-cell-{i}')
require(not assert_locations, 'optimization-removable assertion gates')
require(len(code_cells)==6, 'Notebook cell count mismatch')
require([c['execution_count'] for c in code_cells] == list(range(1,7)), 'Notebook execution counts mismatch')
require(not notebook['metadata']['execution_provenance']['jupyter_kernel_used'], 'false kernel claim')
require(all(c['outputs'] for c in code_cells), 'missing executed outputs')
counts['notebook_code_cells_inspected'] = len(code_cells)

print(json.dumps({'status':'passed','counts':counts,'negative_failed_predicates':failures,
                  'optimization':sys.flags.optimize,'bare_assert_locations':assert_locations,
                  'scope':'independent finite audit; not formal proof or Jupyter kernel execution'},
                 ensure_ascii=False,indent=2))
