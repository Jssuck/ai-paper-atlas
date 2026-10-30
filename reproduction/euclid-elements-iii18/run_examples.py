from geometry import *
for name,o,b,r,v in [('tangent',(0,0),(3,0),3,(0,1)),('oblique',(0,0),(3,0),3,(1,1)),('outward_ray_but_secant_line',(0,0),(3,0),3,(1,2)),('radial',(0,0),(3,0),3,(1,0))]:
 c=certify(o,b,r,v);print(name, 'q=',c['q'],'t=',c['t'],'H=',c['h'],'power=',c['power'],'verified=',verify(c))
for name,r,b,v in [('zero_radius',0,(0,0),(1,0)),('non_boundary',3,(2,0),(1,0)),('zero_direction',3,(3,0),(0,0))]:
 try:certify((0,0),b,r,v)
 except ValueError as e:print(name,'rejected:',e)
print('grid:',grid())
