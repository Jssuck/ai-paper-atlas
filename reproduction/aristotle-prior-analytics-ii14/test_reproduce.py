"""Unit tests for the explicitly bounded teaching reconstruction."""
import unittest
from reproduce import *

class ReconstructionTests(unittest.TestCase):
    def test_model_policy_counts(self):
        self.assertEqual([len(models(x)) for x in ('empty_allowed','all_terms_nonempty','C_nonempty')],[255,218,240])
    def test_exact_negation(self):
        for m in models('empty_allowed'):
            for kind in KINDS:
                for a,b in (('A','B'),('A','C'),('C','B')):
                    x=Proposition(kind,a,b)
                    self.assertNotEqual(holds(m,x),holds(m,x.negate()))
                    self.assertEqual(x,x.negate().negate())
    def test_all_internal_routes(self):
        for r in ROUTES:
            self.assertTrue(check_route(r,'empty_allowed')['internal']['valid'],r.name)
    def test_all_direct_with_C_existence(self):
        for r in ROUTES:
            self.assertTrue(check_route(r,'C_nonempty')['direct']['valid'],r.name)
    def test_only_Darapti_needs_existence(self):
        bad=[r.name for r in ROUTES if not check_route(r,'empty_allowed')['direct']['valid']]
        self.assertEqual(bad,['F1_I_both_universal'])
    def test_empty_C_counterexample_with_A_B_nonempty(self):
        m=(1<<1)|(1<<2)
        self.assertTrue(holds(m,p('UAC')) and holds(m,p('UBC')))
        self.assertFalse(holds(m,p('IAB')))
        self.assertTrue(extension(m,'A') and extension(m,'B'))
        self.assertFalse(extension(m,'C'))
    def test_reverse_refutation(self):
        for r in ROUTES:
            self.assertTrue(check_route(r,'C_nonempty')['reverse_refutation']['valid'],r.name)
    def test_background_result_conflict(self):
        for r in ROUTES:
            self.assertTrue(check_route(r,'C_nonempty')['conflict']['incompatible'],r.name)
    def test_partial_I_O_can_coexist(self):
        m=(1<<2)|(1<<3)
        self.assertTrue(holds(m,p('IAB')) and holds(m,p('OAB')))
    def test_same_figure_alternative(self):
        # Direct III: U(A,C), I(B,C) => I(A,B).
        # Convert I(B,C) to I(C,B); internal III: E(A,B), I(C,B)
        # => O(A,C), which contradicts U(A,C). No unique-figure claim.
        ms=models('empty_allowed')
        self.assertTrue(implication(ms,(p('UAC'),p('IBC')),p('IAB'))['valid'])
        self.assertTrue(implication(ms,(p('ICB'),p('EAB')),p('OAC'))['valid'])
        for m in ms:
            self.assertEqual(holds(m,p('IBC')),holds(m,p('ICB')))
    def test_erase_background_is_invalid(self):
        self.assertFalse(implication(models('empty_allowed'),(p('UAC'),),p('UAB'))['valid'])
    def test_invalid_input(self):
        for m in (0,256,-1,True,'1',1.0):
            with self.assertRaises(ValueError): extension(m,'A')
        for x in ('','U','UABX','XAB','UAA','UAD',None):
            with self.assertRaises(ValueError): p(x)
        with self.assertRaises(ValueError): models('unknown')
        with self.assertRaises(ValueError): extension(1,'AB')
    def test_deterministic_result(self):
        self.assertEqual(run(),run())

if __name__=='__main__': unittest.main(verbosity=2)
