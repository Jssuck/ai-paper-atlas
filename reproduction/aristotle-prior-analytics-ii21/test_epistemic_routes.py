import unittest
from epistemic_routes import (RecognitionState, acquire_verified, census,
                              premises, recognition_census, worlds)

class RoutesTest(unittest.TestCase):
    def test_world_counts(self):
        for n in (1,2,3):
            self.assertEqual(census(n)['counts']['worlds'], 2**(4*n))
    def test_full_nonempty_impossible(self):
        for n in (1,2,3):
            self.assertEqual(census(n)['counts']['full_nonempty_D'], 0)
    def test_empty_D_is_not_contradiction(self):
        for n in (1,2,3):
            self.assertGreater(census(n)['counts']['full_empty_D'], 0)
    def test_missing_bridge_consistent(self):
        for n in (1,2,3):
            report = census(n)
            self.assertGreater(report['counts']['missing_p4_nonempty_D'],0)
            w = {t:frozenset(x) for t,x in report['missing_p4_witness'].items()}
            self.assertEqual(premises(w),(True,True,True,False))
    def test_route_soundness(self):
        for w in worlds(3):
            p1,p2,p3,p4 = premises(w)
            if p1 and p2:
                self.assertTrue(w['D'] <= w['A'])
            if p3 and p4:
                self.assertFalse(w['D'] & w['A'])
    def test_world_validation(self):
        for bad in ({}, {'A':set(),'B':frozenset(),'C':frozenset(),'D':frozenset()},
                    {t:frozenset([-1]) for t in 'ABCD'}):
            with self.assertRaises(ValueError): premises(bad)
        for n in (0,4,True,1.5,'2'):
            with self.assertRaises(ValueError): list(worlds(n))
    def test_knowledge_is_factive(self):
        w = {t:frozenset([0]) for t in 'ABCD'}
        self.assertEqual(acquire_verified(w,'B',0),('B',0))
        for pred,ind in [('B',1),('Z',0),('A',True),('A',-1)]:
            with self.assertRaises(ValueError): acquire_verified(w,pred,ind)
    def test_no_automatic_exercise(self):
        s=RecognitionState(True,True,True)
        self.assertTrue(s.available)
        self.assertFalse(s.exercised)
        self.assertFalse(s.explicit_conflict)
        self.assertTrue(s.exercise().explicit_conflict)
        self.assertFalse(s.exercised)
    def test_missing_recognition_blocks(self):
        for u,r in [(False,False),(True,False),(False,True)]:
            with self.assertRaises(ValueError): RecognitionState(u,r,True).exercise()
    def test_valid_state_invariants(self):
        for args in [(1,True,False),(True,False,False,True)]:
            with self.assertRaises(ValueError): RecognitionState(*args)
    def test_eight_state_summary(self):
        rows=recognition_census()
        self.assertEqual(len(rows),8)
        self.assertEqual(sum(r['available'] for r in rows),2)
        self.assertEqual(sum(r['conflict_after'] is True for r in rows),1)
        self.assertEqual(sum(r['conflict_after'] is None for r in rows),6)
    def test_no_error_when_opinion_absent(self):
        self.assertFalse(RecognitionState(True,True,False).exercise().explicit_conflict)

if __name__ == '__main__': unittest.main(verbosity=2)
