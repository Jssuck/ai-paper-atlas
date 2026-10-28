from fractions import Fraction
from copy import deepcopy

def example(): return {'A':['0','1'],'B':['2','1'],'C':['0','3'],'D':['-1','3'],'E':['0','0'],'F':['1','0']}
def positives():
    for slope in range(-3,4):
      w=(Fraction(1),Fraction(slope)); n=(-w[1],w[0])
      for h,k in ((1,3),(-1,2),(-3,-1),(3,1)):
       for a,b in ((1,1),(-1,2),(2,-1),(-2,-3)):
        for rotation in range(4):
         for shift in ((0,0),(2,-3)):
          def point(q):
           x,y=q
           for _ in range(rotation): x,y=-y,x
           return [str(x+shift[0]),str(y+shift[1])]
          A=tuple(h*z for z in n); C=tuple(k*z for z in n)
          yield {'A':point(A),'B':point(tuple(A[i]+a*w[i] for i in range(2))), 'C':point(C),'D':point(tuple(C[i]+b*w[i] for i in range(2))), 'E':point((Fraction(0),Fraction(0))),'F':point(w)}
def negatives():
    out=[]
    for key,value in [('B',['0','1']),('D',['0','3']),('F',['0','0']),('B',['2','1000001/1000000']),('D',['-1','4'])]:
      d=example();d[key]=value;out.append(d)
    d=example();d['A']=['0','0'];d['B']=['2','0'];out.append(d)
    d=example();d['C']=['0','0'];d['D']=['-1','0'];out.append(d)
    d=example();d['C']=['0','1'];d['D']=['-1','1'];out.append(d)
    return out
