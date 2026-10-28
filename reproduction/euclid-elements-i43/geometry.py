"""Original rational-coordinate teaching model, not a formal Euclidean prover."""
from fractions import Fraction as Q
import json

def point(p):
    if not isinstance(p,(tuple,list)) or len(p)!=2 or any(type(x) not in (int,Q) for x in p):
        raise ValueError('coordinates must be int or Fraction, never bool/float')
    return tuple(Q(x) for x in p)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(t,a): return tuple(t*x for x in a)
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def area(poly):
    return abs(sum(det(poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly))))/2

def split(A,u,v,s,t):
    """General internal grid, not necessarily an I.43 configuration."""
    A,u,v=point(A),point(u),point(v)
    E=add(A,mul(s,u)); H=add(A,mul(t,v)); K=add(E,mul(t,v))
    B=add(A,u); D=add(A,v); C=add(B,v); G=add(B,mul(t,v)); F=add(D,mul(s,u))
    return dict(A=A,B=B,C=C,D=D,E=E,G=G,F=F,H=H,K=K)

def validate(data):
    if type(data) is not dict or set(data)!={'A','B','C','D','K'}: raise ValueError('exact A B C D K fields required')
    p={k:point(v) for k,v in data.items()}; A,B,C,D,K=(p[k] for k in 'ABCDK')
    u,v=sub(B,A),sub(D,A); delta=det(u,v)
    if delta==0: raise ValueError('nondegenerate parallelogram required')
    if C!=add(B,v): raise ValueError('ABCD must be boundary-ordered parallelogram')
    w=sub(K,A); s=det(w,v)/delta; t=det(u,w)/delta
    if s!=t: raise ValueError('K must lie on AC')
    if not 0<t<1: raise ValueError('K must be strictly internal; endpoints excluded')
    return split(A,u,v,t,t),t

def encode(x):
    if isinstance(x,Q): return str(x)
    if isinstance(x,dict): return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [encode(v) for v in x]
    return x

def make_certificate(data):
    p,t=validate(data)
    def ar(names): return area([p[n] for n in names])
    values={n:ar(n) for n in ('ABCD','ABC','ACD','AEKH','KGCF','AEK','AHK','KGC','KFC','EBGK','HKFD')}
    if not (values['ABC']==values['ACD'] and values['AEK']==values['AHK'] and values['KGC']==values['KFC'] and values['EBGK']==values['HKFD']):
        raise ArithmeticError('internal identity failed')
    if values['ABC']!=values['AEK']+values['KGC']+values['EBGK'] or values['ACD']!=values['AHK']+values['KFC']+values['HKFD']:
        raise ArithmeticError('dissection failed')
    return encode({'input':data,'points':p,'t':t,'areas':values,'scope':'internal rational affine model'})

def verify(data,certificate):
    try:
        return json.dumps(make_certificate(data),sort_keys=True,separators=(',',':'))==json.dumps(certificate,sort_keys=True,separators=(',',':'))
    except (ValueError,TypeError,ArithmeticError): return False

def example(A=(0,0),u=(6,0),v=(0,3),t=Q(1,3)):
    p=split(A,u,v,t,t)
    return {k:p[k] for k in 'ABCDK'}
