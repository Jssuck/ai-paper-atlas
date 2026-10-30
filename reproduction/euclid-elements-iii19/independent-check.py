"""Finite independent parameter oracle; no claim of a general proof."""
from fractions import Fraction as Q
from copy import deepcopy
from geometry import certify, verify

def check(ok, name):
    if not ok: raise RuntimeError(name)

count = mutations = 0
# Rational unit circle parameterisation, not geometry.grid's four directions.
for p in range(-4, 5):
 for q in range(1, 5):
  u = (Q(q*q-p*p, q*q+p*p), Q(2*p*q, q*q+p*p))
  for radius in [Q(2,3), Q(7,2)]:
   for centre in [(Q(0),Q(0)),(Q(5,7),Q(-11,3))]:
    contact = tuple(centre[i]+radius*u[i] for i in range(2))
    for k in [Q(-5,3),Q(7,4)]:
     tangent = (-k*u[1], k*u[0])
     for j in [Q(-9,2),Q(-1,7),Q(2,9),Q(11,3)]:
      normal = tuple(j*x for x in u)
      args = (centre,contact,radius,tangent,normal)
      cert = certify(*args)
      # Solve one nonzero coordinate, independent of dot-product formula.
      axis = 0 if normal[0] else 1
      expected = (centre[axis]-contact[axis])/normal[axis]
      check(cert['t']==expected, 'coordinate oracle')
      check(all(contact[i]+expected*normal[i]==centre[i] for i in range(2)), 'both coordinates')
      check(verify(*args,cert), 'valid certificate')
      for key,value in [('t',expected+1),('centre_on_line',(99,99)),('tangent_power_coefficient',0),('normal_norm2',0),('ray_reaches_centre',not cert['ray_reaches_centre'])]:
       bad=deepcopy(cert);bad[key]=value
       check(not verify(*args,bad), 'tamper '+key);mutations+=1
      count+=1
base=((0,0),(3,4),5,(-4,3),(-3,-4))
cert=certify(*base)
malformed=[None,[],{},dict(cert,t=True),dict(cert,t=1.0),dict(cert,ray_reaches_centre=1),dict(cert,centre_on_line=(False,0)),dict(cert,extra=0)]
for value in malformed:check(not verify(*base,value),'malformed certificate')
for bad in [((0,0),(3,4),5,(1,0),(0,1)),((0,0),(3,4),5,(-4,3),(1,0)),((0,0),(3,4),5,(-4,3),(0,0)),((0,0),(3,4),False,(-4,3),(-3,-4))]:
 try:certify(*bad)
 except ValueError:pass
 else:raise RuntimeError('invalid premise accepted')
# Segment and ray cases in prose.
for normal,expected in [((3,4),Q(-1)),((-6,-8),Q(1,2)),((-1,Q(-4,3)),Q(3))]:
 check(certify(*base[:-1],normal)['t']==expected,'article parameter')
# Distinct opposite contacts + equidistance fix midpoint, not just a line.
A=(Q(-3),Q(0));B=(Q(3),Q(0))
M=tuple((A[i]+B[i])/2 for i in range(2))
check(M==(0,0),'opposite contacts midpoint')
print('coordinate-oracle configurations:',count)
print('tampered field certificates rejected:',mutations)
print('malformed certificates rejected:',len(malformed))
print('invalid premise sets rejected: 4')
print('article parameter cases: 3; distinct opposite contact midpoint: passed')
print('finite exact checks only; not a proof assistant')
