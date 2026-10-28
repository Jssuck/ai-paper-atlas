"""Original exact rational Euclidean-coordinate teaching model of I.32."""
from fractions import Fraction as Q
import hashlib
import json

def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def s(x): return str(x)
def canonical(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def parse(data):
    if type(data) is not dict or set(data)!=set('ABCDE'): raise ValueError('five point keys required')
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

def pair(u,v):
    return (dot(u,v),abs(cross(u,v)))
def multiply(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def encode_pair(p): return [s(x) for x in p]
def positive_proportional(a,b): return cross(a,b)==0 and dot(a,b)>0

def make_certificate(data):
    p=parse(data); A,B,C,D,E=(p[k] for k in 'ABCDE')
    ab=sub(B,A); ac=sub(C,A); ba=sub(A,B); bc=sub(C,B)
    ca=sub(A,C); cb=sub(B,C); cd=sub(D,C); ce=sub(E,C)
    area=cross(ab,ac)
    if area==0: raise ValueError('nondegenerate triangle required')
    j=0 if bc[0]!=0 else 1
    t=cd[j]/bc[j]
    if t<=0 or any(cd[i]!=t*bc[i] for i in range(2)): raise ValueError('D must lie beyond C on BC')
    j=0 if ba[0]!=0 else 1
    u=ce[j]/ba[j]
    if u<=0 or any(ce[i]!=u*ba[i] for i in range(2)): raise ValueError('CE must have direction BA')
    # Interior ray is checked separately, not inferred from angle magnitudes.
    whole=cross(ca,cd)
    if cross(ca,ce)*whole<=0 or cross(ce,cd)*whole<=0:
        raise ValueError('CE must be strictly inside exterior angle ACD')
    alpha=pair(ab,ac); beta=pair(ba,bc); gamma=pair(ca,cb)
    left=pair(ca,ce);right=pair(ce,cd);exterior=pair(ca,cd)
    ab_sum=multiply(alpha,beta); split_sum=multiply(left,right)
    total=multiply(ab_sum,gamma)
    if not positive_proportional(alpha,left) or not positive_proportional(beta,right):
        raise ValueError('angle transfer failed')
    if not positive_proportional(ab_sum,exterior) or not positive_proportional(split_sum,exterior):
        raise ValueError('exterior angle addition failed')
    if total[1]!=0 or total[0]>=0: raise ValueError('total angle failed')
    return {'schema':1,'input':json.loads(canonical(data)),
            'input_sha256':hashlib.sha256(canonical(data).encode()).hexdigest(),
            'area_cross':s(area),'scales':{'extension':s(t),'parallel_ray':s(u)},
            'angles':{k:encode_pair(v) for k,v in [('A',alpha),('B',beta),('C',gamma),('ACE',left),('ECD',right),('ACD',exterior)]},
            'products':{'A_plus_B':encode_pair(ab_sum),'split_exterior':encode_pair(split_sum),'A_plus_B_plus_C':encode_pair(total)},
            'conclusion':{'ray_inside_exterior':True,'exterior_equals_A_plus_B':True,'triangle_sum_two_right_angles':True}}

def strict_equal(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict: return set(a)==set(b) and all(strict_equal(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(strict_equal(x,y) for x,y in zip(a,b))
    if type(a) in (str,int,bool,type(None)): return a==b
    return False

def verify_certificate(expected_input,certificate):
    try: return strict_equal(make_certificate(expected_input),certificate)
    except (ValueError,TypeError,OverflowError): return False
