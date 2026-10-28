"""Original exact-rational teaching model of Elements II.5, right-half branch."""
from fractions import Fraction as Q

REGIONS = {'CH': ('C','D','H','L'), 'HF': ('H','M','F','G'),
 'DM': ('D','B','M','H'), 'LG': ('L','H','G','E'),
 'CM': ('C','B','M','L'), 'DF': ('D','B','F','G'),
 'AL': ('A','C','L','K'), 'AH': ('A','D','H','K'),
 'gnomon': ('C','B','F','G','H','L'), 'square': ('C','B','F','E')}

def scalar(x):
    if type(x) not in (int, Q): raise ValueError('integer or Fraction required')
    return Q(x)

def point(p):
    if type(p) not in (list,tuple) or len(p)!=2: raise ValueError('point requires two coordinates')
    return tuple(scalar(x) for x in p)

def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def sub(a,b): return (a[0]-b[0],a[1]-b[1])

def inputs(C,u,v,t):
    C,u,v=point(C),point(u),point(v);t=scalar(t)
    if not 0<t<1: raise ValueError('right-half cut requires 0 < t < 1')
    if dot(u,u)==0 or dot(u,u)!=dot(v,v) or dot(u,v)!=0:
        raise ValueError('square basis must be nonzero, equal and perpendicular')
    return C,u,v,t

def construct(C=(0,0),u=(5,0),v=(0,5),t=Q(2,5)):
    C,u,v,t=inputs(C,u,v,t)
    xy={'A':(-1,0),'C':(0,0),'D':(t,0),'B':(1,0),'E':(0,1),
        'F':(1,1),'G':(t,1),'H':(t,1-t),'L':(0,1-t),'M':(1,1-t),'K':(-1,1-t)}
    pts={name:tuple(C[i]+x*u[i]+y*v[i] for i in range(2)) for name,(x,y) in xy.items()}
    return {'points':pts,'regions':dict(REGIONS)}

def area(vertices):
    return abs(sum(cross(a,b) for a,b in zip(vertices,vertices[1:]+vertices[:1])))/2

def verify(cert,C=(0,0),u=(5,0),v=(0,5),t=Q(2,5)):
    C,u,v,t=inputs(C,u,v,t)
    if type(cert)!=dict or set(cert)!= {'points','regions'}: raise ValueError('certificate fields')
    raw=cert['points']; regions=cert['regions']
    if type(raw)!=dict or set(raw)!=set('ACDBEFGHLMK'): raise ValueError('point names')
    if type(regions)!=dict or set(regions)!=set(REGIONS): raise ValueError('region names')
    pts={k:point(p) for k,p in raw.items()};det=cross(u,v)
    # Inverse coordinates, independent of the constructor implementation.
    uv={k:(cross(sub(p,C),v)/det,cross(u,sub(p,C))/det) for k,p in pts.items()}
    expected={'A':(-1,0),'C':(0,0),'B':(1,0),'D':(t,0),'E':(0,1),'F':(1,1),
              'G':(t,1),'H':(t,1-t),'L':(0,1-t),'M':(1,1-t),'K':(-1,1-t)}
    if uv!=expected: raise ValueError('point incidence or location mismatch')
    for name,boundary in REGIONS.items():
        if type(regions[name]) not in (tuple,list) or tuple(regions[name])!=boundary:
            raise ValueError('ordered region boundary mismatch')
    # Explicit qualifications: H on BE, DH=DB, small squares LG and DM.
    if cross(sub(pts['H'],pts['B']),sub(pts['E'],pts['B']))!=0: raise ValueError('H off diagonal')
    if dot(sub(pts['H'],pts['D']),sub(pts['H'],pts['D'])) != dot(sub(pts['B'],pts['D']),sub(pts['B'],pts['D'])):
        raise ValueError('DH != DB')
    for name in ('LG','DM','square'):
        vs=[pts[k] for k in REGIONS[name]];es=[sub(vs[(i+1)%4],vs[i]) for i in range(4)]
        if len({dot(e,e) for e in es})!=1 or any(dot(es[i],es[(i+1)%4]) for i in range(4)):
            raise ValueError('not a square')
    areas={k:area([pts[n] for n in REGIONS[k]]) for k in REGIONS}
    # Fixed vertices and strictly interior cuts certify the four disjoint interiors:
    # [0,t]x[0,1-t], [t,1]x[0,1-t], [t,1]x[1-t,1], [0,t]x[1-t,1].
    checks=(areas['CH']==areas['HF'], areas['CH']+areas['DM']==areas['CM'],
            areas['HF']+areas['DM']==areas['DF'], areas['AL']==areas['CM'],
            areas['AH']==areas['AL']+areas['CH'], areas['gnomon']==areas['DF']+areas['CH'],
            areas['AH']==areas['gnomon'], areas['gnomon']+areas['LG']==areas['square'],
            sum(areas[x] for x in ('CH','DM','HF','LG'))==areas['square'],
            areas['AH']==(1+t)*(1-t)*dot(u,u), areas['LG']==t*t*dot(u,u))
    if not all(checks):raise ValueError('area certificate failed')
    return areas
