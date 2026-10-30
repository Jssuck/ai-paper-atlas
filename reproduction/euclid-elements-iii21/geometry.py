"""Exact rational teaching model for III.21; finite checks are not a proof."""
from fractions import Fraction as F
from itertools import combinations

def scalar(x):
    if type(x) not in (int, F):
        raise ValueError('only int or Fraction; no bool or float')
    return F(x)

def point(p):
    if type(p) not in (tuple, list) or len(p) != 2:
        raise ValueError('point must have two rational coordinates')
    return tuple(scalar(x) for x in p)

def sub(p,q): return (p[0]-q[0],p[1]-q[1])
def dot(p,q): return p[0]*q[0]+p[1]*q[1]
def cross(p,q): return p[0]*q[1]-p[1]*q[0]
def sign(x): return (x>0)-(x<0)

def certificate(O,r2,B,C,A,D):
    O,B,C,A,D = map(point,(O,B,C,A,D)); r2=scalar(r2)
    if r2<=0: raise ValueError('positive squared radius required')
    if B==C: raise ValueError('distinct chord endpoints required')
    if any(dot(sub(P,O),sub(P,O))!=r2 for P in (B,C,A,D)):
        raise ValueError('all four points must belong to the specified circle')
    if any(P in (B,C) for P in (A,D)):
        raise ValueError('angle vertex must not be a chord endpoint')
    # A=D is allowed: the equality is then tautological.
    sides=[]; cots=[]
    for P in (A,D):
        u,v=sub(B,P),sub(C,P)
        determinant=cross(u,v)
        if determinant==0: raise ValueError('nondegenerate angle required')
        sides.append(sign(cross(sub(C,B),sub(P,B))))
        cots.append(dot(u,v)/abs(determinant))
    same=sides[0]==sides[1]
    diameter=tuple(B[i]+C[i] for i in range(2))==tuple(2*x for x in O)
    holds=cots[0]==cots[1] if same else cots[0]==-cots[1]
    if not holds: raise ArithmeticError('circle-angle identity failed')
    return dict(sides=tuple(sides),cotangents=tuple(cots),relation='equal' if same else 'supplementary',diameter=diameter,equal=cots[0]==cots[1])

def verify(O,r2,B,C,A,D,record):
    """Recompute the certificate; exact schema and types reject bool/int aliases."""
    try:
        expected=certificate(O,r2,B,C,A,D)
        if type(record) is not dict or set(record)!=set(expected): return False
        for key,value in expected.items():
            actual=record[key]
            if type(actual) is not type(value) or actual!=value: return False
            if type(value) is tuple and any(type(x) is not type(y) for x,y in zip(actual,value)): return False
        return True
    except (ValueError,TypeError,KeyError): return False

def rational_circle(n=4):
    # Rational parameter t, plus the missing parameter-at-infinity point.
    return sorted({(F(1),F(0))}|{((t*t-1)/(t*t+1),2*t/(t*t+1)) for t in (F(k,2) for k in range(-n,n+1))})

def grid():
    pts=rational_circle(); counts=dict(points=len(pts),configurations=0,same_side=0,opposite_side=0,diameter=0,obtuse=0)
    for B,C in combinations(pts,2):
        vertices=[P for P in pts if P not in (B,C)]
        for A,D in combinations(vertices,2):
            record=certificate((0,0),1,B,C,A,D)
            if not verify((0,0),1,B,C,A,D,record): raise RuntimeError('verification failed')
            counts['configurations']+=1
            counts['same_side' if record['relation']=='equal' else 'opposite_side']+=1
            counts['diameter']+=record['diameter']
            counts['obtuse']+=any(x<0 for x in record['cotangents'])
    return counts

CASES={
 'same_major_segment':((0,0),25,(-3,4),(3,4),(0,-5),(-5,0)),
 'same_minor_segment':((0,0),25,(-3,4),(3,4),(0,5),(F(7,5),F(24,5))),
 'opposite_not_equal':((0,0),25,(-3,4),(3,4),(0,5),(0,-5)),
 'diameter_exception':((0,0),25,(-5,0),(5,0),(0,5),(0,-5)),
}
