"""Original exact rational teaching model for Euclid I.48; no floating tolerances."""
from fractions import Fraction as Q
from math import isqrt

def point(p):
    if not isinstance(p,(tuple,list)) or len(p)!=2: raise ValueError('point must have two coordinates')
    if any(type(x) not in (int,Q) for x in p): raise ValueError('coordinates must be exact int or Fraction, not bool/float')
    return tuple(Q(x) for x in p)
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def mul(t,a): return tuple(t*x for x in a)
def dot(a,b): return sum((x*y for x,y in zip(a,b)),Q(0))
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def norm(a): return dot(a,a)
def length2(a,b): return norm(sub(a,b))
def rotate(a): return (-a[1],a[0])
def rational_sqrt(q):
    if type(q) not in (int,Q) or q<0: raise ValueError('nonnegative exact rational required')
    q=Q(q);n=isqrt(q.numerator);d=isqrt(q.denominator)
    if n*n!=q.numerator or d*d!=q.denominator: raise ValueError('square root is not rational')
    return Q(n,d)
def premises(a,b,c):
    a,b,c=map(point,(a,b,c));u=sub(b,a);v=sub(c,a)
    if cross(u,v)==0: raise ValueError('nondegenerate triangle required')
    if length2(b,c)!=norm(u)+norm(v): raise ValueError('square-sum premise fails')
    return a,b,c

def construct(a,b,c):
    a,b,c=premises(a,b,c);u=sub(b,a);v=sub(c,a)
    # Compute a square root of the ratio, not a conclusion-based dot-product filter.
    t=rational_sqrt(norm(u)/norm(v));w=rotate(v)
    if cross(w,v)*cross(u,v)>0: w=mul(-1,w)
    d=add(a,mul(t,w))
    return {'A':a,'B':b,'C':c,'D':d}

def verify(a,b,c,certificate):
    try:
        a,b,c=premises(a,b,c)
        if type(certificate) is not dict or set(certificate)!=set('ABCD'): return False
        p={k:point(v) for k,v in certificate.items()}
        if (p['A'],p['B'],p['C'])!=(a,b,c): return False
        d=p['D'];ab=sub(b,a);ac=sub(c,a);ad=sub(d,a)
        # Local construction, I.47 comparison, SSS side data, then conclusion.
        checks=[norm(ad)>0,dot(ad,ac)==0,norm(ad)==norm(ab),
                cross(ad,ac)*cross(ab,ac)<0,
                length2(d,c)==norm(ad)+norm(ac),
                length2(d,c)==length2(b,c),
                dot(ad,ac)==dot(ab,ac),dot(ab,ac)==0]
        return all(checks)
    except (ValueError,TypeError,KeyError,ZeroDivisionError): return False

def report(p):
    a,b,c,d=(p[k] for k in 'ABCD')
    return {'AB_squared':str(length2(a,b)),'AC_squared':str(length2(a,c)),
            'BC_squared':str(length2(b,c)),'AD_squared':str(length2(a,d)),
            'DC_squared':str(length2(d,c)),'BAC_dot':str(dot(sub(b,a),sub(c,a))),
            'DAC_dot':str(dot(sub(d,a),sub(c,a))),
            'D':[str(x) for x in d]}
