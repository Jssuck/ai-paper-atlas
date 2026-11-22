"""VII.4: a canonical equal-parts model on positive integers."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Parts:
    step: int
    count: int
    whole_count: int
    branch: str

    def is_part(self):
        return self.count==1


def classify(a,b,ancient_domain=False):
    if any(type(x) is not int for x in (a,b)) or not 0<a<b:
        raise ValueError("require strictly ordered positive integers")
    if ancient_domain and a==1:
        raise ValueError("unit is not an ancient number")
    x,y=b,a
    while y:
        x,y=y,x%y
    g=x
    if a==1:
        branch="initial-unit"
    elif g==1:
        branch="coprime-units"
    elif a==g:
        branch="measures-whole"
    else:
        branch="common-measure"
    return Parts(g,a//g,b//g,branch)


def divisor_oracle(a,b):
    return tuple(d for d in range(1,a+1) if not a%d and not b%d)
