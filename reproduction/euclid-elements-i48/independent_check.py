"""Independent Cartesian-domain technical review, not a general proof."""
from geometry import construct,verify,length2,cross,sub
from fractions import Fraction as Q
import itertools
count=0;rejected=0
A=(Q(1,3),Q(-2,5))
for coords in itertools.product(range(-3,4),repeat=4):
    u=coords[:2];v=coords[2:]
    B=tuple(A[i]+Q(u[i],2) for i in range(2))
    C=tuple(A[i]+Q(v[i],3) for i in range(2))
    eligible=cross(sub(B,A),sub(C,A))!=0 and length2(B,C)==length2(A,B)+length2(A,C)
    try:p=construct(A,B,C)
    except ValueError:
        if eligible:raise RuntimeError('eligible rejected')
        rejected+=1
    else:
        if not eligible or not verify(A,B,C,p):raise RuntimeError('unexpected acceptance')
        count+=1
print('Independent Cartesian enumeration: 2401 rational input triples')
print('Accepted exact premise cases:',count)
print('Rejected other cases:',rejected)
print('All accepted certificates verified; no perpendicular-family preselection.')
print('Finite enumeration does not prove the general theorem.')
