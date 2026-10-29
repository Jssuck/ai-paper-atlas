"""Euclid III.5: exact finite witnesses, not circle intersection construction."""
from fractions import Fraction
import json
import re


def rational(x):
    """Accept exact integers, Fraction or canonical rational strings only."""
    if type(x) is int or type(x) is Fraction:
        return Fraction(x)
    if type(x) is str and re.fullmatch(r'-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?', x):
        q = Fraction(x)
        if str(q) == x:
            return q
    raise ValueError('expected exact canonical rational, not bool or float')


def point(p):
    if type(p) not in (tuple, list) or len(p) != 2:
        raise ValueError('expected two coordinates')
    return tuple(rational(v) for v in p)


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), Fraction(0))


def distance_squared(a, b):
    v = sub(point(a), point(b))
    return dot(v, v)


def circle(O, r2):
    O = point(O); r2 = rational(r2)
    if r2 <= 0:
        raise ValueError('radius squared must be positive')
    return O, r2


def circle_relation(O1, r1_squared, O2, r2_squared):
    """Only decide concentric cases; nonconcentric intersection is unresolved."""
    O1, r1 = circle(O1, r1_squared); O2, r2 = circle(O2, r2_squared)
    if O1 == O2:
        return 'coincident' if r1 == r2 else 'concentric-disjoint'
    return 'different-centers-unresolved'


def certificate(O1, r1_squared, O2, r2_squared, P):
    """Verify a supplied common point, not discover it or classify contact."""
    O1, r1 = circle(O1, r1_squared); O2, r2 = circle(O2, r2_squared); P = point(P)
    d1 = distance_squared(P, O1); d2 = distance_squared(P, O2)
    if d1 != r1 or d2 != r2:
        raise ValueError('point must lie on both positive-radius circles')
    delta = sub(O2, O1)
    lhs = 2 * dot(P, delta)
    rhs = dot(O2, O2) - dot(O1, O1) + r1 - r2
    same = O1 == O2
    # This equality follows by subtracting the two squared-distance equations.
    if lhs != rhs or (same and r1 != r2):
        raise ArithmeticError('inconsistent exact identity')
    return {
        'input': {'O1': list(map(str, O1)), 'r1_squared': str(r1),
                  'O2': list(map(str, O2)), 'r2_squared': str(r2), 'P': list(map(str, P))},
        'classification': 'coincident' if same else 'distinct-common-point',
        'same_center': same, 'same_radius_squared': r1 == r2,
        'distinct_circles': not same,
        'center_distance_squared': str(dot(delta, delta)),
        'point_distances_squared': [str(d1), str(d2)],
        'linear_lhs': str(lhs), 'linear_rhs': str(rhs),
        'scope': 'one supplied common point; crossing versus tangency not classified'
    }


def verify(c):
    """Strict canonical JSON equality avoids bool == int confusion."""
    if type(c) is not dict or type(c.get('input')) is not dict:
        return False
    try:
        i = c['input']
        expected = certificate(i['O1'], i['r1_squared'], i['O2'], i['r2_squared'], i['P'])
        return json.dumps(c, sort_keys=True, allow_nan=False) == json.dumps(expected, sort_keys=True, allow_nan=False)
    except (ValueError, TypeError, KeyError, OverflowError):
        return False


EXAMPLES = {
    'crossing_upper': ((-3,0),25,(3,0),25,(0,4)),
    'crossing_lower': ((-3,0),25,(3,0),25,(0,-4)),
    'external_tangent': ((0,0),1,(2,0),1,(1,0)),
    'internal_tangent': ((0,0),25,(3,0),4,(5,0)),
    'coincident': ((0,0),25,(0,0),25,(3,4)),
}


def transformed(args, scale=1, shift=(0,0), quarter_turns=0, reflect=False):
    scale = rational(scale); shift = point(shift)
    if scale == 0:
        raise ValueError('nonzero scale required')
    if type(quarter_turns) is not int or type(reflect) is not bool:
        raise ValueError('invalid transformation controls')
    def f(p):
        x,y = point(p)
        if reflect: x = -x
        for _ in range(quarter_turns % 4): x,y = -y,x
        return scale*x+shift[0], scale*y+shift[1]
    o1,r1,o2,r2,p = args
    return f(o1),rational(r1)*scale*scale,f(o2),rational(r2)*scale*scale,f(p)


def grid():
    for args in EXAMPLES.values():
        for s in (1,2,-1,Fraction(1,3),-2):
            for t in ((0,0),(2,-3),(Fraction(1,2),Fraction(-2,3))):
                for k in range(4):
                    for reflection in (False,True):
                        yield transformed(args,s,t,k,reflection)
