"""Greatest common measure and backward witnesses for Euclid X.3."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Certificate:
    measure: Fraction
    divisions: tuple
    backward_counts: tuple


def greatest_common_measure(a,b):
    if any(type(x) not in (int,Fraction) for x in (a,b)) or not a>=b>0:
        raise ValueError("expected exact positive rational magnitudes a>=b")
    x,y=Fraction(a),Fraction(b)
    steps=[]
    while y:
        q,r=divmod(x,y)
        steps.append((x,y,q,r))
        x,y=y,r
    counts=[1,0]
    for _,_,q,_ in reversed(steps):
        counts.insert(0,q*counts[0]+counts[1])
    if any((steps[i][0],steps[i][1])!=(x*counts[i],x*counts[i+1])
           for i in range(len(steps))):
        raise ArithmeticError("backward reconstruction failed")
    return Certificate(x,tuple(steps),tuple(counts))


def common_measure_at(certificate,n):
    """Submeasure d/n, for positive integer n."""
    if type(n) is not int or n<1:
        raise ValueError("expected positive integer subdivision")
    return certificate.measure/n


def is_common_measure(certificate,c):
    if type(c) not in (int,Fraction) or c<=0:
        raise ValueError("expected positive exact rational candidate")
    return (certificate.measure/c).denominator==1
