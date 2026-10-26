import math,random,json,hashlib
from itertools import product
from fractions import Fraction as F
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from geometry import angle_equal, strict_cut_certificate, cut_from_rational_ratio, triangle_certificate
rng=random.Random(6006)
vec=[x for x in product(range(-2,3),repeat=2) if x!=(0,0)]
def ref(u,v): return math.atan2(abs(u[0]*v[1]-u[1]*v[0]),u[0]*v[0]+u[1]*v[1])
for _ in range(10000):
 u,v,w,z=[rng.choice(vec) for i in range(4)]
 if angle_equal(u,v,w,z)!=(abs(ref(u,v)-ref(w,z))<1e-12): raise RuntimeError('angle comparison disagreement')
# Deliberately distinguish equal scalar area from correct placement on AB.
q=strict_cut_certificate((0,0),(5,0),(0,3),(F(2),F(1)))
if not(q['proper_area'] and not q['strict_inside'] and not q['valid_cut']):raise RuntimeError('off-line cut not distinguished')
# Noncollinear rational affine transformed right triangle; scaling preserves certificate.
for k in range(1,21):
 s=F(k,7);a=(F(2),F(-3));b=(2+5*s,-3);c=(2,-3+3*s)
 d=cut_from_rational_ratio(a,b,c,F(3,5));q=strict_cut_certificate(a,b,c,d)
 if not(q['valid_cut'] and q['area_ratio']==F(3,5) and not q['contradiction_premises']):raise RuntimeError('transformed cut')
# Degenerate equal-angle example requires explicit rejection, not an alleged theorem counterexample.
if not angle_equal((1,0),(3,0),(-2,0),(-3,0)):raise RuntimeError('zero angle model')
try:triangle_certificate((1,0),(0,0),(3,0))
except ValueError:pass
else:raise RuntimeError('degenerate accepted')
# Pointwise biconditional, not merely equality of aggregate counts.
triangles=0
for b,c in product(list(product(range(-3,4),repeat=2)),repeat=2):
 if b[0]*c[1]-b[1]*c[0]==0:continue
 q=triangle_certificate((0,0),b,c);triangles+=1
 if q['base_angles_equal']!=q['opposite_sides_equal']:raise RuntimeError('pointwise converse disagreement')
print(json.dumps({'pointwise_biconditional_triangles':triangles,'angle_oracle_pairs':10000,'oracle':'independent atan2(abs(cross),dot), integer ray grid -2..2, seed 6006, tolerance 1e-12; finite diagnostic only','transformed_cuts':20,'off_line_area_trap':'passed','degenerate_equal_angle_rejection':'passed','all_passed':True},indent=2))
