from fractions import Fraction as F
from condillac_model import R,L,transfer,certificate,solve,holds,feasible,equivalent,oracle,sequential

rows = transfer()
print('rows:', rows)
print('solution:',solve(rows))
trace = certificate(rows,[('add',1,0,-1),('scale',1,-1),('add',0,1,1)])
for index,state in enumerate(trace):
    print('step',index,state,'equivalent:',equivalent(rows,state))
print('conjunction loss witness:',holds((rows[1]-rows[0],),0,5),holds(rows,0,5))
print('sequential:',solve(sequential()))
print('k4:',solve(transfer(1,1,4)),'feasible:',feasible(F(13,3),F(7,3)))
print('bounded original:',oracle(rows,12))
