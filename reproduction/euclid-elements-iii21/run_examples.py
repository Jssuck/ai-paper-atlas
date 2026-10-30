from geometry import CASES,certificate,grid
for name,args in CASES.items():print(name,certificate(*args))
print('finite rational grid:',grid())
print('Finite exact checks are not a proof for all real circle points.')
