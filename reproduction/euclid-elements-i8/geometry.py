"""Exact rational teaching reconstruction, not Euclid's superposition proof."""
from fractions import Fraction as F

class DegenerateTriangle(ValueError):
    pass

class CorrespondenceMismatch(ValueError):
    pass

def point(p):
    if len(p) != 2 or any(isinstance(x, bool) or not isinstance(x, (int, F)) for x in p):
        raise TypeError('coordinates must be two integers or Fractions')
    return tuple(F(x) for x in p)

def triangle(t):
    if len(t) != 3:
        raise ValueError('three ordered vertices required')
    return tuple(point(p) for p in t)

def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def vectors(t):
    a,b,c=triangle(t)
    return sub(b,a),sub(c,a)

def sides_squared(t):
    a,b,c=triangle(t)
    return tuple(dot(v,v) for v in (sub(b,a),sub(c,a),sub(c,b)))

def gram_from_sides(s):
    """Polarization identity; not a triangle-existence validator."""
    a,b,c=map(F,s)
    d=(a+b-c)/2
    return ((a,d),(d,b))

def gram(t):
    u,v=vectors(t)
    return ((dot(u,u),dot(u,v)),(dot(u,v),dot(v,v)))

def angle_signature(t):
    """Sign(cos angle A), cos(angle A)^2; no inverse trig or square roots."""
    u,v=vectors(t); a,b,d=dot(u,u),dot(v,v),dot(u,v)
    if not a or not b:
        raise DegenerateTriangle('zero arm has no angle')
    return ((d>0)-(d<0), d*d/(a*b))

def apply(m,t,p):
    return tuple(dot(row,p)+shift for row,shift in zip(m,t))

def determinant(m): return m[0][0]*m[1][1]-m[0][1]*m[1][0]

def verify_certificate(source,target,m,translation):
    """Independent exact orthogonality + point mapping check; returns bool."""
    source,target=triangle(source),triangle(target)
    m=tuple(point(row) for row in m); translation=point(translation)
    if len(m)!=2: return False
    columns=tuple(zip(*m))
    if tuple(tuple(dot(x,y) for y in columns) for x in columns) != ((1,0),(0,1)):
        return False
    return all(apply(m,translation,p)==q for p,q in zip(source,target))

def certificate(source,target):
    """Construct unique plane isometry for NONDEGENERATE fixed correspondence.

    Equal Gram matrices imply (YX^-1)^T(YX^-1)=I. No SSS oracle is used.
    """
    source,target=triangle(source),triangle(target)
    u,v=vectors(source); U,V=vectors(target)
    d=det(u,v)
    if d==0 or det(U,V)==0:
        raise DegenerateTriangle('nonzero area required for invertible basis')
    if sides_squared(source)!=sides_squared(target):
        raise CorrespondenceMismatch('ordered (AB^2, AC^2, BC^2) differ')
    inverse=((v[1]/d,-v[0]/d),(-u[1]/d,u[0]/d))
    y=((U[0],V[0]),(U[1],V[1]))
    cols=tuple(zip(*inverse))
    m=tuple(tuple(dot(row,col) for col in cols) for row in y)
    translation=sub(target[0],apply(m,(0,0),source[0]))
    if not verify_certificate(source,target,m,translation):
        raise ArithmeticError('constructed certificate failed exact verification')
    return m,translation
