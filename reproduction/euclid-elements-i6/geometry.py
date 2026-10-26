"""Original exact rational teaching model for Elements I.6; not a ruler/compass engine."""
from fractions import Fraction as F

def rational(x):
    if isinstance(x, bool) or not isinstance(x, (int, F)):
        raise TypeError('only integers and Fraction values are accepted')
    return F(x)

def point(p):
    if not isinstance(p, (tuple, list)) or len(p) != 2:
        raise TypeError('a point has two rational coordinates')
    return tuple(rational(x) for x in p)

def sub(a,b):
    a,b=point(a),point(b)
    return (a[0]-b[0],a[1]-b[1])

def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def norm2(v): return dot(v,v)
def distance2(a,b): return norm2(sub(a,b))
def signed_double_area(a,b,c): return cross(sub(b,a),sub(c,a))
def sign(x): return (x>0)-(x<0)

def angle_equal(u,v,w,z):
    """Equality of ordinary angles in [0,pi]; reject zero rays, preserve cosine sign."""
    u,v,w,z=map(point,(u,v,w,z))
    a,b,c,d=map(norm2,(u,v,w,z))
    if not all((a,b,c,d)): raise ValueError('zero ray')
    p,q=dot(u,v),dot(w,z)
    return sign(p)==sign(q) and p*p*c*d==q*q*a*b

def base_angles_equal(a,b,c):
    return angle_equal(sub(a,b),sub(c,b),sub(a,c),sub(b,c))

def triangle_certificate(a,b,c):
    a,b,c=map(point,(a,b,c))
    area=signed_double_area(a,b,c)
    if not area: raise ValueError('nondegenerate triangle required')
    angles=base_angles_equal(a,b,c)
    sides=distance2(a,b)==distance2(a,c)
    return dict(base_angles_equal=angles, opposite_sides_equal=sides,
                implication_holds=(not angles or sides))

def strict_cut_certificate(a,b,c,d):
    """Check AB>AC and DB=AC with D strictly inside AB, never assume equal base angles.
    Area ratio is a modern certificate of a proper subtriangle, not the ancient proof's definition.
    """
    a,b,c,d=map(point,(a,b,c,d))
    area=signed_double_area(a,b,c)
    if not area: raise ValueError('nondegenerate triangle required')
    ab=sub(b,a); ad=sub(d,a); l2=norm2(ab)
    t=dot(ad,ab)/l2
    on_line=cross(ad,ab)==0
    inside=on_line and 0<t<1
    longer=distance2(a,b)>distance2(a,c)
    cut=distance2(d,b)==distance2(a,c)
    ratio=signed_double_area(d,b,c)/area
    angles=base_angles_equal(a,b,c)
    valid=inside and longer and cut
    return dict(on_line=on_line,strict_inside=inside,AB_longer_AC=longer,
                DB_equals_AC=cut,valid_cut=valid,area_ratio=ratio,
                proper_area=(0<ratio<1),base_angles_equal=angles,
                contradiction_premises=valid and angles)

def cut_from_rational_ratio(a,b,c,r):
    """Given exact r=AC/AB in (0,1), form D=A+(1-r)(B-A)."""
    a,b,c=map(point,(a,b,c)); r=rational(r)
    if not 0<r<1: raise ValueError('strict length ratio required')
    if not signed_double_area(a,b,c): raise ValueError('nondegenerate triangle required')
    if r*r*distance2(a,b)!=distance2(a,c): raise ValueError('ratio is not AC/AB')
    return tuple(a[i]+(1-r)*(b[i]-a[i]) for i in range(2))

def factor_certificate(x,y,z):
    """For positive strict-triangle side lengths AC=x, AB=y, BC=z; rational subset only."""
    x,y,z=map(rational,(x,y,z))
    if min(x,y,z)<=0 or not (x+y>z and x+z>y and y+z>x):
        raise ValueError('positive strict triangle inequalities required')
    # Positive denominators removed from cos(B)=cos(C).
    lhs=x*(y*y+z*z-x*x)-y*(x*x+z*z-y*y)
    rhs=(y-x)*((x+y)**2-z*z)
    return dict(identity_holds=lhs==rhs,angle_equation=lhs==0,
                strict_factor_positive=((x+y)**2-z*z)>0,
                equal_sides=x==y, implication_holds=lhs!=0 or x==y)
