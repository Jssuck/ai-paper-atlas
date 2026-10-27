"""Deterministic finite checks, with exact Q(sqrt(3)) predicates."""
import json
from fractions import Fraction as R
from geometry import *

def examples():
    values=[R(1,3),R(1,2),R(2,3),R(1),R(3,2),R(2),R(3),R(5)]
    count=0
    for u in values:
      for v in values:
       for shift in [point(0,0),point(2,-3),point(R(1,3),R(2,5))]:
        for quarter_turns in range(4):
         for swap in [False,True]:
          a,d,e=canonical(u,v)
          for _ in range(quarter_turns): a,d,e=rotate(a),rotate(d),rotate(e)
          a,d,e=add(a,shift),add(d,shift),add(e,shift)
          if swap: d,e=e,d
          f=construct(a,d,e)
          if not all(certificate(a,d,e,f).values()): raise RuntimeError('positive certificate failed')
          count+=1
    branches={}
    for name,u,v in [('same_side_internal',Q3(2),Q3(1)),('same_side_zero',S,Q3(1)),('same_side_external',Q3(1),Q3(1))]:
        a,d,e=canonical(u,v)
        f=point(u-S*v,0)
        branches[name]={'F':[str(x) for x in f],'checks':certificate(a,d,e,f)}
    a,d,e=canonical(1,1); f=construct(a,d,e)
    bad={
      'outward_ray':certificate(a,d,e,scale(-1,f)),
      'unequal_cuts':certificate(a,d,scale(2,e),f),
      'coincident_cuts':certificate(a,d,d,f),
      'collinear_angle':certificate(a,point(1,0),point(-1,0),point(0,1)),
      'arbitrary_point':certificate(a,d,e,point(3,1)),
    }
    if any(all(x.values()) for x in bad.values()): raise RuntimeError('bad certificate accepted')
    return {'positive_certificates':count,'canonical_parameter_pairs':len(values)**2,
      'translations':3,'quarter_turns':4,'endpoint_orders':2,
      'same_side_branch_cases':branches,'additional_rejected_certificates':bad,
      'scope':'finite exact teaching checks, not a proof of the general theorem'}

if __name__=='__main__': print(json.dumps(examples(),ensure_ascii=False,indent=2))
