"""Independent finite oracle: midpoint and determinant, not production projection."""
from fractions import Fraction as Q
from itertools import combinations
import json
from geometry import Circle,chord,compare,validate

def require(condition,label):
    if not condition:raise RuntimeError(label)
def sqdist(a,b):return (a[0]-b[0])**2+(a[1]-b[1])**2
def reject(f):
    try:f()
    except (ValueError,TypeError):return
    raise RuntimeError('invalid input accepted')
def run():
    counts=dict(chords=0,comparisons=0,reversals=0,tampers=0,invalid=0,nearest_checks=0)
    # Hand-selected rational unit points, including omitted parametrization direction.
    units=[(Q(1),Q(0)),(Q(-1),Q(0)),(Q(0),Q(1)),(Q(0),Q(-1)),(Q(3,5),Q(4,5)),(Q(-3,5),Q(4,5)),(Q(3,5),Q(-4,5)),(Q(-3,5),Q(-4,5)),(Q(5,13),Q(12,13)),(Q(-5,13),Q(12,13))]
    for center in [(Q(0),Q(0)),(Q(7,3),Q(-9,2)),(Q(-10),Q(17))]:
      for radius in [Q(1,7),Q(5),Q(13,2)]:
        c=Circle(center,radius);pts=[(center[0]+radius*x,center[1]+radius*y) for x,y in units];certs=[]
        for a,b in combinations(pts,2):
          q=chord(c,a,b);mid=((a[0]+b[0])/2,(a[1]+b[1])/2);dx,dy=b[0]-a[0],b[1]-a[1];l2=dx*dx+dy*dy
          # Distance to supporting line from determinant formula, independent of projection.
          det=dx*(center[1]-a[1])-dy*(center[0]-a[0]);d2=det*det/l2
          require(q['foot']==mid and q['projection_parameter']==Q(1,2),'midpoint')
          require(q['distance2']==d2==sqdist(mid,center),'distance')
          require(q['length2']==l2 and q['half_length2']==l2/4,'length')
          require(l2+4*d2==4*radius*radius,'identity')
          require(q['diameter']==(a[0]+b[0]==2*center[0] and a[1]+b[1]==2*center[1]),'diameter')
          require(validate(c,q),'valid certificate');certs.append((a,b,l2,d2));counts['chords']+=1
          rev=chord(c,b,a)
          for key in ['foot','length2','half_length2','distance2','radius2','diameter']:require(rev[key]==q[key],'reversal')
          counts['reversals']+=1
          for t in [Q(-3),Q(-1,7),Q(0),Q(1,7),Q(3)]:
            x=(mid[0]+t*dx,mid[1]+t*dy);require(sqdist(x,center)==d2+t*t*l2,'nearest decomposition');counts['nearest_checks']+=1
          for key in ['projection_parameter','length2','distance2','half_length2','radius2']:
            bad=dict(q);bad[key]+=Q(1,11);require(not validate(c,bad),'numeric tamper');counts['tampers']+=1
          for key in ['a','b','foot']:
            bad=dict(q);bad[key]=(q[key][0]+1,q[key][1]);require(not validate(c,bad),'point tamper');counts['tampers']+=1
          bad=dict(q);bad['diameter']=not q['diameter'];require(not validate(c,bad),'bool tamper');counts['tampers']+=1
          bad=dict(q);bad['radius2']=float(q['radius2']);require(not validate(c,bad),'float certificate');counts['tampers']+=1
          bad=dict(q);del bad['diameter'];require(not validate(c,bad),'missing');counts['tampers']+=1
          bad=dict(q);bad['extra']=1;require(not validate(c,bad),'extra');counts['tampers']+=1
        for a,b,l1,d1 in certs:
          for e,f,l2,d2 in certs:
            q=compare(c,a,b,e,f);require(q['equal_chords']==(l1==l2) and q['equal_distances']==(d1==d2) and q['equivalence_holds'],'comparison');counts['comparisons']+=1
    c=Circle((0,0),5)
    badcalls=[lambda:Circle((0,0),0),lambda:Circle((0,0),-1),lambda:Circle((0,0),True),lambda:Circle((0,0),5.0),lambda:Circle((0,0), '5'),lambda:Circle((0,),5),lambda:Circle((True,0),5),lambda:Circle(None,5),lambda:chord(c,(5,0),(5,0)),lambda:chord(c,(0,0),(5,0)),lambda:chord(c,(6,0),(5,0)),lambda:chord(c,(5.0,0),(-5,0)),lambda:chord(None,(-5,0),(5,0)),lambda:chord(c,(True,0),(5,0)),lambda:chord(c,None,(5,0))]
    for f in badcalls:reject(f);counts['invalid']+=1
    # Both ways the radius assumption matters, with rational radii.
    a=chord(c,(-4,3),(4,3));b=chord(Circle((0,0),4),(-4,0),(4,0));require(a['length2']==b['length2'] and a['distance2']!=b['distance2'],'different radius equal length')
    a=chord(c,(-5,0),(5,0));require(a['distance2']==b['distance2'] and a['length2']!=b['length2'],'different radius equal distance')
    print(json.dumps(counts,sort_keys=True));print('finite independent oracle passed; not a general theorem proof')
if __name__=='__main__':run()
