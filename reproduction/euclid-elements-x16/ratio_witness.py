"""X.16 exact teaching model over Q(sqrt(2))."""
from fractions import Fraction


def sign(a,b):
    if a==0 or b==0 or (a>0)==(b>0):
        x = a or b
        return (x>0)-(x<0)
    delta = a*a-2*b*b
    return ((delta>0)-(delta<0))*((a>0)-(a<0))


def _side(x):
    a,b = x
    if any(type(t) not in (int,Fraction) for t in (a,b)):
        raise ValueError("expected exact rational coefficients")
    a,b = Fraction(a),Fraction(b)
    if sign(a,b) <= 0:
        raise ValueError("expected a positive length")
    return a,b


def analyze(part, remainder):
    """Return (whole coefficients, incommensurability of P:R, P:W, R:W)."""
    a,b = _side(part)
    c,d = _side(remainder)
    e,f = a+c,b+d
    return (e,f), (a*d!=b*c, a*f!=b*e, c*f!=d*e)
