from fractions import Fraction as Q
from geometry import *
def display(name,args):
    c=certificate(*args)
    print(name, 'AF2=',c['AF_squared'],'BF2=',c['BF_squared'],'dot=',c['dot_EF_AB'],'branch=',c['branch'],'verified=',verify_certificate(c))
display('midpoint',((0,0),25,(-3,4),(3,4),(0,4)))
display('oblique',((0,0),25,(-3,4),(3,4),(1,4)))
display('quarter',((0,0),25,(-3,4),(3,4),(Q(-3,2),4)))
display('translated',((2,-3),100,(-4,5),(8,5),(2,5)))
print('diameter excluded counterexample: F=E=(0,0), A=(-5,0), B=(5,0), line direction=(1,1); bisects=True, perpendicular=',perpendicular((1,1),(10,0)))
print('off-center counterexample: vertical x=1 cuts chord y=4 at F=(1,4); perpendicular=',perpendicular((0,1),(6,0)), 'AF2=16 BF2=4; line misses E=(0,0)')
try: perpendicular((0,0),(6,0))
except ValueError as e: print('zero-direction rejection:',str(e))
rows=list(grid());print('grid:',len(rows),'midpoints:',sum(c['bisects'] for c in rows),'non-midpoints:',sum(not c['bisects'] for c in rows))
