"""Independent finite checker: integer lattice circles, cyclic order oracle.
Does not call geometry.unit/make_arc or its vector helper functions.
"""
import sys, json, hashlib, platform, math
from pathlib import Path
from fractions import Fraction as F
from functools import cmp_to_key
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from geometry import Arc


def require(ok,msg):
    if not ok: raise RuntimeError(msg)


def cmp(a,b):
    ha=0 if a[1]>0 or (a[1]==0 and a[0]>0) else 1
    hb=0 if b[1]>0 or (b[1]==0 and b[0]>0) else 1
    if ha!=hb: return -1 if ha<hb else 1
    c=a[0]*b[1]-a[1]*b[0]
    return -1 if c>0 else 1 if c<0 else 0


def image(p): return (10-p[1],-7-p[0])
def sq(a,b):return sum((a[i]-b[i])**2 for i in range(2))


def run():
    counts=dict(lattice_points=0,arcs=0,membership=0,inscribed=0,maps=0,distance=0,negative_controls=0,invalid_inputs=0)
    for r in (5,13,25):
        pts=sorted([(x,y) for x in range(-r,r+1) for y in range(-r,r+1) if x*x+y*y==r*r],key=cmp_to_key(cmp))
        counts['lattice_points']+=len(pts)
        n=len(pts)
        for i,b in enumerate(pts):
            for j,c in enumerate(pts):
                if i==j:continue
                for ccw in (True,False):
                    a=Arc((0,0),r,b,c,ccw)
                    target=Arc((10,-7),r,image(b),image(c),not ccw)
                    counts['arcs']+=1
                    require(a.congruent_to(target),'reflected arcs not congruent')
                    cosine=1-F(sq(b,c),2*r*r)
                    require(a.sweep_key()[1]==cosine,'chord cosine mismatch')
                    for k,p in enumerate(pts):
                        # Cyclic rank oracle, not the implementation's cross-product branches.
                        start,end=(i,j) if ccw else (j,i)
                        inside=0<(k-start)%n<(end-start)%n
                        require(a.contains_open(p)==inside,'cyclic membership mismatch')
                        counts['membership']+=1
                        q=a.map_point_to(target,p)
                        require(q==image(p),'explicit reflection mismatch')
                        require(sq(p,b)==sq(q,image(b)),'distance mismatch')
                        counts['maps']+=1;counts['distance']+=1
                        if k in (i,j) or inside: continue
                        area2=abs(b[0]*(c[1]-p[1])+c[0]*(p[1]-b[1])+p[0]*(b[1]-c[1]))
                        # Law of cosines + sine via triangle area; exact cot(angle at p).
                        expected=F(sq(p,b)+sq(p,c)-sq(b,c),2*area2)
                        require(a.inscribed_cot(p)==expected,'triangle-law cot mismatch')
                        require(a.half_sweep_cot()==expected,'half-sweep cot mismatch')
                        require(target.inscribed_cot(image(p))==expected,'reflection angle mismatch')
                        counts['inscribed']+=1
                    doubled=Arc((0,0),2*r,tuple(2*x for x in b),tuple(2*x for x in c),ccw)
                    require(not a.congruent_to(doubled) and a.half_sweep_cot()==doubled.half_sweep_cot(),'scale negative control')
                    counts['negative_controls']+=1
    a=Arc((0,0),5,(5,0),(0,5))
    bad=[lambda:Arc((0,0),True,(1,0),(0,1)),lambda:Arc((0,0),5.0,(5,0),(0,5)),lambda:Arc((0,0),5,(5,0),(0.0,5)),lambda:Arc((0,0),5,(5,0),(0,5),1),lambda:a.inscribed_cot((5,0)),lambda:a.inscribed_cot((3,4)),lambda:a.inscribed_cot((0,0)),lambda:a.contains_open((True,0)),lambda:a.map_point_to(a,(0.5,1)),lambda:Arc((0,0),0,(0,0),(0,0)),lambda:Arc((0,0),5,(5,0),(5,0)),lambda:a.congruent_to(None)]
    for fn in bad:
        try:fn()
        except (TypeError,ValueError):counts['invalid_inputs']+=1
        else:raise RuntimeError('invalid input accepted')
    # Same ordinary angle at center vs circumference is not a valid mixed comparison.
    central=Arc((0,0),5,(5,0),(0,5))
    inscribed=Arc((0,0),5,(5,0),(-5,0))
    require(central.sweep_key()!=inscribed.sweep_key(),'mixed type control')
    counts['negative_controls']+=1
    return dict(result='PASS',timestamp_utc=datetime.now(timezone.utc).isoformat(),python=sys.version,optimization=sys.flags.optimize,counts=counts,production_sha256=hashlib.sha256((ROOT/'geometry.py').read_bytes()).hexdigest(),scope='finite exact rational integer-lattice tests; independent enumeration and cyclic-order oracle; no general formal proof or remote validation')

if __name__=='__main__':print(json.dumps(run(),indent=2))
