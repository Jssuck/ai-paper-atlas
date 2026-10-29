"""Euclid III.3: exact coordinate teaching reconstruction, not a proof engine."""
from fractions import Fraction as Q

def rational(x):
    if type(x) not in (int,Q): raise TypeError('exact int or Fraction required; bool and float excluded')
    return Q(x)
def point(p):
    if type(p) not in (tuple,list) or len(p)!=2: raise TypeError('two-coordinate point required')
    return tuple(rational(x) for x in p)
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def norm2(v): return dot(v,v)
def perpendicular(u,v):
    u,v=point(u),point(v)
    if norm2(u)==0 or norm2(v)==0: raise ValueError('zero vector has no perpendicular direction')
    return dot(u,v)==0

def certificate(E,radius_squared,A,B,F):
    E,A,B,F=map(point,(E,A,B,F)); r=rational(radius_squared)
    if r<=0: raise ValueError('positive radius squared required')
    if A==B: raise ValueError('distinct endpoints required')
    if norm2(sub(A,E))!=r or norm2(sub(B,E))!=r: raise ValueError('endpoints must lie on the circle')
    v=sub(B,A); w=sub(F,A); e=sub(E,A)
    if cross(v,e)==0: raise ValueError('diameter chord excluded by III.3')
    if cross(v,w)!=0: raise ValueError('F must lie on the chord line')
    t=dot(w,v)/norm2(v)
    if not 0<t<1: raise ValueError('F must be a strict chord interior point')
    ef=sub(F,E); af=norm2(sub(F,A)); bf=norm2(sub(F,B)); product=dot(ef,v)
    middle=af==bf; right=perpendicular(ef,v)
    # Equal-radius expansion gives 2 EF dot AB = AF^2 - BF^2.
    if 2*product != af-bf: raise ArithmeticError('coordinate identity failure')
    if middle!=right: raise ArithmeticError('equivalence failure')
    return {'E':E,'radius_squared':r,'A':A,'B':B,'F':F,'parameter':t,
            'AF_squared':af,'BF_squared':bf,'EF_squared':norm2(ef),
            'dot_EF_AB':product,'bisects':middle,'perpendicular':right,
            'branch':'midpoint-and-right' if middle else 'neither',
            'equivalent':middle==right}

def same_typed(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict: return a.keys()==b.keys() and all(same_typed(a[k],b[k]) for k in a)
    if type(a) in (tuple,list): return len(a)==len(b) and all(same_typed(x,y) for x,y in zip(a,b))
    return a==b

def verify_certificate(c):
    if type(c) is not dict: return False
    try:
        expected=certificate(c['E'],c['radius_squared'],c['A'],c['B'],c['F'])
        return same_typed(c,expected)
    except (KeyError,TypeError,ValueError,ArithmeticError): return False

def grid():
    """900 rational configurations, with midpoint and non-midpoint branches."""
    for s in (Q(1,2),Q(1),Q(2),Q(3),Q(5)):
        for ox,oy in ((0,0),(2,-3),(-4,1)):
            for u,v in ((1,0),(0,1),(3,4),(4,-3)):
                def T(x,y): return (Q(ox)+s*(u*x-v*y),Q(oy)+s*(v*x+u*y))
                E,A,B=T(0,0),T(-3,4),T(3,4)
                for t in (Q(k,16) for k in range(1,16)):
                    F=tuple(A[i]+t*(B[i]-A[i]) for i in range(2))
                    yield certificate(E,25*s*s*(u*u+v*v),A,B,F)
