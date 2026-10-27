"""Exact teaching reconstruction for Euclid I.15, not a formalization of Euclid."""
from fractions import Fraction as F
import json


def rational(x):
    if type(x) is int:
        return F(x)
    if type(x) is str:
        try:
            return F(x)
        except (ValueError, ZeroDivisionError):
            pass
    raise ValueError('coordinate must be an integer or rational string, not bool/float')


def point(p):
    if type(p) not in (list, tuple) or len(p) != 2:
        raise ValueError('point requires two coordinates')
    return tuple(rational(x) for x in p)


def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def encode(v): return [str(x) for x in v]


def angle(a,b):
    """Injective descriptor of an ordinary angle in [0, pi], for nonzero vectors.

    Scale-free (cos,sin) direction in the upper half-plane, using L1 scaling.
    Its second component is nonnegative. This does not measure degrees.
    """
    if dot(a,a)==0 or dot(b,b)==0: raise ValueError('zero ray')
    d,s=dot(a,b),abs(cross(a,b))
    norm=abs(d)+s
    return (F(d)/F(norm),F(s)/F(norm))


def opposite_scale(a,b):
    if dot(a,a)==0 or dot(b,b)==0: raise ValueError('zero ray')
    if cross(a,b)!=0 or dot(a,b)>=0: raise ValueError('not opposite rays')
    i=0 if a[0] else 1
    k=-F(b[i])/F(a[i])
    if k<=0 or b!=(-k*a[0],-k*a[1]): raise ValueError('invalid opposite scale')
    return k


def canonical(value):
    """Strict JSON tree: tuples/custom classes/nonfinite floats are rejected."""
    def check(v):
        if v is None or type(v) in (bool,int,str): return
        if type(v) is list:
            for x in v: check(x)
            return
        if type(v) is dict and all(type(k) is str for k in v):
            for x in v.values(): check(x)
            return
        raise ValueError('not strict JSON data')
    check(value)
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)


def certificate(data):
    if type(data) is not dict or set(data)!={'A','B','C','D','E'}:
        raise ValueError('exactly A B C D E required')
    p={k:point(v) for k,v in data.items()}
    a,b,c,d=(sub(p[k],p['E']) for k in ('A','B','C','D'))
    k,l=opposite_scale(a,b),opposite_scale(c,d)
    determinant=cross(a,c)
    if determinant==0: raise ValueError('coincident supporting lines')
    angles=[angle(c,a),angle(a,d),angle(d,b),angle(b,c)]
    if angles[0]!=angles[2] or angles[1]!=angles[3]:
        raise ArithmeticError('vertical angle identity failed')
    return {'schema_version':1,'input':{k:encode(p[k]) for k in sorted(p)},
            'opposite_scales':[str(k),str(l)],'cross_AE_CE':str(determinant),
            'angles_CEA_AED_DEB_BEC':[encode(x) for x in angles],
            'vertical_pairs_equal':[True,True]}


def verify(data,claim):
    try:
        return canonical(certificate(data))==canonical(claim)
    except (ValueError,TypeError,KeyError,ZeroDivisionError): return False


def angle_ledger(x,y,z):
    """Separate scalar reconstruction: x+y=2 and y+z=2 imply x=z.

    Unit = one right angle. It does not derive a numeric angle from coordinates.
    """
    x,y,z=map(rational,(x,y,z))
    if not all(0<t<2 for t in (x,y,z)): raise ValueError('ordinary nonstraight angles')
    if x+y!=2 or y+z!=2: raise ValueError('I.13 premises absent')
    if x!=z: raise ArithmeticError('cancellation failed')
    return {'x':str(x),'y':str(y),'z':str(z),'common_sum':'2',
            'subtract_common_y':True,'opposite_equal':True,
            'four_angles_sum':str(2*x+2*y)}
