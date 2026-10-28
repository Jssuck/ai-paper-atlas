from fractions import Fraction as F
from itertools import product
VALID=[(a,b,S,p,q) for a,b,S,p,q in product([F(1),F(3),F(7,2)],[F(1,2),F(2)],[F(1),F(5,2)],[-3,0,2],[1,2])]
INVALID=[(0,2,3,1,1),(-1,2,3,1,1),(2,0,3,1,1),(2,-1,3,1,1),(2,2,0,1,1),(2,2,-1,1,1),(2,2,3,1,0),(2,2,3,1,-1),(True,2,3,1,1),(2,2,3,1,1.0),(2,2,'3',1,1),(2,2,3,None,1)]
