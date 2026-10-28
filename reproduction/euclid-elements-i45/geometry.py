"""Original exact teaching model for Euclid I.45; not a general proof engine."""
from fractions import Fraction as Q

def rational(x):
    if type(x) not in (int,Q): raise ValueError('exact int/Fraction required')
    return Q(x)
def point(x):
    if type(x) not in (tuple,list) or len(x)!=2: raise ValueError('two coordinates required')
    return tuple(rational(t) for t in x)
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def orient(a,b,c): return cross(sub(b,a),sub(c,a))
def area(poly):
    poly=[point(p) for p in poly]
    return abs(sum(cross(a,b) for a,b in zip(poly,poly[1:]+poly[:1])))/2

def inputs(vertices,h,p,q):
    if type(vertices) not in (tuple,list) or len(vertices)!=4: raise ValueError('four ordered vertices required')
    v=tuple(point(x) for x in vertices)
    turns=[orient(v[i],v[(i+1)%4],v[(i+2)%4]) for i in range(4)]
    if not (all(t>0 for t in turns) or all(t<0 for t in turns)):
        raise ValueError('strict convex boundary required')
    h,p,q=map(rational,(h,p,q))
    if h<=0 or q<=0: raise ValueError('h and q must be positive')
    return v,h,p,q

def construct(vertices,h=2,p=1,q=2):
    v,h,p,q=inputs(vertices,h,p,q); A,B,C,D=v
    s1=abs(orient(A,B,D))/2; s2=abs(orient(D,B,C))/2
    K=(Q(0),Q(0)); F=(h*p/q,h); H=(s1/h,Q(0)); G=add(H,F)
    M=((s1+s2)/h,Q(0)); L=add(M,F)
    return {'points':dict(K=K,F=F,G=G,H=H,L=L,M=M),'areas':(s1,s2,s1+s2)}

def verify(vertices,h,p,q,certificate):
    """Strict schema and exact representation check, then geometric invariants.

    This shares primitive arithmetic with construction; independent review is separate.
    """
    try:
        v,h,p,q=inputs(vertices,h,p,q)
        if type(certificate) is not dict or set(certificate)!={'points','areas'}: return False
        pts=certificate['points']; ar=certificate['areas']
        if type(pts) is not dict or set(pts)!=set('KFGHLM'): return False
        if any(type(z) is not tuple or len(z)!=2 or any(type(t) is not Q for t in z) for z in pts.values()): return False
        if type(ar) is not tuple or len(ar)!=3 or any(type(t) is not Q for t in ar): return False
        expected=construct(v,h,p,q)
        if certificate!=expected: return False
        K,F,G,H,L,M=(pts[k] for k in 'KFGHLM')
        s1,s2,total=ar
        return (area(list(v))==total and area([K,F,G,H])==s1 and area([H,G,L,M])==s2
          and area([K,F,L,M])==total and sub(F,K)==sub(G,H)==sub(L,M)
          and orient(K,H,M)==0 and orient(F,G,L)==0
          and K[0]<H[0]<M[0] and F[0]<G[0]<L[0]
          and cross(sub(G,H),sub(K,H))*cross(sub(G,H),sub(M,H))<0
          and cross(sub(F,K),(p,q))==0 and sub(F,K)[1]>0)
    except (ValueError,TypeError,KeyError,ZeroDivisionError): return False
