"""Exact coordinate probes for Elements VI.1, not its synthetic proof."""
from fractions import Fraction


def exact(value):
    if type(value) not in (int, Fraction):
        raise TypeError("expected an int or Fraction")
    return Fraction(value)


def positive(value):
    result = exact(value)
    if result <= 0:
        raise ValueError("expected a positive length")
    return result


def multiplier(value):
    if type(value) is not int or value <= 0:
        raise ValueError("expected a positive integer multiplier")
    return value


def sign(a, b):
    return (a > b) - (a < b)


def determinant(p, q):
    x, y = map(exact, p)
    u, v = map(exact, q)
    return x * v - y * u


def fan(base, height, count, *, direction=1, apex_x=0, shear=0):
    """Return (extended base, piece areas, whole triangle, parallelogram)."""
    base, height = positive(base), positive(height)
    count, apex_x, shear = multiplier(count), exact(apex_x), exact(shear)
    if type(direction) is not int or direction not in (-1, 1):
        raise ValueError("direction must be 1 or -1")
    step = direction * base
    pieces = tuple(
        abs(determinant((step, 0), (apex_x - i * step, height))) / 2
        for i in range(count)
    )
    whole = abs(determinant((count * step, 0), (apex_x, height))) / 2
    parallelogram = abs(determinant((count * step, 0), (shear, height)))
    return count * base, pieces, whole, parallelogram


def probe(base_left, base_right, height_left, height_right, m, n):
    """Compare base, triangle and parallelogram multiples; do not assume equal heights."""
    left = fan(base_left, height_left, m, direction=-1, apex_x=3, shear=2)
    right = fan(base_right, height_right, n, apex_x=3, shear=-1)
    return left, right, tuple(sign(left[i], right[i]) for i in (0, 2, 3))


def sqrt2_probe(m, n):
    """Exact signs of m versus n√2, for base and two area models at height 2."""
    m, n = multiplier(m), multiplier(n)
    # Positive quantities retain their comparison after squaring.
    return (sign(m*m, 2*n*n), sign(m*m, 2*n*n), sign(4*m*m, 8*n*n))
