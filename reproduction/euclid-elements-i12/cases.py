"""Finite teaching families; neither exhaustive nor a general theorem proof."""
from dataclasses import replace
from fractions import Fraction as F
from geometry import *


def positive_cases():
    for origin in ((0,0),(3,-2),(-4,5)):
        for direction in ((1,0),(0,1),(3,4),(-2,1)):
            a=point(*origin);u=point(*direction);v=point(-direction[1],direction[0]);b=add(a,u)
            for t in (F(-2),F(1,3),F(2)):
                for height in (F(-2),F(1),F(3,2)):
                    c=add(add(a,scale(t,u)),scale(height,v))
                    for offset in (F(-1),F(0),F(2)):
                        for depth in (F(1,2),F(2)):
                            d=add(add(a,scale(t+offset,u)),scale(-depth*height,v))
                            yield a,b,c,d,construct(a,b,c,d)


def rejected_cases():
    a,b,c,d=point(0,0),point(1,0),point(2,3),point(4,-1)
    k=construct(a,b,c,d)
    variants={
      'wrong_center':replace(k,center=point(9,9)),
      'wrong_radius':replace(k,radius_squared=k.radius_squared+1),
      'E_moved_off_line':replace(k,e=add(k.e,point(0,1))),
      'G_moved_along_line':replace(k,g=add(k.g,point(1,0))),
      'coincident_intersections':replace(k,g=k.e),
      'not_midpoint':replace(k,h=add(k.h,point(1,0))),
      'H_off_line':replace(k,h=add(k.h,point(0,1))),
      'perpendicular_only_wrong_circle':replace(k,e=point(3,0),g=point(1,0)),
      'malformed_point':replace(k,e=(Q(1),)),
    }
    for name,bad in variants.items():yield name,a,b,c,d,bad
    yield 'transplanted_C',a,b,point(2,4),d,k
    yield 'transplanted_D',a,b,c,point(4,-2),k
    yield 'C_on_line',a,b,point(2,0),d,k
    yield 'D_on_line',a,b,c,point(4,0),k
    yield 'same_side_D',a,b,c,point(4,1),k
    yield 'zero_line',a,a,c,d,k
    yield 'different_line',a,point(0,1),c,d,k
