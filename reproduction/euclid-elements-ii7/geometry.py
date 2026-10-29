"""Original exact-rational teaching audit of Elements II.7, not a proof assistant."""
from fractions import Fraction as Q

def scalar(x):
    if type(x) not in (int,Q):raise ValueError('exact int/Fraction required')
    return Q(x)
def point(p):
    if not isinstance(p,(tuple,list)) or len(p)!=2:raise ValueError('two coordinates required')
    return tuple(scalar(x) for x in p)
def dot(u,v):return u[0]*v[0]+u[1]*v[1]
def cross(u,v):return u[0]*v[1]-u[1]*v[0]
def sub(u,v):return tuple(x-y for x,y in zip(u,v))
def area(vertices):return abs(sum(cross(vertices[i],vertices[(i+1)%len(vertices)]) for i in range(len(vertices))))/2

def parameters(a=3,b=2,origin=(0,0),u=(1,0),v=(0,1)):
    a,b=scalar(a),scalar(b);o,u,v=point(origin),point(u),point(v)
    if a<=0 or b<=0:raise ValueError('strictly internal cut requires a,b>0')
    if dot(u,u)==0 or dot(u,u)!=dot(v,v) or dot(u,v)!=0:raise ValueError('nonzero equal orthogonal basis required')
    return a,b,o,u,v

def construct(a=3,b=2,origin=(0,0),u=(1,0),v=(0,1)):
    a,b,o,u,v=parameters(a,b,origin,u,v);s=a+b
    local={'A':(0,0),'B':(s,0),'C':(a,0),'D':(0,s),'E':(s,s),'F':(s,b),'G':(a,b),'H':(0,b),'N':(a,s)}
    return {'points':{k:(o[0]+x*u[0]+y*v[0],o[1]+x*u[1]+y*v[1]) for k,(x,y) in local.items()}}

REGIONS={'AG':'ACGH','GE':'GFEN','CF':'CBFG','DG':'HGND','AF':'ABFH','CE':'CBEN','gnomon':'ABENGH','whole':'ABED'}

def verify(cert,a=3,b=2,origin=(0,0),u=(1,0),v=(0,1)):
    a,b,o,u,v=parameters(a,b,origin,u,v)
    if not isinstance(cert,dict) or set(cert)!={'points'} or not isinstance(cert['points'],dict):raise ValueError('certificate schema')
    if set(cert['points'])!=set('ABCDEFGHN'):raise ValueError('point names')
    p={k:point(z) for k,z in cert['points'].items()}
    if p!=construct(a,b,o,u,v)['points']:raise ValueError('construction differs')
    if cross(sub(p['G'],p['D']),sub(p['B'],p['D'])):raise ValueError('G must lie on DB')
    for name in ('CF','DG','whole'):
        ns=REGIONS[name];es=[sub(p[ns[(i+1)%4]],p[ns[i]]) for i in range(4)]
        if len({dot(e,e) for e in es})!=1 or any(dot(es[i],es[(i+1)%4]) for i in range(4)):raise ValueError('square qualification')
    r={k:area([p[n] for n in ns]) for k,ns in REGIONS.items()}
    if not (r['AG']==r['GE'] and r['AG']+r['CF']==r['AF']==r['CE']==r['GE']+r['CF']):raise ValueError('complement-addition chain')
    if not (r['AF']+r['CE']==r['gnomon']+r['CF'] and r['gnomon']+r['DG']==r['whole']):raise ValueError('overlap accounting')
    # Exact coordinate interval intersection in the construction's orthogonal basis.
    # AF=[0,a+b] x [0,b], CE=[a,a+b] x [0,a+b].
    intersection=(min(a+b,a+b)-max(Q(0),a))*(min(b,a+b)-max(Q(0),Q(0)))*dot(u,u)
    if intersection!=r['CF'] or r['AF']+r['CE']-intersection!=r['gnomon']:
        raise ValueError('intersection/union audit')
    scale=dot(u,u)
    if r['AF']!=(a+b)*b*scale or r['CF']!=b*b*scale or r['DG']!=a*a*scale:raise ValueError('metric identification')
    if r['whole']+r['CF']!=2*r['AF']+r['DG']:raise ValueError('conclusion')
    return r
