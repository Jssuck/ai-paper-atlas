"""Exact rational teaching certificates for Euclid I.5; not a ruler/compass engine."""
from fractions import Fraction as Q


def rational(x):
    if isinstance(x, bool) or not isinstance(x, (int, Q)):
        raise TypeError('Coordinates and parameters must be integers or Fractions')
    return Q(x)


def point(p):
    if not isinstance(p, (tuple, list)) or len(p) != 2:
        raise TypeError('A point requires exactly two rational coordinates')
    return tuple(rational(x) for x in p)


def sub(p, q):
    return (p[0]-q[0], p[1]-q[1])


def dot(u, v):
    return u[0]*v[0]+u[1]*v[1]


def det(u, v):
    return u[0]*v[1]-u[1]*v[0]


def squared(p, q):
    u = sub(point(p), point(q))
    return dot(u, u)


def angle_equal(p, o, q, r, s, t):
    """Equality of undirected angles in [0, pi], including dot-product sign."""
    p,o,q,r,s,t = map(point, (p,o,q,r,s,t))
    u,v,w,z = sub(p,o),sub(q,o),sub(r,s),sub(t,s)
    n = dot(u,u)*dot(v,v)
    m = dot(w,w)*dot(z,z)
    if not n or not m:
        raise ValueError('An angle ray must be nonzero')
    d,e = dot(u,v),dot(w,z)
    return (d > 0)-(d < 0) == (e > 0)-(e < 0) and d*d*m == e*e*n


def outward(a,b,f):
    """A,B,F collinear with B strictly between A and F."""
    a,b,f = map(point, (a,b,f))
    u,v = sub(b,a),sub(f,a)
    n = dot(u,u)
    return bool(n and det(u,v) == 0 and dot(u,v) > n)


def certificate(a,b,c,f,g):
    a,b,c,f,g = map(point, (a,b,c,f,g))
    pre = {
        'nondegenerate_ABC': det(sub(b,a),sub(c,a)) != 0,
        'equal_legs_AB_AC': squared(a,b) == squared(a,c),
        'A_B_F_order': outward(a,b,f),
        'A_C_G_order': outward(a,c,g),
        'equal_AF_AG': squared(a,f) == squared(a,g),
    }
    if not all(pre.values()):
        return {'accepted': False, 'premises': pre, 'steps': {}, 'conclusions': {}}
    # Independent geometric equality checks record each stage, not formal inference rules.
    steps = {
        'first_included_FAC_GAB': angle_equal(f,a,c,g,a,b),
        'first_cross_FC_GB': squared(f,c) == squared(g,b),
        'first_angle_AFC_AGB': angle_equal(a,f,c,a,g,b),
        'first_angle_ACF_ABG': angle_equal(a,c,f,a,b,g),
        'remainders_BF_CG': squared(b,f) == squared(c,g),
        'second_included_BFC_CGB': angle_equal(b,f,c,c,g,b),
        'second_angle_FBC_GCB': angle_equal(f,b,c,g,c,b),
        'second_angle_FCB_GBC': angle_equal(f,c,b,g,b,c),
        # CB is strictly inside ACF and BC inside ABG in this construction.
        'split_at_C': det(sub(a,c),sub(b,c))*det(sub(b,c),sub(f,c)) > 0,
        'split_at_B': det(sub(a,b),sub(c,b))*det(sub(c,b),sub(g,b)) > 0,
    }
    conclusions = {
        'base_ABC_ACB': angle_equal(a,b,c,a,c,b),
        'external_FBC_GCB': angle_equal(f,b,c,g,c,b),
    }
    return {'accepted': all(steps.values()) and all(conclusions.values()),
            'premises': pre, 'steps': steps, 'conclusions': conclusions}


def family(b,h,t):
    b,h,t = map(rational, (b,h,t))
    if b <= 0 or h <= 0 or t <= 1:
        raise ValueError('Require b>0, h>0 and t>1')
    a=(Q(0),h); left=(-b,Q(0)); right=(b,Q(0))
    f=(-t*b,h*(1-t)); g=(t*b,h*(1-t))
    return (a,left,right,f,g)


def transform(points, cosine=1, sine=0, orientation=1, translation=(0,0)):
    a,c = map(rational, (cosine,sine))
    if isinstance(orientation,bool) or orientation not in (-1,1):
        raise ValueError('orientation is +1 or -1')
    if a*a+c*c != 1:
        raise ValueError('Require rational orthogonal matrix')
    tx,ty = point(translation)
    out=[]
    for x,y in map(point, points):
        out.append((a*x-orientation*c*y+tx,c*x+orientation*a*y+ty))
    return tuple(out)
