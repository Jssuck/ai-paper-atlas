import unittest
from model import Atom, Rule, Bridge, Step, allowed, verify, closure, semantic_entailments, enumerate_checks

class TypedCertificates(unittest.TestCase):
    def setUp(self):
        self.a, self.b, self.c = Atom('G','p'), Atom('G','q'), Atom('O','q')
        self.bridge = Bridge('b',self.b,self.c)
        self.r = Rule(self.b,self.c,'bridge','b')
    def test_local(self): self.assertTrue(allowed(Rule(self.a,self.b)))
    def test_common_local(self): self.assertTrue(allowed(Rule(self.a,self.b,'common')))
    def test_local_cross(self): self.assertFalse(allowed(Rule(self.a,self.c)))
    def test_common_cross(self): self.assertFalse(allowed(Rule(self.a,self.c,'common')))
    def test_missing_bridge(self): self.assertFalse(allowed(self.r))
    def test_exact_bridge(self): self.assertTrue(allowed(self.r,[self.bridge]))
    def test_wrong_name(self): self.assertFalse(allowed(Rule(self.b,self.c,'bridge','other'),[self.bridge]))
    def test_wrong_source(self): self.assertFalse(allowed(Rule(self.a,self.c,'bridge','b'),[self.bridge]))
    def test_reverse(self): self.assertFalse(allowed(Rule(self.c,self.b,'bridge','b'),[self.bridge]))
    def test_same_name_different_domain(self): self.assertFalse(verify([Atom('X','q')],[Step(self.r,0)],self.c,[self.bridge]))
    def test_unknown_kind(self): self.assertFalse(allowed(Rule(self.a,self.b,'magic')))
    def test_local_cannot_carry_bridge(self): self.assertFalse(allowed(Rule(self.a,self.b,'local','b')))
    def test_sequence(self): self.assertTrue(verify([self.a],[Step(Rule(self.a,self.b),0),Step(self.r,1)],self.c,[self.bridge]))
    def test_forward_reference(self): self.assertFalse(verify([self.a],[Step(Rule(self.a,self.b),1)],self.b))
    def test_negative_reference(self): self.assertFalse(verify([self.a],[Step(Rule(self.a,self.b),-1)],self.b))
    def test_bool_reference(self): self.assertFalse(verify([self.a],[Step(Rule(self.a,self.b),False)],self.b))
    def test_wrong_goal(self): self.assertFalse(verify([self.a],[],self.b))
    def test_given_goal(self): self.assertTrue(verify([self.a],[],self.a))
    def test_unseeded_cycle(self): self.assertEqual(closure([],[Rule(self.a,self.b),Rule(self.b,self.a)]),set())
    def test_seeded_cycle(self): self.assertEqual(closure([self.a],[Rule(self.a,self.b),Rule(self.b,self.a)]),{self.a,self.b})
    def test_rejected_edge_no_entailment(self): self.assertEqual(semantic_entailments([self.a,self.c],[self.a],[Rule(self.a,self.c)]),{self.a})
    def test_policy_and_truth_enumeration(self):
        r=enumerate_checks()
        self.assertEqual(r['policy_cases'],2304)
        self.assertEqual(r['closure_cases'],1024)
        self.assertEqual(r['policy_mismatches'],0)
        self.assertEqual(r['closure_truth_mismatches'],0)

if __name__ == '__main__': unittest.main(verbosity=2)
