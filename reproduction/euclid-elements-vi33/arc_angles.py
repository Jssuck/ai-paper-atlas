"""VI.33 modern exact unit model; turns are additive, not folded."""
from dataclasses import dataclass
from fractions import Fraction as Q


@dataclass(frozen=True)
class Arc:
    radius: Q
    sweep: Q

    def __post_init__(self):
        r,t=Q(self.radius),Q(self.sweep)
        if r<=0 or not 0<t<1:
            raise ValueError("positive radius and given proper arc required")
        object.__setattr__(self,"radius",r)
        object.__setattr__(self,"sweep",t)

    def length_over_tau(self):
        return self.radius*self.sweep

    def central_turns(self):
        return self.sweep

    def inscribed_turns(self):
        return self.sweep/2


def sign(x):
    return (x>0)-(x<0)


def comparison(a,b,m,n):
    if m<=0 or n<=0 or type(m) is not int or type(n) is not int:
        raise ValueError("positive integer multipliers required")
    return sign(m*a-n*b)


def compare_arcs(a,b,m,n):
    return (comparison(a.length_over_tau(),b.length_over_tau(),m,n),
            comparison(a.central_turns(),b.central_turns(),m,n),
            comparison(a.inscribed_turns(),b.inscribed_turns(),m,n))


def principal_turns(angle):
    wrapped=Q(angle)%1
    return min(wrapped,1-wrapped)
