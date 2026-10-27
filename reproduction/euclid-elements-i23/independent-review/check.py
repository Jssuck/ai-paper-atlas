"""Independent squared-distance reconstruction from certificate coordinates."""
import sys,json,copy,itertools,hashlib
from pathlib import Path
from fractions import Fraction as Q
repo=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(repo))
from geometry import construct,verify

def plus(a,b): return (a[0]+b[0],a[1]+b[1])
def minus(a,b):return (a[0]-b[0],a[1]-b[1])
def times(a,b,d):return (a[0]*b[0]+d*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def point(c,k):return [(Q(a),Q(b)) for a,b in zip(c[k]['constant'],c[k]['sqrt_coefficient'])]
def delta(p,q):return [minus(a,b) for a,b in zip(p,q)]
def dist2(p,q,d):
    z=delta(p,q);return plus(times(z[0],z[0],d),times(z[1],z[1],d))
def rational_point(p):return [(Q(x),Q(0)) for x in p]
def euclidean2(p,q):return sum((Q(x)-Q(y))**2 for x,y in zip(p,q))
vec=[v for v in itertools.product(range(-2,3),repeat=2) if v!=(0,0)]
targets=[((0,0),(1,0)),((Q(1,3),-2),(Q(4,3),1)),((0,0),(-2,3))]
n=0
for u,v in itertools.product(vec,repeat=2):
    X=v[0]*u[1]-v[1]*u[0]
    if not X:continue
    for A,B in targets:
        for side in (-1,1):
            args=((0,0),u,v,A,B,side);c=construct(*args);d=Q(c['radicand']); F,G=point(c,'F'),point(c,'G');AA=rational_point(A)
            if not d>0:raise RuntimeError('root sign')
            for p,q,r,s in [(F,AA,u,(0,0)),(G,AA,v,(0,0)),(F,G,u,v)]:
                if dist2(p,q,d)!=(euclidean2(r,s),0):raise RuntimeError('independent distance failure')
            af,ag=delta(F,AA),delta(G,AA)
            area=minus(times(ag[0],af[1],d),times(ag[1],af[0],d))
            if area!=(side*abs(X),0):raise RuntimeError('side failure')
            # AG is positive multiple of B-A: its rational part vanishes,
            # radical coefficient is exactly B-A, root strictly positive.
            if any(ag[i]!=(0,Q(B[i])-Q(A[i])) for i in range(2)):raise RuntimeError('positive ray failure')
            if not verify(c,*args):raise RuntimeError('self certificate rejected')
            n+=1
base=((0,0),(2,0),(1,2),(1,-1),(4,3),1);cert=construct(*base)
mutants=[]
for key,new in [('schema_version',True),('side',True),('ordinary_angle_preserved',1),('signed_orientation_preserved',0),('radicand',5.0),('source_cross',True)]:
    x=copy.deepcopy(cert);x[key]=new;mutants.append(x)
for node in ['F','G']:
    for field in ['constant','sqrt_coefficient']:
        for i in range(2):
            x=copy.deepcopy(cert);x[node][field][i]=str(Q(x[node][field][i])+1);mutants.append(x)
for key in cert['checks']:
    x=copy.deepcopy(cert);x['checks'][key]=str(Q(x['checks'][key])+1);mutants.append(x)
x=copy.deepcopy(cert);x['new']=None;mutants.append(x)
x=copy.deepcopy(cert);del x['input'];mutants.append(x)
for x in mutants:
    if verify(x,*base):raise RuntimeError('tampered certificate accepted')
if verify(cert,*base[:-1],-1):raise RuntimeError('side input unbound')
changed=list(base);changed[3]=(2,-1)
if verify(cert,*changed):raise RuntimeError('position input unbound')
print(json.dumps({'method':'independent Q(sqrt(d)) coordinate arithmetic; no use of geometry dot/cross/sub or supplied checks for geometric truth','positive_cases':n,'tampered_certificates_rejected':len(mutants),'input_rebinding_rejections':2,'finite_check_not_general_proof':True,'geometry_sha256':hashlib.sha256((repo/'geometry.py').read_bytes()).hexdigest()},indent=2))
