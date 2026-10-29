"""Independent finite checks; midpoint/cross-product oracle, not a general proof."""
from fractions import Fraction as Q
from itertools import combinations
import json
import geometry as g

def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def sgn(x):return (x>0)-(x<0)
def oracle(o,a,b):
    u=(b[0]-a[0],b[1]-a[1]);v=(o[0]-a[0],o[1]-a[1])
    length=u[0]**2+u[1]**2
    distance=(u[0]*v[1]-u[1]*v[0])**2/length
    mid=((a[0]+b[0])/2,(a[1]+b[1])/2)
    return length,distance,mid
counts=dict(chords=0,comparisons=0,reversals=0,nearest_decompositions=0,tamper_rejections=0,invalid_rejections=0,angle_configurations=0)
unit=[(Q(1),Q(0)),(Q(-1),Q(0)),(Q(0),Q(1)),(Q(0),Q(-1))]
unit += [(Q(sx*x,5),Q(sy*y,5)) for x,y in [(3,4),(4,3)] for sx in [-1,1] for sy in [-1,1]]
for radius in [Q(2),Q(7,2),Q(11,3)]:
 for center in [(Q(0),Q(0)),(Q(7,3),Q(-5,2)),(Q(-3),Q(8))]:
    c=g.Circle(center,radius)
    pts=[(center[0]+radius*x,center[1]+radius*y) for x,y in unit]
    rows=[]
    for a,b in combinations(pts,2):
      length,distance,mid=oracle(center,a,b);q=g.chord(c,a,b);counts['chords']+=1
      require(q['length2']==length and q['distance2']==distance and q['foot']==mid,'independent chord mismatch')
      require(q['projection_parameter']==Q(1,2) and length+4*distance==4*radius**2,'invariant')
      require(q['diameter']==(length==4*radius**2),'maximum equality')
      require(g.validate(c,q),'valid rejected')
      rev=g.chord(c,b,a);counts['reversals']+=1
      require(rev['length2']==length and rev['distance2']==distance and rev['foot']==mid,'reverse')
      u=(b[0]-a[0],b[1]-a[1])
      for t in [Q(-3),Q(-1,3),Q(0),Q(1,4),Q(4)]:
        x=(mid[0]+t*u[0],mid[1]+t*u[1]);counts['nearest_decompositions']+=1
        require((x[0]-center[0])**2+(x[1]-center[1])**2==distance+t*t*length,'nearest')
      mutations=[]
      for field in ['length2','distance2','half_length2','radius2','projection_parameter']:
        bad=dict(q);bad[field]+=1;mutations.append(bad)
      for field in ['a','b','foot']:
        bad=dict(q);bad[field]=(q[field][0]+1,q[field][1]);mutations.append(bad)
      bad=dict(q);bad['diameter']=not bad['diameter'];mutations.append(bad)
      bad=dict(q);bad['distance2']=float(q['distance2']);mutations.append(bad)
      bad=dict(q);del bad['foot'];mutations.append(bad)
      bad=dict(q);bad['extra']=0;mutations.append(bad)
      for bad in mutations:
        counts['tamper_rejections']+=1;require(not g.validate(c,bad),'tamper accepted')
      rows.append((a,b,length,distance))
    for a,b,l1,d1 in rows:
     for d,e,l2,d2 in rows:
      result=g.compare(c,a,b,d,e);counts['comparisons']+=1
      require(result['length_order']==sgn(l1-l2) and result['distance_order']==sgn(d1-d2),'order mismatch')
      require(result['order_reversal_holds'] and result['first_within_diameter'] and result['second_within_diameter'],'theorem flag')
      require(l1-l2==4*(d2-d1),'difference identity')
# Explicit geometric gap check: rational radii and points, independent of geometry module.
for r in [Q(1),Q(5),Q(13)]:
 for a,b in [(Q(3,5)*r,Q(4,5)*r),(Q(5,13)*r,Q(12,13)*r),(Q(7,25)*r,Q(24,25)*r)]:
    # Here both distances have rational complementary heights.
    w2=r*r-a*a;v2=r*r-b*b;p2=a*a*v2/(b*b)
    require(0<a<b<r and 0<p2<w2,'angle point order')
    require((a/b)**2*r*r<r*r,'intersection inside radial segment')
    counts['angle_configurations']+=1
c=g.Circle((0,0),5)
bad_calls=[lambda:g.Circle((0,0),0),lambda:g.Circle((0,0),-1),lambda:g.Circle((0,0),True),lambda:g.Circle((0,0),5.0),lambda:g.Circle((False,0),5),lambda:g.Circle((0,),5),lambda:g.Circle('xx',5),lambda:g.chord(c,(5,0),(5,0)),lambda:g.chord(c,(0,0),(5,0)),lambda:g.chord(c,(5.0,0),(-5,0)),lambda:g.chord(c,(True,0),(-5,0)),lambda:g.chord(c,(5,0,0),(-5,0)),lambda:g.chord(None,(5,0),(-5,0)),lambda:g.compare(c,(5,0),(-5,0),(1,0),(2,0)),lambda:g.Circle((0,0),'5')]
for call in bad_calls:
 try:call()
 except ValueError:counts['invalid_rejections']+=1
 else:raise RuntimeError('invalid accepted')
print(json.dumps(counts,sort_keys=True));print('PASS: finite independent oracle, not a general proof')
