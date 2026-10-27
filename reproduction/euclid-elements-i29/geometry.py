"""Original exact rational teaching model for Euclid I.29; Python stdlib only."""
from fractions import Fraction
import hashlib
import json


def rational(x):
    if type(x) is not str:
        raise ValueError('coordinate must be a canonical rational string')
    try:
        q = Fraction(x)
    except (ValueError, ZeroDivisionError):
        raise ValueError('invalid rational') from None
    if str(q) != x:
        raise ValueError('noncanonical rational')
    return q


def sub(a, b): return tuple(x-y for x,y in zip(a,b))
def dot(a, b): return sum(x*y for x,y in zip(a,b))
def det(a, b): return a[0]*b[1]-a[1]*b[0]
def neg(a): return tuple(-x for x in a)
def sign(x): return (x>0)-(x<0)


def angle(a, b):
    """Sign(cos θ), cos²θ; unique for θ in [0,π], no square roots."""
    aa,bb=dot(a,a),dot(b,b)
    if not aa or not bb:
        raise ValueError('zero ray')
    d=dot(a,b)
    return {'cos_sign':sign(d), 'cos_squared':str(d*d/(aa*bb))}


def parse(data):
    if type(data) is not dict or set(data) != {'G','H','B','D'}:
        raise ValueError('exact point keys required')
    p={}
    for k,v in data.items():
        if type(v) is not list or len(v)!=2:
            raise ValueError('point requires two coordinates in a list')
        p[k]=tuple(rational(x) for x in v)
    return p


def make_certificate(data):
    p=parse(data)
    t,u,v=sub(p['H'],p['G']),sub(p['B'],p['G']),sub(p['D'],p['H'])
    s1,s2=det(t,u),det(t,v)
    if not s1 or not s2:
        raise ValueError('distinct intersections and nonzero transverse rays required')
    if s1*s2 <= 0:
        raise ValueError('B and D must be strictly on the same side of GH')
    if det(u,v):
        raise ValueError('the two lines must be parallel')
    lam=v[0]/u[0] if u[0] else v[1]/u[1]
    agh,ghd,egb,bgh=angle(neg(u),t),angle(neg(t),v),angle(neg(t),u),angle(u,t)
    alternate=agh==ghd
    corresponding=egb==ghd
    supplementary=(bgh['cos_sign']==-ghd['cos_sign'] and bgh['cos_squared']==ghd['cos_squared'])
    if not (lam>0 and alternate and corresponding and supplementary):
        raise ValueError('internal exact consistency failure')
    canonical=json.dumps(data,sort_keys=True,separators=(',',':'))
    return {'schema':1,'input':json.loads(canonical),'input_sha256':hashlib.sha256(canonical.encode()).hexdigest(),
            'model':'rational Euclidean plane; not an axiomatic proof',
            'side_determinants':[str(s1),str(s2)],'positive_scale':str(lam),
            'angles':{'AGH':agh,'GHD':ghd,'EGB':egb,'BGH':bgh},
            'conclusions':{'alternate_equal':alternate,'corresponding_equal':corresponding,'interior_supplementary':supplementary}}


def strict_equal(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict:
        return set(a)==set(b) and all(strict_equal(a[k],b[k]) for k in a)
    if type(a) is list:
        return len(a)==len(b) and all(strict_equal(x,y) for x,y in zip(a,b))
    if type(a) in (str,int,bool,type(None)): return a==b
    return False


def verify_certificate(expected_input, certificate):
    try: return strict_equal(make_certificate(expected_input),certificate)
    except (ValueError,TypeError,KeyError,ZeroDivisionError): return False
