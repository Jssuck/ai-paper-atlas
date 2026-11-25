"""Exact teaching reconstruction for Euclid IX.9."""
from dataclasses import dataclass
from math import isqrt


@dataclass(frozen=True)
class PowerChain:
    terms: tuple
    roots: tuple


def _cube_floor(n):
    lo,hi=0,1 << ((n.bit_length()+2)//3)
    while lo+1<hi:
        m=(lo+hi)//2
        if m**3<=n:
            lo=m
        else:
            hi=m
    return lo


def power_chain(q,length,degree):
    """After the implicit unit, give length terms and roots for degree 2 or 3."""
    if type(degree) is not int or degree not in (2,3):
        raise ValueError("degree must be 2 or 3")
    if type(q) is not int or q<2 or type(length) is not int or length<1:
        raise ValueError("expected integer base >= 2 and length >= 1")
    r=isqrt(q) if degree==2 else _cube_floor(q)
    if r**degree!=q:
        raise ValueError("the first nonunit term must be the indicated power")
    if degree==2:
        # Seeds q and q²; the stride multiplier q² has square root q.
        stride,r_stride=q*q,q
        terms,roots=[q,stride],[r,r_stride]
    else:
        # Seeds q,q² (IX.3),q³ (IX.8); q³ has cube root q.
        stride,r_stride=q**3,q
        terms,roots=[q,q*q,stride],[r,r*r,r_stride]
    for i in range(degree,length):
        terms.append(terms[i-degree]*stride)
        roots.append(roots[i-degree]*r_stride)
    for value,root in zip(terms,roots):
        if root**degree!=value:
            raise ArithmeticError("positional root certificate failed")
    return PowerChain(tuple(terms[:length]),tuple(roots[:length]))
