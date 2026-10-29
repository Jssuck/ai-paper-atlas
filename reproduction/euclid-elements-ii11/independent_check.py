import sys,copy
from fractions import Fraction as R
from decimal import Decimal,localcontext
from geometry import Q5,validate_certificate,make_certificate
q=lambda p=0,s=0:Q5(R(p),R(s))
x=q(R(-1,2),R(1,2))
pts={'A':(q(),q()),'B':(q(1),q()),'C':(q(),q(1)),'D':(q(1),q(1)),'E':(q(),q(R(1,2))),'F':(q(),-x),'G':(x,-x),'H':(x,q()),'K':(x,q(1))}
c={'a':R(1),'origin':(R(0),R(0)),'u':(R(1),R(0)),'v':(R(0),R(1)),'points':pts}
m=validate_certificate(c)
if m['FH'] != q(R(3,2),R(-1,2)):raise RuntimeError('area')
print('PASS manually assembled independent a=1 certificate')
count=0
for a in [R(1,1000),R(2,3),R(1),R(1000)]:
 for u,v in [((3,4),(-4,3)),((R(3,5),R(4,5)),(R(4,5),R(-3,5))),((-1,0),(0,1))]:
  o=(R(17,3),R(-9,2))
  t={k:tuple(q(o[j])+a*(p[0]*u[j]+p[1]*v[j]) for j in range(2)) for k,p in pts.items()}
  m=validate_certificate(dict(a=a,origin=o,u=u,v=v,points=t));count+=1
print('PASS independent similarity/reflection certificates:',count)
count=0
for name in pts:
 d=copy.deepcopy(c);p=d['points'][name];d['points'][name]=(p[0]+q(R(1,100)),p[1])
 try:validate_certificate(d)
 except ValueError:count+=1
 else:raise RuntimeError('accepted corrupted '+name)
print('PASS point corruption rejections:',count)
count=0
with localcontext() as ctx:
 ctx.prec=120
 rt=Decimal(5).sqrt()
 for p in range(-30,31):
  for s in range(-30,31):
   z=Decimal(p)+Decimal(s)*rt
   if q(p,s).sign() != ((z>0)-(z<0)):raise RuntimeError('sign')
   count+=1
 # Continued fraction convergents for sqrt(5), near-cancellation is decided rationally.
 h0,h1,k0,k1=0,1,1,0
 for i in range(60):
  t=2 if i==0 else 4;h0,h1=h1,t*h1+h0;k0,k1=k1,t*k1+k0
  expected=1 if h1*h1>5*k1*k1 else -1
  if q(h1,-k1).sign()!=expected:raise RuntimeError('near cancellation')
print('PASS sign grid:',count,'; exact near-cancellation convergents: 60')
for z in [q(2,3),q(-7,5),q(R(1,17),R(-3,11))]:
 if (z/z)!=q(1):raise RuntimeError('inverse')
print('PASS field inverses: 3')
print('SCOPE: fixed algebraic construction regression; not a general geometric theorem prover.')
