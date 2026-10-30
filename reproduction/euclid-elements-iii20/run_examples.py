from geometry import EXAMPLES,check,grid
for name,points in EXAMPLES.items():
 r=check(*points)
 print(name, 'arc='+r['arc'], 'center='+r['center_location'], 'central='+str(r['central']), 'double='+str(r['doubled']), 'side_through_center='+str(r['side_through_center']), 'base_diameter='+str(r['base_diameter']))
print(grid())
