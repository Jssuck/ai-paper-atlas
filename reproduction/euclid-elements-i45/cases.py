from fractions import Fraction as Q
BASE=((0,0),(4,0),(5,3),(0,2))
def valid_cases():
    for a in (1,2,3):
      for reverse in (False,True):
       poly=tuple((a*x+2,a*y-3) for x,y in BASE)
       if reverse: poly=poly[::-1]
       for h in (Q(1),Q(3,2)):
        for p in (-2,0,1):
         for q in (1,3): yield (poly,h,p,q)
INVALID=[('repeated',((0,0),(4,0),(4,0),(0,2)),2,1,2),('collinear',((0,0),(1,0),(2,0),(0,2)),2,1,2),('concave',((0,0),(4,0),(1,1),(0,4)),2,1,2),('bowtie',((0,0),(4,3),(0,3),(4,0)),2,1,2),('triangle',BASE[:3],2,1,2),('float-coordinate',((0.,0),)+BASE[1:],2,1,2),('bool-coordinate',((False,0),)+BASE[1:],2,1,2),('zero-height',BASE,0,1,2),('negative-height',BASE,-1,1,2),('zero-q',BASE,2,1,0),('negative-q',BASE,2,1,-1),('float-angle',BASE,2,0.5,2),('bool-height',BASE,True,1,2),('string-q',BASE,2,1,'2')]
