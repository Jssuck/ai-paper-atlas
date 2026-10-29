"""Independent exact checks of article tables, counterexamples and exercises."""
from fractions import Fraction as F
from geometry import construct,sqrt_interval

def require(test,name):
    if not test:raise RuntimeError(name)
rows=[(9,4,F(13,2),F(5,2),36),(2,1,F(3,2),F(1,2),2),(3,3,F(3),F(0),9),(F(9,4),1,F(13,8),F(5,8),F(9,4)),(4,9,F(13,2),F(5,2),36)]
for a,b,r,d,h2 in rows:
    require((F(a)+b)/2==r,'table radius')
    require(abs(F(a)-b)/2==d,'table offset')
    require(r*r-d*d==h2==a*b,'table area')
    require(construct(a,b)['side_squared']==h2,'production table match')
require(F(13,2)**2-F(5,2)**2==36,'example II5')
require(2*(9+4)==26 and 4*6==24,'perimeters')
require(F(13,2)**2==F(169,4),'wrong output radius')
require(F(13,2)**2-5**2==F(69,4),'wrong full difference')
require(13**2-F(5,2)**2==F(651,4),'wrong diameter radius')
require(F(13,2)**2-F(5,2)==F(159,4),'wrong dimensions')
require(F(1414,1000)**2==F(1999396,1000000)!=2,'rounded root')
require(10**18*F(1,10**18)==1,'extreme example')
require(F(5,12)!=F(3,2) and F(5,12)!=F(2,3),'not similar even reversed')
require(F(9,6)==F(6,4),'similar correct pair')
require(F(25,2)**2-F(7,2)**2==144,'exercise4')
require(F(25,2)**2-7**2==F(429,4),'exercise4 wrong')
require(construct(5,5)['branch']=='already_square','exercise5')
require(F(17,4)**2-F(15,4)**2==4,'exercise6')
lo,hi=sqrt_interval(2,16)
require((lo,hi)==(F(11585,8192),F(46341,32768)) and hi-lo==F(1,32768),'reported enclosure')
print('PASS: 5 article table rows, 5 wrong-formula/rounding checks, exact root enclosure,')
print('perimeters, extreme ratio, similarity counterexample, exercises 4/5/6.')
print('Hand checks overlap other test suites; counts are not independent unique inputs.')
