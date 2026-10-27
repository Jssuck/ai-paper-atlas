"""Finite rational test families; they are not a universal theorem proof."""
from geometry import point,F

def positive_cases():
    result=[]
    for k in (1,2,3,4):
        for x in (-2,0,1,3):
            for y in (-3,-1,1,2):
                for shift in (0,F(1,3)):
                    result.append((point(shift,-shift),point(k+shift,-shift),point(x+shift,y-shift)))
    return result

def invalid_cases():
    return [(point(0,0),point(k,0),point(j,0)) for k,j in ((0,0),(0,1),(1,0),(1,1),(1,2),(1,-1),(2,1),(2,3),(3,2),(3,-2),(4,2),(4,5))]
