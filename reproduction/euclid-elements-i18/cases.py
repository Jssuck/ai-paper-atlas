"""Finite coverage includes both orientations, rational and irrational cuts."""
from geometry import point, F


def positives():
    for x in (-2,-1,0,1,2):
        for y in (-2,-1,1,2):
            for length in (4,5,6):
                for dx,dy in ((0,0),(F(1,3),F(-2,5)),(-3,2)):
                    yield point(dx,dy),point(dx+x,dy+y),point(dx+length,dy)


def negatives():
    p=point
    return [
      (p(0,0),p(0,0),p(4,0)),(p(0,0),p(1,0),p(4,0)),
      (p(0,0),p(0,4),p(4,0)),(p(0,0),p(0,5),p(4,0)),
      (p(0,0),p(1,1),p(0,0)),(p(0,0),p(1,1),p(1,1)),
      (p(0,0),p(-1,0),p(4,0)),(p(0,0),p(5,0),p(4,0)),
      ((0,0),p(1,1),p(4,0)),(p(0,0),(1,1),p(4,0)),
      (p(0,0),p(1,1),(4,0)),([0,0],p(1,1),p(4,0)),
      (p(0,0),p(1,1),None), (None,p(1,1),p(4,0)),
    ]
