"""Original exact-rational teaching model of Elements II.6; not a proof assistant."""
from fractions import Fraction as Q

def scalar(x):
    if type(x) not in (int,Q): raise ValueError('exact int/Fraction required; no bool or float')
    return Q(x)
def point(p):
    if not isinstance(p,(tuple,list)) or len(p)!=2: raise ValueError('point must have two coordinates')
    return tuple(scalar(x) for x in p)
def sub(p,q):return (p[0]-q[0],p[1]-q[1])
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def area(vertices):
    return abs(sum(cross(vertices[i],vertices[(i+1)%len(vertices)]) for i in range(len(vertices))))/2

def parameters(a=3,b=2,origin=(0,0),u=(1,0),v=(0,1)):
    a,b=scalar(a),scalar(b);origin,u,v=point(origin),point(u),point(v)
    if a<=0 or b<=0:raise ValueError('a and b must be strictly positive')
    if dot(u,u)==0 or dot(v,v)!=dot(u,u) or dot(u,v)!=0:raise ValueError('basis must be nonzero, equal length and orthogonal')
    return a,b,origin,u,v

def construct(a=3,b=2,origin=(0,0),u=(1,0),v=(0,1)):
    a,b,o,u,v=parameters(a,b,origin,u,v)
    local={'A':(0,0),'C':(a,0),'B':(2*a,0),'D':(2*a+b,0),
           'E':(a,a+b),'F':(2*a+b,a+b),'G':(2*a,a+b),
           'H':(2*a,b),'K':(0,b),'L':(a,b),'M':(2*a+b,b)}
    return {'points':{n:(o[0]+x*u[0]+y*v[0],o[1]+x*u[1]+y*v[1]) for n,(x,y) in local.items()}}

REGIONS={'AL':'ACLK','CH':'CBHL','HF':'HMFG','CM':'CDML','AM':'ADMK','LG':'LHGE','square':'CDFE','DM':'BDMH'}

def verify(cert,a=3,b=2,origin=(0,0),u=(1,0),v=(0,1)):
    a,b,o,u,v=parameters(a,b,origin,u,v)
    if not isinstance(cert,dict) or set(cert)!={'points'} or not isinstance(cert['points'],dict):raise ValueError('certificate schema')
    if set(cert['points'])!=set('ABCDEFGHKLM'):
        raise ValueError('point names')
    p={n:point(x) for n,x in cert['points'].items()}
    expected=construct(a,b,o,u,v)['points']
    if p!=expected:raise ValueError('construction coordinates differ')
    if cross(sub(p['H'],p['D']),sub(p['E'],p['D']))!=0:raise ValueError('H not on DE')
    for names in ('CDFE','LHGE'):
        edges=[sub(p[names[(i+1)%4]],p[names[i]]) for i in range(4)]
        if len({dot(e,e) for e in edges})!=1 or any(dot(edges[i],edges[(i+1)%4]) for i in range(4)):
            raise ValueError('square qualification')
    r={name:area([p[n] for n in names]) for name,names in REGIONS.items()}
    r['gnomon']=r['CM']+r['HF']
    if not (r['AL']==r['CH']==r['HF'] and r['AM']==r['AL']+r['CM']==r['gnomon'] and r['gnomon']+r['LG']==r['square']):
        raise ValueError('area-chain failure')
    scale=dot(u,u)
    if r['AM']!=(2*a+b)*b*scale or r['LG']!=a*a*scale or r['square']!=(a+b)**2*scale:raise ValueError('metric audit')
    return r
