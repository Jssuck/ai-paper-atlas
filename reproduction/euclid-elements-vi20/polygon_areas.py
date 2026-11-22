"""VI.20 teaching: corresponding fans and exact polygon areas."""
from fractions import Fraction as Q

SOURCE = ((0,0), (4,0), (5,2), (3,5), (0,4))
CONCAVE = ((0,0), (4,0), (4,4), (2,1), (0,4))


def sub(a, b):
    return (a[0]-b[0], a[1]-b[1])


def cross(a, b):
    return a[0]*b[1]-a[1]*b[0]


def double_triangle(a, b, c):
    return cross(sub(b, a), sub(c, a))


def double_polygon(vertices):
    return sum(cross(u,v) for u,v in zip(vertices, vertices[1:]+vertices[:1]))


def fan(vertices, anchor=-1):
    i = anchor % len(vertices)
    rotated = vertices[i:]+vertices[:i]
    return tuple((rotated[0], a,b) for a,b in zip(rotated[1:],rotated[2:]))


def side_squares(vertices):
    return tuple(sum(c*c for c in sub(u,v))
                 for u,v in zip(vertices,vertices[1:]+vertices[:1]))


def similarity(point, k, rotation, shift, reflected=False):
    x,y = point
    u,v = rotation
    if k <= 0 or u*u+v*v != 1:
        raise ValueError("positive scale and unit rotation required")
    if reflected:
        y = -y
    return (shift[0]+k*(u*x-v*y), shift[1]+k*(v*x+u*y))


def intersection(a,b,c,d):
    """Exact proper interior crossing of segments AB and CD."""
    u,v,w = sub(b,a),sub(d,c),sub(c,a)
    denominator = cross(u,v)
    if not denominator:
        raise ValueError("parallel or coincident lines")
    s,t = Q(cross(w,v), denominator), Q(cross(w,u), denominator)
    if not (0<s<1 and 0<t<1):
        raise ValueError("not a proper interior crossing")
    return (a[0]+s*u[0],a[1]+s*u[1])


def worked_map(p):
    return similarity(p, Q(3,2), (0,1), (11,-3))


def worked():
    return SOURCE, tuple(worked_map(p) for p in SOURCE)


def grid():
    shapes = (SOURCE, ((0,0),(4,0),(3,2),(1,3),(-2,2)),
              ((0,0),(4,0),(5,2),(4,4),(2,5),(0,3)))
    for p in shapes:
        for k in (Q(1,2), Q(1), Q(3,2), Q(7,3)):
            for rot in ((1,0),(0,1),(Q(3,5),Q(4,5))):
                for shift in ((0,0),(Q(2,7),Q(-4,3))):
                    for ref in (False,True):
                        q=tuple(similarity(x,k,rot,shift,ref) for x in p)
                        yield p,q,k,ref
