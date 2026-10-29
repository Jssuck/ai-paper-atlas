"""Exact rational-coordinate verification of Euclid II.13; no floating point."""
from fractions import Fraction


def point(value):
    if not isinstance(value, (tuple, list)) or len(value) != 2:
        raise TypeError('a point must be a pair of integers or Fractions')
    if any(type(x) not in (int, Fraction) for x in value):
        raise TypeError('coordinates must be integers or Fractions, not bool/float')
    return tuple(Fraction(x) for x in value)


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def dot(a, b):
    return a[0]*b[0] + a[1]*b[1]


def verify(A, B, C, *, original_only=False):
    """Verify II.13's identity; reject nonacute B and collinear triangles.

    original_only=True restricts to all three angles acute. Otherwise accepts
    the modern extension with selected angle B acute, labelling its domain.
    BC*BD is computed as a dot product, without taking irrational square roots.
    """
    if type(original_only) is not bool:
        raise TypeError('original_only must be bool')
    A, B, C = map(point, (A, B, C))
    u, v = sub(A, B), sub(C, B)
    bc2, ba2, ac2 = dot(v, v), dot(u, u), dot(sub(A, C), sub(A, C))
    cross = u[0]*v[1] - u[1]*v[0]
    if bc2 == 0 or cross == 0:
        raise ValueError('nondegenerate triangle required')
    projection_product = dot(u, v)
    if projection_product <= 0:
        raise ValueError('selected angle B must be strictly acute')
    angle_a = dot(sub(B, A), sub(C, A))
    angle_c = dot(sub(A, C), sub(B, C))
    all_acute = angle_a > 0 and angle_c > 0
    if original_only and not all_acute:
        raise ValueError('original domain requires all three angles acute')
    t = projection_product / bc2
    D = (B[0] + t*v[0], B[1] + t*v[1])
    case = 'interior' if t < 1 else ('at-C' if t == 1 else 'beyond-C')
    bd2 = t*t*bc2
    dc2 = (1-t)*(1-t)*bc2
    ad2 = dot(sub(A, D), sub(A, D))
    twice_rectangle = 2*projection_product
    lhs, rhs = bc2+ba2, ac2+twice_rectangle
    # Explicit runtime checks survive both -O and -OO.
    checks = {
        'perpendicular': dot(sub(A, D), v) == 0,
        'II7_algebra': bc2+bd2 == dc2+twice_rectangle,
        'I47_AB': ba2 == ad2+bd2,
        'I47_AC': ac2 == ad2+dc2,
        'II13': lhs == rhs,
    }
    if not all(checks.values()):
        raise ArithmeticError('exact identity verification failed')
    return dict(A=A, B=B, C=C, D=D, t=t, case=case,
                domain='original-domain' if all_acute else 'modern-extension',
                all_acute=all_acute, bc2=bc2, ba2=ba2, ac2=ac2,
                bd2=bd2, dc2=dc2, ad2=ad2,
                rectangle=projection_product, twice_rectangle=twice_rectangle,
                lhs=lhs, rhs=rhs, checks=checks)
