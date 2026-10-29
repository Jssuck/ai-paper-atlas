"""Independent finite review: different geometric oracle, no production assertions."""
from fractions import Fraction as F
from itertools import permutations
from geometry import classify, rational_intersections, same_circle_from_three

def require(ok, message):
    if not ok: raise RuntimeError(message)

def norm2(p, o):
    return (p[0]-o[0])**2+(p[1]-o[1])**2

def distance_oracle(dx,dy,r,s):
    # Uses squared center-distance versus sums/differences of actual integer radii.
    d=dx*dx+dy*dy
    if d==0: return None if r==s else 0
    if d>(r+s)**2 or d<(r-s)**2: return 0
    if d==(r+s)**2 or d==(r-s)**2: return 1
    return 2

counts={'distance_oracle_cases':0,'rational_points_backsubstituted':0,
        'constructed_common_chords':0,'three_point_permutations':0,'invalid_inputs':0}
for dx in range(-8,9):
 for dy in range(-8,9):
  for r in range(1,7):
   for s in range(1,7):
    expected=distance_oracle(dx,dy,r,s)
    got=classify((0,0),r*r,(dx,dy),s*s)
    require(got['count']==expected,'independent distance oracle mismatch')
    require(classify((dx,dy),s*s,(0,0),r*r)['count']==expected,'swap mismatch')
    pts=rational_intersections((0,0),r*r,(dx,dy),s*s)
    if pts is not None:
     require(len(set(pts))==expected,'point count mismatch')
     for p in pts:
      require(norm2(p,(0,0))==r*r and norm2(p,(dx,dy))==s*s,'back-substitution')
      counts['rational_points_backsubstituted']+=1
    counts['distance_oracle_cases']+=1
# Construct two common endpoints first, then circles with centers on their bisector.
for h in [F(1,3),F(1),F(7,2)]:
 for cx in range(-3,4):
  for cy in range(-3,4):
   for k in [F(-2),F(1,2),F(3)]:
    p,q=(F(cx),F(cy)+h),(F(cx),F(cy)-h)
    a,b=(F(cx)-1,F(cy)),(F(cx)+k,F(cy))
    R,S=1+h*h,k*k+h*h
    require(set(rational_intersections(a,R,b,S))=={p,q},'constructed chord mismatch')
    counts['constructed_common_chords']+=1
for seq in permutations([(F(3),F(4)),(F(3),F(-4)),(F(-5),F(0))]):
 result=same_circle_from_three(seq,(0,0),25,(0,0),25)
 require(result['equal_centers'] and result['equal_squared_radii'],'three point certificate')
 counts['three_point_permutations']+=1
for value in [True,False,1.0,float('inf'),float('nan'),None,{},[],complex(1,0),'1/0','bad']:
 for target in ['center','radius']:
  try:
   if target=='center':classify((value,0),1,(1,0),1)
   else:classify((0,0),value,(1,0),1)
  except ValueError:counts['invalid_inputs']+=1
  else:raise RuntimeError('invalid input accepted')
# Non-square rational discriminant must not be rounded into an exact point.
require(classify((0,0),1,(1,1),1)['count']==2,'irrational diagonal count')
# This diagonal case is rational; explicit expected roots check representation.
require(set(rational_intersections((0,0),1,(1,1),1))=={(F(1),F(0)),(F(0),F(1))},'diagonal roots')
require(rational_intersections((0,0),1,(1,0),1) is None,'irrational roots rounded')
import json
print(json.dumps({'result':'PASS','counts':counts,'scope':'finite independent checks; not a general proof'},indent=2))
