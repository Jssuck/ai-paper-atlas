"""III.19: exact rational line-through-centre certificates; not a proof assistant."""
from fractions import Fraction as F

def scalar(x):
    if type(x) not in (int,F): raise ValueError('exact int or Fraction required')
    return F(x)
def point(x):
    if type(x) not in (tuple,list) or len(x)!=2: raise ValueError('two coordinates required')
    return tuple(scalar(t) for t in x)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(k,a): return tuple(k*x for x in a)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def inputs(o,c,r,v,w):
    o,c,v,w=map(point,(o,c,v,w));r=scalar(r);a=sub(c,o)
    if r<=0: raise ValueError('positive radius required')
    if dot(a,a)!=r*r: raise ValueError('contact must be on circle')
    if dot(v,v)==0 or dot(w,w)==0: raise ValueError('nonzero directions required')
    # Given the on-circle premise, P(C+t v)=s*t*t+2*q*t.
    # Absence of interior points for every real t is equivalent to q=0
    # by the general proof in the article (not finite sampling).
    if dot(a,v)!=0: raise ValueError('line has a strict interior point; not tangent')
    if dot(w,v)!=0: raise ValueError('candidate is not perpendicular to tangent')
    return o,c,r,v,w

def certify(o,c,r,v,w):
    o,c,r,v,w=inputs(o,c,r,v,w)
    t=dot(sub(o,c),w)/dot(w,w)
    return {'t':t,'centre_on_line':add(c,mul(t,w)),
            'tangent_power_coefficient':dot(v,v),
            'normal_norm2':dot(w,w),'ray_reaches_centre':t>=0}

def verify(o,c,r,v,w,cert):
    try:
        o,c,r,v,w=inputs(o,c,r,v,w)
        if type(cert)!=dict or set(cert)!={'t','centre_on_line','tangent_power_coefficient','normal_norm2','ray_reaches_centre'}:return False
        t=scalar(cert['t']);h=point(cert['centre_on_line'])
        s=scalar(cert['tangent_power_coefficient']);n=scalar(cert['normal_norm2'])
        if type(cert['ray_reaches_centre']) is not bool:return False
        # Check geometry directly without calling the constructor.
        return (h==o and add(c,mul(t,w))==o and det(sub(o,c),w)==0
                and s==dot(v,v)>0 and n==dot(w,w)>0
                and cert['ray_reaches_centre']==(t>=0) and t!=0)
    except (ValueError,TypeError,KeyError,ZeroDivisionError):return False

def grid():
    count=inward=outward=powers=0
    for o in [(0,0),(2,-3),(F(1,3),F(-2,5))]:
      for r in [F(1),F(3),F(5,2)]:
       for u in [(F(1),F(0)),(F(0),F(1)),(F(3,5),F(4,5)),(F(-4,5),F(3,5))]:
        c=add(o,mul(r,u));perp=(-u[1],u[0])
        for k in [F(-2),F(1,2),F(3)]:
         for j in [F(-3),F(-1,2),F(1),F(5,2)]:
          v=mul(k,perp);w=mul(j,u);cert=certify(o,c,r,v,w)
          if not verify(o,c,r,v,w,cert):raise RuntimeError('bad certificate')
          count+=1;inward+=cert['ray_reaches_centre'];outward+=not cert['ray_reaches_centre']
          for t in [F(-2),F(-1,3),F(0),F(2,5),F(3)]:
           z=sub(add(c,mul(t,v)),o)
           if dot(z,z)-r*r!=dot(v,v)*t*t:raise RuntimeError('power mismatch')
           powers+=1
    return dict(configurations=count,inward_rays=inward,outward_rays=outward,power_values=powers)
