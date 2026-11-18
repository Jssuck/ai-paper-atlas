"""Exact rational teaching model for Euclid III.26; not a formal proof assistant."""
from dataclasses import dataclass
from fractions import Fraction as F


def rational(x):
    if isinstance(x, bool) or not isinstance(x, (int, F)):
        raise TypeError("Only int and Fraction inputs are accepted")
    return F(x)


def point(p):
    if not isinstance(p, (tuple, list)) or len(p) != 2:
        raise TypeError("A point must have exactly two rational coordinates")
    return tuple(rational(x) for x in p)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def scale(k, a):
    return (k * a[0], k * a[1])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def unit(t):
    """Rational unit-circle point, t = tan(theta/2); omit (-1,0)."""
    t = rational(t)
    d = 1 + t*t
    return ((1-t*t)/d, 2*t/d)


@dataclass(frozen=True)
class Arc:
    center: tuple
    radius: F
    start: tuple
    end: tuple
    ccw: bool = True

    def __post_init__(self):
        object.__setattr__(self, "center", point(self.center))
        object.__setattr__(self, "radius", rational(self.radius))
        object.__setattr__(self, "start", point(self.start))
        object.__setattr__(self, "end", point(self.end))
        if type(self.ccw) is not bool:
            raise TypeError("ccw must be bool")
        if self.radius <= 0:
            raise ValueError("radius must be positive")
        if self.start == self.end:
            raise ValueError("distinct arc endpoints are required")
        for p in (self.start, self.end):
            if dot(sub(p,self.center),sub(p,self.center)) != self.radius**2:
                raise ValueError("endpoint is not on the circle")

    def vectors(self):
        return tuple(scale(1/self.radius, sub(p,self.center))
                     for p in (self.start, self.end))

    def sweep_key(self):
        """(minor/semicircle/major, cos sweep); exact on 0 < sweep < 2pi."""
        u, v = self.vectors()
        s = cross(u,v) * (1 if self.ccw else -1)
        return (("minor" if s > 0 else "major" if s < 0 else "semicircle"), dot(u,v))

    def half_sweep_cot(self):
        u, v = self.vectors()
        return cross(u,v) * (1 if self.ccw else -1) / (1-dot(u,v))

    def contains_open(self, p):
        p = point(p)
        w0 = sub(p,self.center)
        if dot(w0,w0) != self.radius**2:
            raise ValueError("point is not on the circle")
        if p in (self.start,self.end):
            return False
        u,v = self.vectors()
        w = scale(1/self.radius,w0)
        if not self.ccw:
            u,v = v,u
        s = cross(u,v)
        if s > 0:
            return cross(u,w)>0 and cross(w,v)>0
        if s < 0:
            return not (cross(v,w)>0 and cross(w,u)>0)
        return cross(u,w)>0

    def inscribed_cot(self, p):
        p = point(p)
        # Membership also validates the circle before checking the complement.
        on_target = self.contains_open(p)
        if p in (self.start,self.end):
            raise ValueError("angle vertex cannot be an endpoint")
        if on_target:
            raise ValueError("vertex must be outside the selected open arc")
        u,v = sub(self.start,p),sub(self.end,p)
        d = abs(cross(u,v))
        if d == 0:
            raise ValueError("degenerate inscribed angle")
        return dot(u,v)/d

    def congruent_to(self, other):
        if not isinstance(other, Arc):
            raise TypeError("other must be an Arc")
        return self.radius == other.radius and self.sweep_key() == other.sweep_key()

    def map_point_to(self, other, p):
        """Endpoint-preserving isometry when radii and selected sweeps match."""
        if not self.congruent_to(other):
            raise ValueError("arcs must have equal radii and equal selected sweeps")
        p = point(p)
        u,_ = self.vectors()
        v,_ = other.vectors()
        n = (-u[1],u[0])
        m = (-v[1],v[0])
        q = sub(p,self.center)
        orientation = 1 if self.ccw == other.ccw else -1
        return add(other.center,add(scale(dot(q,u),v),scale(orientation*dot(q,n),m)))


def make_arc(radius=1, t=1, center=(0,0), rotation=(1,0), ccw=True):
    """Convenience factory; t=None selects the antipodal endpoint."""
    r = rational(radius)
    c = point(center)
    u = point(rotation)
    if dot(u,u) != 1:
        raise ValueError("rotation must be a rational unit vector")
    v = (F(-1),F(0)) if t is None else unit(t)
    end = (u[0]*v[0]-u[1]*v[1],u[1]*v[0]+u[0]*v[1])
    return Arc(c,r,add(c,scale(r,u)),add(c,scale(r,end)),ccw)
