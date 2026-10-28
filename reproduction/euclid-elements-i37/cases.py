from fractions import Fraction as F
from geometry import encode

def build(t=2,a=1,h=3,base=4,origin=(0,0),u=(1,0),v=(0,1)):
    t,a,h,base=map(F,(t,a,h,base))
    def p(x,y):return [str(F(origin[i])+x*u[i]+y*v[i]) for i in range(2)]
    return {'A':p(a,h),'B':p(0,0),'C':p(base,0),'D':p(a+t*base,h)}
EXAMPLE={'A':[1,3],'B':[0,0],'C':[4,0],'D':[9,3]}
def positives():
    for t in [-3,-1,F(-1,2),0,F(1,2),1,3]:
      for a in [-5,0,2,7]:
       for h in [-3,F(1,2),4]:
        for base in [1,4]:
         for u,v in [((1,0),(0,1)),((0,1),(1,0)),((2,1),(-1,3)),((-1,2),(3,1))]:
          yield build(t,a,h,base,(2,-3),u,v)
def negatives():
    for k,val in [('A',[1,0]),('B',[4,0]),('C',[0,0]),('D',[9,4]),('D',[9,-3]),('D',[9,0]),('A',[1,4]),('B',[0,1]),('C',[4,1])]:
        d={k:list(v) for k,v in EXAMPLE.items()};d[k]=val;yield d
