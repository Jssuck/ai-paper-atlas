"""Exact rational teaching certificates for Euclid I.7, not a ruler/compass engine."""
from fractions import Fraction as F

def point(p):
    if not isinstance(p, (tuple, list)) or len(p) != 2:
        raise TypeError('a point must have two rational coordinates')
    if any(isinstance(x, bool) or not isinstance(x, (int, F)) for x in p):
        raise TypeError('only int and Fraction coordinates are accepted')
    return tuple(F(x) for x in p)

def sub(p,q): return (p[0]-q[0],p[1]-q[1])
def dot(p,q): return p[0]*q[0]+p[1]*q[1]
def cross(p,q): return p[0]*q[1]-p[1]*q[0]
def distance2(p,q):
    d=sub(point(p),point(q)); return dot(d,d)

def certificate(A,B,C,D):
    """Report all premises separately; valid implies C=D, not distinct witnesses."""
    A,B,C,D=map(point,(A,B,C,D))
    u=sub(B,A); v=sub(C,A); w=sub(D,A); q=dot(u,u)
    if q == 0: raise ValueError('baseline endpoints must be distinct')
    s=dot(u,v); t=dot(u,w); h=cross(u,v); k=cross(u,w)
    ac=dot(v,v); ad=dot(w,w); bc=distance2(B,C); bd=distance2(B,D)
    equal_a=ac==ad; equal_b=bc==bd
    same_side=h*k>0; nondegenerate=h!=0 and k!=0
    valid=equal_a and equal_b and same_side
    return dict(equal_a=equal_a,equal_b=equal_b,same_side=same_side,
        nondegenerate=nondegenerate,distinct=C!=D,premises=valid,
        conclusion=C==D,implication=(not valid or C==D),
        baseline2=q,projection_c=s,projection_d=t,cross_c=h,cross_d=k,
        projection_difference=t-s,
        distance_difference_identity=(bc-bd)==(ac-ad)-2*(s-t),
        norm_cross_identity_c=q*ac==s*s+h*h,
        norm_cross_identity_d=q*ad==t*t+k*k,
        projection_equal=s==t,height_square_equal=h*h==k*k,
        signed_height_equal=h==k,
        reconstruction_c=(q*v[0]==s*u[0]-h*u[1] and q*v[1]==s*u[1]+h*u[0]),
        reconstruction_d=(q*w[0]==t*u[0]-k*u[1] and q*w[1]==t*u[1]+k*u[0]))

def reflect(A,B,C):
    A,B,C=map(point,(A,B,C)); u=sub(B,A); v=sub(C,A); q=dot(u,u)
    if q == 0: raise ValueError('baseline endpoints must be distinct')
    s=dot(u,v)
    return tuple(A[i]+2*s*u[i]/q-v[i] for i in (0,1))

def verify_claim(A,B,C,D):
    """Strict I.7-domain verifier: rejects wrong premises, not vacuous success."""
    r=certificate(A,B,C,D)
    return r['premises'] and r['conclusion']
