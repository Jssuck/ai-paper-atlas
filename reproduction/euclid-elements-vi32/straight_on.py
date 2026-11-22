"""VI.32: correspondence, ray orientation, and the order B–C–E."""
from fractions import Fraction as Q


def sub(a,b):
    return a[0]-b[0],a[1]-b[1]


def add(a,b):
    return a[0]+b[0],a[1]+b[1]


def mul(k,v):
    return k*v[0],k*v[1]


def det(u,v):
    return u[0]*v[1]-u[1]*v[0]


def dot(u,v):
    return u[0]*v[0]+u[1]*v[1]


def data(a,b,c,d,e):
    """Exact diagnostics; assumes neither triangle is degenerate."""
    ab,ac,dc,de=sub(b,a),sub(c,a),sub(c,d),sub(e,d)
    if not det(ab,ac) or not det(dc,de):
        raise ValueError("two nondegenerate triangles required")
    cb,ce=sub(b,c),sub(e,c)
    return {
        "pairs_parallel": (det(ab,dc)==0,det(ac,de)==0),
        "pairs_codirected": (det(ab,dc)==0 and dot(ab,dc)>0,
                             det(ac,de)==0 and dot(ac,de)>0),
        "length_ratio": dot(ab,ab)*dot(de,de)==dot(ac,ac)*dot(dc,dc),
        "det": det(sub(c,b),ce),
        "straight_on": det(cb,ce)==0 and dot(cb,ce)<0,
    }


def construct(a,b,c,k,dsign=1,esign=1):
    """Generate D,E on the required or diagnostic reversed rays."""
    k=Q(k)
    if k<=0 or dsign not in (-1,1) or esign not in (-1,1):
        raise ValueError("positive scale and directions ±1 required")
    d=sub(c,mul(dsign*k,sub(b,a)))
    e=add(d,mul(esign*k,sub(c,a)))
    return d,e
