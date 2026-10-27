"""Original exact rational teaching model for Elements I.21, not a formalization."""
from fractions import Fraction as Q
from math import isqrt
import json

def rational(x):
    if type(x) not in (int, Q): raise ValueError('exact int/Fraction required')
    return Q(x)
def point(x,y): return (rational(x),rational(y))
def checked(p):
    if type(p) not in (tuple,list) or len(p)!=2: raise ValueError('point required')
    return point(*p)
def add(u,v):return (u[0]+v[0],u[1]+v[1])
def sub(u,v):return (u[0]-v[0],u[1]-v[1])
def mul(t,u):return (t*u[0],t*u[1])
def dot(u,v):return u[0]*v[0]+u[1]*v[1]
def cross(u,v):return u[0]*v[1]-u[1]*v[0]
def norm2(u):return dot(u,u)
def distance2(p,q):return norm2(sub(p,q))
def sign(x):return (x>0)-(x<0)
def angle_compare(u,v,w,z):
    """-1/0/1 for angle(u,v) vs angle(w,z), ordinary angles [0,pi]."""
    p,q=norm2(u)*norm2(v),norm2(w)*norm2(z)
    if p<=0 or q<=0:raise ValueError('zero ray')
    a,b=dot(u,v),dot(w,z)
    if sign(a)!=sign(b):return -sign(sign(a)-sign(b))
    if a==b==0:return 0
    return -sign(a)*sign(a*a*q-b*b*p)
def radical_difference_equal(p,q,t):
    if t<0:return radical_difference_equal(q,p,-t)
    if t==0:return p==q
    r=p-q-t*t
    return p>q and r>=0 and r*r==4*t*t*q

def sqrt_bounds(x,bits):
    scale=1<<bits
    k=isqrt((x.numerator*scale*scale)//x.denominator)
    lo=Q(k,scale)
    return lo,lo if lo*lo==x else Q(k+1,scale)
def sum_compare(a,b,c,d):
    """Exact comparison sqrt(a)+sqrt(b) vs sqrt(c)+sqrt(d).
    Equality is decided algebraically; unequal sums use certified rational bounds.
    Arbitrary precision doubles until disjoint; no floating point/tolerance.
    """
    a,b,c,d=map(rational,(a,b,c,d))
    if min(a,b,c,d)<0:raise ValueError('negative radicand')
    if radical_difference_equal(a*b,c*d,(c+d-a-b)/2):return 0
    bits=8
    while True:
        bounds=[sqrt_bounds(x,bits) for x in (a,b,c,d)]
        llo,lhi=bounds[0][0]+bounds[1][0],bounds[0][1]+bounds[1][1]
        rlo,rhi=bounds[2][0]+bounds[3][0],bounds[2][1]+bounds[3][1]
        if lhi<rlo:return -1
        if rhi<llo:return 1
        bits*=2

def enc(x):
    if isinstance(x,Q):return [x.numerator,x.denominator]
    if isinstance(x,tuple):return [enc(t) for t in x]
    return x

def construct(A,B,C,D):
    A,B,C,D=map(checked,(A,B,C,D))
    area=cross(sub(B,A),sub(C,A))
    if area==0:raise ValueError('nondegenerate triangle required')
    beta=cross(sub(D,A),sub(C,A))/area
    gamma=cross(sub(B,A),sub(D,A))/area
    alpha=1-beta-gamma
    if min(alpha,beta,gamma)<=0:raise ValueError('D must be strictly interior')
    # D=alpha A+beta B+gamma C, E=(alpha A+gamma C)/(alpha+gamma).
    E=mul(1/(alpha+gamma),add(mul(alpha,A),mul(gamma,C)))
    t=1/(alpha+gamma)
    sq={name:distance2(p,q) for name,p,q in [('AB',A,B),('AC',A,C),('BD',B,D),('CD',C,D),('AE',A,E),('EC',E,C),('BE',B,E),('DE',D,E)]}
    checks={
      'strict_interior':min(alpha,beta,gamma)>0,
      'A_E_C_order':0<gamma/(alpha+gamma)<1,
      'B_D_E_order':t>1 and E==add(B,mul(t,sub(D,B))),
      'AC_decomposition':sum_compare(sq['AE'],sq['EC'],sq['AC'],Q(0))==0,
      'BE_decomposition':sum_compare(sq['BD'],sq['DE'],sq['BE'],Q(0))==0,
      'I20_AB_AE_gt_BE':sum_compare(sq['AB'],sq['AE'],sq['BE'],Q(0))==1,
      'I20_EC_DE_gt_CD':sum_compare(sq['EC'],sq['DE'],sq['CD'],Q(0))==1,
      'outer_gt_bridge':sum_compare(sq['AB'],sq['AC'],sq['BE'],sq['EC'])==1,
      'bridge_gt_inner':sum_compare(sq['BE'],sq['EC'],sq['BD'],sq['CD'])==1,
      'outer_gt_inner':sum_compare(sq['AB'],sq['AC'],sq['BD'],sq['CD'])==1,
      'I16_BDC_gt_CED':angle_compare(sub(B,D),sub(C,D),sub(C,E),sub(D,E))==1,
      'CED_equals_CEB':angle_compare(sub(C,E),sub(D,E),sub(C,E),sub(B,E))==0,
      'I16_CEB_gt_BAC':angle_compare(sub(C,E),sub(B,E),sub(B,A),sub(C,A))==1,
      'BDC_gt_BAC':angle_compare(sub(B,D),sub(C,D),sub(B,A),sub(C,A))==1}
    if not all(checks.values()):raise ArithmeticError('certificate invariant failed')
    return {'schema':'euclid-i21-teaching-v1','input':[enc(p) for p in (A,B,C,D)],'E':enc(E),'barycentric':[enc(v) for v in (alpha,beta,gamma)],'extension_factor':enc(t),'squared_lengths':{k:enc(v) for k,v in sq.items()},'checks':checks}

def strict_json(x):
    if x is None or type(x) in (str,int,bool):return
    if type(x) is list:
        for y in x:strict_json(y)
        return
    if type(x) is dict and all(type(k) is str for k in x):
        for y in x.values():strict_json(y)
        return
    raise ValueError('canonical JSON types only; no floats or tuples')
def accepted(A,B,C,D,certificate):
    try:
        strict_json(certificate)
        expected=construct(A,B,C,D)
        return json.dumps(expected,sort_keys=True,separators=(',',':'))==json.dumps(certificate,sort_keys=True,separators=(',',':'))
    except (ValueError,TypeError,ArithmeticError,KeyError):return False
