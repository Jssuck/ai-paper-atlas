"""Independent exact checks; hand-built fixtures do not call sample/transform."""
from fractions import Fraction as Q
from copy import deepcopy
import json
import geometry as g

counts={}
def tick(k,n=1): counts[k]=counts.get(k,0)+n
def require(condition,message):
    if not condition: raise RuntimeError(message)
def norm2(p,q): return (p[0]-q[0])**2+(p[1]-q[1])**2
def independent_map(p,sc,co,si,flip,off):
    x,y=p; x=flip*x
    return (off[0]+sc*(co*x-si*y),off[1]+sc*(si*x+co*y))
def rejects(points):
    try: g.recover_center(*points)
    except (TypeError,ValueError): tick('invalid_recovery_rejected'); return
    raise RuntimeError('invalid recovery accepted')

def run():
    rotations=((1,0,1),(0,1,1),(Q(3,5),Q(4,5),1),(Q(5,13),Q(-12,13),1),(Q(3,5),Q(4,5),-1))
    offsets=((0,0),(7,-11),(Q(-5,7),Q(9,2)))
    scales=(Q(1,7),3,Q(13,2))
    chords=((5,0),(4,3),(4,-3),(3,4),(3,-4))
    for a,t in chords:
      for co,si,flip in rotations:
       for off in offsets:
        for sc in scales:
         M=lambda p:independent_map(p,sc,co,si,flip,off)
         raw=[M((-a,t)),M((a,t)),M((0,5)),M((0,-5))]
         for reverse_ab,reverse_ce in ((False,False),(True,False),(False,True),(True,True)):
          A,B,C,E=raw
          if reverse_ab:A,B=B,A
          if reverse_ce:C,E=E,C
          expected={'A':A,'B':B,'C':C,'E':E,'D':M((0,t)),'F':off,'radius_squared':25*sc*sc,'branch':'diameter' if t==0 else 'non-diameter'}
          require(g.verify_certificate(expected),'hand-built certificate rejected')
          actual=g.recover_center(A,B,C,E)
          require(actual==expected,'recovery differs from independently known answer')
          tick('independent_certificates')
          if t==0:tick('diameter_certificates')
          if flip==-1:tick('genuine_reflection_certificates')
          for P in (A,B,C,E):
           require(norm2(P,off)==25*sc*sc,'independent circle distance failed');tick('independent_radius_comparisons')
          require(tuple((A[i]+B[i])/2 for i in range(2))==expected['D'],'D not midpoint')
          require(tuple((C[i]+E[i])/2 for i in range(2))==off,'F not midpoint')
          require(sum((B[i]-A[i])*(E[i]-C[i]) for i in range(2))==0,'not perpendicular')
          tick('independent_geometry_comparisons',3)
          for key in ('A','B','C','E','D','F'):
           for dim in (0,1):
            bad=deepcopy(expected);p=list(bad[key]);p[dim]+=1;bad[key]=p
            require(not g.verify_certificate(bad),'tampered point accepted');tick('tampered_certificates_rejected')
          for key,value in (('radius_squared',expected['radius_squared']+1),('branch','non-diameter' if t==0 else 'diameter')):
           bad={**expected,key:value};require(not g.verify_certificate(bad),'tampered scalar accepted');tick('tampered_certificates_rejected')
    base=[(-3,4),(3,4),(0,5),(0,-5)]
    invalid_values=(True,False,0.0,float('nan'),float('inf'),None,'0',complex(0),{})
    for index in range(4):
     for dim in (0,1):
      for value in invalid_values:
       p=deepcopy(base);p[index]=list(p[index]);p[index][dim]=value;rejects(p)
    for index in range(4):
     for value in (None,(),(0,),(0,0,0),'00',{'x':0,'y':0},iter([0,0])):
      p=deepcopy(base);p[index]=value;rejects(p)
    for p in ((base[0],base[0],base[2],base[3]),(base[0],base[1],base[2],base[2]),((-1,8),(1,8),(0,5),(0,-5)),((-1,5),(1,5),(0,5),(0,-5)),((-1,0),(1,0),(-2,-2),(2,2)),((-3,4),(3,4),(0,6),(0,-5))):rejects(p)
    cert={'A':base[0],'B':base[1],'C':base[2],'E':base[3],'D':(0,4),'F':(0,0),'radius_squared':25,'branch':'non-diameter'}
    for key in ('A','B','C','E','D','F'):
     for dim in (0,1):
      for value in invalid_values:
       bad=deepcopy(cert);p=list(bad[key]);p[dim]=value;bad[key]=p
       require(not g.verify_certificate(bad),'bad certificate coordinate accepted');tick('malformed_certificates_rejected')
    for value in invalid_values:
     require(not g.verify_certificate({**cert,'radius_squared':value}),'bad radius type accepted');tick('malformed_certificates_rejected')
    for value in (True,False,0,None,[],{},'Diameter',''):
     require(not g.verify_certificate({**cert,'branch':value}),'bad branch accepted');tick('malformed_certificates_rejected')
    for bad in (None,[],{}, {**cert,'extra':0}, {k:v for k,v in cert.items() if k!='F'}):
     require(not g.verify_certificate(bad),'bad schema accepted');tick('malformed_certificates_rejected')
    # A point on the bisector can be equidistant to A,B yet not C,E.
    for y in (-9,-5,-1,Q(1,3),1,4,5,9):
     G=(0,y)
     require(norm2(G,base[0])==norm2(G,base[1]),'AB equality missing')
     require(norm2(G,base[2])!=norm2(G,base[3]),'noncenter on line passed CE equality')
     tick('collinear_noncenter_counterexamples')
    for scale in (Q(1,10**80),10**80):
     off=(10**100,-10**100);P=[independent_map(p,scale,Q(3,5),Q(4,5),-1,off) for p in base]
     R=g.recover_center(*P);require(R['F']==off and R['radius_squared']==25*scale**2,'extreme exact failure');tick('extreme_exact_cases')
    # Explicitly reject interpreting a finite sample as a whole-curve test:
    # no curve input exists, so no empirical claim about unseen curve is tested.
    return counts
if __name__=='__main__': print(json.dumps({'status':'pass','checks':run(),'scope':'Exact rational supplied-point model; not circle-intersection, image recognition, or a general proof.'},ensure_ascii=False,indent=2))
