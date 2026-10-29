"""Exact finite teaching checks for Euclid II.9; not a formal proof."""
from fractions import Fraction as Q

def scalar(x):
    if isinstance(x,bool) or not isinstance(x,(int,Q)):
        raise ValueError('expected int or Fraction, excluding bool')
    return Q(x)

def vector(x):
    if not isinstance(x,(tuple,list)) or len(x)!=2:raise ValueError('expected 2-vector')
    return tuple(scalar(z) for z in x)

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def sq(a,b):return dot(sub(a,b),sub(a,b))

def parameters(h,d,origin,u,v):
    h,d=scalar(h),scalar(d);o,u,v=map(vector,(origin,u,v))
    if not 0<d<h:raise ValueError('require 0 < d < h')
    if dot(u,u)==0 or dot(u,v)!=0 or dot(u,u)!=dot(v,v):
        raise ValueError('basis must be nonzero, orthogonal, equal length')
    return h,d,o,u,v

def construct(h=5,d=2,origin=(0,0),u=(1,0),v=(0,1)):
    h,d,o,u,v=parameters(h,d,origin,u,v)
    local={'A':(0,0),'C':(h,0),'B':(2*h,0),'D':(h+d,0),
           'E':(h,h),'F':(h+d,h-d),'G':(h,h-d)}
    return {'points':{k:tuple(o[i]+x*u[i]+y*v[i] for i in range(2)) for k,(x,y) in local.items()}}

def verify(c,h=5,d=2,origin=(0,0),u=(1,0),v=(0,1)):
    h,d,o,u,v=parameters(h,d,origin,u,v)
    if not isinstance(c,dict) or set(c)!={'points'} or not isinstance(c['points'],dict):raise ValueError('invalid certificate')
    p=c['points']; expected=construct(h,d,o,u,v)['points']
    if set(p)!=set(expected):raise ValueError('point labels differ')
    p={k:vector(x) for k,x in p.items()}
    if p!=expected:raise ValueError('point coordinates differ')
    right={'ACE':('A','C','E'),'ECB':('E','C','B'),'EGF':('E','G','F'),
           'FDB':('F','D','B'),'AEF':('A','E','F'),'ADF':('A','D','F')}
    for label,(a,b,e) in right.items():
        if dot(sub(p[a],p[b]),sub(p[e],p[b]))!=0:raise ValueError('right angle '+label)
    for a,b,c_,d_ in [('A','C','C','E'),('C','E','C','B'),('E','G','G','F'),('F','D','D','B'),('G','F','C','D')]:
        if sq(p[a],p[b])!=sq(p[c_],p[d_]):raise ValueError('required equal lengths')
    s={k:sq(p[k[0]],p[k[1]]) for k in ['AC','CE','AE','EG','GF','EF','AF','AD','DF','DB','CD']}
    equations={'ACE':(s['AE'],s['AC']+s['CE']), 'EGF':(s['EF'],s['EG']+s['GF']),
               'AEF':(s['AF'],s['AE']+s['EF']), 'ADF':(s['AF'],s['AD']+s['DF'])}
    for label,(left,right_) in equations.items():
        if left!=right_:raise ValueError('Pythagorean identity '+label)
    left=s['AD']+s['DB'];right_=2*(s['AC']+s['CD'])
    if left!=right_ or left!=s['AF']:raise ValueError('two AF routes disagree')
    return {'squares':s,'routes':equations,'lhs':left,'rhs':right_,'basis_norm_squared':dot(u,u)}

def normalized_segments(h,t):
    """Signed displacement is normalized by exchanging endpoint roles when t<0."""
    h,t=scalar(h),scalar(t)
    if not h>0 or not 0<abs(t)<h:raise ValueError('strict interior unequal division required')
    return {'h':h,'d':abs(t),'swap_endpoints':t<0,'AD_original':h+t,'DB_original':h-t}
