"""Exact rational teaching model of Euclid III.1; no circle-intersection oracle."""
from fractions import Fraction as Q

def rational(x):
    if type(x) is int or type(x) is Q:
        return Q(x)
    raise TypeError('coordinates must be int or Fraction, not bool/float')

def point(p):
    if type(p) not in (tuple,list) or len(p)!=2:
        raise TypeError('point must have two rational coordinates')
    return tuple(rational(x) for x in p)

def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(t,a): return tuple(t*x for x in a)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def midpoint(a,b): return mul(Q(1,2),add(a,b))
def distance_squared(a,b): return dot(sub(a,b),sub(a,b))

def recover_center(A,B,C,E):
    """Recover from a chord AB and supplied intersections C,E of its bisector.

    A,B,C,E are finite exact input evidence. Checks only establish this
    configuration; no claim of checking an arbitrary unseen circumference.
    """
    A,B,C,E=map(point,(A,B,C,E))
    if A==B or C==E: raise ValueError('each chord needs two distinct endpoints')
    D=midpoint(A,B); F=midpoint(C,E)
    v=sub(B,A); w=sub(E,C)
    if cross(sub(D,C),w)!=0: raise ValueError('D must lie on line CE')
    if dot(sub(D,C),sub(D,E))>=0: raise ValueError('D must be strictly between C and E')
    if dot(v,w)!=0: raise ValueError('AB and CE must be perpendicular')
    r2=distance_squared(F,C)
    if any(distance_squared(F,P)!=r2 for P in (A,B,E)):
        raise ValueError('four supplied points must lie on the recovered circle')
    return {'A':A,'B':B,'C':C,'E':E,'D':D,'F':F,'radius_squared':r2,
            'branch':'diameter' if D==F else 'non-diameter'}

def verify_certificate(cert):
    """Reject malformed/tampered fields; explicit checks survive -O/-OO."""
    keys={'A','B','C','E','D','F','radius_squared','branch'}
    if type(cert) is not dict or set(cert)!=keys: return False
    try:
        candidate=recover_center(*(cert[k] for k in ('A','B','C','E')))
        # Normalize before comparison, preventing bool == Fraction(0/1).
        return (point(cert['D'])==candidate['D'] and point(cert['F'])==candidate['F']
                and rational(cert['radius_squared'])==candidate['radius_squared']
                and type(cert['branch']) is str and cert['branch']==candidate['branch'])
    except (TypeError,ValueError): return False

def transform(p,scale=1,cosine=1,sine=0,offset=(0,0)):
    """Rational similarity for tests; negative scale adds a half-turn, not a reflection."""
    p=point(p); scale,co,si=map(rational,(scale,cosine,sine)); offset=point(offset)
    if scale==0 or co*co+si*si!=1: raise ValueError('nonzero scale and unit rotation required')
    return add(offset,mul(scale,(co*p[0]-si*p[1],si*p[0]+co*p[1])))

def sample(diameter=False,scale=1,cosine=1,sine=0,offset=(0,0),lower=False):
    """Known-center fixture generator, NOT the recovery algorithm."""
    if type(diameter) is not bool or type(lower) is not bool: raise TypeError('flags must be bool')
    A,B=((-5,0),(5,0)) if diameter else ((-3,-4 if lower else 4),(3,-4 if lower else 4))
    return tuple(transform(p,scale,cosine,sine,offset) for p in (A,B,(0,5),(0,-5)))
