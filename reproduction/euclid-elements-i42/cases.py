from fractions import Fraction as Q
from geometry import add,scale

def example(x=1): return {'A':(1,3),'B':(0,0),'C':(4,0),'u':(x,1)}
def valid_cases():
    for reverse in [False,True]:
      for h in [-3,Q(1,2),4]:
       for ax in [-5,0,2,8]:
        for ux in [-3,0,Q(1,100),2,100]:
         B=(Q(-2),Q(1)); C=(Q(4),Q(1))
         if reverse: B,C=C,B
         yield {'A':(Q(ax),1+h),'B':B,'C':C,'u':(Q(ux),Q(1 if h>0 else -1))}
    # Inclined base: invertible affine maps preserve the algebraic construction.
    for shear in [-2,Q(1,2),3]:
      for ux in [-2,0,2]:
       p=example(ux)
       def T(v): return (Q(v[0])+shear*Q(v[1]),Q(v[0])+ (shear+1)*Q(v[1]))
       yield {k:T(v) for k,v in p.items()}
def invalid_cases():
    for name,key,value in [('collinear','A',(1,0)),('equal base endpoints','C',(0,0)),('zero vector','u',(0,0)),('straight angle','u',(-1,0)),('zero angle','u',(1,0)),('wrong side','u',(1,-1)),('float coordinate','A',(1.,3)),('boolean coordinate','u',(True,1)),('string coordinate','B',('0',0)),('wrong dimension','C',(4,0,0))]:
      p=example();p[key]=value;yield name,p
    p=example();p['extra']=0;yield 'extra field',p
    p=example();del p['u'];yield 'missing field',p
