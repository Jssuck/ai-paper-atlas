from geometry import *
def positive_cases():
    out=[]
    for h in (2,3,5,7):
      for s in (-2,0,2):
       for weights in ((1,1,1),(1,2,3),(3,1,2),(2,3,1),(1,9,1)):
        for reflect in (1,-1):
         A,B,C=point(s,reflect*h),point(-3,0),point(4,0)
         a,b,c=map(Q,weights);total=a+b+c
         D=mul(1/total,add(add(mul(a,A),mul(b,B)),mul(c,C)))
         out.append((A,B,C,D))
    return out

def invalid_cases():
    A,B,C=point(0,4),point(-3,0),point(4,0)
    return [(A,B,C,p) for p in (A,B,C,point(0,0),point(8,4),point(0,-1),point(-4,2),point(4,2),point(0,5))]+[(point(0,0),point(1,0),point(2,0),point(1,1)),(A,A,C,point(0,1)),((True,4),B,C,point(0,1))]
