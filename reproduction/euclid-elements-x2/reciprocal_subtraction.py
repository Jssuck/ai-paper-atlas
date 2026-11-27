"""Exact rational and symbolic demonstrations for Euclid X.2."""
from fractions import Fraction


def rational_trace(a,b):
    """Return (dividend, divisor, quotient, remainder) rows for a>=b>0."""
    if any(type(x) not in (int,Fraction) for x in (a,b)) or not a>=b>0:
        raise ValueError("expected exact rational magnitudes a>=b>0")
    a,b=Fraction(a),Fraction(b)
    rows=[]
    while b:
        q,r=divmod(a,b)
        rows.append((a,b,q,r))
        a,b=b,r
    return tuple(rows)


def mul(x,y):
    """Multiply coefficient pairs representing a+b*sqrt(2)."""
    a,b=x
    c,d=y
    return a*c+2*b*d,a*d+b*c


def sqrt2_trace(count):
    """Finite symbolic prefix for sqrt(2), 1 justified by t²+2t=1."""
    if type(count) is not int or count<1:
        raise ValueError("expected a positive row count")
    t=(-1,1)
    a,b=(0,1),(1,0)
    rows=[]
    for i in range(count):
        q=1 if i==0 else 2
        r=tuple(v-q*w for v,w in zip(a,b))
        if r!=mul(b,t):
            raise ArithmeticError("symbolic remainder failed")
        rows.append((a,b,q,r))
        a,b=b,r
    return tuple(rows)
