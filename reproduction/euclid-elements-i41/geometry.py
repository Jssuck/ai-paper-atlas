"""Original rational-coordinate teaching checker for Elements I.41.
Not a formalization of Euclid's axioms; finite runs do not prove a theorem.
"""
from fractions import Fraction
import json

NAMES = ('A', 'B', 'C', 'D', 'E')

def number(x):
    if type(x) is int:
        return Fraction(x)
    if type(x) is str:
        try:
            q = Fraction(x)
        except (ValueError, ZeroDivisionError):
            raise ValueError('invalid rational') from None
        if str(q) == x:
            return q
    raise ValueError('coordinate must be integer or canonical rational string')

def parse(data):
    if type(data) is not dict or set(data) != set(NAMES):
        raise ValueError('expected exactly A B C D E')
    out = {}
    for k in NAMES:
        p = data[k]
        if type(p) is not list or len(p) != 2:
            raise ValueError('point must be a two-element list')
        out[k] = tuple(number(x) for x in p)
    return out

def sub(a,b): return (a[0]-b[0], a[1]-b[1])
def add(a,b): return (a[0]+b[0], a[1]+b[1])
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def area2(a,b,c): return abs(det(sub(b,a), sub(c,a)))
def polygon2(points):
    return abs(sum(det(p,points[(i+1)%len(points)]) for i,p in enumerate(points)))

def validate(data):
    p = parse(data)
    a,b,c,d,e = (p[k] for k in NAMES)
    u,w = sub(c,b),sub(a,b)
    if u == (0,0): raise ValueError('zero base BC')
    if det(u,w) == 0: raise ValueError('degenerate parallelogram')
    if d != add(a,u): raise ValueError('ABCD is not the specified parallelogram')
    if det(u,sub(e,a)) != 0: raise ValueError('E is not on upper supporting line AD')
    return p

def make_certificate(data):
    p = validate(data)
    a,b,c,d,e = (p[k] for k in NAMES)
    u = sub(c,b)
    t = sub(e,a)[0]/u[0] if u[0] else sub(e,a)[1]/u[1]
    abc,acd,ebc = area2(a,b,c),area2(a,c,d),area2(e,b,c)
    quad = polygon2([a,b,c,d])
    # Explicit checks survive python -O and -OO.
    if not (abc == acd == ebc and quad == abc+acd == 2*ebc):
        raise ArithmeticError('coordinate identity inconsistent')
    return {
      'schema':'euclid-i41-v1',
      'points':{k:[str(x) for x in p[k]] for k in NAMES},
      'upper_parameter':str(t),
      'upper_position':('E=A' if t==0 else 'E=D' if t==1 else 'inside AD' if 0<t<1 else 'outside AD'),
      'double_areas':{'ABC':str(abc),'ACD':str(acd),'EBC':str(ebc),'ABCD':str(quad)},
      'chain':['I.37: area ABC = area EBC','I.34: area ABC = area ACD','partition: area ABCD = area ABC + area ACD','substitution: area ABCD = 2 * area EBC'],
      'model_note':'Modern rational coordinates check instances; chain labels are not a formal proof kernel.'
    }

def json_tree(x, seen=None):
    if type(x) is str: return True
    if type(x) not in (list,dict): return False
    if seen is None: seen=set()
    if id(x) in seen: return False
    seen.add(id(x))
    if type(x) is dict:
        ok=all(type(k) is str and json_tree(v,seen) for k,v in x.items())
    else: ok=all(json_tree(v,seen) for v in x)
    seen.remove(id(x))
    return ok

def verify_certificate(data, certificate):
    try:
        if not json_tree(certificate): return False
        return certificate == make_certificate(data)
    except (ValueError, TypeError, RecursionError, ArithmeticError):
        return False
