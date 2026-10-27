"""Finite deterministic teaching cases, not a proof of all inputs."""
from fractions import Fraction as Q

def positive_cases():
    for a in range(1,7):
        for b in range(1,7):
            for c in range(1,7):
                if abs(a-b)<c<a+b:
                    for scale in (Q(1),Q(2,3)):
                        yield tuple(Q(v)*scale for v in (a,b,c))

NEGATIVE=[(0,1,1),(-1,1,1),(1,0,1),(1,1,0),(1,1,2),(1,2,1),
          (2,1,1),(1,1,3),(3,1,1),(1,3,1),(True,1,1),(1.0,1,1),
          ('bad',1,1),('1/0',1,1),(None,1,1)]
