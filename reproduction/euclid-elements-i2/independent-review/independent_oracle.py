"""Independent exact Euclid I.2 review oracle; requires existing SymPy.

Run: python3 independent_oracle.py PATH_TO_REPRODUCTION_DIRECTORY

Only uses the reviewed module's public constructor/certificate, Q3 as a data
adapter, and Q3 operations when they themselves are the object of a test.
Oracle geometry uses SymPy's algebraic number field, not reviewed helpers.
Ray order uses an exact affine coordinate > 1, not the reviewed dot product.
These finite checks are not a universal proof or a primitive-action verifier.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import importlib
import json
import sys
import time
import sympy as S

SOURCE = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent).resolve()
sys.path.insert(0, str(SOURCE))
subject = importlib.import_module('euclid_i2')
K = S.QQ.algebraic_field(S.sqrt(3))
ZERO, ONE = K.zero, K.one
ROOT3 = K.new([S.QQ.one, S.QQ.zero])
COUNTS = Counter()
FAILURES = []
START = time.monotonic()


def check(condition, label):
    if not condition:
        FAILURES.append(label)


def rational(q):
    q = F(q)
    return K.new([S.QQ(q.numerator, q.denominator)])


def from_subject_number(q):
    return K.new([S.QQ(q.b.numerator, q.b.denominator),
                  S.QQ(q.a.numerator, q.a.denominator)])


def to_subject_number(q):
    coefficients = [S.QQ.zero] * (2-len(q.to_list())) + q.to_list()
    b, a = coefficients
    return subject.Q3(F(int(a.numerator), int(a.denominator)),
                      F(int(b.numerator), int(b.denominator)))


def from_subject(points):
    return {key: tuple(from_subject_number(x) for x in p) for key, p in points.items()}


def to_subject(points):
    return {key: tuple(to_subject_number(x) for x in p) for key, p in points.items()}


def plus(p, q):
    return (p[0]+q[0], p[1]+q[1])


def minus(p, q):
    return (p[0]-q[0], p[1]-q[1])


def times(q, p):
    return (q*p[0], q*p[1])


def norm2(p):
    return sum((coordinate**2 for coordinate in p), ZERO)


def d2(p, q):
    return norm2(minus(p, q))


def det(p, q):
    return p[0]*q[1] - p[1]*q[0]


@lru_cache(maxsize=None)
def positive(q):
    answer = K.to_sympy(q).is_positive
    if answer is None:
        raise RuntimeError('SymPy did not decide an algebraic sign')
    return bool(answer)


def after(origin, through, target):
    """Independent order oracle via a line parameter, not a dot product."""
    direction, displacement = minus(through, origin), minus(target, origin)
    if direction == (ZERO, ZERO) or det(direction, displacement) != ZERO:
        return False
    index = 0 if direction[0] != ZERO else 1
    parameter = displacement[index] / direction[index]
    return positive(parameter-ONE)


def oracle(p):
    a, b, c, d, g, l = (p[key] for key in ('A','B','C','D','G','L'))
    ab, bc = d2(a, b), d2(b, c)
    out = {
        'nonzero_input': positive(bc),
        'distinct_anchor': a != b,
        'equilateral_frame': ab == d2(d,a) == d2(d,b) and det(minus(a,d),minus(b,d)) != ZERO,
        'circle_B_through_C': d2(b,g) == bc,
        'D_B_G_order': after(d,b,g),
        'circle_D_through_G': d2(d,l) == d2(d,g),
        'D_A_L_order': after(d,a,l),
        'output_length': d2(a,l) == bc,
    }
    out['accepted'] = all(out.values())
    return out


def compare(points, label, expected, category):
    actual = subject.certificate(to_subject(points))
    reference = oracle(points)
    check(actual == reference, label+': certificate differs from independent oracle')
    check(reference['accepted'] is expected, label+': unexpected oracle acceptance')
    COUNTS[category] += 1
    return reference


VALUES = [F(1,97), F(1,3), F(1,2), F(1), F(2), F(3), F(97)]
OFFSETS = [(0,0), (F(13,17),F(-29,31)), (-11,23)]
for s,r,side,offset in product(VALUES,VALUES,(-1,1),OFFSETS):
    p = from_subject(subject.construct(s,r,side,offset))
    label = f'constructor s={s} r={r} side={side} offset={offset}'
    compare(p,label,True,'normalized_constructor_cases')
    check(d2(p['A'],p['L']) == rational(r*r), label+': target length is wrong')
    check(d2(p['D'],p['G']) == rational((s+r)**2), label+': total length is wrong')

# Construct certificate fixtures independently, beyond the constructor API:
# four exact rotations, both reflected equilateral frames, irrational translation,
# and four orientations of the originally given segment. The fourth direction
# passes through A; r=s gives A=C, while r>s puts A inside BC.
ROTATIONS = [(F(1),F(0)), (F(0),F(1)), (F(3,5),F(4,5)), (F(-5,13),F(12,13))]
O = (rational(2)+ROOT3, rational(F(1,3))-ROOT3)
representatives = []
for s,r,rotation,side in product(VALUES,VALUES,ROTATIONS,(-1,1)):
    ss,rr = rational(s),rational(r)
    u = tuple(rational(q) for q in rotation)
    perpendicular = (-u[1],u[0])
    v = plus(times(rational(F(1,2)),u),times(rational(side)*ROOT3/rational(2),perpendicular))
    a,b = plus(O,times(ss,u)),plus(O,times(ss,v))
    directions = [(ONE,ZERO),(ZERO,ONE),(rational(F(3,5)),rational(F(4,5))),minus(u,v)]
    for direction_index,w in enumerate(directions):
        p = dict(A=a,B=b,C=plus(b,times(rr,w)),D=O,
                 G=plus(O,times(ss+rr,v)),L=plus(O,times(ss+rr,u)))
        label = f'general certificate s={s} r={r} rotation={rotation} side={side} C-direction={direction_index}'
        compare(p,label,True,'broader_valid_certificate_cases')
        check(d2(a,p['L']) == rr**2, label+': independent target mismatch')
        if direction_index == 3:
            if r == s:
                check(p['C']==a,label+': intended A=C was not generated')
                COUNTS['A_equals_C_valid_cases'] += 1
            if r > s:
                check(after(b,a,p['C']),label+': intended internal A was not generated')
                COUNTS['A_strictly_inside_BC_valid_cases'] += 1
        # A balanced, explicit set of 3 radius relations x4 rotations x2 sides.
        if s == 1 and r in (F(1,3),F(1),F(3)) and direction_index == 3:
            representatives.append((p,u,v,ss,rr,label))

MUTATION_RESULTS = Counter()
for p,u,v,s,r,label in representatives:
    replacements = {
        'other_first_circle_intersection': {'G':plus(p['D'],times(s-r,v))},
        'opposite_second_circle_intersection': {'L':plus(p['D'],times(-(s+r),u))},
        'G_equals_B': {'G':p['B']},
        'L_equals_A': {'L':p['A']},
        'zero_given_segment': {'C':p['B']},
        'collapsed_AB': {'A':p['B']},
        'bad_equilateral_vertex': {'D':plus(p['D'],times(s,u))},
        'wrong_radius_on_right_ray': {'G':plus(p['D'],times(s+2*r,v))},
        'offray_G': {'G':plus(p['G'],times(r,(-v[1],v[0])))},
    }
    for name,replacement in replacements.items():
        q=dict(p);q.update(replacement)
        compare(q,label+' mutation='+name,False,'mutated_certificate_cases')
        MUTATION_RESULTS[name] += 1

# Test the arithmetic actually used by the subject against SymPy's field.
coefficients = [F(-7,3),F(-1),F(0),F(1,5),F(2)]
scalars = [subject.Q3(a,b) for a,b in product(coefficients,repeat=2)]
for x,y in product(scalars,repeat=2):
    sx,sy = from_subject_number(x),from_subject_number(y)
    for name,actual,expected in [('add',x+y,sx+sy),('subtract',x-y,sx-sy),('multiply',x*y,sx*sy)]:
        check(from_subject_number(actual)==expected,'arithmetic '+name)
        COUNTS['arithmetic_operation_comparisons'] += 1
for x in scalars:
    sx=from_subject_number(x)
    expected=1 if positive(sx) else (-1 if positive(-sx) else 0)
    check(x.sign()==expected,'arithmetic sign grid')
    COUNTS['sign_comparisons'] += 1
# Pell near-cancellation cases exercise sign without relying on float rounding.
x,y=1,0
for power in range(1,65):
    x,y=2*x+3*y,x+2*y
    for a,b in [(x,-y),(-x,y)]:
        z=subject.Q3(a,b);sz=from_subject_number(z)
        expected=1 if positive(sz) else -1
        check(z.sign()==expected,f'Pell sign power={power}')
        COUNTS['sign_comparisons'] += 1

# Degenerate direct branch stays separate: it is not a normal certificate.
for a,c in [((ONE,ZERO),(ZERO,ONE)),(O,plus(O,(ROOT3,ONE))),((ZERO,ZERO),(rational(3),rational(4)))]:
    returned=subject.coincident_anchor(tuple(map(to_subject_number,a)),tuple(map(to_subject_number,a)),tuple(map(to_subject_number,c)))
    check(tuple(map(from_subject_number,returned))==c,'direct A=B branch')
    COUNTS['coincident_anchor_cases'] += 1

# Reproduce the paper and attachment counterexamples separately.
COUNTEREXAMPLES={}
for s,r,name in [(2,1,'attachment_s2_r1'),(2,3,'paper_s2_r3')]:
    p=from_subject(subject.construct(s,r))
    q=dict(p);q['L']=(-rational(s+r),ZERO)
    c=oracle(q)
    check(c['circle_D_through_G'] and not c['D_A_L_order'] and not c['output_length'],name+' opposite L flags')
    COUNTEREXAMPLES[name+'_opposite_L']={'AL_squared':str(K.to_sympy(d2(q['A'],q['L']))),'BC_squared':str(r*r),'checks':c}
p=from_subject(subject.construct(2,1));q=dict(p);q['G']=times(rational(F(1,2)),p['B'])
c=oracle(q)
check(c['circle_B_through_C'] and not c['D_B_G_order'], 'near G first-circle and order flags')
COUNTEREXAMPLES['s2_r1_near_G']={'DG_squared':str(K.to_sympy(d2(q['D'],q['G']))),'DA_squared':'4','checks':c}

report={
 'review_kind':'independent exact finite differential oracle; not a universal proof',
 'python':sys.version.split()[0], 'sympy':S.__version__,
 'oracle_arithmetic':'SymPy QQ<sqrt(3)> algebraic field; no subject arithmetic in oracle geometry',
 'oracle_order':'exact affine line parameter > 1; no subject beyond, dot or sign helper',
 'tested_source_sha256':{name:hashlib.sha256((SOURCE/name).read_bytes()).hexdigest() for name in ['exact.py','euclid_i2.py','test_euclid_i2.py']},
 'parameters':{'positive_rational_values':[str(x) for x in VALUES],'radius_ratio_min':'1/9409','radius_ratio_max':'9409','constructor_offsets':[[str(x) for x in o] for o in OFFSETS],'exact_rotations':[[str(x) for x in r] for r in ROTATIONS],'broader_translation':['2+sqrt(3)','1/3-sqrt(3)'],'given_segment_directions':['(1,0)','(0,1)','(3/5,4/5)','from B toward A']},
 'counts':dict(COUNTS), 'mutation_cases_by_kind':dict(MUTATION_RESULTS),
 'counterexamples':COUNTEREXAMPLES,
 'failures':FAILURES,'elapsed_seconds':round(time.monotonic()-START,3),
 'scope_limits':['finite exact fixtures, not all real inputs','broader fixtures test certificate only; constructor still has its original limited API','no primitive-operation history or ancient-axiom existence verification','SymPy is a review dependency only; original reproduction remains standard-library-only'],
}
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(FAILURES))
