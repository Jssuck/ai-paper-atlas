from geometry import *
for lo,hi in ((0,1),(-1,1),(1,1+F(1,10**30))):
 print('nested k:',lo,hi,'certificate:',ordered_witness(lo,hi))
print('upper k=1 and lower k=-1: similar, congruent, noncoincident; NOT unequal:',segment_cot(1,1),segment_cot(-1,-1))
print('finite grid:',grid())
