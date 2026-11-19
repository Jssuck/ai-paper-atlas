"""Exact coordinate certificates for Euclid III.35 and a signed extension."""
from fractions import Fraction as Q
from itertools import combinations
from functools import cmp_to_key


def add(a, b):
    return a[0]+b[0], a[1]+b[1]


def subtract(a, b):
    return a[0]-b[0], a[1]-b[1]


def scale(s, a):
    return s*a[0], s*a[1]


def dot(a, b):
    return a[0]*b[0]+a[1]*b[1]


def det(a, b):
    return a[0]*b[1]-a[1]*b[0]


def norm2(a):
    return dot(a, a)


def point(a):
    if len(a) != 2:
        raise ValueError("expected two coordinates")
    return Q(a[0]), Q(a[1])


def intersection(a, c, b, d):
    u, v = subtract(c, a), subtract(d, b)
    den = det(u, v)
    if den == 0:
        raise ValueError("expected distinct nonparallel support lines")
    between = subtract(b, a)
    s, t = Q(det(between, v))/den, Q(det(between, u))/den
    return add(a, scale(s, u)), s, t


def midpoint_witness(o, e, a, c):
    """Check both ingredients of the modern II.5/Pythagoras calculation."""
    u = subtract(c, a)
    m = scale(Q(1, 2), add(a, c))
    half_sq = norm2(subtract(a, m))
    offset_sq = norm2(subtract(e, m))
    return {
        "midpoint_normal": dot(subtract(o, m), u) == 0,
        "half_sq": half_sq,
        "offset_sq": offset_sq,
        "center_offset_sq": norm2(subtract(o, m)),
    }


def audit(o, r, a, c, b, d):
    """Return incidence, point order, products and midpoint witnesses separately."""
    o, a, c, b, d = map(point, (o, a, c, b, d))
    r = Q(r)
    if r <= 0:
        raise ValueError("radius must be positive")
    if len({a,c,b,d}) != 4:
        raise ValueError("expected four distinct endpoints")
    e, s, t = intersection(a, c, b, d)
    powers = (s*(s-1)*norm2(subtract(c, a)), t*(t-1)*norm2(subtract(d, b)))
    radial_power = norm2(subtract(e,o))-r*r
    same_circle = all(norm2(subtract(x,o)) == r*r for x in (a,c,b,d))
    interior = 0 < s < 1 and 0 < t < 1
    mids = (midpoint_witness(o,e,a,c), midpoint_witness(o,e,b,d))
    return {
        "point": e, "parameters": (s,t),
        "same_circle": same_circle, "inside_both_segments": interior,
        "iii35_premises": same_circle and interior,
        "unsigned_products": tuple(abs(x) for x in powers),
        "directed_products": powers, "radial_power": radial_power,
        "signed_match": powers[0] == powers[1] == radial_power,
        "midpoints": mids,
        "diameter_count": sum(m["center_offset_sq"] == 0 for m in mids),
        "perpendicular": dot(subtract(c,a), subtract(d,b)) == 0,
    }


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def cyclic_compare(a, b):
    """Counterclockwise order starting from positive x, no angle approximation."""
    ha, hb = (a[1]<0 or (a[1]==0 and a[0]<0)), (b[1]<0 or (b[1]==0 and b[0]<0))
    if ha != hb:
        return 1 if ha else -1
    return (det(a,b)<0)-(det(a,b)>0)


def circle_points(o, r):
    ts = {Q(i,j) for j in range(1,4) for i in range(-3,4)}
    offsets = {(r*(1-t*t)/(1+t*t), r*2*t/(1+t*t)) for t in ts}
    offsets.add((-r, 0))
    return [add(o,p) for p in sorted(offsets,key=cmp_to_key(cyclic_compare))]


def sweep():
    cases = [((0,0),1), ((2,-3),Q(7,3))]
    n, counts = 0, [0,0,0]
    perpendicular = 0
    for o,r in cases:
        pts = circle_points(o,r)
        for a,b,c,d in combinations(pts,4):
            s = audit(o,r,a,c,b,d)
            require(s["iii35_premises"] and s["signed_match"] and s["radial_power"]<0,
                    "interior intersecting chords failed")
            for m,u in zip(s["midpoints"], s["unsigned_products"]):
                require(m["midpoint_normal"] and m["half_sq"]-m["offset_sq"] == u
                        and m["half_sq"]+m["center_offset_sq"] == r*r,
                        "midpoint decomposition failed")
            n += 1
            counts[s["diameter_count"]] += 1
            perpendicular += s["perpendicular"]
    return len(pts), n, tuple(counts), perpendicular


EXAMPLES = {
    "center two diameters": ((-5,0),(5,0),(0,-5),(0,5)),
    "one diameter perpendicular": ((-5,0),(5,0),(3,-4),(3,4)),
    "neither diameter": ((-4,3),(4,3),(3,-4),(3,4)),
    "exterior supports": ((-5,0),(5,0),(3,4),(4,3)),
    "off-circle endpoint": ((-5,0),(5,0),(3,-4),(3,3)),
}


def main():
    for label,p in EXAMPLES.items():
        out = audit((0,0),5,*p)
        print(label, {k:out[k] for k in ("point","iii35_premises","unsigned_products",
                                        "directed_products","radial_power","signed_match")})
    pts,n,counts,orthogonal = sweep()
    print(f"points per circle: {pts}; two circles; interior configurations: {n}")
    print(f"diameter count 0/1/2: {counts}; perpendicular: {orthogonal}")


if __name__ == "__main__":
    main()
