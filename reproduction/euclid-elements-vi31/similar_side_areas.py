"""VI.31: exact projected lengths and areas of corresponding side figures."""
from fractions import Fraction as Q

TEMPLATE=((0,0),(1,0),(Q(6,5),Q(1,2)),(Q(1,4),Q(3,4)))


def sub(a,b):
    return a[0]-b[0],a[1]-b[1]


def dot(a,b):
    return a[0]*b[0]+a[1]*b[1]


def triangle(u,v,scale=1):
    if min(u,v,scale)<=0 or u==v:
        raise ValueError("positive distinct parameters and positive scale required")
    g,h,w=abs(u*u-v*v)*scale,2*u*v*scale,(u*u+v*v)*scale
    return ((Q(g*g,w),Q(g*h,w)),(0,0),(w,0))


def projection(a,b,c):
    bc=sub(c,b)
    amount=Q(dot(sub(a,b),bc),dot(bc,bc))
    return b[0]+amount*bc[0],b[1]+amount*bc[1]


def place(template,start,end,sign=1):
    if sign not in (-1,1) or start==end:
        raise ValueError("orientation ±1 and distinct base endpoints required")
    dx,dy=sub(end,start)
    return tuple((start[0]+s*dx-sign*t*dy,start[1]+s*dy+sign*t*dx) for s,t in template)


def area(p):
    return Q(abs(sum(x*v-y*u for (x,y),(u,v) in zip(p,p[1:]+p[:1]))),2)


def area_three(a,b,c,shape=TEMPLATE,sign=1):
    return tuple(area(place(shape,u,v,sign)) for u,v in ((b,a),(a,c),(b,c)))
