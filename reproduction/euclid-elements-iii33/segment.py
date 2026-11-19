"""Exact rational teaching construction for Euclid III.33."""
from fractions import Fraction as F

def add(a, b): return tuple(x+y for x, y in zip(a, b, strict=True))
def sub(a, b): return tuple(x-y for x, y in zip(a, b, strict=True))
def scale(a, k): return tuple(k*x for x in a)
def dot(a, b): return sum(x*y for x, y in zip(a, b, strict=True))
def cross(a, b): return a[0]*b[1]-a[1]*b[0]
def rot(a): return -a[1], a[0]
def vector(a):
    x, y = a
    if not all(type(z) in (int, F) for z in (x, y)):
        raise TypeError("use integers or Fractions")
    return F(x), F(y)

def angle(a, b):
    if not dot(a,a) or not dot(b,b):
        raise ValueError("angle requires two nonzero vectors")
    return dot(a,b), abs(cross(a,b))

def same_angle(a, b):
    return cross(a,b) == 0 and dot(a,b) > 0

def construct(a, b, u, v):
    """The angle input is the ordinary angle between (1,0) and (u,v), v>0."""
    a, b, (u,v) = vector(a), vector(b), vector((u,v))
    d = sub(b,a)
    if not dot(d,d) or v <= 0:
        raise ValueError("distinct chord endpoints and v > 0 required")
    j = rot(d)
    t = add(scale(d,u),scale(j,v))
    middle = scale(add(a,b),F(1,2))
    if u == 0:
        center = middle
    else:
        # Intersect A + k*rot(t) with midpoint + h*j using cross product.
        normal = rot(t)
        center = add(a,scale(normal,cross(sub(middle,a),j)/cross(normal,j)))
    s = v/(abs(u)+v)
    def witness(sign):
        w = add(d,scale(j,sign*s))
        # Nonzero root of |A + k*w - O|² = |A - O|².
        k = 2*dot(sub(center,a),w)/dot(w,w)
        if k <= 0:
            raise RuntimeError("chosen secant ray does not enter the circle")
        return add(a,scale(w,k))
    return {"branch": "acute" if u>0 else "obtuse" if u<0 else "right",
            "center":center, "tangent":t, "alternate":witness(-1), "control":witness(1)}

def check(a, b, u, v, result):
    """Check the construction via independent incidence and angle predicates."""
    a, b, (u,v) = vector(a), vector(b), vector((u,v))
    d, o, t = sub(b,a), result["center"], result["tangent"]
    p, q = result["alternate"], result["control"]
    r = sub(a,o)
    r2 = dot(r,r)
    angle_input = (u,v)
    return {
        "unique_configuration_points": len({a,b,p,q}) == 4,
        "same_circle": r2>0 and all(dot(sub(x,o),sub(x,o))==r2 for x in (b,p,q)),
        "tangent": cross(d,t)>0 and dot(t,r)==0 and same_angle(angle(d,t),angle_input),
        "alternate_side": cross(d,t)*cross(d,sub(p,a)) < 0,
        "alternate_angle": same_angle(angle(sub(a,p),sub(b,p)),angle_input),
        "same_side": cross(d,t)*cross(d,sub(q,a)) > 0,
        "same_side_supplement": same_angle(angle(sub(a,q),sub(b,q)),(-u,v)),
        "same_side_equal_iff_right": same_angle(angle(sub(a,q),sub(b,q)),angle_input)==(u==0),
    }

def sweep():
    chords=[((0,0),(4,0)),((2,-1),(5,3)),((F(-1,3),2),(1,F(4,3)))]
    ratios={F(u,v) for u in range(-10,11) for v in range(1,9)}
    counts=dict(acute=0,right=0,obtuse=0)
    for a,b in chords:
        for u in sorted(ratios):
            result=construct(a,b,u,1)
            checks=check(a,b,u,1,result)
            if not all(checks.values()):
                raise RuntimeError((a,b,u,checks))
            counts[result["branch"]]+=1
    return counts

if __name__=="__main__":
    for u in (3,0,-3):
        out=construct((0,0),(4,0),u,4)
        print(out["branch"], "center", tuple(map(str,out["center"])),
              "alternate",tuple(map(str,out["alternate"])),
              check((0,0),(4,0),u,4,out))
    counts=sweep()
    print("exact cases:",sum(counts.values()),counts)
