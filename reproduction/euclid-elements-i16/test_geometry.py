import copy
import unittest
from fractions import Fraction as Q
from geometry import construct, verify, same_angle, strict_inside, canonical_json
from cases import positives, negatives, run_cases

P={'A':[1,2],'B':[0,0],'C':[3,0],'D':[5,0]}
class GeometryTests(unittest.TestCase):
    def test_all_positive(self):
        self.assertEqual(run_cases()['positive_certificates'],180)
    def test_all_invalid(self):
        self.assertEqual(run_cases()['negative_inputs'],16)
    def test_exact_points(self):
        self.assertEqual(construct(P)['points'],{'E':['2','1'],'F':['4','2'],'M':['3/2','0'],'N':['2','-2'],'G':['5','-2']})
    def test_coefficients(self):
        self.assertEqual(construct(P)['coefficients']['CF_in_CA_CD'],['1','3/2'])
    def test_input_bound(self):
        self.assertFalse(verify(dict(P,A=[2,2]),construct(P)))
    def test_translation(self):
        self.assertTrue(verify({k:[v[0]+7,v[1]-4] for k,v in P.items()},construct({k:[v[0]+7,v[1]-4] for k,v in P.items()})))
    def test_rotation(self):
        q={k:[-v[1],v[0]] for k,v in P.items()}; self.assertTrue(verify(q,construct(q)))
    def test_reflection(self):
        q={k:[v[0],-v[1]] for k,v in P.items()}; self.assertTrue(verify(q,construct(q)))
    def test_rationals(self):
        q={'A':['1/7','2/9'],'B':['-3/8','0'],'C':['7/13','0'],'D':['1','0']}; self.assertTrue(verify(q,construct(q)))
    def test_large_exact(self):
        q={k:[v[0]*10**50,v[1]*10**50] for k,v in P.items()}; self.assertTrue(verify(q,construct(q)))
    def test_very_flat(self):
        q=dict(P,A=['1','1/1000000000000000000000000']);self.assertTrue(verify(q,construct(q)))
    def test_zero_angle_ray(self): self.assertFalse(same_angle((0,0),(1,0),(1,0),(1,0)))
    def test_opposite_acute_obtuse(self): self.assertFalse(same_angle((1,0),(1,1),(1,0),(-1,1)))
    def test_right_angle(self): self.assertTrue(same_angle((1,0),(0,1),(3,0),(0,-7)))
    def test_inside_ccw(self): self.assertTrue(strict_inside((1,0),(0,1),(1,1)))
    def test_inside_cw(self): self.assertTrue(strict_inside((0,1),(1,0),(1,1)))
    def test_boundary_not_inside(self): self.assertFalse(strict_inside((1,0),(0,1),(2,0)))
    def test_opposite_not_inside(self): self.assertFalse(strict_inside((1,0),(0,1),(-1,-1)))
    def test_straight_wedge_rejected(self): self.assertFalse(strict_inside((1,0),(-1,0),(0,1)))
    def test_json_types(self): self.assertNotEqual(canonical_json(True),canonical_json(1))
    def test_json_float(self):
        with self.assertRaises(ValueError):canonical_json(float('nan'))
    def test_json_tuple(self):
        with self.assertRaises(ValueError):canonical_json((1,2))
    def test_no_extra_payload(self): self.assertFalse(verify(dict(P,extra=1),construct(P)))
    def test_dict_order_irrelevant(self): self.assertTrue(verify(P,dict(reversed(list(construct(P).items())))))

mutations={
 'schema_bool':lambda c:c.update(schema=True),
 'schema_float':lambda c:c.update(schema=1.0),
 'point_F':lambda c:c['points'].update(F=['4','3']),
 'point_N':lambda c:c['points'].update(N=['2','2']),
 'check_integer':lambda c:c['checks'].update(CF_inside_ACD=1),
 'check_false':lambda c:c['checks'].update(CF_inside_ACD=False),
 'coefficient':lambda c:c['coefficients'].update(CF_in_CA_CD=['1','1']),
 'input_change':lambda c:c['input'].update(D=['6','0']),
 'extra_field':lambda c:c.update(extra=True),
 'missing_field':lambda c:c.pop('scope'),
 'conclusion':lambda c:c.update(conclusions=['all angles equal']),
 'tuple_point':lambda c:c['points'].update(E=('2','1')),
}
def make_test(mutation):
    def test(self):
        c=copy.deepcopy(construct(P));mutation(c);self.assertFalse(verify(P,c))
    return test
for name,mutation in mutations.items():setattr(GeometryTests,'test_tamper_'+name,make_test(mutation))
if __name__=='__main__':unittest.main(verbosity=2)
