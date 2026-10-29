"""Original exact-rational teaching model of Euclid II.12, not a theorem prover."""
from fractions import Fraction as F


def rational(x):
    if isinstance(x, bool) or not isinstance(x, (int, F)):
        raise TypeError('coordinates must be int or Fraction, not float/bool/string')
    return F(x)


def point(p):
    if not isinstance(p, (tuple, list)) or len(p) != 2:
        raise TypeError('a point must be a pair')
    return tuple(rational(x) for x in p)


def sub(p, q):
    return (p[0]-q[0], p[1]-q[1])


def dot(p, q):
    return p[0]*q[0]+p[1]*q[1]


def squared_distance(p, q):
    v=sub(point(p), point(q))
    return dot(v, v)


def construct(a, b, c):
    """Require noncollinear ABC and an obtuse angle BAC; return exact evidence.

    D=A+t(C-A), t<0 is the external perpendicular foot. We return
    AC*AD as -t*AC², avoiding square roots even for irrational lengths.
    """
    a,b,c=map(point,(a,b,c))
    u,v=sub(c,a),sub(b,a)
    ac2=dot(u,u)
    if ac2 == 0:
        raise ValueError('A and C must differ')
    cross=u[0]*v[1]-u[1]*v[0]
    if cross == 0:
        raise ValueError('triangle must be nondegenerate')
    uv=dot(u,v)
    if uv >= 0:
        raise ValueError('angle BAC must be strictly obtuse')
    t=uv/ac2
    d=tuple(a[i]+t*u[i] for i in range(2))
    ab2,bc2=squared_distance(a,b),squared_distance(b,c)
    ad2,bd2,cd2=(squared_distance(a,d),squared_distance(b,d),squared_distance(c,d))
    rectangle=-uv
    checks={
        'external_foot':t<0,
        'perpendicular':dot(sub(b,d),u)==0,
        'ii4':cd2==ac2+ad2+2*rectangle,
        'i47_ab':ab2==ad2+bd2,
        'i47_bc':bc2==cd2+bd2,
        'ii12':bc2==ab2+ac2+2*rectangle,
        'strict_excess':bc2>ab2+ac2,
    }
    if not all(checks.values()):
        raise ArithmeticError('evidence check failed')
    return {'A':a,'B':b,'C':c,'D':d,'t':t,'AB2':ab2,'AC2':ac2,
            'BC2':bc2,'AD2':ad2,'BD2':bd2,'CD2':cd2,
            'AC_times_AD':rectangle,'correction':2*rectangle,'checks':checks}


def normalized(c,d,h):
    c,d,h=map(rational,(c,d,h))
    if c<=0 or d<=0 or h==0:
        raise ValueError('require c>0, d>0 and h!=0')
    return construct((0,0),(-d,h),(c,0))
