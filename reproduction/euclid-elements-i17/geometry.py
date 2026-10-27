"""Exact rational teaching model for I.17; not a formal Euclidean proof."""
import json
from fractions import Fraction as F

def scalar(x):
    if type(x) is int: return F(x)
    if type(x) is str:
        try: return F(x)
        except (ValueError, ZeroDivisionError): pass
    raise ValueError('coordinate must be an integer or rational string')

def point(p):
    if type(p) is not list or len(p)!=2: raise ValueError('point must be a two-item list')
    return tuple(scalar(x) for x in p)

def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def dot(u,v): return u[0]*v[0]+u[1]*v[1]
def cross(u,v): return u[0]*v[1]-u[1]*v[0]
def q(x): return str(x.numerator) if x.denominator==1 else f'{x.numerator}/{x.denominator}'
def angle(u,v): return (dot(u,v),abs(cross(u,v)))
def encode(a): return [q(x) for x in a]

def strict_json(value):
    def validate(x):
        if x is None or type(x) in (str,int,bool): return
        if type(x) is list:
            for y in x: validate(y)
            return
        if type(x) is dict and all(type(k) is str for k in x):
            for y in x.values(): validate(y)
            return
        raise ValueError('noncanonical JSON type')
    validate(value)
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)

def construct(payload):
    if type(payload) is not dict or set(payload)!= {'A','B','C'}: raise ValueError('exactly A B C required')
    pts={k:point(payload[k]) for k in 'ABC'}
    area=cross(sub(pts['B'],pts['A']),sub(pts['C'],pts['A']))
    if not area: raise ValueError('nondegenerate triangle required')
    pairs={}
    for a,b in [('A','B'),('B','C'),('C','A')]:
        third=next(k for k in 'ABC' if k not in (a,b))
        # At b, extend the side from third through b. This yields an exterior
        # supplement to interior angle b. I.16 compares it to remote angle a.
        alpha=angle(sub(pts[b],pts[a]),sub(pts[third],pts[a]))
        beta=angle(sub(pts[a],pts[b]),sub(pts[third],pts[b]))
        exterior=(-beta[0],beta[1])
        larger=alpha[0]*exterior[1]-alpha[1]*exterior[0]
        sine_sum=alpha[1]*beta[0]+alpha[0]*beta[1]
        # Both angles are strictly between 0 and pi; their sum is in (0,2pi).
        # A positive unnormalized sine therefore selects the interval (0,pi).
        if not (larger>0 and sine_sum==larger): raise ArithmeticError('exact inequality failed')
        pairs[a+b]={'alpha':encode(alpha),'beta':encode(beta),'external_at_second':encode(exterior),
                    'external_minus_remote_sine_numerator':q(larger),'pair_sum_sine_numerator':q(sine_sum),
                    'external_gt_remote':True,'pair_sum_lt_two_right_angles':True}
    return {'schema':1,'input':{k:encode(pts[k]) for k in 'ABC'},'oriented_double_area':q(area),'pairs':pairs,
            'conclusion':'All three pairs have sum strictly below two right angles in this rational Euclidean model.'}

def verify(payload,certificate):
    try: return strict_json(certificate)==strict_json(construct(payload))
    except (ValueError,TypeError,ArithmeticError,OverflowError): return False

def ledger(alpha,beta,exterior,right=1):
    """Abstract ordered angle quantities: I.16 plus I.13, not a triangle API."""
    a,b,e,r=map(scalar,(alpha,beta,exterior,right))
    if not (r>0 and 0<a<e and b>0 and b+e==2*r): raise ValueError('I.16/I.13 premises required')
    return {'sum':q(a+b),'two_right_angles':q(2*r),'strict_gap':q(e-a),'conclusion':a+b<2*r}
