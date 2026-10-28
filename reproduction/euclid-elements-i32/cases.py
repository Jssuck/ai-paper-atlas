from fractions import Fraction as Q
from copy import deepcopy

def fixture(a=0,h=1,w=2,t=1,u=1):
 A=(Q(a),Q(h)); B=(Q(0),Q(0));C=(Q(w),Q(0))
 pts={'A':A,'B':B,'C':C,'D':(Q(w)*(1+Q(t)),Q(0)), 'E':(Q(w)+Q(u)*A[0],Q(u)*A[1])}
 return {k:list(map(str,p)) for k,p in pts.items()}

def positives():
 for a in [-3,0,1,4]:
  for h in [-3,-1,1,2]:
   for w in [Q(1),Q(2),Q(3,2)]:
    for t,u in [(Q(1),Q(1)),(Q(1,2),Q(3,2)),(Q(3),Q(2))]:
     for rotate in range(4):
      x=fixture(a,h,w,t,u)
      for k,p in x.items():
       v=list(map(Q,p))
       for _ in range(rotate):v=[-v[1],v[0]]
       x[k]=[str(v[0]+Q(2,3)),str(v[1]-Q(1,4))]
      yield x

def negatives():
 x=fixture(); out=[]
 for name,k,v in [('A_equals_B','A',x['B']),('B_equals_C','B',x['C']),('collinear','A',['1','0']),('D_equals_C','D',x['C']),('D_backwards','D',['1','0']),('D_off_line','D',['4','1']),('E_equals_C','E',x['C']),('E_opposite','E',['2','-1']),('E_not_parallel','E',['3','1'])]:
  y=deepcopy(x);y[k]=deepcopy(v);out.append((name,y))
 return out
