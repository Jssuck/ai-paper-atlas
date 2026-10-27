"""Exact modern Gram model for Euclid I.25; finite checking is not a proof."""
from fractions import Fraction as Q
import json
import math
import copy


def keys(x, wanted):
    if type(x) is not dict or set(x) != set(wanted):
        raise ValueError('unexpected object fields')


def rational(x):
    if type(x) is not list or len(x) != 2 or any(type(v) is not int for v in x):
        raise ValueError('rational must contain exactly two integers, not bool')
    n, d = x
    if d <= 0 or math.gcd(n, d) != 1:
        raise ValueError('rational must be reduced with positive denominator')
    return Q(n, d)


def pair(q):
    return [q.numerator, q.denominator]


def triangle(x):
    keys(x, ('a2', 'b2', 'dot'))
    a, b, d = (rational(x[k]) for k in ('a2','b2','dot'))
    if a <= 0 or b <= 0 or d*d >= a*b:
        raise ValueError('not a nondegenerate Euclidean Gram triangle')
    return a, b, d, a+b-2*d


def classify(data):
    keys(data, ('ABC','DEF'))
    a,b,d,c = triangle(data['ABC'])
    e,f,g,h = triangle(data['DEF'])
    if a != e or b != f:
        raise ValueError('corresponding adjacent sides are not equal')
    # Equal positive norm product: cosine and dot have the same order.
    # Cosine is strictly decreasing for interior angles in (0, pi).
    relation = 'greater' if d < g else 'equal' if d == g else 'less'
    return {'BC2':pair(c), 'EF2':pair(h), 'base_gap':pair(c-h),
            'dot_gap':pair(d-g), 'angle_relation':relation}


def certify(data):
    metric = classify(data)
    if rational(metric['base_gap']) <= 0:
        raise ValueError('I.25 requires BC > EF')
    return {'schema_version':1, 'input':copy.deepcopy(data), 'metric':metric,
            'branches':{
                'equal':{'lemma':'I.4','consequence':'BC = EF','contradiction':'BC > EF'},
                'less':{'lemma':'I.24','swap_triangles':True,'consequence':'BC < EF','contradiction':'BC > EF'},
                'remaining':'angle BAC > angle EDF',
                'order_assumption':'exactly one of less, equal, greater'},
            'scope':'modern Gram check plus original-proof dependency record'}


def strict_equal(x,y):
    if type(x) is not type(y): return False
    if type(x) is dict:
        return set(x)==set(y) and all(strict_equal(x[k],y[k]) for k in x)
    if type(x) is list:
        return len(x)==len(y) and all(strict_equal(a,b) for a,b in zip(x,y))
    return x==y


def verify(data, certificate):
    try:
        return strict_equal(certificate, certify(data))
    except (ValueError, TypeError, KeyError, OverflowError, RecursionError):
        return False


def load_json(text):
    def object_pairs(ps):
        result={}
        for k,v in ps:
            if k in result: raise ValueError('duplicate JSON key')
            result[k]=v
        return result
    def constant(x): raise ValueError('non-finite JSON constant')
    return json.loads(text, object_pairs_hook=object_pairs, parse_constant=constant)


def verify_json(data_text, certificate_text):
    try: return verify(load_json(data_text),load_json(certificate_text))
    except (ValueError, TypeError, RecursionError): return False
