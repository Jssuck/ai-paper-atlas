import unittest
from fractions import Fraction
from chains import (affirmative_bridge, negative_bridge, middles, strict_chain,
                    equivalence_classes, midpoint, dyadic_prefix, experiment)

class ChainTests(unittest.TestCase):
    def setUp(self):
        self.t={'C':frozenset({0}),'B':frozenset({0,1}),'A':frozenset({0,1,2})}
    def test_finite_chain_rank(self):
        self.assertEqual(strict_chain(self.t,['C','B','A']),{'steps':2,'ranks':[1,2,3]})
        self.assertEqual(strict_chain(self.t,['B'])['steps'],0)
    def test_reject_cycle_and_reverse(self):
        for names in [['C','B','C'],['A','B'],['B','B'],[],['missing']]:
            with self.assertRaises(ValueError): strict_chain(self.t,names)
    def test_vocabulary_relative_middles(self):
        self.assertEqual(middles({'C':self.t['C'],'A':self.t['A']},'C','A'),[])
        self.assertEqual(middles(self.t,'C','A'),['B'])
    def test_equivalent_names_not_strict_steps(self):
        self.t['D']=self.t['B']
        self.assertIn(['B','D'],equivalence_classes(self.t))
        self.assertEqual(middles(self.t,'C','A'),['B','D'])
        with self.assertRaises(ValueError): strict_chain(self.t,['B','D'])
    def test_affirmative_direction(self):
        self.assertTrue(affirmative_bridge(self.t['C'],self.t['B'],self.t['A']))
        with self.assertRaises(ValueError): affirmative_bridge(self.t['A'],self.t['B'],self.t['C'])
    def test_negative_requires_both_premises(self):
        self.assertTrue(negative_bridge(frozenset({0}),frozenset({0,1}),frozenset({2})))
        for c,b,a in [({0},{1},{2}),({0},{0,1},{1,2})]:
            with self.assertRaises(ValueError): negative_bridge(*map(frozenset,(c,b,a)))
    def test_bad_extension_and_endpoints(self):
        for bad in [set({0}),frozenset(),frozenset({True}),frozenset({-1})]:
            with self.assertRaises(ValueError): equivalence_classes({'X':bad})
        for ends in [('A','C'),('B','B'),('X','A')]:
            with self.assertRaises(ValueError): middles(self.t,*ends)
    def test_midpoint_exact(self):
        for lo,hi in [(Fraction(-3,7),Fraction(5,9)),(Fraction(0),Fraction(1))]:
            mid=midpoint(lo,hi)
            self.assertLess(lo,mid); self.assertLess(mid,hi)
            self.assertEqual(mid-lo,hi-mid)
        for args in [(0,1),(Fraction(1),Fraction(0))]:
            with self.assertRaises(ValueError): midpoint(*args)
    def test_prefix_not_endpoint_claim(self):
        for depth in [0,1,8,64,256]:
            p=dyadic_prefix(depth)
            self.assertEqual(len(p),depth+2)
            self.assertEqual(p[-1]-p[-2],Fraction(1,2**depth))
            self.assertTrue(all(a<b for a,b in zip(p,p[1:])))
        for bad in [-1,257,True,1.5]:
            with self.assertRaises(ValueError): dyadic_prefix(bad)
    def test_exhaustive_domain(self):
        r=experiment()
        self.assertEqual(r['ordered_triples_checked'],3375)
        self.assertEqual(r['bridge_failures'],0)
        # Independent per-object count: 4 membership states for C subset B subset A,
        # excluding C empty; 4 states for C subset B and A disjoint B,
        # excluding C empty and A empty via inclusion-exclusion.
        self.assertEqual(r['affirmative_valid_premises'],4**4-3**4)
        self.assertEqual(r['negative_valid_premises'],4**4-2*3**4+2**4)

if __name__=='__main__': unittest.main(verbosity=2)
