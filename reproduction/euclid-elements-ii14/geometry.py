"""Original exact-rational teaching model of Euclid II.14's rectangle stage.
Not a construction engine, not an implementation of I.45, not a general proof.
"""
from fractions import Fraction

def positive_rational(value, name='length'):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f'{name} must be int or Fraction, not bool or approximate input')
    result = Fraction(value)
    if result <= 0:
        raise ValueError(f'{name} must be strictly positive')
    return result

def sqrt_interval(value, steps=80):
    """Return rational lo,hi with lo² <= value <= hi²; no floats or sqrt oracle.
    Initial bracket [0,max(1,value)]; each iteration halves its width unless exact.
    """
    value = positive_rational(value, 'radicand')
    if isinstance(steps, bool) or not isinstance(steps, int):
        raise TypeError('steps must be an integer')
    if not 0 <= steps <= 10000:
        raise ValueError('steps must be between 0 and 10000')
    lo, hi = Fraction(0), max(Fraction(1), value)
    if hi*hi == value:
        return hi, hi
    for _ in range(steps):
        mid = (lo+hi)/2
        if mid*mid == value:
            return mid, mid
        if mid*mid < value:
            lo = mid
        else:
            hi = mid
    if not lo*lo <= value <= hi*hi:
        raise ArithmeticError('root bracket invariant failed')
    return lo, hi

def construct(a, b):
    """Normalize BE=L >= ED=S; B=0,E=L,F=L+S,G=(L+S)/2.
    For L>S, H=(L,sqrt(L*S)); GH and GF have equal squared lengths.
    The equality branch returns the existing square, not a degenerate GHE proof.
    """
    a, b = positive_rational(a, 'a'), positive_rational(b, 'b')
    L, S = max(a,b), min(a,b)
    area = L*S
    if L == S:
        return dict(branch='already_square', L=L, S=S, area=area,
                    side_squared=area, side=L, checks={'square_area': L*L == area})
    r, d = (L+S)/2, (L-S)/2
    h2 = r*r-d*d
    checks = {'II5': area+d*d == r*r,
              'I47': h2+d*d == r*r,
              'equal_area': h2 == area,
              'strict_intersection': 0 < d < r,
              'order': 0 < r < L < L+S}
    if not all(checks.values()):
        raise ArithmeticError('construction identity failed')
    return dict(branch='semicircle', L=L, S=S, area=area,
                B=Fraction(0), G=r, E=L, F=L+S, radius=r, offset=d,
                radius_squared=r*r, offset_squared=d*d, side_squared=h2,
                checks=checks)

def check_interval(area, lo, hi):
    """A small independent postcondition checker accepting zero as lower bound."""
    area=positive_rational(area, 'area')
    if any(isinstance(x,bool) or not isinstance(x,(int,Fraction)) for x in (lo,hi)):
        raise TypeError('endpoints must be exact rationals')
    return 0 <= lo <= hi and lo*lo <= area <= hi*hi
