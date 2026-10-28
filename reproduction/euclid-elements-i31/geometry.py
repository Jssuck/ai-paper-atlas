"""Original exact rational Euclidean-coordinate teaching model of I.31."""
from fractions import Fraction as Q
import hashlib
import json

def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def s(x): return str(x)
def canonical(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def parse(data):
    if type(data) is not dict or set(data)!=set('ABCDEF'): raise ValueError('six point keys required')
    out={}
    for k,v in data.items():
        if type(v) is not list or len(v)!=2: raise ValueError('point list required')
        p=[]
        for z in v:
            if type(z) is not str: raise ValueError('canonical rational strings required')
            try: q=Q(z)
            except (ValueError,ZeroDivisionError): raise ValueError('invalid rational') from None
            if str(q)!=z: raise ValueError('noncanonical rational')
            p.append(q)
        out[k]=tuple(p)
    return out

def angle_equal(u,v,w,z):
    """Unsigned nondegenerate angle equality by dot sign and squared cosine."""
    a,b=dot(u,v),dot(w,z)
    return (a>0)-(a<0)==(b>0)-(b<0) and a*a*dot(w,w)*dot(z,z)==b*b*dot(u,u)*dot(v,v)

def make_certificate(data):
    p=parse(data); A,B,C,D,E,F=(p[k] for k in 'ABCDEF')
    bc=sub(C,B); dc=sub(C,D); da=sub(A,D); ad=sub(D,A); ae=sub(E,A); af=sub(F,A)
    if dot(bc,bc)==0 or cross(bc,sub(D,B))!=0 or dot(dc,dc)==0: raise ValueError('D on BC, D different C required')
    if cross(bc,sub(A,B))==0: raise ValueError('A must be off BC')
    if dot(ae,ae)==0 or dot(af,af)==0: raise ValueError('nonzero constructed rays required')
    side_e=cross(ad,ae); side_c=cross(ad,sub(C,A))
    if side_e*side_c>=0: raise ValueError('E and C must be opposite sides of AD')
    if not angle_equal(ae,ad,da,dc): raise ValueError('copied angle EAD must equal ADC')
    if cross(ae,af)!=0 or dot(ae,af)>=0: raise ValueError('F must extend EA beyond A')
    # Derive scale and inspect the output independently of angle comparison.
    j=0 if dc[0]!=0 else 1
    t=-ae[j]/dc[j]; u=af[j]/dc[j]
    if t<=0 or u<=0 or any(ae[i]!=-t*dc[i] or af[i]!=u*dc[i] for i in range(2)):
        raise ValueError('coordinate consequence failed')
    return {'schema':1,'input':json.loads(canonical(data)),
            'input_sha256':hashlib.sha256(canonical(data).encode()).hexdigest(),
            'angle':{'dot_EAD':s(dot(ae,ad)),'dot_ADC':s(dot(da,dc)),
                     'norm2_AE':s(dot(ae,ae)),'norm2_AD':s(dot(ad,ad)),
                     'norm2_DC':s(dot(dc,dc))},
            'side_product':s(side_e*side_c),'scales':{'t':s(t),'u':s(u)},
            'conclusion':{'parallel_cross':s(cross(ae,bc)),
                          'distinct_line_cross':s(cross(bc,sub(A,B))),
                          'A_between_E_F':True}}

def strict_equal(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict: return set(a)==set(b) and all(strict_equal(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(strict_equal(x,y) for x,y in zip(a,b))
    if type(a) in (str,int,bool,type(None)): return a==b
    return False

def verify_certificate(expected_input,certificate):
    try: return strict_equal(make_certificate(expected_input),certificate)
    except (ValueError,TypeError,OverflowError): return False
