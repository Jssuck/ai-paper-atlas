"""Independent finite audit of the II.4 certificate contract; not a theorem prover.
No use of construct() for positive inputs. Explicit checks survive -O/-OO.
"""
from fractions import Fraction as F
from copy import deepcopy
import json
import geometry as g

COUNTS={'valid_certificates':0,'area_comparisons':0,'rejected_mutations':0,'rejected_inputs':0}
BOUNDARIES={'whole':('A','D','E','B'),'HF':('H','D','F','G'),'CK':('C','G','K','B'),'AG':('A','H','G','C'),'GE':('G','F','E','K')}
def check(condition,message):
    if not condition: raise RuntimeError(message)
def independent(A,u,v,t):
    # Geometric intersections from the two endpoint sides, not author constructor.
    B=tuple(A[i]+u[i] for i in range(2)); D=tuple(A[i]+v[i] for i in range(2))
    E=tuple(B[i]+v[i] for i in range(2))
    C=tuple(A[i]+t*u[i] for i in range(2)); Fp=tuple(D[i]+t*u[i] for i in range(2))
    # Parameter of G measured from D toward B is t.
    G=tuple(D[i]+t*(B[i]-D[i]) for i in range(2))
    H=tuple(G[i]-t*u[i] for i in range(2)); K=tuple(H[i]+u[i] for i in range(2))
    return {'points':dict(A=A,B=B,D=D,E=E,C=C,F=Fp,G=G,H=H,K=K),'regions':deepcopy(BOUNDARIES)}
def reject(cert,args,key):
    try:g.verify(cert,*args)
    except ValueError:COUNTS[key]+=1
    else:raise RuntimeError('bad certificate/input accepted')

def run():
    # 5 independent directions, 3 scales, 2 orientations, 2 shifts, 4 cuts.
    for p,q in [(1,0),(0,1),(2,3),(-4,1),(F(1,3),F(-2,7))]:
      for scale in [F(1,5),F(1),F(7,3)]:
       u=(scale*p,scale*q)
       for orientation in [-1,1]:
        v=(-orientation*u[1],orientation*u[0])
        for A in [(F(0),F(0)),(F(-7,11),F(4,9))]:
         for t in [F(1,13),F(2,5),F(1,2),F(12,13)]:
          args=(A,u,v,t); cert=independent(*args); got=g.verify(cert,*args)
          length2=u[0]**2+u[1]**2
          oracle={'whole':length2,'HF':length2*t*t,'CK':length2*(1-t)**2,'AG':length2*t*(1-t),'GE':length2*t*(1-t)}
          for key in oracle:
              check(got[key]==oracle[key],key+' independent area mismatch');COUNTS['area_comparisons']+=1
              check(type(got[key]) is F,'area should be exact Fraction')
          COUNTS['valid_certificates']+=1
          # Move each named vertex in both independent coordinate directions.
          for name in cert['points']:
           for axis in [0,1]:
            bad=deepcopy(cert); xyz=list(bad['points'][name]);xyz[axis]+=F(1,17);bad['points'][name]=tuple(xyz)
            reject(bad,args,'rejected_mutations')
          for region in BOUNDARIES:
           bad=deepcopy(cert); bad['regions'][region]=tuple(reversed(BOUNDARIES[region]));reject(bad,args,'rejected_mutations')
          # Area-preserving whole shift is not the certificate for the specified A.
          bad=deepcopy(cert);bad['points']={k:(xy[0]+1,xy[1]-2) for k,xy in bad['points'].items()};reject(bad,args,'rejected_mutations')
          # Missing/extra point names and replaced complementary block.
          bad=deepcopy(cert);del bad['points']['G'];reject(bad,args,'rejected_mutations')
          bad=deepcopy(cert);bad['points']['X']=(0,0);reject(bad,args,'rejected_mutations')
          bad=deepcopy(cert);bad['regions']['GE']=BOUNDARIES['AG'];reject(bad,args,'rejected_mutations')
    args=((0,0),(5,0),(0,5),F(2,5));cert=independent(*args)
    for t in [0,1,-1,2,F(-1,100),F(101,100),.4,True,'2/5',None]:reject(cert,(*args[:3],t),'rejected_inputs')
    for u,v in [((0,0),(0,0)),((5,0),(0,4)),((5,0),(3,4)),((5,0),(5,0)),((5,0),(0,0)),((True,0),(0,1)),((5.0,0),(0,5)),(('5',0),(0,5))]:reject(cert,(args[0],u,v,args[3]),'rejected_inputs')
    for A in [None,'00',(0,),[0,0,0],(False,0),(0,.0)]:reject(cert,(A,*args[1:]),'rejected_inputs')
    for bad in [None,[],{},dict(points={}),dict(points=cert['points'],regions=cert['regions'],extra=1)]:reject(bad,args,'rejected_inputs')
    for value in [None,(),(0,),[0,0,0],(True,0),(0.0,0),('0',0)]:
        bad=deepcopy(cert);bad['points']['G']=value;reject(bad,args,'rejected_inputs')
    # A moved horizontal cut still covers the outer square, but is not II.4.
    bad=deepcopy(cert)
    for name in ['G','H','K']:
        x,y=bad['points'][name];bad['points'][name]=(x,F(2))
    reject(bad,args,'rejected_inputs')
    # Certificate regions require the documented canonical ordered tuples.
    for region in BOUNDARIES:
        bad=deepcopy(cert);ns=bad['regions'][region];bad['regions'][region]=ns[1:]+ns[:1];reject(bad,args,'rejected_inputs')
    print(json.dumps({'result':'passed','scope':'finite independent coordinate and mutation audit; not general proof',**COUNTS},sort_keys=True))
if __name__=='__main__':run()
