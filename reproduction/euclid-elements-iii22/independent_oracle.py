"""Separate floating atan2 oracle; finite numerical sanity check, not exact proof."""
import math
from geometry import configurations

def angle(p,q,r):
    ux,uy=float(p[0]-q[0]),float(p[1]-q[1]); vx,vy=float(r[0]-q[0]),float(r[1]-q[1])
    return math.atan2(abs(ux*vy-uy*vx),ux*vx+uy*vy)
def check():
    n=0; error=0.0
    for q,o,r in configurations():
        a=[angle(q[(i-1)%4],q[i],q[(i+1)%4]) for i in range(4)]
        for i in (0,1):
            e=abs(a[i]+a[i+2]-math.pi); error=max(error,e)
            if e>1e-12: raise RuntimeError('independent angle sum failed')
        n+=1
    return dict(configurations=n,opposite_pairs=2*n,max_absolute_radian_error=error,tolerance=1e-12)
if __name__=='__main__': print(check())
