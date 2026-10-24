"""Independent set/assignment checks; no claim to certify real causes."""
import sys
from pathlib import Path
import itertools
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import model as m

def members(mask):
    return {w for w in range(8) if mask & (1 << w)}

def oracle_supports(premises, goal):
    good=[]
    for bits in itertools.product((False, True), repeat=len(premises)):
        ids=tuple(i for i,b in enumerate(bits) if b)
        allowed=set(range(8))
        for i in ids: allowed.intersection_update(members(premises[i]))
        if allowed and allowed <= members(goal): good.append(ids)
    return {ids for ids in good if not any(set(other)<set(ids) for other in good)}

class IndependentChecks(unittest.TestCase):
    def test_all_mask_pair_entailment_and_consistency(self):
        count=0
        for p in range(256):
            for g in range(256):
                v=m.assess([p],g)
                difference=members(p)-members(g)
                self.assertEqual(v['entails'],not difference)
                self.assertEqual(members(v['countermodels']),difference)
                self.assertEqual(v['consistent'],bool(members(p)))
                count+=bool(members(p)) and not difference
        self.assertEqual(count,3**8-2**8)
    def test_material_implication_exhaustive(self):
        for a in range(256):
            for b in range(256):
                wanted={w for w in range(8) if w not in members(a) or w in members(b)}
                self.assertEqual(members(m.implication(a,b)),wanted)
    def test_minimal_supports_independent_subsets(self):
        masks=[0,255,170,204,240,221,243,15]
        for premises in itertools.product(masks,repeat=3):
            for goal in masks:
                self.assertEqual(set(m.minimal_supports(premises,goal)),oracle_supports(premises,goal))
    def test_all_declarations_are_only_external_policy(self):
        for flags in itertools.product((False,True),repeat=5):
            for p in range(256):
                for goal in (0,240,255):
                    v=m.certificate([p],goal,m.Declarations(*flags))
                    expected=bool(members(p)) and members(p)<=members(goal) and flags[0] and flags[1] and (flags[2] or (flags[3] and flags[4]))
                    self.assertEqual(v['policy_pass'],expected)
    def test_empty_and_inconsistent_are_distinct(self):
        self.assertEqual(m.assess([],0)['models'],255)
        self.assertFalse(m.assess([],0)['entails'])
        self.assertTrue(m.assess([0],0)['entails'])
        self.assertFalse(m.assess([0],0)['consistent'])
        self.assertEqual(m.minimal_supports([0,240],255),[()])
    def test_nonminimum_cardinality_support_and_duplicates(self):
        x,y,z=map(m.atom,range(3))
        self.assertEqual(set(m.minimal_supports([y,m.implication(y,z),x,m.implication(x,y)],z)),{(0,1),(1,2,3)})
        self.assertEqual(set(m.minimal_supports([z,z],z)),{(0,),(1,)})
    def test_body_counterexamples(self):
        p,q,c=map(m.atom,range(3))
        self.assertFalse(m.assess([p,m.implication(p,q)],c)['entails'])
        self.assertTrue(m.assess([p,m.implication(p,q),m.implication(q,c)],c)['entails'])
        from fractions import Fraction
        target=Fraction(3,2)
        self.assertLess(1,target); self.assertGreater(2,target)
        self.assertNotEqual(target.denominator,1)
    def test_reject_unsupported_inputs(self):
        for bad in (-1,256,True,1.0,'0',None):
            with self.assertRaises(ValueError): m.assess([bad],240)
            with self.assertRaises(ValueError): m.minimal_supports([240],bad)
        with self.assertRaises(ValueError): m.certificate([240],240,m.Declarations(True,True,1))

if __name__=='__main__': unittest.main(verbosity=2)
