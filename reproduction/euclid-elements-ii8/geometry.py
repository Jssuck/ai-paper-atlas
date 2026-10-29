"""Exact finite teaching model of Elements II.8; not a general proof."""
from fractions import Fraction as Q

def rational(x):
    if isinstance(x,bool) or not isinstance(x,(int,Q)):
        raise ValueError('expected exact integer or Fraction, not bool/float')
    return Q(x)

def pair(x):
    if not isinstance(x,(tuple,list)) or len(x)!=2:raise ValueError('expected coordinate pair')
    return tuple(rational(z) for z in x)

def parameters(a,b,origin,u,v):
    a,b=rational(a),rational(b)
    if a<=0 or b<=0:raise ValueError('a and b must be positive')
    origin,u,v=pair(origin),pair(u),pair(v);n=sum(z*z for z in u)
    if n==0 or sum(z*z for z in v)!=n or sum(x*y for x,y in zip(u,v))!=0:
        raise ValueError('basis must be nonzero, orthogonal, equal length')
    return a,b,origin,u,v,n

def construct(a=3,b=2,origin=(0,0),u=(1,0),v=(0,1)):
    a,b,o,u,v,n=parameters(a,b,origin,u,v);s=a+2*b
    coords={'A':(0,0),'C':(a,0),'B':(a+b,0),'D':(s,0),
            'M':(0,b),'G':(a,b),'K':(a+b,b),'N':(s,b),
            'O':(0,2*b),'Q':(a,2*b),'R':(a+b,2*b),'P':(s,2*b),
            'E':(0,s),'H':(a,s),'L':(a+b,s),'F':(s,s)}
    return {'points':{k:tuple(o[i]+x*u[i]+y*v[i] for i in range(2)) for k,(x,y) in coords.items()}}

REGIONS={'CK':'CBKG','KD':'BDNK','GR':'GKRQ','RN':'KNPR',
         'AG':'ACGM','MQ':'MGQO','QL':'QRLH','RF':'RPFL',
         'OH':'OQHE','AK':'ABKM','whole':'ADFE',
         'gnomon':'ADFH QO'.replace(' ',''),'CP':'CDPQ','ML':'MKLE'}

def area(points,labels):
    p=[pair(points[k]) for k in labels]
    return abs(sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p))))/2

def verify(c,a=3,b=2,origin=(0,0),u=(1,0),v=(0,1)):
    a,b,o,u,v,n=parameters(a,b,origin,u,v)
    if not isinstance(c,dict) or set(c)!={'points'} or not isinstance(c['points'],dict):raise ValueError('certificate shape invalid')
    p=c['points'];expected=construct(a,b,o,u,v)['points']
    if set(p)!=set(expected):raise ValueError('point labels differ')
    for k in expected:
        if pair(p[k])!=expected[k]:raise ValueError('point '+k+' violates construction')
    r={k:area(p,labels) for k,labels in REGIONS.items()}
    for k in ('CK','KD','GR','RN'):
        if r[k]!=b*b*n:raise ValueError('small square mismatch')
    for k in ('AG','MQ','QL','RF'):
        if r[k]!=a*b*n:raise ValueError('rectangle mismatch')
    cells=('CK','KD','GR','RN','AG','MQ','QL','RF')
    if sum(r[k] for k in cells)!=r['gnomon']:raise ValueError('eight-cell partition mismatch')
    if r['AK']!=r['AG']+r['CK'] or r['gnomon']!=4*r['AK']:raise ValueError('quadruple mismatch')
    if r['OH']!=a*a*n or r['whole']!=r['gnomon']+r['OH']:raise ValueError('completion mismatch')
    return r
