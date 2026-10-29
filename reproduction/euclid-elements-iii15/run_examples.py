from geometry import *
def examples():
 c=Circle((0,0),5)
 cases=[('longer-nearer',((-4,3),(4,3),(-3,4),(3,4))),('diameter',((-5,0),(5,0),(-4,3),(4,3))),('equal-diameters',((-5,0),(5,0),(0,-5),(0,5))),('opposite-sides',((-4,-3),(4,-3),(-3,4),(3,4)))]
 for name,ends in cases:
  x=compare(c,*ends);print(name,'length order',x['length_order'],'distance order',x['distance_order'],'reversal',x['order_reversal_holds'])
 a=chord(c,(-4,3),(4,3));b=chord(Circle((0,0),1),(-1,0),(1,0))
 print('different-radii counterexample:',a['length2'],b['length2'],'distance squares',a['distance2'],b['distance2'])
 for ends in [((5,0),(5,0)),((0,0),(5,0))]:
  try:chord(c,*ends)
  except ValueError as e:print('rejected:',str(e))
  else:raise RuntimeError('invalid accepted')
if __name__=='__main__':examples()
