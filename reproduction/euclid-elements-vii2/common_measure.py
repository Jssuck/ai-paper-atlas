"""VII.2 modern positive-integer division trace and two-way certificates."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Step:
    a: int
    b: int
    q: int
    r: int


def trace(a,b):
    if any(type(i) is not int or i<1 for i in (a,b)):
        raise ValueError("positive integers required")
    a,b=max(a,b),min(a,b)
    rows=[]
    while b:
        q,r=divmod(a,b)
        rows.append(Step(a,b,q,r))
        a,b=b,r
    return tuple(rows)


def greatest_measure(a,b,original_domain=False):
    rows=trace(a,b)
    g=rows[-1].b
    if original_domain and g==1:
        raise ValueError("ancient proposition assumes non-coprime inputs")
    return g


def backward_witness(rows):
    """Return g and a verified chain (a,b) in reverse, with integral coefficients."""
    g=rows[-1].b
    a_coeff,b_coeff=1,0
    rev=[]
    for row in reversed(rows):
        a_coeff,b_coeff=row.q*a_coeff+b_coeff,a_coeff
        if (row.a,row.b)!=(g*a_coeff,g*b_coeff):
            raise ValueError("inconsistent trace")
        rev.append((row.a,row.b,a_coeff,b_coeff))
    return g,tuple(rev)


def common_divisors(a,b):
    return tuple(d for d in range(1,min(a,b)+1) if not (a%d or b%d))
