"""Exact rational teaching checks for Euclid Elements III.37."""
from fractions import Fraction as Q
from math import isqrt

O = (0, 0)


def sub(a, b):
    return a[0]-b[0], a[1]-b[1]


def dot(a, b):
    return a[0]*b[0]+a[1]*b[1]


def sq(a):
    return dot(a, a)


def cross(a, b):
    return a[0]*b[1]-a[1]*b[0]


def points(*args):
    return tuple(tuple(map(Q, p)) for p in args)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sqrt_q(n):
    a, b = isqrt(n.numerator), isqrt(n.denominator)
    require(a*a == n.numerator and b*b == n.denominator,
            "reference construction needs a rational square root")
    return Q(a, b)


def reference_tangents(f, r, d):
    """Coordinate construction using only center, radius and exterior point."""
    f, d = points(f, d)
    r = Q(r)
    v = sub(d, f)
    m = sq(v)
    require(r > 0 and m > r*r, "reference needs exterior D and positive radius")
    beta = r * sqrt_q(m-r*r)
    x, y = v
    return tuple((f[0]+(r*r*x-sign*beta*y)/m,
                  f[1]+(r*r*y+sign*beta*x)/m) for sign in (1,-1))


def verify(f, r, d, c, a, b):
    """Verify givens before following the III.36, I.8 and III.16 chain."""
    f, d, c, a, b = points(f, d, c, a, b)
    r = Q(r)
    r2 = r*r
    fd = sub(d, f)
    require(r > 0 and sq(fd) > r2, "D must be exterior; radius must be positive")
    require(sq(sub(c, f)) == sq(sub(a, f)) == r2, "secant endpoints must be on circle")
    dc, da = sub(c, d), sub(a, d)
    # dot(dc, da) equals the product of lengths only after these order tests.
    product = dot(dc, da)
    require(cross(dc, da) == 0 and 0 < sq(dc) < product < sq(da), "require D-C-A in order")
    db = sub(d, b)
    require(sq(db) == product, "candidate square does not equal secant product")
    fb = sub(b, f)
    require(sq(fb) == r2, "candidate endpoint B must lie on circle")

    e = next(e for e in reference_tangents(f, r, d) if e != b)
    fe, de = sub(e, f), sub(d, e)
    require(sq(fe) == r2 and dot(fe, de) == 0, "invalid reference tangency")
    # Independent III.36 output check at the already certified reference tangent.
    require(sq(de) == product, "III.36 reference equality failed")
    reference_sides = sq(de), sq(fe), sq(fd)
    candidate_sides = sq(db), sq(fb), sq(fd)
    require(reference_sides == candidate_sides, "SSS comparison failed")
    # Squared-distance polarization is the numerical analogue of I.8 here.
    derived = (sq(fd)-sq(db)-sq(fb))/2
    require(derived == 0 and dot(db, fb) == derived, "candidate radius must be perpendicular")
    return {"branch": "diameter" if cross(dc, fd) == 0 else "offset",
            "product": product, "reference": e, "squared_sides": candidate_sides,
            "candidate_dot": derived}


DIAMETER = (O, 5, (13,0), (5,0), (-5,0), (Q(25,13), Q(60,13)))
OFFSET = (O, 5, (5,3), (4,3), (-4,3), (5,0))
OFF_CIRCLE = OFFSET[:-1] + ((2,3),)


def sweep():
    """Generate ray endpoints by fixing one intersection then factoring."""
    counts = {"diameter": 0, "offset": 0}
    for f, r in (((0,0), 5), ((Q(1,2),Q(-2,3)), Q(7,4))):
        f, = points(f)
        for i in range(1, 9):
            # A vertical tangent gives rational tangent length, hence rational contacts.
            d = (f[0]+r, f[1]+r*Q(i,3))
            seen = set()
            for t in sorted({Q(k,j) for k in range(-8,9) for j in (1,2,3)}):
                a = (f[0]+r*(1-t*t)/(1+t*t), f[1]+r*2*t/(1+t*t))
                w = sub(a,d)
                s = (sq(sub(d,f))-r*r)/sq(w)
                if s == 1:
                    continue
                c = (d[0]+s*w[0], d[1]+s*w[1])
                near, far = (c,a) if s < 1 else (a,c)
                if (near, far) in seen:
                    continue
                seen.add((near, far))
                out = verify(f,r,d,near,far,(f[0]+r,f[1]))
                counts[out["branch"]] += 1
    counts[verify(*DIAMETER)["branch"]] += 1
    return counts


if __name__ == "__main__":
    for name, args in (("diameter",DIAMETER),("offset",OFFSET)):
        print(name, verify(*args))
    try:
        verify(*OFF_CIRCLE)
    except ValueError as exc:
        print("rejected:", exc)
    else:
        raise RuntimeError("counterexample was not rejected")
    print("finite sweep:", sweep())
