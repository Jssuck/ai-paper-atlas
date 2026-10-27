"""Exact finite coordinate checks for Euclid I.26; not a formal proof kernel."""
from fractions import Fraction
import hashlib
import json


def rational(text):
    if type(text) is not str:
        raise ValueError('rational coordinates must be canonical strings')
    try:
        result = Fraction(text)
    except (ValueError, ZeroDivisionError):
        raise ValueError('invalid rational') from None
    if str(result) != text:
        raise ValueError('noncanonical rational')
    return result


def triangle(value):
    if type(value) is not list or len(value) != 3:
        raise ValueError('triangle must have three vertices')
    points = []
    for point in value:
        if type(point) is not list or len(point) != 2:
            raise ValueError('point must have two coordinates')
        points.append(tuple(rational(x) for x in point))
    if cross(sub(points[1], points[0]), sub(points[2], points[0])) == 0:
        raise ValueError('degenerate triangle')
    return points


def sub(a, b):
    return (a[0]-b[0], a[1]-b[1])


def dot(a, b):
    return a[0]*b[0]+a[1]*b[1]


def cross(a, b):
    return a[0]*b[1]-a[1]*b[0]


def length2(a, b):
    v = sub(a, b)
    return dot(v, v)


def angle_key(points, vertex):
    """dot/absolute determinant; one-to-one on nondegenerate interior angles."""
    a = sub(points[(vertex+1) % 3], points[vertex])
    b = sub(points[(vertex+2) % 3], points[vertex])
    return dot(a, b)/abs(cross(a, b))


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False)


def strict_equal(a, b):
    """No bool==int, tuple==list, extra fields, or non-string object keys."""
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return (all(type(k) is str for k in a) and a.keys() == b.keys()
                and all(strict_equal(a[k], b[k]) for k in a))
    if type(a) is list:
        return len(a) == len(b) and all(strict_equal(x, y) for x, y in zip(a, b))
    if type(a) in (str, int, bool, type(None)):
        return a == b
    return False


def make_certificate(data):
    if type(data) is not dict or set(data) != {'triangle_1', 'triangle_2', 'side_case'}:
        raise ValueError('invalid input fields')
    if type(data['side_case']) is not str or data['side_case'] not in ('included', 'opposite'):
        raise ValueError('unknown side case')
    p, q = triangle(data['triangle_1']), triangle(data['triangle_2'])
    k, l = [angle_key(p, i) for i in range(3)], [angle_key(q, i) for i in range(3)]
    if k[1:] != l[1:]:
        raise ValueError('corresponding B/E and C/F angles must agree')
    edges = [(0, 1), (1, 2), (0, 2)]
    a, b = [[length2(t[i], t[j]) for i, j in edges] for t in (p, q)]
    given_edge = 1 if data['side_case'] == 'included' else 0
    if a[given_edge] != b[given_edge]:
        raise ValueError('specified corresponding side must agree')
    # Explicitly calculate the conclusion; do not replace this with a true flag.
    if a != b or k[0] != l[0]:
        raise ValueError('conclusion failed in coordinate model')
    copied = json.loads(canonical(data))
    return {'schema': 1, 'input': copied,
            'input_sha256': hashlib.sha256(canonical(data).encode()).hexdigest(),
            'angle_keys': [[str(x) for x in row] for row in (k, l)],
            'squared_sides_AB_BC_AC': [[str(x) for x in row] for row in (a, b)],
            'given_edge_index': given_edge,
            'conclusion': 'three corresponding sides and remaining angles equal'}


def verify_certificate(expected_input, certificate):
    """Caller supplies the expected input independently, never only the certificate."""
    try:
        rebuilt = make_certificate(expected_input)
        return strict_equal(rebuilt, certificate)
    except (ValueError, TypeError, KeyError, ZeroDivisionError, OverflowError):
        return False
