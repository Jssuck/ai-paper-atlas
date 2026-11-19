"""Euclid IV.1 teaching model: exact normalized points (x, sign*sqrt(y²))."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Point:
    x: Fraction
    y_squared: Fraction
    sign: int


def intersections(radius, length):
    """Return intersections of O=(0,0), R and C=(R,0), L.

    Zero is a point-circle extension, not a case asserted by Euclid.
    Accept exact fractions, integers or fraction strings; reject floats.
    """
    if not all(isinstance(v, (int, str, Fraction)) and not isinstance(v, bool)
               for v in (radius, length)):
        raise TypeError("use exact integers, fractions or strings")
    r, ell = Fraction(radius), Fraction(length)
    if r <= 0 or ell < 0:
        raise ValueError("positive radius and nonnegative length required")
    x = r - ell**2 / (2*r)
    y2 = r**2 - x**2
    if y2 < 0:
        return ()
    if y2 == 0:
        return (Point(x, y2, 0),)
    return tuple(Point(x, y2, sign) for sign in (-1, 1))


def verifies(radius, length, point):
    """Check a witness by both original squared distances, not reconstruction."""
    r, ell = Fraction(radius), Fraction(length)
    x, y2, sign = point.x, point.y_squared, point.sign
    return (r > 0 and ell >= 0 and y2 >= 0
            and ((sign == 0 and y2 == 0) or (sign in (-1, 1) and y2 > 0))
            and x*x + y2 == r*r and (x-r)**2 + y2 == ell*ell)


def sweep():
    """Finite exact grid; coordinate normalization does not restrict orientation."""
    counts = dict(zero=0, interior=0, diameter=0, impossible=0)
    for r in (Fraction(n, d) for d in (1, 5) for n in range(1, 9)):
        for k in range(26):
            ell = r * Fraction(k, 10)
            category, expected = (
                ('zero', 1) if ell == 0 else
                ('interior', 2) if ell < 2*r else
                ('diameter', 1) if ell == 2*r else ('impossible', 0))
            pts = intersections(r, ell)
            if (len(pts) != expected or len(set(pts)) != expected
                    or not all(verifies(r, ell, p) for p in pts)):
                raise ArithmeticError((r, ell, pts))
            counts[category] += 1
    return counts


if __name__ == "__main__":
    for r, ell in ((5, 6), (1, 1), (5, 10), (5, 11), (5, 0)):
        print(f"R={r}, L={ell}:", intersections(r, ell))
    print("finite sweep:", sweep())
