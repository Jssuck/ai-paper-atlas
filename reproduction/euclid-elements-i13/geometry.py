"""Exact teaching reconstruction of I.13, not a historical proof assistant.

Directed vector pairs encode positive rotations without computing radians.
All coordinates are rational; no trigonometric library or float is used.
"""
from fractions import Fraction as F


def rational(x):
    if isinstance(x, bool) or not isinstance(x, (int, F)):
        raise TypeError('coordinates and turns must be int or Fraction, not float/bool')
    return F(x)


def vector(v):
    if not isinstance(v, (tuple, list)) or len(v) != 2:
        raise ValueError('a vector needs exactly two rational coordinates')
    return tuple(rational(x) for x in v)


def dot(a, b):
    return a[0]*b[0] + a[1]*b[1]


def cross(a, b):
    return a[0]*b[1] - a[1]*b[0]


def sub(a, b):
    return (a[0]-b[0], a[1]-b[1])


def rotate_pair(a, b):
    return (dot(a,b), cross(a,b))


def multiply(z, w):
    return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])


def encode(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, (tuple, list)):
        return [encode(v) for v in x]
    if isinstance(x, dict):
        return {k:encode(v) for k,v in x.items()}
    return x


def build_certificate(b, c, d, a):
    """B lies between C,D; A off CD. Output bound to all four inputs.

    Orientation is chosen so BA lies in the positive half-plane of BC.
    Reflection is handled by an orientation sign rather than an angle wrap.
    """
    b,c,d,a = map(vector, (b,c,d,a))
    u,v,w = sub(c,b),sub(d,b),sub(a,b)
    if dot(u,u)==0 or dot(v,v)==0:
        raise ValueError('base rays must be nonzero')
    if cross(u,v)!=0 or dot(u,v)>=0:
        raise ValueError('BC and BD must be opposite rays, not merely collinear')
    side = cross(u,w)
    if side==0:
        raise ValueError('BA must leave the supporting line')
    s = F(1) if side>0 else F(-1)
    e = (-s*u[1],s*u[0])  # same-side perpendicular auxiliary ray
    z1=(dot(u,w),s*cross(u,w))
    z2=(dot(w,v),s*cross(w,v))
    product=multiply(z1,z2)
    expected=(dot(u,v)*dot(w,w),F(0))
    if product != expected or product[0]>=0 or z1[1]<=0 or z2[1]<=0:
        raise RuntimeError('algebraic invariant failed')
    position='right' if dot(u,w)==0 else ('before_perpendicular' if dot(u,w)>0 else 'after_perpendicular')
    return encode({'inputs':{'B':b,'C':c,'D':d,'A':a},
        'orientation':s,'base_opposition':{'cross':cross(u,v),'dot':dot(u,v)},
        'auxiliary_ray':e,'perpendicular_dot':dot(u,e),
        'first_rotation':z1,'second_rotation':z2,'rotation_product':product,
        'expected_product':expected,'ray_order_case':position,
        'conclusion':'two positive ordinary angles sum to a half-turn'})


def verify_certificate(cert, b, c, d, a):
    """Recompute from independently supplied inputs; reject extra/missing fields."""
    try:
        return cert == build_certificate(b,c,d,a)
    except (TypeError,ValueError,KeyError):
        return False


def angle_partition(t):
    """Separate additive model, in turns. No claim that rational vectors have
    rational angles. The input is an angle measure under explicit angle axioms.
    """
    t=rational(t)
    half,quarter=F(1,2),F(1,4)
    if not 0<t<half:
        raise ValueError('ordinary nondegenerate angle must be in (0,1/2) turns')
    complement=half-t
    case='right' if t==quarter else ('before_perpendicular' if t<quarter else 'after_perpendicular')
    excess=abs(t-quarter)
    # Both quarter-turns decompose into adjacent sectors in the relevant order.
    pieces=(t,quarter-t,quarter) if t<=quarter else (quarter,t-quarter,half-t)
    if sum(pieces)!=half:
        raise RuntimeError('partition arithmetic failed')
    return {'first':t,'second':complement,'sum':t+complement,
            'case':case,'distance_from_right':excess,'ordered_sectors':pieces}
