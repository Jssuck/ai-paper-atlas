"""Exact rational teaching reconstruction of Elements III.9, not a proof assistant."""
from fractions import Fraction as F

def scalar(x):
    if isinstance(x, bool) or not isinstance(x, (int, str, F)):
        raise ValueError('expected exact integer, rational string, or Fraction')
    try:
        return F(x)
    except (ValueError, ZeroDivisionError):
        raise ValueError('invalid rational') from None

def point(p):
    if not isinstance(p, (list, tuple)) or len(p) != 2:
        raise ValueError('point needs two coordinates')
    return tuple(map(scalar,p))

def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def distance2(a,b): return dot(sub(a,b),sub(a,b))
def midpoint(a,b): return ((a[0]+b[0])/2,(a[1]+b[1])/2)
def encode(p): return [str(x) for x in p]

def triangle(points):
    if not isinstance(points,(list,tuple)) or len(points)!=3:
        raise ValueError('exactly three points required')
    a,b,c=map(point,points)
    if len({a,b,c})!=3: raise ValueError('points must be distinct')
    if cross(sub(b,a),sub(c,a))==0: raise ValueError('points must be noncollinear')
    return a,b,c

def circumcenter(points):
    a,b,c=triangle(points)
    u,v=sub(b,a),sub(c,a)
    rhs1=(dot(b,b)-dot(a,a))/2
    rhs2=(dot(c,c)-dot(a,a))/2
    det=cross(u,v)
    return ((rhs1*v[1]-u[1]*rhs2)/det,(u[0]*rhs2-rhs1*v[0])/det)

def make_certificate(points, candidate):
    a,b,c=triangle(points); d=point(candidate)
    r2=distance2(a,d)
    if distance2(b,d)!=r2 or distance2(c,d)!=r2:
        raise ValueError('candidate is not equidistant')
    e,f=midpoint(a,b),midpoint(b,c)
    # Normals, rather than D-E directions, describe bisectors even if D=E.
    normals=[sub(b,a),sub(c,b)]
    residuals=[dot(normals[0],sub(d,e)),dot(normals[1],sub(d,f))]
    return {'schema':1,'points':[encode(a),encode(b),encode(c)],'candidate':encode(d),
            'center':encode(circumcenter((a,b,c))),'radius_squared':str(r2),
            'midpoints':[encode(e),encode(f)],'bisector_normals':[encode(n) for n in normals],
            'bisector_residuals':[str(x) for x in residuals],
            'determinant':str(cross(*normals)),
            'zero_midpoint_directions':[d==e,d==f]}

def verify_certificate(cert):
    if not isinstance(cert,dict): return False
    try: expected=make_certificate(cert['points'],cert['candidate'])
    except (KeyError,ValueError,TypeError,OverflowError): return False
    # Type-strict equality prevents True==1 or False==0 from silently validating.
    import json
    try: return json.dumps(cert,sort_keys=True,allow_nan=False)==json.dumps(expected,sort_keys=True,allow_nan=False)
    except (TypeError,ValueError): return False

def certify_known_circle(points,candidate,known_center,radius_squared):
    a,b,c=triangle(points); o=point(known_center); r2=scalar(radius_squared)
    if r2<=0: raise ValueError('positive radius squared required')
    if any(distance2(p,o)!=r2 for p in (a,b,c)):
        raise ValueError('points are not on supplied circle')
    cert=make_certificate((a,b,c),candidate)
    if point(cert['center'])!=o: raise ValueError('circle center mismatch')
    return cert
