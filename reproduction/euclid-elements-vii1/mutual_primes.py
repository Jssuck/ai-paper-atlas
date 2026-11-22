"""VII.1 teaching trace, exact integer model (not a text reconstruction)."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Step:
    larger: int
    smaller: int
    quotient: int
    remainder: int


def _validate(a,b):
    if any(type(i) is not int or i<1 for i in (a,b)):
        raise ValueError("positive integers required")
    return max(a,b),min(a,b)


def trace(a,b,batched=False):
    """Return (outcome, tuple of steps); stop on new unit or exact division."""
    a,b=_validate(a,b)
    if b==1:
        return "input-unit",()
    if a==b:
        return "input-equal",()
    steps=[]
    while True:
        if batched:
            q,r=divmod(a,b)
        else:
            q,r=0,a
            while r>=b:
                r-=b
                q+=1
        steps.append(Step(a,b,q,r))
        if r==1:
            return "unit-remainder",tuple(steps)
        if r==0:
            return "exact-division",tuple(steps)
        a,b=b,r


def coprime(a,b,batched=False):
    outcome,_=trace(a,b,batched)
    return outcome in ("input-unit","unit-remainder")


def divisor_oracle(a,b):
    """Independent exhaustive divisors of the two starting inputs."""
    a,b=_validate(a,b)
    return tuple(d for d in range(1,b+1) if a%d==0 and b%d==0)
