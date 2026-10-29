from fractions import Fraction as F
from geometry import construct,sqrt_interval,check_interval
cases=[('integer square area',9,4),('irrational side',2,1),('equal rectangle',3,3),('rational sides',F(3,2),F(2,3)),('swapped',4,9),('tiny positive',F(1,100),F(1,1000)),('near equal',1,1+F(1,10**30)),('extreme ratio',10**120,F(1,10**120))]
for name,a,b in cases:
    r=construct(a,b)
    print(name,':',r['branch'],'area =',r['area'],'side² =',r['side_squared'])
    if not all(r['checks'].values()):raise ArithmeticError(name)
lo,hi=sqrt_interval(2,16)
print('sqrt(2), 16 bisections:',lo,'<= sqrt(2) <=',hi,'width =',hi-lo)
if not check_interval(2,lo,hi):raise ArithmeticError('bracket')
print('PASS: 8 named examples and 1 root enclosure; finite checks, not a theorem proof.')
