"""Exact correspondence and invariants; explanatory model for Euclid VI.21."""
from fractions import Fraction as Q

REFERENCE = ((0,0),(4,0),(1,2))


def distance2(a,b):
    return sum((x-y)**2 for x,y in zip(a,b))


def is_boundary_order(order):
    n=len(order)
    return n>=3 and any(tuple((start+step*i)%n for i in range(n))==tuple(order)
                        for start in range(n) for step in (-1,1))


def label_map(reference_to_a, reference_to_b):
    """Return a positional map A→B by composing (C→B) ∘ (C→A)^(-1)."""
    if len(reference_to_a)!=len(reference_to_b) or not all(
        is_boundary_order(order) for order in (reference_to_a,reference_to_b)
    ):
        raise ValueError("both label maps must be cyclic or reversed boundary orders")
    out=[None]*len(reference_to_a)
    for i,j in zip(reference_to_a,reference_to_b):
        out[i]=j
    return tuple(out)


def squared_scale(a,b,mapping):
    """Check all labelled distances, not just adjacent edges; return scale² or None."""
    if len(a)!=len(b) or len(a)!=len(mapping) or not is_boundary_order(mapping):
        raise ValueError("vertex arrays and boundary map disagree")
    if len(set(a))!=len(a) or len(set(b))!=len(b):
        raise ValueError("vertices must be distinct")
    s=Q(distance2(b[mapping[0]],b[mapping[1]]),distance2(a[0],a[1]))
    for i in range(len(a)):
        for j in range(i):
            if distance2(b[mapping[i]],b[mapping[j]])!=s*distance2(a[i],a[j]):
                return None
    return s


def reorder(points, mapping):
    out=[None]*len(points)
    for i,j in enumerate(mapping):
        out[j]=points[i]
    return tuple(out)


def worked():
    c=REFERENCE
    ca,cb=(1,2,0),(0,2,1)
    a=reorder(tuple((10-2*y,1+2*x) for x,y in c),ca)
    b=reorder(tuple((-3+Q(x,2),5-Q(y,2)) for x,y in c),cb)
    return c,a,b,ca,cb


def transform(vertices,k,rot,shift,sign):
    u,v=rot
    if u*u+v*v!=1 or k<=0 or sign not in (-1,1):
        raise ValueError("positive scale, unit rotation, and orientation required")
    return tuple((shift[0]+k*(u*x-sign*v*y),shift[1]+k*(v*x+sign*u*y))
                 for x,y in vertices)


def wrong_angle_pair():
    return (((0,0),(5,0),(5,5),(0,5)),((0,0),(5,0),(8,4),(3,4)))


def wrong_ratio_pair():
    return (((0,0),(2,0),(2,1),(0,1)),((0,0),(3,0),(3,1),(0,1)))


def corner_dots(points):
    return tuple(sum((u-x)*(v-x) for u,v,x in zip(points[i-1],points[(i+1)%len(points)],p))
                 for i,p in enumerate(points))
