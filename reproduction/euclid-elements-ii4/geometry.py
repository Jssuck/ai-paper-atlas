"""Original exact-coordinate teaching model for Elements II.4; not an axiom prover."""
from fractions import Fraction as Q

def scalar(x):
    if type(x) not in (int,Q): raise ValueError('exact integer or Fraction required')
    return Q(x)
def point(p):
    if type(p) not in (tuple,list) or len(p)!=2: raise ValueError('two coordinates required')
    return tuple(scalar(x) for x in p)
def add(p,q): return (p[0]+q[0],p[1]+q[1])
def sub(p,q): return (p[0]-q[0],p[1]-q[1])
def mul(t,p): return (t*p[0],t*p[1])
def dot(p,q): return p[0]*q[0]+p[1]*q[1]
def det(p,q): return p[0]*q[1]-p[1]*q[0]
def area(vertices):
    return abs(sum(det(vertices[i],vertices[(i+1)%len(vertices)]) for i in range(len(vertices))))/2
REGIONS={'whole':('A','D','E','B'),'HF':('H','D','F','G'),'CK':('C','G','K','B'),'AG':('A','H','G','C'),'GE':('G','F','E','K')}
def inputs(A,u,v,t):
    A,u,v=point(A),point(u),point(v); t=scalar(t)
    if dot(u,u)==0 or dot(u,v)!=0 or dot(u,u)!=dot(v,v): raise ValueError('nonzero perpendicular equal square sides required')
    if not 0<t<1: raise ValueError('internal cut required')
    return A,u,v,t

def construct(A=(0,0),u=(5,0),v=(0,5),t=Q(2,5)):
    A,u,v,t=inputs(A,u,v,t)
    specs={'A':(0,0),'B':(1,0),'D':(0,1),'E':(1,1),'C':(t,0),'F':(t,1),'G':(t,1-t),'H':(0,1-t),'K':(1,1-t)}
    pts={n:add(A,add(mul(x,u),mul(y,v))) for n,(x,y) in specs.items()}
    return {'points':pts,'regions':dict(REGIONS)}

def verify(cert,A=(0,0),u=(5,0),v=(0,5),t=Q(2,5)):
    A,u,v,t=inputs(A,u,v,t)
    if type(cert)!=dict or set(cert)!={'points','regions'}: raise ValueError('certificate fields')
    if type(cert['points'])!=dict or set(cert['points'])!=set('ABDECFGHK'): raise ValueError('point names')
    pts={n:point(p) for n,p in cert['points'].items()}
    # Independently recover affine coordinates, rather than call construct.
    coordinates={n:(det(sub(p,A),v)/det(u,v),det(u,sub(p,A))/det(u,v)) for n,p in pts.items()}
    expected={'A':(0,0),'B':(1,0),'D':(0,1),'E':(1,1),'C':(t,0),'F':(t,1),'G':(t,1-t),'H':(0,1-t),'K':(1,1-t)}
    if coordinates!=expected: raise ValueError('point incidence or order mismatch')
    if cert['regions']!=REGIONS: raise ValueError('ordered region boundaries mismatch')
    # Each region is a rectangle. The two diagonal regions are squares.
    for name,ns in REGIONS.items():
        edges=[sub(pts[ns[(i+1)%4]],pts[ns[i]]) for i in range(4)]
        if any(dot(edges[i],edges[(i+1)%4])!=0 for i in range(4)): raise ValueError('not rectangular')
        if name in ('whole','HF','CK') and len({dot(e,e) for e in edges})!=1: raise ValueError('not square')
    if det(sub(pts['G'],pts['B']),sub(pts['D'],pts['B']))!=0: raise ValueError('G not on BD')
    # Exact partition: the cuts x=t and y=1-t produce four adjacent parameter cells.
    boxes={'HF':(0,t,1-t,1),'CK':(t,1,0,1-t),'AG':(0,t,0,1-t),'GE':(t,1,1-t,1)}
    names=list(boxes)
    for i,n in enumerate(names):
        for m in names[i+1:]:
            a,b=boxes[n],boxes[m]
            if min(a[1],b[1])>max(a[0],b[0]) and min(a[3],b[3])>max(a[2],b[2]): raise ValueError('interior overlap')
    if sum((x1-x0)*(y1-y0) for x0,x1,y0,y1 in boxes.values())!=1: raise ValueError('not covering unit square')
    areas={n:area([pts[k] for k in ns]) for n,ns in REGIONS.items()}
    if areas['AG']!=areas['GE'] or areas['whole']!=sum(areas[n] for n in boxes): raise ValueError('area equality failed')
    return areas
