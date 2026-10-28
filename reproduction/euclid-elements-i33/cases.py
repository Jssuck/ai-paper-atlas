from fractions import Fraction as F

def positive_cases():
    for ux,uy in [(1,0),(0,1),(2,1),(-2,1),(1,-2),(3,2)]:
        for a in range(-2,3):
            for h in [-3,-1,1,3]:
                for scale in [F(1,2),F(1),F(3,2)]:
                    A=(F(a),F(1,3));u=(scale*ux,scale*uy);w=(F(a)*ux-h*uy,F(a)*uy+h*ux)
                    B=tuple(A[i]+u[i] for i in range(2));C=tuple(A[i]+w[i] for i in range(2));D=tuple(C[i]+u[i] for i in range(2))
                    yield {k:[str(x) for x in p] for k,p in zip('ABCD',[A,B,C,D])}

BASE={'A':[0,0],'B':[3,0],'C':[1,2],'D':[4,2]}
NEGATIVE=[
 {'A':[0,0],'B':[3,0],'C':[4,2],'D':[1,2]},
 {'A':[0,0],'B':[3,0],'C':[1,2],'D':[5,2]},
 {'A':[0,0],'B':[3,0],'C':[1,2],'D':[4,3]},
 {'A':[0,0],'B':[3,0],'C':[1,0],'D':[4,0]},
 {'A':[0,0],'B':[0,0],'C':[1,2],'D':[4,2]},
 {'A':[0,0],'B':[3,0],'C':[1,2],'D':[1,2]},
 {'A':[False,0],'B':[3,0],'C':[1,2],'D':[4,2]},
 {'A':[0.0,0],'B':[3,0],'C':[1,2],'D':[4,2]},
 {'A':['0/1',0],'B':[3,0],'C':[1,2],'D':[4,2]},
 {'A':[0,0],'B':[3,0],'C':[1,2],'D':[4,2],'extra':0},
]
