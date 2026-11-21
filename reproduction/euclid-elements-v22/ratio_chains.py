"""Exact positive-rational teaching model for Elements V.22."""
from fractions import Fraction


def compare(a, b):
    return (a > b) - (a < b)


def normalize(column):
    """Input items are (positive exact value, kind), in one unit per column."""
    column = tuple(column)
    if len(column) < 2:
        raise ValueError("each column needs two or more quantities")
    values = []
    kind0 = column[0][1]
    for value, kind in column:
        if not isinstance(kind, str) or not kind or kind != kind0:
            raise ValueError("a column must have one nonempty kind")
        if type(value) not in (int, Fraction):
            raise TypeError("use int or Fraction, not floats or bool")
        if value <= 0:
            raise ValueError("magnitudes must be positive")
        values.append(Fraction(value))
    return tuple(values)


def _ordered(left, right):
    return all(a * d == b * c for a, b, c, d
               in zip(left, left[1:], right, right[1:]))


def compare_scaled_endpoints(left, right, scales):
    """Return two endpoint signs after paired, independently chosen scales.

    The test uses exact quotients only to model/check EqRat in rational data.
    An arbitrary scales argument demonstrates one probe, not a universal proof.
    """
    x, y, k = normalize(left), normalize(right), tuple(scales)
    if len(x) != len(y) or len(k) != len(x):
        raise ValueError("chain lengths and scale count must agree")
    if any(type(i) is not int or i <= 0 for i in k):
        raise ValueError("scales must be positive integers")
    if not _ordered(x, y):
        raise ValueError("adjacent ratios do not match in order")
    xx, yy = tuple(a * i for a, i in zip(x, k)), tuple(b * i for b, i in zip(y, k))
    if not _ordered(xx, yy):
        raise ArithmeticError("V.4 scaled-ratio check failed")
    if len(xx) == 2:
        # V.Def.5 directly: only one ratio pair; arbitrary endpoint scales.
        return compare(xx[0], xx[1]), compare(yy[0], yy[1])
    for j in range(2, len(xx)):
        # Prefix ratio agreement established by induction in V.22.
        # Here an exact rational equality checks this proof dependency.
        left_prefix, right_prefix = xx[0] / xx[j-1], yy[0] / yy[j-1]
        if left_prefix != right_prefix:
            raise ArithmeticError("prefix ratio check failed")
        left_inverse, right_inverse = xx[j] / xx[j-1], yy[j] / yy[j-1]
        if left_inverse != right_inverse:
            raise ArithmeticError("last inverse ratio check failed")
        left_sign = compare(left_prefix, left_inverse)
        right_sign = compare(right_prefix, right_inverse)
        if left_sign != right_sign:
            raise ArithmeticError("V.20 order transfer check failed")
    return left_sign, right_sign


def magnitudes(values, kind):
    return tuple((value, kind) for value in values)


if __name__ == "__main__":
    x = magnitudes((8, 4, 2, 1), "length")
    y = magnitudes((12, 6, 3, Fraction(3, 2)), "area")
    for k in ((1, 5, 3, 7), (1, 5, 3, 8), (1, 5, 3, 9)):
        print(k, compare_scaled_endpoints(x, y, k))
