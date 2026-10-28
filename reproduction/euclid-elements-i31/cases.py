from fractions import Fraction as Q
from copy import deepcopy

def fixture(m=0,a=1,d=0,t=1,u=1):
    # D=(d,md); A=D+(0,a); C=D+(1,m), B=D-(1,m).
    D=(Q(d),Q(m*d)); A=(D[0],D[1]+a); v=(Q(1),Q(m))
    pts={'A':A,'B':tuple(D[i]-v[i] for i in range(2)),
         'C':tuple(D[i]+v[i] for i in range(2)),'D':D,
         'E':tuple(A[i]-t*v[i] for i in range(2)),
         'F':tuple(A[i]+u*v[i] for i in range(2))}
    return {k:[str(z) for z in p] for k,p in pts.items()}

def positives():
    for m in range(-3,4):
      for a in [-2,-1,1,2]:
       for d in [-2,0,3]:
        for t,u in [(Q(1),Q(1)),(Q(2),Q(3)),(Q(1,2),Q(3,2))]:
         for rotate in range(4):
          x=fixture(m,a,d,t,u)
          for k,p in x.items():
           v=[Q(z) for z in p]
           for _ in range(rotate): v=[-v[1],v[0]]
           x[k]=list(map(str,v))
          yield x

def negatives():
    x=fixture(); cases=[]
    for name,k,v in [('zero_line','B',x['C']),('D_off_line','D',['0','2']),('D_equals_C','D',x['C']),('A_on_line','A',['0','0']),('zero_E','E',x['A']),('wrong_side','E',['1','1']),('wrong_angle','E',['-1','2']),('zero_F','F',x['A']),('F_not_extension','F',['1','2']),('F_same_ray','F',['-2','1'])]:
      y=deepcopy(x);y[k]=deepcopy(v);cases.append((name,y))
    return cases
