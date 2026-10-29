"""III.8 exact rational teaching model. Origin-centred circle; D=(d,0)."""
from fractions import Fraction as F
from itertools import product

def q(x):
    if isinstance(x,bool) or not isinstance(x,(int,F)): raise TypeError('integers or Fraction only')
    return F(x)

def domain(r,d):
    r,d=q(r),q(d)
    if not 0<r<d: raise ValueError('requires 0 < radius < external distance')
    return r,d

def point(r,p):
    if len(p)!=2: raise ValueError('point requires two coordinates')
    x,y=map(q,p)
    if x*x+y*y!=r*r: raise ValueError('point is not on circle')
    return x,y

def sample(r,u):
    r,u=q(r),q(u)
    if r<=0: raise ValueError('positive radius required')
    return r*(1-u*u)/(1+u*u),2*r*u/(1+u*u)

def certificate(r,d,p):
    r,d=domain(r,d);x,y=point(r,p)
    dist=(d-x)**2+y*y
    horizon=d*x-r*r
    return {'r':r,'d':d,'point':(x,y),'squared_distance':dist,
            'identity':d*d+r*r-2*d*x,'minimum_squared':(d-r)**2,
            'maximum_squared':(d+r)**2,'branch':'near' if horizon>0 else 'far' if horizon<0 else 'tangent',
            'horizon':horizon,'mirror':(x,-y),'distinct_mirror':y!=0,
            'equal_point_count':1 if y==0 else 2}

def equal_shell(r,d,squared_distance):
    r,d=domain(r,d);s=q(squared_distance)
    x=(d*d+r*r-s)/(2*d);ysq=r*r-x*x
    count=0 if s<0 or ysq<0 else 1 if ysq==0 else 2
    return {'x':x,'y_squared':ysq,'count':count}

def secant(r,d,p):
    """Ray D+s(P-D), s>=0. Roots rational because P is a known circle point."""
    r,d=domain(r,d);x,y=point(r,p);vx,vy=x-d,y
    a=vx*vx+vy*vy;b=2*d*vx;c=d*d-r*r
    roots=sorted((F(1),c/a))
    pts=tuple((d+s*vx,s*vy) for s in roots)
    return {'a':a,'b':b,'c':c,'parameters':tuple(roots),'points':pts,
            'squared_lengths':tuple(a*s*s for s in roots),'tangent':roots[0]==roots[1]}

def compare(r,d,p1,p2):
    """Sign of distance(P2)^2-distance(P1)^2; no angle approximation."""
    a,b=certificate(r,d,p1),certificate(r,d,p2)
    delta=b['squared_distance']-a['squared_distance']
    return {'delta':delta,'projection_identity':2*q(d)*(a['point'][0]-b['point'][0])}

def verify(c):
    try:
        expected=certificate(c['r'],c['d'],c['point'])
        return set(c)==set(expected) and all(type(c[k]) is type(v) and c[k]==v for k,v in expected.items())
    except (KeyError,TypeError,ValueError): return False

def grid():
    for r,k,n,m in product((F(1),F(3),F(5,2)),(F(6,5),F(2),F(3)),range(1,8),range(-8,9)):
        yield r,r*k,sample(r,F(m,n))
