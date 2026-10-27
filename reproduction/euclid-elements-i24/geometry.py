"""Exact modern coordinate audit of I.24, not a formal Euclidean proof."""
from fractions import Fraction as Q
import json


def rational(x):
    if type(x) is not list or len(x) != 2 or any(type(v) is not int for v in x):
        raise ValueError('rational must be an integer pair, excluding bool')
    if x[1] <= 0:
        raise ValueError('denominator must be positive')
    q = Q(*x)
    if [q.numerator, q.denominator] != x:
        raise ValueError('rational must be reduced')
    return q


def pair(q):
    return [q.numerator, q.denominator]


def unit(t):
    return ((1-t*t)/(1+t*t), 2*t/(1+t*t))


def sub(p, q):
    return tuple(a-b for a,b in zip(p,q))


def cross(p, q):
    return p[0]*q[1]-p[1]*q[0]


def norm2(p):
    return sum(v*v for v in p)


def certify(data):
    if type(data) is not dict or set(data) != {'a','b','s','t','reflection'}:
        raise ValueError('unexpected input schema')
    a,b,s,t = (rational(data[k]) for k in ('a','b','s','t'))
    r=data['reflection']
    if type(r) is not int or r not in (-1,1):
        raise ValueError('reflection must be integer -1 or 1')
    if not (a>0 and b>0 and 0<s<t):
        raise ValueError('require positive sides and 0 < s < t')
    us,ut=unit(s),unit(t)
    E=(a,Q(0)); F=(b*us[0],r*b*us[1]); G=(b*ut[0],r*b*ut[1])
    ef2,eg2=norm2(sub(E,F)),norm2(sub(E,G))
    determinant=cross(sub(F,E),sub(G,E))
    gap=eg2-ef2
    identity=4*a*b*(t*t-s*s)/((1+s*s)*(1+t*t))
    if gap != identity or gap <= 0 or norm2(F)!=b*b or norm2(G)!=b*b:
        raise ArithmeticError('exact invariant failed')
    return {'schema':'euclid-i24-v1','input':{k:([*v] if type(v) is list else v) for k,v in data.items()},
            'points':{k:[pair(v) for v in p] for k,p in [('E',E),('F',F),('G',G)]},
            'EF_squared':pair(ef2),'EG_squared':pair(eg2),'gap':pair(gap),
            'gap_identity':pair(identity),'cos_small':pair(us[0]),'cos_large':pair(ut[0]),
            'EFG_orientation':(determinant>0)-(determinant<0),
            'EFG_determinant':pair(determinant),
            'configuration':('outside' if r*determinant>0 else 'inside' if r*determinant<0 else 'collinear'),'conclusion':'EG > EF'}


def strict_equal(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(strict_equal(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(strict_equal(x,y) for x,y in zip(a,b))
    return a==b


def verify(data,certificate):
    try:return strict_equal(certify(data),certificate)
    except (ValueError,TypeError,ArithmeticError):return False


def load_json(text):
    def pairs(items):
        result={}
        for k,v in items:
            if k in result:raise ValueError('duplicate JSON key')
            result[k]=v
        return result
    def bad(x):raise ValueError('nonfinite JSON number')
    return json.loads(text,object_pairs_hook=pairs,parse_constant=bad)
