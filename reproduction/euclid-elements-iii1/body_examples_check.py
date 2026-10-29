"""Independently check numerical claims in the article; no assert statements."""
from fractions import Fraction as Q
import json
from geometry import recover_center

def check(a,b,label):
 if a!=b:raise RuntimeError(label)
def dist(a,b):return sum((x-y)**2 for x,y in zip(a,b))
A=(-3,4);B=(3,4);C=(0,5);E=(0,-5);D=(0,4);F=(0,0)
check([dist(F,P) for P in (A,B,C,E)],[25]*4,'7.1 F radii')
check([dist(D,P) for P in (A,B,C,E)],[9,9,1,81],'7.1 wrong D')
G=(0,1);H=(1,1)
check([dist(G,P) for P in (A,B,C,E)],[18,18,16,36],'7.2 line candidate')
check([dist(H,P) for P in (A,B)],[25,13],'7.2 outside candidate')
check(recover_center((-5,0),(5,0),C,E)['branch'],'diameter','7.3 diameter')
T=lambda p:(2-2*p[1],-3+2*p[0])
check([T(p) for p in (A,B,C,E,D,F)],[(-6,-9),(-6,3),(-8,-3),(12,-3),(-6,-3),(2,-3)],'7.3 transformed points')
R=recover_center(*(T(p) for p in (A,B,C,E)))
check((R['F'],R['radius_squared']),((2,-3),100),'7.3 recovered result')
wrongF=(0,Q(1,2))
check((dist(wrongF,A),dist(wrongF,C)),(Q(85,4),Q(81,4)),'7.4 wrong E')
try:recover_center(A,B,C,(0,-4))
except ValueError:pass
else:raise RuntimeError('7.4 wrong E accepted')
# Counterexample to assuming noncollinear chords suffice for independent constraints.
for t in (-3,3):
 check(dist((-4,t),(0,0)),25,'parallel chord endpoint')
 check(dist((4,t),(0,0)),25,'parallel chord endpoint')
check(tuple((x+y)/2 for x,y in zip((-4,3),(4,3))),(0,3),'parallel chord midpoint')
check(tuple((x+y)/2 for x,y in zip((-4,-3),(4,-3))),(0,-3),'parallel chord midpoint')
print(json.dumps({'status':'pass','groups':10,'scope':'Article sections 7.1–7.4 and parallel-chord counterexample; finite checks only.'},ensure_ascii=False,indent=2))
