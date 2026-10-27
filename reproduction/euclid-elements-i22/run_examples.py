import json
from fractions import Fraction as Q
from geometry import construct,verify,classify
from cases import positive_cases,NEGATIVE
n=0;irr=0
from math import isqrt
for sides in positive_cases():
    for sign in (-1,1):
        cert=construct(*sides,orientation=sign)
        if not verify(cert,*sides,orientation=sign):raise RuntimeError('certificate failed')
        h=Q(cert['height_squared'])
        irr+=int(isqrt(h.numerator)**2!=h.numerator or isqrt(h.denominator)**2!=h.denominator)
        n+=1
neg=0
for values in NEGATIVE:
    try:construct(*values)
    except (ValueError,ZeroDivisionError,TypeError):neg+=1
    else:raise RuntimeError('invalid input accepted')
print(json.dumps({'positive_certificates':n,'negative_inputs':neg,'irrational_height_certificates':irr,
    'examples':{'3_4_5':construct(3,4,5),'equilateral':construct(1,1,1),
    'outside_base_projection':construct(2,4,3)},
    'boundary_classes':[classify(*v) for v in [(1,1,2),(3,1,2),(1,1,3),(3,1,1)]]},indent=2))
