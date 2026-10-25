"""Boundary and exhaustive finite checks; unittest checks survive python -O/-OO."""
import unittest
from fractions import Fraction as F
from model import frequency, subsets, bound_values, majority_example, enumerate_models, world_example

class TeachingModelTests(unittest.TestCase):
    def test_empty_condition(self):
        self.assertIsNone(frequency({1},set()))
    def test_empty_event(self):
        self.assertEqual(frequency(set(),{1,2}),F(0))
    def test_exact_frequency(self):
        self.assertEqual(frequency({1,2},{1,2,3}),F(2,3))
    def test_outside_condition_irrelevant(self):
        self.assertEqual(frequency({1,99},{1,2}),F(1,2))
    def test_counterexample(self):
        self.assertEqual(majority_example(),{'P(B|C)':'3/5','P(A|B)':'5/8','P(A|C)':'0','P(A|B∩C)':'0'})
    def test_product_equal_joint(self):
        a,b,c={1,3},{1,2},{1,2,3}
        target,lower=bound_values(a,b,c)
        self.assertEqual(target,F(2,3)); self.assertEqual(lower,F(1,3))
        self.assertEqual(lower,frequency(a&b,c))
    def test_no_independence_required(self):
        target,lower=bound_values({1},{1},{1,2})
        self.assertEqual((target,lower),(F(1,2),F(1,2)))
    def test_disjoint_middle_undefined(self):
        self.assertEqual(bound_values({1},{2},{1}),(F(1),None))
    def test_empty_C_undefined(self):
        self.assertEqual(bound_values({1},{1},set()),(None,None))
    def test_universal_vacuity_not_frequency(self):
        self.assertTrue(set()<={1}<={1,2})
        self.assertIsNone(frequency({1,2},set()))
    def test_product_can_be_below_majority(self):
        self.assertLess(F(3,5)*F(3,5),F(1,2))
    def test_powerset(self):
        self.assertEqual(len(subsets(4)),16)
        self.assertEqual(len(set(subsets(4))),16)
    def test_enumeration_bound_and_inclusion(self):
        for row in enumerate_models():
            self.assertEqual(row['bound_failures'],0)
            self.assertEqual(row['inclusion_failures'],0)
            self.assertEqual(row['triples'],8**row['n'])
            self.assertEqual(row['inclusion_premises'],4**row['n'])
            self.assertEqual(row['triples'],row['empty_C']+row['empty_B_intersect_C']+row['defined_product_bounds'])
    def test_every_product_is_joint(self):
        for a in subsets(3):
            for b in subsets(3):
                for c in subsets(3):
                    target,lower=bound_values(a,b,c)
                    if lower is not None:
                        self.assertEqual(lower,frequency(a&b,c))
                        self.assertGreaterEqual(target,lower)
    def test_threshold_bound(self):
        for a in subsets(3):
            for b in subsets(3):
                for c in subsets(3):
                    x,y=frequency(b,c),frequency(a,b&c)
                    if x is not None and y is not None:
                        for s,t in [(F(0),F(0)),(F(1,2),F(1,2)),(F(2,3),F(1,3)),(F(1),F(1))]:
                            if x>=s and y>=t:
                                self.assertGreaterEqual(frequency(a,c),s*t)
    def test_observed_one_not_necessity(self):
        self.assertEqual(world_example(),{'observed_frequency':'1','all_objects_succeed_in_every_stipulated_world':False})

if __name__=='__main__': unittest.main(verbosity=2)
