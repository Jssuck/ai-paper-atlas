from geometry import *
def examples():
 c=Circle((0,0),5)
 cases=[('equal opposite-side',(-4,3),(4,3),(-4,-3),(4,-3)),('unequal',(-4,3),(4,3),(-3,4),(3,4)),('two diameters',(-5,0),(5,0),(0,-5),(0,5)),('one diameter',(-5,0),(5,0),(-4,3),(4,3))]
 for name,a,b,d,e in cases:
  q=compare(c,a,b,d,e)
  print(name, 'length squared:',q['first']['length2'],q['second']['length2'],'distance squared:',q['first']['distance2'],q['second']['distance2'],'equivalence:',q['equivalence_holds'])
 a=chord(c,(-4,3),(4,3));b=chord(Circle((0,0),4),(-4,0),(4,0))
 print('different radii counterexample:',a['length2'],b['length2'],a['distance2'],b['distance2'])
 for name,a,b in [('degenerate',(5,0),(5,0)),('off-circle',(0,0),(5,0))]:
  try:chord(c,a,b)
  except ValueError as e:print(name,'rejected:',e)
  else:raise RuntimeError('invalid input accepted')
if __name__=='__main__':examples()
