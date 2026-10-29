"""Independent III.8 finite checks; no theorem-proof claim."""
from fractions import Fraction as F
import json
from geometry import certificate, secant, equal_shell

def need(b, message):
    if not b: raise RuntimeError(message)

counts={'circle_points':0,'near_internal_pairs':0,'distance_shells':0,'same_ray_pairs':0}
for r in (F(1),F(7,3),F(9,2)):
  for ratio in (F(11,10),F(7,4),F(5)):
    d=r*ratio; near=[]
    for m in range(-20,21):
      for n in (3,7,11):
        # Homogeneous rational-circle parametrization, independent of sample/grid.
        P=(r*F(n*n-m*m,n*n+m*m),r*F(2*m*n,n*n+m*m))
        x,y=P; square=(d-x)*(d-x)+y*y
        c=certificate(r,d,P)
        need(c['squared_distance']==square,'distance oracle')
        need((d-r)**2<=square<=(d+r)**2,'extrema')
        # Roots are verified by substituting into circle equation, rather than verify().
        s=secant(r,d,P)
        for t,Q in zip(s['parameters'],s['points']):
          need(t>0 and Q==(d+t*(x-d),t*y),'positive-ray parameter')
          need(sum(z*z for z in Q)==r*r,'circle substitution')
        low,high=s['squared_lengths']
        need(low<=d*d-r*r<=high,'branch length separation')
        need(low*high==(d*d-r*r)**2,'product identity')
        need(c['branch']==('near' if square<d*d-r*r else 'far' if square>d*d-r*r else 'tangent'),'independent branch oracle')
        counts['circle_points']+=1;counts['same_ray_pairs']+=1
        if y>0 and square<d*d-r*r:near.append(P)
    near=sorted(set(near),key=lambda p:-p[0])
    for K,L in zip(near,near[1:]):
      a=K[1]/L[1];b=(K[0]-a*L[0])/d
      need(a>0 and b>0 and 1-a-b>0,'I.21 interior coefficients')
      counts['near_internal_pairs']+=1
    for k in range(-5,101):
      square=F(k,25)*(d+r)**2
      out=equal_shell(r,d,square)
      expected=0 if square<(d-r)**2 or square>(d+r)**2 else 1 if square in ((d-r)**2,(d+r)**2) else 2
      need(out['count']==expected,'distance-shell interval oracle')
      counts['distance_shells']+=1
# Manuscript's distinct hand example, not merely reproduction's named example.
s=secant(5,13,(4,3))
need(s['parameters']==(F(1),F(8,5)),'hand parameters')
need(s['points'][1]==(F(-7,5),F(24,5)),'hand endpoint')
need(s['squared_lengths']==(F(90),F(1152,5)),'hand distances')
for sign in (-1,1):
 c=certificate(5,13,(F(25,13),sign*F(60,13)))
 need(c['branch']=='tangent' and c['squared_distance']==144 and c['equal_point_count']==2,'tangent counting')
print(json.dumps({'passed':True,'checks':counts,'hand_example':'P=(4,3), Q=(-7/5,24/5), squares 90 and 1152/5','tangent_circle_endpoints':2,'scope':'finite exact independent checks, not general proof'},ensure_ascii=False,indent=2))
