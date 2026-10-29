"""Exact rational teaching certificates for Euclid III.2, not a proof engine."""
from fractions import Fraction as Q

def rational(x):
    if type(x) not in (int,Q):
        raise TypeError('expected int or Fraction, excluding bool and float')
    return Q(x)

def point(x):
    if type(x) not in (tuple,list) or len(x)!=2:
        raise TypeError('expected a pair of exact coordinates')
    return tuple(rational(v) for v in x)

def sqdist(a,b):
    a,b=point(a),point(b)
    return sum((u-v)**2 for u,v in zip(a,b))

def certificate(center,radius_squared,a,b,t):
    """Accept two distinct points on a positive circle, 0 <= t <= 1."""
    c,a,b=map(point,(center,a,b));r2=rational(radius_squared);t=rational(t)
    if r2<=0: raise ValueError('radius squared must be positive')
    if a==b: raise ValueError('endpoints must be distinct')
    if sqdist(c,a)!=r2 or sqdist(c,b)!=r2: raise ValueError('endpoints must lie on the circle')
    if not 0<=t<=1: raise ValueError('parameter must belong to the closed segment')
    e=tuple((1-t)*x+t*y for x,y in zip(a,b))
    chord2=sqdist(a,b);e2=sqdist(c,e);gap=t*(1-t)*chord2
    branch='endpoint' if t in (0,1) else ('center' if e==c else 'strict-interior')
    return {'center':c,'radius_squared':r2,'A':a,'B':b,'t':t,'E':e,
            'chord_squared':chord2,'distance_squared':e2,'gap':gap,'branch':branch}

def verify_certificate(record):
    """Recompute every field, reject unknown fields and bool/int equivalence."""
    if type(record) is not dict: return False
    try:
        expected=certificate(record['center'],record['radius_squared'],record['A'],record['B'],record['t'])
        if set(record)!=set(expected): return False
        for key,v in expected.items():
            w=record[key]
            if type(v) is tuple:
                if type(w) is not tuple or len(w)!=2 or any(type(x) is not Q for x in w): return False
            elif type(w) is not type(v): return False
            if w!=v: return False
        return True
    except (ValueError,TypeError,KeyError,OverflowError): return False

def rational_circle_points():
    """Finite exact fixtures, not a representation of an arbitrary circle."""
    out={(Q(-1),Q(0))}
    for k in range(-4,5):
        u=Q(k,3);out.add(((1-u*u)/(1+u*u),2*u/(1+u*u)))
    return sorted(out)

def grid_records():
    pts=rational_circle_points()
    for shift in ((0,0),(3,-2)):
        for scale in (Q(1),Q(2,3)):
            ps=[tuple(Q(o)+scale*x for o,x in zip(shift,p)) for p in pts]
            for i,a in enumerate(ps):
                for b in ps[i+1:]:
                    for t in (Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)):
                        yield certificate(shift,scale*scale,a,b,t)
