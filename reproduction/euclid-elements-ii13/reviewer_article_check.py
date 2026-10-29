"""Independent exact certificates for every numeric article example."""
from fractions import Fraction as F
from geometry import verify

def require(ok, msg):
    if not ok: raise AssertionError(msg)
def sq(P,Q): return sum((F(x)-F(y))**2 for x,y in zip(P,Q))
cases=[
 ('table acute',(2,4),(5,0),(20,25,20),True),
 ('table obtuse A',(2,1),(5,0),(5,10,20),True),
 ('table right C',(5,3),(5,0),(34,9,50),True),
 ('table obtuse C',(7,3),(5,0),(58,13,70),True),
 ('table right B',(0,3),(5,0),(9,34,0),False),
 ('table obtuse B',(-2,3),(5,0),(13,58,-20),False),
 ('collinear',(2,0),(5,0),(4,9,20),False),
 ('zero base',(2,4),(0,0),(20,20,0),False),
 ('tiny full acute',(F(1,10**18),1),(1,0),(1+F(1,10**36),2-F(2,10**18)+F(1,10**36),F(2,10**18)),True),
 ('exercise 4',(F(1,2),2),(3,0),(F(17,4),F(41,4),3),True)]
for name,A,C,expected,accept in cases:
    B=(0,0)
    actual=(sq(A,B),sq(A,C),sq(B,C)+sq(A,B)-sq(A,C))
    require(actual==expected,(name,'hand values',actual))
    try: result=verify(A,B,C)
    except ValueError: require(not accept,(name,'unexpected rejection')); status='correct rejection'
    else:
        require(accept,(name,'unexpected acceptance'))
        require((result['ba2'],result['ac2'],result['twice_rectangle'])==expected,(name,'output'))
        if name in ('table acute','tiny full acute','exercise 4'): require(result['all_acute'],name)
        status='exact match'
    print(name+': '+status)
# Deliberately wrong alternatives in article 7.1.
require(2*5*3==30 and 2*5*4==40,'wrong-segment examples')
print('PASS: 10 article input cases; 2 wrong-segment arithmetic comparisons.')
