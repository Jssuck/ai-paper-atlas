"""III.18 pedagogical rational certificates, not a general theorem prover."""
from fractions import Fraction as F
from itertools import product

def scalar(x):
    if isinstance(x,bool) or not isinstance(x,(int,F)): raise ValueError('int or Fraction required')
    return F(x)
def point(p):
    if not isinstance(p,(list,tuple)) or len(p)!=2: raise ValueError('two coordinates required')
    return tuple(map(scalar,p))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(t,a): return tuple(t*x for x in a)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def data(o,b,r,v):
    o,b,v=point(o),point(b),point(v);r=scalar(r)
    if r<=0: raise ValueError('positive radius required')
    if dot(v,v)==0: raise ValueError('nonzero direction required')
    u=sub(b,o)
    if dot(u,u)!=r*r: raise ValueError('B must lie on circle')
    return o,b,r,v,u

def certify(o,b,r,v):
    o,b,r,v,u=data(o,b,r,v);s=dot(v,v);q=dot(u,v);t=-q/s;h=add(b,mul(t,v))
    return dict(o=o,b=b,r=r,v=v,q=q,s=s,t=t,h=h,power=dot(sub(h,o),sub(h,o))-r*r,kind='tangent' if q==0 else 'interior_witness')

def verify(c):
    """Check coordinates/equalities independently of certify; exact field shape."""
    try:
        if not isinstance(c,dict) or set(c)!={'o','b','r','v','q','s','t','h','power','kind'}: return False
        o,b,r,v,u=data(c['o'],c['b'],c['r'],c['v']);h=point(c['h'])
        q,s,t,p=(scalar(c[k]) for k in ('q','s','t','power'))
        if q!=dot(u,v) or s!=dot(v,v) or h!=add(b,mul(t,v)): return False
        if dot(sub(h,o),v)!=0 or p!=dot(sub(h,o),sub(h,o))-r*r: return False
        if q==0: return c['kind']=='tangent' and t==0 and h==b and p==0
        return c['kind']=='interior_witness' and p<0 and t!=0 and p*s==-q*q
    except (ValueError,TypeError,KeyError): return False

def line_power(c,t):
    t=scalar(t);x=add(c['b'],mul(t,c['v']));return dot(sub(x,c['o']),sub(x,c['o']))-c['r']**2

def grid():
    n=tan=interior=powers=0
    axes=[(F(1),F(0)),(F(0),F(1)),(F(3,5),F(4,5)),(F(-3,5),F(4,5))]
    for o,r,u,a,k in product([(0,0),(2,-3),(F(1,2),F(-2,3))],[1,3,F(5,2)],axes,[-2,-1,0,1,2],[1,2]):
        b=add(o,mul(r,u));v=add(mul(a,u),mul(k,(-u[1],u[0])));c=certify(o,b,r,v)
        if not verify(c):raise RuntimeError('grid certificate rejected')
        n+=1;tan+=c['kind']=='tangent';interior+=c['kind']=='interior_witness'
        for t in [-2,-1,0,1,2]:
            if line_power(c,t)!=2*c['q']*t+c['s']*t*t:raise RuntimeError('power mismatch')
            powers+=1
    return dict(configurations=n,tangent=tan,interior_witness=interior,power_checks=powers)
