from geometry import certificate,circle_points,grid
from independent_oracle import check,angle
from test_geometry import Q
print('square:',certificate(Q))
print('nonrectangular:',certificate(tuple(circle_points()[:4])))
crossed=(Q[0],Q[2],Q[1],Q[3])
print('crossed nonreflex opposite-angle sum (radians):',angle(crossed[3],crossed[0],crossed[1])+angle(crossed[1],crossed[2],crossed[3]))
try: certificate(crossed)
except ValueError as e: print('crossed rejected:',e)
print('exact grid:',grid())
print('independent floating oracle:',check())
