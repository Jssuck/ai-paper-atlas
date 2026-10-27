"""Exact modern I.19 teaching model, not a formalization of ancient geometry."""
from fractions import Fraction as Q
import json

def rational(x):
    if type(x) is int: return Q(x)
    if type(x) is str:
        try: return Q(x)
        except (ValueError, ZeroDivisionError): pass
    raise ValueError('coordinate must be an integer or rational string')

def point(p):
    if type(p) not in (list, tuple) or len(p)!=2: raise ValueError('point needs two coordinates')
    return tuple(rational(x) for x in p)

def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def norm2(a): return dot(a,a)
def sign(x): return (x>0)-(x<0)

def angle_compare(u,v,w,z):
    """Compare ordinary angles in (0,pi) via decreasing cotangent, exactly.
    cot = dot/abs(cross); denominator positive, so cross multiplication is safe.
    No trig call or floating point is used in any verdict.
    """
    c,d=abs(cross(u,v)),abs(cross(w,z))
    if not c or not d: raise ValueError('angle must be strictly between zero and pi')
    return -sign(dot(u,v)*d-dot(w,z)*c)

def inspect_triangle(A,B,C):
    A,B,C=point(A),point(B),point(C)
    area=cross(sub(B,A),sub(C,A))
    if not area: raise ValueError('noncollinear triangle required')
    ab,ac=norm2(sub(B,A)),norm2(sub(C,A))
    beta=dot(sub(A,B),sub(C,B))
    gamma=dot(sub(A,C),sub(B,C))
    angle=angle_compare(sub(A,B),sub(C,B),sub(A,C),sub(B,C))
    return {'input':[[str(x) for x in p] for p in (A,B,C)],'signed_double_area':str(area),
            'AB_squared':str(ab),'AC_squared':str(ac),'beta_dot':str(beta),'gamma_dot':str(gamma),
            'angle_relation':angle,'side_relation':sign(ac-ab),
            'cot_difference_numerator':str(beta-gamma),
            'identity_residual':str((gamma-beta)-(ac-ab))}

def infer_side(angle_relation, total=True, equal_implies_equal=True, less_implies_less=True):
    """Finite relation abstraction; assumptions are supplied, not established here."""
    if type(angle_relation) is not int or angle_relation not in (-1,0,1): raise ValueError('relation')
    if any(type(v) is not bool for v in (total,equal_implies_equal,less_implies_less)): raise ValueError('flags')
    possible=['less','equal','greater']+([] if total else ['incomparable'])
    if angle_relation==1:
        if equal_implies_equal: possible.remove('equal')
        if less_implies_less: possible.remove('less')
    return possible

def build_certificate(A,B,C):
    observation=inspect_triangle(A,B,C)
    if observation['angle_relation']!=1: raise ValueError('I.19 premise beta > gamma required')
    return {'schema':1,'observation':observation,'premise':'beta > gamma',
            'excluded':[{'side':'equal','source':'I.5','prediction':'beta = gamma'},
                        {'side':'less','source':'I.18 with labels exchanged','prediction':'beta < gamma'}],
            'remaining':infer_side(1),'conclusion':'AC > AB',
            'scope':'exact rational coordinate model plus separately stated order abstraction'}

def strict_json(x):
    if x is None or type(x) in (str,bool,int): return
    if type(x) is list:
        for item in x: strict_json(item)
        return
    if type(x) is dict and all(type(k) is str for k in x):
        for item in x.values(): strict_json(item)
        return
    raise ValueError('only canonical JSON types; no floats or tuples')

def verify_certificate(A,B,C,certificate):
    try:
        strict_json(certificate)
        expected=build_certificate(A,B,C)
        # Canonical serialization distinguishes 1, true, and 1.0.
        return json.dumps(expected,sort_keys=True,separators=(',',':'))==json.dumps(certificate,sort_keys=True,separators=(',',':'))
    except (ValueError,TypeError,KeyError,OverflowError): return False
