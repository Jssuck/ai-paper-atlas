"""Independent coordinate and algebra oracles; standard library only.

Run from the reproduction directory:
  python evidence/independent-review/review_oracles.py
The implementation is imported for comparison only; oracle geometry does not
reuse the implementation's sine length, C-coordinate or chord formulas.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import json
import math
import random
from decimal import Decimal, localcontext
import xml.etree.ElementTree as ET
from sylvester import (Triangle, divider_geometry, bisector_squares, circle_chord,
    near_segment, remote_segment, opposite_sign_example, DegenerateIntersection,
    tangent_ratios, DomainError, sine_residual, cross_residual, exact_opposite_sign_example)
from polynomial_certificate import certificate


def sub(p,q): return p[0]-q[0],p[1]-q[1]
def cross(p,q): return p[0]*q[1]-p[1]*q[0]
def dot(p,q): return p[0]*q[0]+p[1]*q[1]
def unit(p):
    norm=math.hypot(*p)
    return p[0]/norm,p[1]/norm

def intersect(p,u,q,v):
    """Solve p+t*u=q+s*v via 2x2 determinants, no angle-sum ratios."""
    delta=sub(q,p); det=cross(u,v)
    if abs(det)<1e-10: raise ValueError('independent oracle: near parallel')
    t=cross(delta,v)/det; s=cross(delta,u)/det
    return (p[0]+t*u[0],p[1]+t*u[1]),t,s

def close(actual,wanted):
    assert math.isclose(actual,wanted,rel_tol=2e-9,abs_tol=2e-9),(actual,wanted)

# Construct C by intersecting two rays, and each divider by intersecting a ray
# with a coordinate-defined opposite line. This is independent of t_A/t_B.
rng=random.Random(1852)
geo_cases=0; stable_excluded=0; max_scaled_error=0.0
for _ in range(1200):
    A=rng.uniform(3,170); B=rng.uniform(3,177-A)
    base=10**rng.uniform(-1,1); n=rng.choice([-3.,-2.,-1.,-.5,.25,.5,1.,2.,3.,8.])
    ar,br=map(math.radians,(A,B)); P=(0.,0.); Q=(base,0.)
    C,_,_=intersect(P,(math.cos(ar),math.sin(ar)),Q,(-math.cos(br),math.sin(br)))
    u=(math.cos(ar/n),math.sin(ar/n)); v=(-math.cos(br/n),math.sin(br/n))
    try:
        D,tA,sA=intersect(P,u,Q,sub(C,Q)); E,tB,sB=intersect(Q,v,P,C)
    except ValueError:
        stable_excluded+=1; continue
    g=divider_geometry(Triangle(A,B,base),n)
    for a,b in list(zip(g.triangle.C,C))+list(zip(g.D,D))+list(zip(g.E,E))+[(g.t_A,tA),(g.t_B,tB),(g.bc_fraction,sA),(g.ac_fraction,sB)]:
        close(a,b); max_scaled_error=max(max_scaled_error,abs(a-b)/max(1.,abs(b)))
    close(math.dist(P,D),g.ordinary_lengths[0]); close(math.dist(Q,E),g.ordinary_lengths[1])
    assert g.both_forward_rays == (dot(sub(D,P),u)>0 and dot(sub(E,Q),v)>0)
    internal=(0<ar/n<ar and 0<br/n<br and 0<sA<1 and 0<sB<1 and tA>0 and tB>0)
    # n=1 is an exact endpoint; do not infer strict segment membership from roundoff.
    if n!=1: assert g.both_internal_cevians==internal
    geo_cases+=1

# Independent coordinate bisectors: directions sum two unit side vectors.
bisector_cases=0
for _ in range(500):
    P=(0.,0.); Q=(rng.uniform(.5,5),0.); C=(rng.uniform(-2,7),rng.uniform(.2,5))
    a,b,c=math.dist(Q,C),math.dist(P,C),math.dist(P,Q)
    uu=unit(sub(Q,P)); vv=unit(sub(C,P)); direction=(uu[0]+vv[0],uu[1]+vv[1])
    D,_,_=intersect(P,direction,Q,sub(C,Q))
    uu=unit(sub(P,Q)); vv=unit(sub(C,Q)); direction=(uu[0]+vv[0],uu[1]+vv[1])
    E,_,_=intersect(Q,direction,P,sub(C,P))
    implementation=bisector_squares(a,b,c)
    close(implementation[0],math.dist(P,D)**2); close(implementation[1],math.dist(Q,E)**2)
    bisector_cases+=1

# Polynomial coefficients encoded in one variable: a=z, b=z^7, c=z^49.
# Total degree is 6, so every individual exponent is <=6; base-7 exponent
# encoding is injective here. Dense list arithmetic is separate from the core's
# dictionary of multivariate exponents. No numerical substitutions are used.
def polyadd(x,y,sign=1):
    out=[0]*max(len(x),len(y))
    for i,a in enumerate(x):out[i]+=a
    for i,b in enumerate(y):out[i]+=sign*b
    return out

def polymul(x,y):
    out=[0]*(len(x)+len(y)-1)
    for i,a in enumerate(x):
        for j,b in enumerate(y):out[i+j]+=a*b
    return out

def product(*xs):
    out=[1]
    for x in xs:out=polymul(out,x)
    return out

def mono(k):return [0]*k+[1]
a,b,c=mono(1),mono(7),mono(49)
aa,bb=product(a,a),product(b,b)
ac2=product(polyadd(a,c),polyadd(a,c)); bc2=product(polyadd(b,c),polyadd(b,c))
left=polyadd(product(b,c,polyadd(bc2,aa,-1),ac2),product(a,c,polyadd(ac2,bb,-1),bc2),-1)
P=polyadd(polyadd(product(a,a,b),product(a,b,b)),[3*q for q in product(a,b,c)])
for term in [product(a,c,c),product(b,c,c),product(c,c,c)]:P=polyadd(P,term)
right=product(polyadd(b,a,-1),c,polyadd(polyadd(a,b),c),P)
residual=polyadd(left,right,-1)
assert not any(residual)
assert certificate()['identity_verified']
nonzero=sum(v!=0 for v in left)

# Circle oracle: intersect general line P+t*d with y=1/2 and independently solve
# its line-circle quadratic (including the already-known t=0 root).
chord_cases=0
for angle in range(-59,60):
    th=math.radians(angle); P=(0.,1.); d=(math.sin(th),-math.cos(th))
    S,t,_=intersect(P,d,(-2.,.5),(4.,0.))
    quadraticA=dot(d,d); quadraticB=2*dot(P,d)
    far_t=-quadraticB/quadraticA
    Q=(P[0]+far_t*d[0],P[1]+far_t*d[1])
    U=(-math.sqrt(.75),.5); b=math.dist(P,U)
    x,remote=math.dist(P,S),math.dist(S,Q)
    assert 0<t<far_t
    g=circle_chord(angle)
    for k,expected in [('S',S),('Q',Q)]:
        for actual,want in zip(g[k],expected):close(actual,want)
    close(g['near'],x);close(g['remote'],remote);close(g['half_chord'],b)
    close(near_segment(remote,b),x);close(remote_segment(x,b),remote)
    chord_cases+=1
    assert .5-1e-15 <= g['near'] < 1
# A valid algebraic positive root need not belong to this FIXED circle/base.
assert 0 < near_segment(3,1) < .5

# Decimal independently evaluates the quadratic root with 90-digit precision.
root_cases=0
with localcontext() as ctx:
    ctx.prec=90
    for ra,rb in [('1','1'),('2','3'),('0.1','5'),('1e12','1')]:
        a,b=Decimal(ra),Decimal(rb)
        expected=(-a+(a*a+4*b*b).sqrt())/2
        close(near_segment(float(a),float(b)),float(expected));root_cases+=1

# Cases that prevent conflating signed roots with ordinary lengths.
g=opposite_sign_example()
assert abs(g.t_A+g.t_B)<1e-12 and g.t_A*g.t_B<0
assert abs(sine_residual(g.triangle,g.n))>1
assert not g.both_forward_rays
opposite_B=g.triangle.B_deg
exact=exact_opposite_sign_example()
assert exact.triangle.A_deg==96 and exact.triangle.B_deg==24
close(exact.t_A,-1);close(exact.t_B,1)
assert not exact.both_forward_rays
special=[]
for A,B,n in [(30,60,.5),(15,105,-.5)]:
    g=divider_geometry(Triangle(A,B),n)
    assert g.both_forward_rays and not g.both_internal_cevians
    close(g.t_A,1);close(g.t_B,1)
    ratios=tangent_ratios(g.triangle,n)
    for r in ratios:close(r,-1)
    special.append({'A':A,'B':B,'n':n,'ratios':ratios})
t=Triangle(50,50)
close(cross_residual(t,-1),0)
try:divider_geometry(t,-1)
except DegenerateIntersection:pass
else:raise AssertionError('zero residual accepted a degenerate intersection')
try:tangent_ratios(t,2)
except DomainError:pass
else:raise AssertionError('isosceles tangent 0/0 accepted')

# Original SVGs: parseable, no scripts, no embedded scans or external resources.
svg_checks=[]
root=Path(__file__).resolve().parents[2]
for name in ['divider-domains.svg','equal-chords.svg']:
    path=root/'output'/name; doc=ET.parse(path); tags=[]
    for el in doc.iter():
        tag=el.tag.split('}')[-1];tags.append(tag)
        assert tag not in ('script','image','foreignObject')
        for key,value in el.attrib.items():
            assert not key.lower().startswith('on')
            if key.endswith('href'):assert not value or value.startswith('#')
    assert 'title' in tags and 'desc' in tags
    svg_checks.append({'file':'output/'+name,'xml_parsed':True,'embedded_or_external_images':False})

print(json.dumps({'status':'PASS','seed':1852,
 'coordinate_divider_cases':geo_cases,'oracle_near_parallel_excluded':stable_excluded,
 'max_scaled_coordinate_error':max_scaled_error,'coordinate_bisector_cases':bisector_cases,
 'polynomial_certificate':{'method':'dense univariate coefficients with injective base-7 exponent encoding; total degree 6','left_nonzero_terms':nonzero,'residual_nonzero_terms':sum(v!=0 for v in residual)},
 'circle_intersection_cases':chord_cases,'decimal_root_cases':root_cases,
 'special_case_corrected_ratios':special,'signed_opposite_branch_B_degrees':opposite_B,
 'exact_opposite_branch':{'A':exact.triangle.A_deg,'B':exact.triangle.B_deg,'t_A':exact.t_A,'t_B':exact.t_B},
 'svg_checks':svg_checks,
 'scope':'Finite geometry checks plus an exact polynomial identity; no proof of a universal proof-method criterion.'},indent=2))
