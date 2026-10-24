import unittest
from dataclasses import replace
from model import *

def fixture():
    p = Premise('p', 0b10101010, True, True, 0, 3)
    return Candidate((p,), 'q', 0b11101110, 1, 1, 2, frozenset({('p','q')}))

class Tests(unittest.TestCase):
    def test_valid(self): self.assertTrue(entails([0b10101010], 0b11101110))
    def test_invalid_reverse(self): self.assertFalse(entails([0b11101110], 0b10101010))
    def test_counterworld(self): self.assertEqual(counterworlds([0b11101110],0b10101010),(2,6))
    def test_false_premise_vacuity(self): self.assertTrue(entails([0], 0b10101010))
    def test_empty_premise(self): self.assertFalse(entails([],1)); self.assertTrue(entails([],255))
    def test_pass_is_not_knowledge(self):
        r=inspect_candidate(fixture()); self.assertTrue(r['declared_policy_pass']); self.assertFalse(r['scientific_knowledge_certified'])
    def test_false_actual(self): self.assertFalse(inspect_candidate(replace(fixture(),actual_world=0))['declared_policy_pass'])
    def test_primary(self):
        c=fixture(); self.assertFalse(inspect_candidate(replace(c,premises=(replace(c.premises[0],primary_declared=False),)))['declared_policy_pass'])
    def test_immediate(self):
        c=fixture(); self.assertFalse(inspect_candidate(replace(c,premises=(replace(c.premises[0],immediate_declared=False),)))['declared_policy_pass'])
    def test_confidence_equal(self): self.assertFalse(inspect_candidate(replace(fixture(),conclusion_confidence=3))['declared_policy_pass'])
    def test_priority(self): self.assertFalse(inspect_candidate(replace(fixture(),conclusion_priority=0))['declared_policy_pass'])
    def test_cause_absent(self): self.assertFalse(inspect_candidate(replace(fixture(),cause_links_declared=frozenset()))['declared_policy_pass'])
    def test_reverse_cause(self): self.assertFalse(inspect_candidate(replace(fixture(),cause_links_declared=frozenset({('q','p')})))['declared_policy_pass'])
    def test_definition(self): self.assertEqual(classify_starting_point(indispensable_for_any_learning=False,existence_assertion=None),'definition')
    def test_hypothesis_both_polarities(self):
        for v in (True,False): self.assertEqual(classify_starting_point(indispensable_for_any_learning=False,existence_assertion=v),'hypothesis')
    def test_axiom(self): self.assertEqual(classify_starting_point(indispensable_for_any_learning=True,existence_assertion=None),'axiom')
    def test_bad_inputs(self):
        for x in (-1,256,True,'2'):
            with self.assertRaises(ValueError): entails([x],255)
        with self.assertRaises(ValueError): inspect_candidate(replace(fixture(),actual_world=8))
        with self.assertRaises(ValueError): inspect_candidate(replace(fixture(),premises=()))
    def test_equivalent_masks_do_not_set_causes(self):
        c=replace(fixture(),conclusion_mask=0b10101010,cause_links_declared=frozenset())
        self.assertTrue(entails([c.conclusion_mask],c.premises[0].truth_mask))
        self.assertFalse(inspect_candidate(c)['checks']['cause_links_declared'])

if __name__ == '__main__': unittest.main()
