"""Independent finite checks: construct circles from arbitrary points, not ray generation."""
from fractions import Fraction as F
import json
from geometry import Segment

def check(condition, message):
    if not condition:
        raise RuntimeError(message)

def distance2(p,q):
    return (p[0]-q[0])**2+(p[1]-q[1])**2

def cot_from_points(a,b,p):
    u=(a[0]-p[0],a[1]-p[1]);v=(b[0]-p[0],b[1]-p[1])
    return (u[0]*v[0]+u[1]*v[1])/abs(u[0]*v[1]-u[1]*v[0])

def run():
    stats=dict(point_defined_circles=0,placements=0,distance_pairs=0,membership_checks=0,non_similar_pairs=0,text_examples=0,invalid_cases=0)
    # Each (a,x,y) supplies a point on its defining circle. No arc_point call.
    for a in [F(1),F(2),F(5,3)]:
      for x in [F(-3),F(-1),F(0),F(2,3),F(4)]:
       for y in [F(1,3),F(1),F(2),F(7,2)]:
        k=(x*x+y*y-a*a)/(2*y)
        source=Segment(a,k)
        p=(x,y);A=(-a,F(0));B=(a,F(0))
        check(distance2(p,(0,k))==a*a+k*k,'independent circle equation')
        check(cot_from_points(A,B,p)==k/a==source.measured_cot(p),'independent angle')
        stats['point_defined_circles']+=1
        # Explicit orthogonal map, separately written rather than local/world composition.
        for c,s in [(F(1),F(0)),(F(3,5),F(4,5)),(F(-5,13),F(12,13))]:
         for orientation in [-1,1]:
          n=(-orientation*s,orientation*c)
          target=Segment(a,k,(F(7,3),F(-4,5)),(c,s),n)
          def image(z):
            return (F(7,3)+c*z[0]-orientation*s*z[1],F(-4,5)+s*z[0]+orientation*c*z[1])
          check(source.align_point_to(target,p)==image(p),'independent map')
          check(target.measured_cot(image(p))==cot_from_points(image(A),image(B),image(p)),'mapped angle')
          check(source.similar(target) and source.aligned_circle_matches(target),'matching certificate')
          stats['placements']+=1
          for q in [A,B,(F(0),F(0)),(F(-2,3),F(5,4))]:
            check(distance2(p,q)==distance2(image(p),image(q)),'distance preservation')
            stats['distance_pairs']+=1
          for u in [-2,-1,0,1,2]:
           for v in [-2,0,1,3]:
            z=(F(u),F(v));w=image(z)
            center=image((F(0),k))
            signed=(w[0]-F(7,3))*n[0]+(w[1]-F(-4,5))*n[1]
            expected=signed>=0 and distance2(w,center)<=a*a+k*k
            check(expected==source.contains(z)==target.contains(w),'global membership oracle')
            stats['membership_checks']+=1
          unequal=Segment(a,k+F(1,101),target.mid,target.e,target.n)
          check(not source.similar(unequal) and not source.aligned_circle_matches(unequal),'different angles not equated')
          stats['non_similar_pairs']+=1
    # Exact body examples and distinctions.
    s=Segment(2,F(3,2));t=Segment(2,F(3,2),(7,1),(0,1),(-1,0))
    check(s.center==(0,F(3,2)) and s.radius2==F(25,4),'example1 radius')
    check(s.measured_cot((0,4))==F(3,4) and s.align_point_to(t,(0,4))==(3,1),'example1 apex')
    check(t.center==(F(11,2),1) and not s.coincides(t),'example1 position');stats['text_examples']+=1
    h=Segment(2,0);check(h.contains((0,2)) and s.contains((0,2)) and not h.contains((0,4)),'example2 nesting');stats['text_examples']+=1
    big=Segment(4,3);check(s.similar(big) and s.radius2*4==big.radius2,'example3 scaling');stats['text_examples']+=1
    other=Segment(2,F(-3,2),n=(0,-1));mirror=Segment(2,F(3,2),n=(0,-1))
    check(s.center==other.center and not s.similar(other) and s.similar(mirror) and not s.coincides(mirror),'example4 mirror');stats['text_examples']+=1
    check(F(4)-F(1)**2==3 and s.power((1,3))==-3,'example5 noncircle');stats['text_examples']+=1
    invalid=[lambda:Segment(0,0),lambda:Segment(1,0.1),lambda:Segment(1,0,e=(1,1)),lambda:s.measured_cot((2,0)),lambda:s.measured_cot((0,0)),lambda:s.align_point_to(big,(0,0))]
    for fn in invalid:
        try:fn()
        except (ValueError,TypeError):stats['invalid_cases']+=1
        else:raise RuntimeError('invalid accepted')
    return stats
if __name__=='__main__': print(json.dumps(run(),sort_keys=True,indent=2))
