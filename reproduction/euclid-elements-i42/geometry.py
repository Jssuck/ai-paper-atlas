"""I.42 rational-coordinate teaching reconstruction, not a proof kernel."""
from fractions import Fraction as Q
import json

def point(p):
    if not isinstance(p,(tuple,list)) or len(p)!=2:
        raise ValueError('point/vector must have two exact coordinates')
    if any(type(x) not in (int,Q) for x in p):
        raise ValueError('coordinates must be int or Fraction, not bool/float')
    return tuple(Q(x) for x in p)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def scale(t,a): return tuple(t*x for x in a)
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def triangle2(a,b,c): return abs(cross(sub(b,a),sub(c,a)))
def polygon2(ps): return abs(sum(cross(a,b) for a,b in zip(ps,ps[1:]+ps[:1])))
def qp(p): return [str(x) for x in p]
def make_certificate(data):
    if type(data) is not dict or set(data)!=set(('A','B','C','u')):
        raise ValueError('exact input fields A B C u required')
    A,B,C,u=(point(data[k]) for k in ('A','B','C','u'))
    v=sub(C,B); E=scale(Q(1,2),add(B,C))
    h=cross(v,sub(A,E)); d=cross(v,u)
    if h==0: raise ValueError('triangle is degenerate')
    if d==0: raise ValueError('given angle must be nonzero and nonstraight')
    t=h/d
    if t<=0: raise ValueError('copied angle ray must lie on the A side of BC')
    F=add(E,scale(t,u)); G=add(F,sub(C,E))
    a=triangle2(A,B,C); a1=triangle2(A,B,E); a2=triangle2(A,E,C)
    pg=polygon2([F,E,C,G]); w=sub(C,E)
    checks=[a1==a2,a==a1+a2,pg==2*a2,pg==a,
            cross(sub(F,A),v)==0,cross(sub(G,A),v)==0,
            sub(G,F)==w,sub(G,C)==sub(F,E),
            cross(sub(F,E),u)==0,dot(sub(F,E),u)>0]
    if not all(checks): raise RuntimeError('construction invariant failure')
    return {'kind':'euclid-i42-rational-v1',
      'input':{k:qp(p) for k,p in zip(('A','B','C','u'),(A,B,C,u))},
      'points':{k:qp(p) for k,p in zip(('E','F','G'),(E,F,G))},
      'parameter_t':str(t),
      'double_areas':{k:str(x) for k,x in zip(('ABC','ABE','AEC','FECG'),(a,a1,a2,pg))},
      'chain':['I.10: BE = EC','I.38: area(ABE) = area(AEC)',
               'partition: area(ABC) = 2 area(AEC)',
               'I.41: area(FECG) = 2 area(AEC)',
               'common value: area(FECG) = area(ABC)'],
      'scope':'exact rational model only; not a general Euclidean proof'}
def verify_certificate(data,certificate):
    try:
        expected=make_certificate(data)
        # Canonical serialization prevents bool/int equality or extra-field acceptance.
        return json.dumps(certificate,sort_keys=True,allow_nan=False,separators=(',',':'))==json.dumps(expected,sort_keys=True,separators=(',',':'))
    except (ValueError,TypeError,OverflowError): return False
