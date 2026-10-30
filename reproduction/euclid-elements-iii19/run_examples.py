from geometry import *
for name,args in [
 ('inward',((0,0),(3,4),5,(-4,3),(-3,-4))),
 ('outward',((0,0),(3,4),5,(-4,3),(3,4))),
 ('translated',((2,-1),(5,3),5,(-8,6),(-6,-8))),
 ('rational',((0,0),(F(3,5),F(4,5)),1,(-4,3),(-3,-4)))]:
 c=certify(*args)
 if not verify(*args,c):raise RuntimeError(name)
 print(name,c)
for name,args in [('secant',((0,0),(3,4),5,(1,0),(0,1))),('wrong normal',((0,0),(3,4),5,(-4,3),(1,0))),('zero normal',((0,0),(3,4),5,(-4,3),(0,0)))]:
 try:certify(*args)
 except ValueError as e:print(name,'rejected:',e)
 else:raise RuntimeError('invalid input accepted')
print('grid',grid())
