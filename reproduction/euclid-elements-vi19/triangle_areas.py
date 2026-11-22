"""VI.19 teaching model: exact areas, similarity and the third proportional."""
from fractions import Fraction as Q


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def scale(k, a):
    return tuple(k*x for x in a)


def cross(a, b):
    return a[0]*b[1]-a[1]*b[0]


def norm2(a):
    return sum(x*x for x in a)


def signed_double_area(a, b, c):
    return cross(sub(b, a), sub(c, a))


def area(a, b, c):
    return Q(abs(signed_double_area(a, b, c)), 2)


def side_squares(a, b, c):
    """Correspondence is AB, BC, CA; never sort these entries."""
    return (norm2(sub(a, b)), norm2(sub(b, c)), norm2(sub(c, a)))


def third_point(b, c, k):
    """k is positive EF/BC; return G on ray BC with BG/BC=k²."""
    if b == c or k <= 0:
        raise ValueError("distinct base endpoints and positive factor required")
    return add(b, scale(k*k, sub(c, b)))


def transform(p, k, shift, rotation, reflected=False):
    """One rational example family of rotations, optional reflection, and scaling."""
    x, y = p
    if reflected:
        y = -y
    u, v = rotation
    if u*u+v*v != 1 or k <= 0:
        raise ValueError("rotation must be unit and scale positive")
    return add(shift, scale(k, (u*x-v*y, v*x+u*y)))


def worked():
    abc = ((1, 3), (0, 0), (4, 0))
    deff = ((Q(3, 2), Q(9, 2)), (0, 0), (6, 0))
    return abc, deff, third_point(abc[1], abc[2], Q(3, 2))


def grid():
    shapes = (((1, 3), (0, 0), (4, 0)), ((-2, 3), (-1, -2), (3, 2)),
              ((Q(7, 5), -3), (1, 2), (-1, 7)), ((4, -3), (0, 0), (5, 0)))
    for abc in shapes:
        for k in (Q(1, 4), Q(2, 3), Q(1), Q(3, 2), Q(5, 2)):
            for rotation in ((1, 0), (0, 1), (Q(3, 5), Q(4, 5)), (Q(-5, 13), Q(12, 13))):
                for shift in ((0, 0), (Q(1, 7), Q(-8, 3))):
                    for reflected in (False, True):
                        deff = tuple(transform(p, k, shift, rotation, reflected) for p in abc)
                        yield abc, deff, k, reflected
