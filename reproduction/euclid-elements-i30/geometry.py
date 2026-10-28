"""Original exact rational coordinate model for I.30, not an axiomatic proof."""
from fractions import Fraction
import hashlib
import json

def rational(x):
    if type(x) is not str: raise ValueError('canonical rational strings required')
    try: q=Fraction(x)
    except (ValueError,ZeroDivisionError): raise ValueError('invalid rational') from None
    if str(q)!=x: raise ValueError('noncanonical rational')
    return q

def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def mul(q,a): return tuple(q*x for x in a)
def parse(data):
    if type(data) is not dict or set(data)!=set('ABCDEF'): raise ValueError('six exact point keys required')
    p={}
    for k,v in data.items():
        if type(v) is not list or len(v)!=2: raise ValueError('two-dimensional point list required')
        p[k]=tuple(rational(x) for x in v)
    return p

def make_certificate(data):
    p=parse(data); u=sub(p['B'],p['A']); v=sub(p['D'],p['C']); w=sub(p['F'],p['E'])
    if not all(dot(z,z)>0 for z in (u,v,w)): raise ValueError('zero line direction')
    if det(u,w)!=0 or det(v,w)!=0: raise ValueError('parallel premises required')
    offsets=[det(sub(p['A'],p['E']),w),det(sub(p['C'],p['E']),w),det(sub(p['C'],p['A']),w)]
    if any(x==0 for x in offsets): raise ValueError('three pairwise distinct lines required')
    j=0 if w[0] else 1
    alpha,beta=u[j]/w[j],v[j]/w[j]
    # A transverse line through E perpendicular to w. Its intersection parameters
    # are signed, so no hidden ordering of the three parallel lines is assumed.
    t=(-w[1],w[0]); denominator=det(t,w)
    sA,sC=offsets[0]/denominator,offsets[1]/denominator
    P,Q=add(p['E'],mul(sA,t)),add(p['E'],mul(sC,t))
    if det(sub(P,p['A']),u) or det(sub(Q,p['C']),v): raise ValueError('intersection consistency failure')
    if det(u,v)!=0: raise ValueError('conclusion consistency failure')
    canonical=json.dumps(data,sort_keys=True,separators=(',',':'))
    return {'schema':1,'model':'rational Euclidean plane; not an axiomatic proof','input':json.loads(canonical),'input_sha256':hashlib.sha256(canonical.encode()).hexdigest(),
        'premise_determinants':['0','0'],'scales':[str(alpha),str(beta)],'distinctness_determinants':[str(z) for z in offsets],
        'transversal':{'direction':[str(z) for z in t],'parameters':[str(sA),str(sC),'0'],'intersections':[[str(z) for z in P],[str(z) for z in Q],data['E'][:]]},
        'conclusion':{'determinant':str(det(u,v)),'distinct':True,'parallel':True}}

def strict_equal(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict: return set(a)==set(b) and all(strict_equal(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(strict_equal(x,y) for x,y in zip(a,b))
    if type(a) in (str,int,bool,type(None)): return a==b
    return False

def verify_certificate(expected_input,certificate):
    try: return strict_equal(make_certificate(expected_input),certificate)
    except (ValueError,TypeError,KeyError,ZeroDivisionError): return False
