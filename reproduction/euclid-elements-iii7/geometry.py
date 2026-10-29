"""Exact rational teaching model for III.7, not an ancient proof engine."""
from fractions import Fraction as F
import json

def scalar(x):
    if type(x) not in (int,str,F): raise ValueError('exact rational required')
    try:return F(x)
    except (ValueError,ZeroDivisionError):raise ValueError('invalid rational') from None

def point(x):
    if type(x) not in (list,tuple) or len(x)!=2:raise ValueError('point requires two coordinates')
    return tuple(map(scalar,x))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(t,a):return tuple(t*x for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def norm(a):return dot(a,a)
def enc(x):
    if type(x) is F:return str(x)
    if type(x) in (tuple,list):return [enc(v) for v in x]
    if type(x) is dict:return {k:enc(v) for k,v in x.items()}
    return x

def setup(center,radius,offset,axis):
    o,u=point(center),point(axis);r,d=scalar(radius),scalar(offset)
    if not 0<d<r:raise ValueError('require 0 < offset < radius')
    if norm(u)!=1:raise ValueError('axis must be a unit vector')
    return o,r,d,u

def certificate(center,radius,offset,axis,p):
    o,r,d,u=setup(center,radius,offset,axis);p=point(p);v=sub(p,o)
    if norm(v)!=r*r:raise ValueError('point must lie on circumference')
    x=dot(v,u);w=sub(v,mul(x,u))
    if norm(w)==0:raise ValueError('non-extreme point required')
    f=add(o,mul(d,u));a=sub(o,mul(r,u));near=add(o,mul(r,u));h=add(o,sub(mul(2*x,u),v));dist=norm(sub(p,f))
    if not (r-d)**2<dist<(r+d)**2:raise ValueError('strict margin failure')
    return enc({'schema':1,'input':{'center':o,'radius':r,'offset':d,'axis':u,'point':p},'interior_point':f,'farthest':a,'nearest':near,'mirror':h,'projection':x,'distance_squared':dist,'mirror_distance_squared':norm(sub(h,f)),'minimum_squared':(r-d)**2,'maximum_squared':(r+d)**2,'above_minimum':dist-(r-d)**2,'below_maximum':(r+d)**2-dist,'distinct_mirror':p!=h})

def verify(c):
    try:
        if type(c) is not dict or type(c.get('input')) is not dict:return False
        i=c['input'];expected=certificate(i['center'],i['radius'],i['offset'],i['axis'],i['point'])
        return json.dumps(c,sort_keys=True,separators=(',',':'),allow_nan=False)==json.dumps(expected,sort_keys=True,separators=(',',':'))
    except (ValueError,TypeError,KeyError,OverflowError):return False

def compare(center,radius,offset,axis,p,q):
    c=certificate(center,radius,offset,axis,p);e=certificate(center,radius,offset,axis,q)
    o,r,d,u=setup(center,radius,offset,axis);v=sub(point(p),o);w=sub(point(q),o)
    cross=lambda z:u[0]*z[1]-u[1]*z[0]
    if cross(v)*cross(w)<=0:raise ValueError('same open semicircle required')
    if point(p)==point(q):raise ValueError('distinct points required')
    delta=scalar(e['projection'])-scalar(c['projection']);distance_delta=scalar(c['distance_squared'])-scalar(e['distance_squared'])
    if delta==0 or distance_delta!=2*d*delta:raise ValueError('ordering failure')
    return enc({'projection_q_minus_p':delta,'distance_p_squared_minus_q_squared':distance_delta,'p_longer':delta>0})

def circle_point(o,r,u,t):
    o,u=point(o),point(u);r,t=scalar(r),scalar(t);v=(-u[1],u[0]);x=(1-t*t)/(1+t*t);y=2*t/(1+t*t)
    return add(o,mul(r,add(mul(x,u),mul(y,v))))
EXAMPLES={
 'simple':((0,0),5,2,(1,0),(3,4)),
 'upper':((0,0),5,2,(1,0),(-3,4)),
 'lower':((0,0),5,2,(1,0),(3,-4)),
 'near_center':((0,0),5,'1/100',(1,0),(0,5)),
}
# Exact rotated example generated from the same rational parameter, not rounded.
EXAMPLES['rotated']=((1,-2),5,2,('3/5','4/5'),circle_point((1,-2),5,('3/5','4/5'),'1/2'))
def grid():
    for o in [(0,0),(2,-3)]:
      for r in [F(1),F(5),F(7,3)]:
       for ratio in [F(1,5),F(1,2),F(4,5)]:
        for u in [(1,0),(0,1),(F(3,5),F(4,5)),(F(-3,5),F(4,5))]:
         for t in [F(-3),F(-1),F(-1,2),F(1,3),F(1),F(2),F(5)]:
          yield o,r,r*ratio,u,circle_point(o,r,u,t)
