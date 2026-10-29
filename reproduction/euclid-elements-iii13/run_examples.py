from geometry import *

def examples():
 a=Circle((0,0),5)
 for label,b,t,k in [('external',Circle((8,0),3),(5,0),'external'),('internal',Circle((2,0),3),(5,0),'internal'),('vertical',Circle((0,8),3),(0,5),'external')]:
  print(label,contact_certificate(a,b,t,k))
 b=Circle((6,0),5)
 print('two intersections midpoint',chord_midpoint_certificate(a,b,(3,4),(3,-4)))
 for label,b,t,k in [('crossing external',b,(3,4),'external'),('crossing internal',b,(3,4),'internal'),('coincident',a,(3,4),'internal')]:
  try:contact_certificate(a,b,t,k)
  except ValueError as e:print(label,'rejected:',e)
  else:raise RuntimeError('invalid case accepted')
 print('coincident distinct common points:',on(a,(3,4)),on(a,(3,-4)))
if __name__=='__main__':examples()
