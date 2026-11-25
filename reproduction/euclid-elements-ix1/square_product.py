"""Exact ordered-factor certificate for Euclid IX.1."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ProductTrace:
    plane_chain: tuple
    lifted_chain: tuple
    root: int


def square_product(left, right):
    """Verify supplied ordered factors and construct a root of the product."""
    a, b = left
    c, d = right
    if any(type(n) is not int or n < 1 for n in (a, b, c, d)):
        raise ValueError("each side factor must be a positive integer")
    m = b*c
    if m != a*d:
        raise ValueError("corresponding sides are not proportional")
    area1, area2 = a*b, c*d
    lifted = area1*area1, area1*m, area1*area2
    if lifted[1]**2 != lifted[0]*lifted[2]:
        raise ArithmeticError("lifted chain is not geometric")
    root, remainder = divmod(lifted[1], area1)
    if remainder or root**2 != lifted[2]:
        raise ArithmeticError("root transfer failed")
    return ProductTrace((area1, m, area2), lifted, root)
