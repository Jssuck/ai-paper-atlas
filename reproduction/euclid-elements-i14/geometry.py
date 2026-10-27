"""Exact modern teaching model for Euclid I.14; no trigonometric floats.

An ordinary angle is represented by (dot, abs(cross)). Its angle lies in
(0, pi); a negative-real product therefore certifies sum pi, not 3*pi.
This interpretation uses modern angle/rotation facts, not Euclid's wording.
"""
from fractions import Fraction as F
import json


def rational(x):
    if isinstance(x, bool) or not isinstance(x, (int, F)):
        raise TypeError('only int or Fraction inputs; no float/bool')
    return F(x)


def vector(v):
    if not isinstance(v, (list, tuple)) or len(v) != 2:
        raise ValueError('expected two coordinates')
    return tuple(rational(x) for x in v)


def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def multiply(z,w): return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])


def encode(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,(tuple,list)): return [encode(y) for y in x]
    if isinstance(x,dict): return {k:encode(v) for k,v in x.items()}
    return x


def inspect_configuration(b,a,c,d):
    """Diagnose angle premise and side premise independently of conclusion."""
    b,a,c,d=map(vector,(b,a,c,d))
    u,v,w=sub(a,b),sub(c,b),sub(d,b)
    if any(dot(t,t)==0 for t in (u,v,w)):
        raise ValueError('all rays must be nonzero')
    h,k=cross(u,v),cross(u,w)
    if h==0 or k==0:
        raise ValueError('both ordinary angles must be nondegenerate')
    z1,z2=(dot(u,v),abs(h)),(dot(u,w),abs(k))
    product=multiply(z1,z2)
    return {'inputs':{'B':b,'A':a,'C':c,'D':d},'side_crosses':(h,k),
            'angle_pairs':(z1,z2),'angle_product':product,
            'opposite_sides':h*k<0,
            'supplementary':product[1]==0 and product[0]<0,
            'conclusion_cross':cross(v,w),'conclusion_dot':dot(v,w),
            'opposite_rays':cross(v,w)==0 and dot(v,w)<0}


def build_certificate(b,a,c,d):
    data=inspect_configuration(b,a,c,d)
    if not data['opposite_sides']:
        raise ValueError('opposite-side premise fails')
    if not data['supplementary']:
        raise ValueError('angle-sum premise fails')
    if not data['opposite_rays']:
        raise RuntimeError('the reconstructed implication failed')
    # Witness D-B = -lambda*(C-B), lambda positive; computed after premises.
    b,a,c,d=map(vector,(b,a,c,d));v,w=sub(c,b),sub(d,b)
    scale=-dot(v,w)/dot(v,v)
    if scale<=0 or w!=(-scale*v[0],-scale*v[1]):
        raise RuntimeError('opposition witness failed')
    data['positive_scale']=scale
    data['conclusion']='BC and BD are opposite rays; B lies between C and D'
    return encode(data)


def canonical_json(value):
    """Reject non-JSON containers/types, and preserve bool versus number types."""
    def validate(x):
        if type(x) in (str, int, float, bool) or x is None:
            return
        if type(x) is list:
            for item in x: validate(item)
            return
        if type(x) is dict and all(type(k) is str for k in x):
            for item in x.values(): validate(item)
            return
        raise TypeError('certificate must contain only JSON types and string keys')
    validate(value)
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


def verify_certificate(cert,b,a,c,d):
    """Strict JSON-typed replay against independently supplied inputs."""
    try:
        return canonical_json(cert)==canonical_json(build_certificate(b,a,c,d))
    except (TypeError,ValueError,KeyError,OverflowError,RecursionError):
        return False


def angle_model(alpha,beta,side_c=1,side_d=-1):
    """Separate rational-turn model; not all rational vectors have rational angles."""
    alpha,beta=map(rational,(alpha,beta))
    if not 0<alpha<F(1,2) or not 0<beta<F(1,2):
        raise ValueError('ordinary angles must be in (0,1/2) turns')
    if type(side_c) is not int or type(side_d) is not int or side_c not in (-1,1) or side_d not in (-1,1):
        raise ValueError('side signs must be integers +1 or -1')
    separation=(side_d*beta-side_c*alpha)%1
    return {'sum':alpha+beta,'opposite_sides':side_c!=side_d,
            'supplementary':alpha+beta==F(1,2),'directed_separation':separation,
            'opposite_rays':separation==F(1,2)}
