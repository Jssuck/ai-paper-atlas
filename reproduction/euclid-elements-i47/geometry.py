"""Exact rational teaching model for I.47; no square-root or Pythagorean input."""
from fractions import Fraction as Q

def point(p):
    if not isinstance(p, (list, tuple)) or len(p) != 2 or any(type(x) not in (int,Q) for x in p):
        raise ValueError('point requires two exact rational coordinates')
    return tuple(Q(x) for x in p)
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def mul(k,a): return (k*a[0],k*a[1])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def norm(a): return dot(a,a)
def rot(a): return (-a[1],a[0])
def area(*ps): return abs(Q(sum(cross(a,b) for a,b in zip(ps,ps[1:]+ps[:1]))))/2

def inputs(A,B,C):
    A,B,C=map(point,(A,B,C));u,v=sub(B,A),sub(C,A)
    if norm(u)==0 or norm(v)==0 or dot(u,v)!=0: raise ValueError('nonzero perpendicular legs required')
    return A,B,C

def construct(A,B,C):
    A,B,C=inputs(A,B,C);u,v=sub(B,A),sub(C,A);s=1 if cross(u,v)>0 else -1
    w=mul(-s,rot(sub(C,B)));f=mul(-s,rot(u));h=mul(s,rot(v))
    t=dot(sub(A,B),sub(C,B))/norm(sub(C,B));M=add(B,mul(t,sub(C,B)))
    return dict(A=A,B=B,C=C,D=add(B,w),E=add(C,w),F=add(B,f),G=add(A,f),H=add(A,h),K=add(C,h),M=M,L=add(M,w))

def square(P,Q,R,S):
    es=[sub(Q,P),sub(R,Q),sub(S,R),sub(P,S)]
    return norm(es[0])>0 and len({norm(e) for e in es})==1 and all(dot(es[i],es[(i+1)%4])==0 for i in range(4)) and len({1 if cross(es[i],es[(i+1)%4])>0 else -1 for i in range(4)})==1

def verify(A,B,C,cert):
    """Verify local constraints and area chain independently of construct."""
    try:
        A,B,C=inputs(A,B,C)
        if not isinstance(cert,dict) or set(cert)!=set('ABCDEFGHKML'):return False
        p={k:point(v) for k,v in cert.items()}
        if (p['A'],p['B'],p['C'])!=(A,B,C):return False
        D,E,F,G,H,K,M,L=(p[k] for k in 'DEFGHKML')
        if not (square(A,B,F,G) and square(A,C,K,H) and square(B,D,E,C)):return False
        # Every square is exterior to ABC, not simply a square on the line.
        if cross(sub(B,A),sub(F,A))*cross(sub(B,A),sub(C,A))>=0:return False
        if cross(sub(C,A),sub(K,A))*cross(sub(C,A),sub(B,A))>=0:return False
        if cross(sub(C,B),sub(D,B))*cross(sub(C,B),sub(A,B))>=0:return False
        bc=sub(C,B);bm=sub(M,B)
        if cross(bc,bm)!=0 or not 0<dot(bm,bc)<norm(bc):return False
        if cross(sub(L,D),sub(E,D))!=0 or sub(L,M)!=sub(D,B):return False
        if cross(sub(M,A),sub(D,B))!=0:return False
        # I.14 lines needed by I.41.
        if cross(sub(G,A),sub(C,A)) or cross(sub(H,A),sub(B,A)):return False
        # SAS expressed by the two squared lengths and their included dot product.
        if (norm(sub(A,B)),norm(sub(D,B)),dot(sub(A,B),sub(D,B))) != (norm(sub(F,B)),norm(sub(C,B)),dot(sub(F,B),sub(C,B))):return False
        if (norm(sub(A,C)),norm(sub(E,C)),dot(sub(A,C),sub(E,C))) != (norm(sub(K,C)),norm(sub(B,C)),dot(sub(K,C),sub(B,C))):return False
        left,right=area(B,D,L,M),area(M,L,E,C)
        ab,ac=area(A,B,F,G),area(A,C,K,H)
        return (area(A,B,D)==area(F,B,C) and area(A,C,E)==area(K,C,B)
                and left==2*area(A,B,D) and ab==2*area(F,B,C)
                and right==2*area(A,C,E) and ac==2*area(K,C,B)
                and left+right==area(B,D,E,C) and left==ab and right==ac)
    except (ValueError,TypeError,KeyError,ZeroDivisionError):return False

def report(cert):
    p=cert; a=lambda *ks:area(*(p[k] for k in ks))
    return {'AB_square':str(a('A','B','F','G')),'AC_square':str(a('A','C','K','H')),'BC_square':str(a('B','D','E','C')),'left_rectangle':str(a('B','D','L','M')),'right_rectangle':str(a('M','L','E','C')),'ABD':str(a('A','B','D')),'FBC':str(a('F','B','C')),'ACE':str(a('A','C','E')),'KCB':str(a('K','C','B'))}
