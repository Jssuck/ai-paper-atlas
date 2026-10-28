"""Exact rational-coordinate teaching reconstruction, not a formal Euclid proof."""
from fractions import Fraction as F
import json

def scalar(x):
    if type(x) is int: return F(x)
    if type(x) is str:
        try: y=F(x)
        except (ValueError,ZeroDivisionError): raise ValueError('invalid rational') from None
        if str(y)==x: return y
    raise ValueError('expected integer or canonical rational string')

def parse(data):
    if type(data) is not dict or set(data)!=set('ABCD'): raise ValueError('exact A B C D keys required')
    out={}
    for k,v in data.items():
        if type(v) is not list or len(v)!=2: raise ValueError('point must be a two-item list')
        out[k]=tuple(map(scalar,v))
    return out

def sub(p,q): return tuple(a-b for a,b in zip(p,q))
def dot(u,v): return sum(a*b for a,b in zip(u,v))
def cross(u,v): return u[0]*v[1]-u[1]*v[0]
def norm2(u): return dot(u,u)
def encode(x):
    if isinstance(x,F): return str(x)
    if type(x) in (tuple,list): return [encode(a) for a in x]
    if type(x) is dict: return {k:encode(v) for k,v in x.items()}
    return x

def make_certificate(data):
    p=parse(data);A,B,C,D=(p[k] for k in 'ABCD')
    u=sub(B,A);v=sub(D,C);w=sub(C,A);bc=sub(C,B)
    if not norm2(u) or not norm2(v): raise ValueError('zero base')
    if cross(u,v): raise ValueError('base directions not parallel')
    if not cross(u,w): raise ValueError('supporting lines must be distinct')
    if dot(u,v)<=0: raise ValueError('wrong endpoint correspondence: opposite direction')
    if norm2(u)!=norm2(v): raise ValueError('base lengths unequal')
    ac=sub(C,A);bd=sub(D,B)
    # Both SAS included angles have the same BC length and equal base lengths.
    sas_left=dot(sub(A,B),bc)
    sas_right=dot(sub(D,C),sub(B,C))
    conclusion={'AC_vector':ac,'BD_vector':bd,'AC_squared':norm2(ac),'BD_squared':norm2(bd),
                'connector_cross':cross(ac,bd),'connector_dot':dot(ac,bd),
                'connector_support_cross':cross(ac,sub(B,A))}
    return encode({'schema':'euclid-i33-exact-v1','input':p,
      'premises':{'AB':u,'CD':v,'AB_squared':norm2(u),'CD_squared':norm2(v),
                  'base_cross':cross(u,v),'base_dot':dot(u,v),'support_cross':cross(u,w)},
      'sas':{'BC_squared':norm2(bc),'included_dot_ABC':sas_left,'included_dot_DCB':sas_right},
      'conclusion':conclusion})

def json_value(x):
    if type(x) is str: return
    if type(x) is list:
        for y in x: json_value(y)
        return
    if type(x) is dict and all(type(k) is str for k in x):
        for y in x.values(): json_value(y)
        return
    raise ValueError('certificate values must be JSON strings, lists, and objects')

def verify_certificate(data,cert):
    try:
        expected=make_certificate(data);json_value(cert)
        return json.dumps(cert,sort_keys=True,ensure_ascii=False)==json.dumps(expected,sort_keys=True,ensure_ascii=False)
    except (ValueError,TypeError,OverflowError,RecursionError): return False
