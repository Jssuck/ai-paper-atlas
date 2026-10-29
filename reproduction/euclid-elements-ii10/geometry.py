"""Exact finite teaching checks for II.10, not a formal geometry proof."""
from fractions import Fraction as Q

def scalar(x):
    if isinstance(x,bool) or not isinstance(x,(int,Q)):raise ValueError('expected int or Fraction, excluding bool')
    return Q(x)
def vector(x):
    if not isinstance(x,(tuple,list)) or len(x)!=2:raise ValueError('expected 2-vector')
    return tuple(scalar(z) for z in x)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def sq(a,b):return dot(sub(a,b),sub(a,b))
def parameters(h,t,origin,u,v):
    h,t=scalar(h),scalar(t);o,u,v=map(vector,(origin,u,v))
    if h<=0 or t<=0:raise ValueError('require h > 0 and t > 0')
    if dot(u,u)==0 or dot(u,v)!=0 or dot(u,u)!=dot(v,v):raise ValueError('basis must be nonzero, orthogonal, equal length')
    return h,t,o,u,v

def construct(h=3,t=2,origin=(0,0),u=(1,0),v=(0,1)):
    h,t,o,u,v=parameters(h,t,origin,u,v)
    local={'A':(0,0),'C':(h,0),'B':(2*h,0),'D':(2*h+t,0),'E':(h,h),'F':(2*h+t,h),'G':(2*h+t,-t)}
    return {'points':{k:tuple(o[i]+x*u[i]+y*v[i] for i in range(2)) for k,(x,y) in local.items()}}

def verify(c,h=3,t=2,origin=(0,0),u=(1,0),v=(0,1)):
    h,t,o,u,v=parameters(h,t,origin,u,v)
    if not isinstance(c,dict) or set(c)!={'points'} or not isinstance(c['points'],dict):raise ValueError('invalid certificate')
    expected=construct(h,t,o,u,v)['points'];p=c['points']
    if set(p)!=set(expected):raise ValueError('point labels differ')
    p={k:vector(x) for k,x in p.items()}
    if p!=expected:raise ValueError('point coordinates differ')
    right={'ACE':('A','C','E'),'ECB':('E','C','B'),'EFG':('E','F','G'),'BDG':('B','D','G'),'AEG':('A','E','G'),'ADG':('A','D','G')}
    for label,(a,b,z) in right.items():
        if dot(sub(p[a],p[b]),sub(p[z],p[b]))!=0:raise ValueError('right angle '+label)
    for a,b,c_,d in [('A','C','C','E'),('C','E','C','B'),('E','F','F','G'),('D','G','D','B'),('E','F','C','D')]:
        if sq(p[a],p[b])!=sq(p[c_],p[d]):raise ValueError('required equal lengths')
    s={k:sq(p[k[0]],p[k[1]]) for k in ['AC','CE','AE','EF','FG','EG','AG','AD','DG','DB','CD']}
    equations={'ACE':(s['AE'],s['AC']+s['CE']),'EFG':(s['EG'],s['EF']+s['FG']),'AEG':(s['AG'],s['AE']+s['EG']),'ADG':(s['AG'],s['AD']+s['DG'])}
    for name,(l,r) in equations.items():
        if l!=r:raise ValueError('Pythagorean identity '+name)
    lhs=s['AD']+s['DB'];rhs=2*(s['AC']+s['CD'])
    if lhs!=rhs or lhs!=s['AG']:raise ValueError('two AG routes differ')
    return {'squares':s,'routes':equations,'lhs':lhs,'rhs':rhs,'basis_norm_squared':dot(u,u)}

def side_diagonal(steps=8):
    """Finite integer recurrence; h=s,t=d maps II.10 to sign reversal."""
    if isinstance(steps,bool) or not isinstance(steps,int) or not 1<=steps<=1000:raise ValueError('require integer steps 1..1000')
    s=d=1;rows=[]
    for _ in range(steps):
        sn,dn=s+d,2*s+d;old=d*d-2*s*s;new=dn*dn-2*sn*sn
        r=verify(construct(s,d),s,d)
        if new!=-old or r['lhs']!=dn*dn+d*d:raise ValueError('recurrence identity differs')
        rows.append({'s':s,'d':d,'difference':old,'next_s':sn,'next_d':dn,'next_difference':new})
        s,d=sn,dn
    return rows
