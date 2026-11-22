"""VI.26: exact side correspondences and a competing diagonal corner."""
from fractions import Fraction as Q

U,V=(6,0),(2,4)


def add(a,b):
    return a[0]+b[0],a[1]+b[1]


def sub(a,b):
    return a[0]-b[0],a[1]-b[1]


def mul(k,a):
    return k*a[0],k*a[1]


def cross(a,b):
    return a[0]*b[1]-a[1]*b[0]


def norm2(a):
    return a[0]**2+a[1]**2


def area(vertices):
    return Q(abs(sum(cross(a,b) for a,b in zip(vertices,vertices[1:]+vertices[:1]))),2)


def construct(u,v,s,t,a=(0,0)):
    """Return A B C D E F G H K in that fixed label order."""
    s,t=Q(s),Q(t)
    if not cross(u,v) or not (0<s<1 and 0<t<1):
        raise ValueError("independent edges and strictly interior scales required")
    b,c,d=add(a,u),add(a,add(u,v)),add(a,v)
    e,g=add(a,mul(s,u)),add(a,mul(t,v))
    f=add(e,mul(t,v))
    h,k=add(a,mul(t,add(u,v))),add(a,mul(t,u))
    return a,b,c,d,e,f,g,h,k


def side_ratios2(a,b,d,e,g):
    return Q(norm2(sub(e,a)),norm2(sub(b,a))),Q(norm2(sub(g,a)),norm2(sub(d,a)))


def grid():
    values=(Q(1,7),Q(1,3),Q(1,2),Q(2,3),Q(6,7))
    for u,v in ((U,V),(V,U),((0,3),(-5,0)),((Q(5,3),2),(4,Q(-1,2)))):
        for origin in ((0,0),(Q(3,7),Q(-9,5))):
            for s in values:
                for t in values:
                    yield u,v,s,t,origin
