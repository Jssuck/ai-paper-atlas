"""Original teaching model for Euclid II.1; exact finite rational geometry."""
from fractions import Fraction as Q

def scalar(x):
    if type(x) not in (int,Q): raise ValueError('exact int or Fraction required')
    return Q(x)

def point(p):
    if type(p) not in (tuple,list) or len(p)!=2: raise ValueError('point must have two coordinates')
    return tuple(scalar(x) for x in p)

def add(a,b):return (a[0]+b[0],a[1]+b[1])
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def mul(t,a):return (t*a[0],t*a[1])
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def area(poly):
    return abs(sum((det(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly))),Q(0)))/2

def inputs(B,C,G,cuts):
    B,C,G=map(point,(B,C,G));u,v=sub(C,B),sub(G,B)
    if dot(u,u)==0 or dot(v,v)==0:raise ValueError('zero side')
    if dot(u,v)!=0:raise ValueError('sides must be perpendicular')
    if type(cuts) not in (tuple,list):raise ValueError('finite ordered cut list required')
    ts=tuple(scalar(t) for t in cuts)
    if any(not Q(0)<t<Q(1) for t in ts):raise ValueError('cuts must be strictly interior')
    if any(a>=b for a,b in zip(ts,ts[1:])):raise ValueError('cuts must be strictly increasing')
    return B,C,G,u,v,(Q(0),)+ts+(Q(1),)

def construct(B,C,G,cuts):
    B,C,G,u,v,ts=inputs(B,C,G,cuts)
    lower=tuple(add(B,mul(t,u)) for t in ts)
    upper=tuple(add(p,v) for p in lower)
    tiles=tuple((lower[i],lower[i+1],upper[i+1],upper[i]) for i in range(len(ts)-1))
    return {'lower':lower,'upper':upper,'tiles':tiles}

def verify(B,C,G,cuts,certificate):
    """Independent of construct: validate binding, right angles, topology and area."""
    try:
        B,C,G,u,v,ts=inputs(B,C,G,cuts)
        if type(certificate)!=dict or set(certificate)!={'lower','upper','tiles'}:return False
        lower=tuple(point(p) for p in certificate['lower']);upper=tuple(point(p) for p in certificate['upper'])
        tiles=tuple(tuple(point(p) for p in r) for r in certificate['tiles'])
        if len(lower)!=len(ts) or len(upper)!=len(ts) or len(tiles)!=len(ts)-1:return False
        if lower[0]!=B or lower[-1]!=C or upper[0]!=G:return False
        for i,t in enumerate(ts):
            if lower[i]!=add(B,mul(t,u)):return False
            if sub(upper[i],lower[i])!=v:return False
        total=Q(0)
        for i,r in enumerate(tiles):
            if r!=(lower[i],lower[i+1],upper[i+1],upper[i]):return False
            if len(r)!=4:return False
            edges=tuple(sub(r[(j+1)%4],r[j]) for j in range(4))
            if any(dot(e,e)==0 for e in edges):return False
            if any(dot(edges[j],edges[(j+1)%4])!=0 for j in range(4)):return False
            if add(edges[0],edges[2])!=(0,0) or add(edges[1],edges[3])!=(0,0):return False
            # Shared boundary plus ordered parameter intervals certifies no gaps/overlap.
            if i and (tiles[i-1][1],tiles[i-1][2])!=(r[0],r[3]):return False
            if det(sub(r[1],r[0]),v)*det(u,v)<=0:return False
            total+=area(r)
        return total==area((lower[0],lower[-1],upper[-1],upper[0]))
    except (ValueError,TypeError,KeyError,IndexError,OverflowError):return False

def summary(B,C,G,cuts):
    cert=construct(B,C,G,cuts)
    if not verify(B,C,G,cuts,cert):raise RuntimeError('invalid certificate')
    return {'whole_area':str(area((cert['lower'][0],cert['lower'][-1],cert['upper'][-1],cert['upper'][0]))),
            'tile_areas':[str(area(r)) for r in cert['tiles']], 'tiles':len(cert['tiles'])}
