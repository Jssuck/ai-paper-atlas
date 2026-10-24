import unittest
from fractions import Fraction
from model import *

class ModelTests(unittest.TestCase):
    def test_empty_definition(self): self.assertTrue(definition_holds(0,0,3)); self.assertFalse(has_instance(0,3))
    def test_nonempty_definition(self): self.assertTrue(definition_holds(5,5,3)); self.assertTrue(has_instance(5,3))
    def test_different_extensions(self): self.assertFalse(definition_holds(1,3,3))
    def test_invalid_mask(self):
        for m,n in [(-1,3),(8,3),(0,0),(0,9)]:
            with self.assertRaises(ValueError): extension(m,n)
    def test_boolean_not_mask(self):
        with self.assertRaises(TypeError): extension(True,3)
    def test_boolean_not_size(self):
        with self.assertRaises(TypeError): extension(0,True)
    def test_integer_subtraction(self):
        self.assertEqual(subtract_equals(*[Quantity('number',v) for v in (5,5,2,2)]),(Quantity('number',3),Quantity('number',3)))
    def test_fraction_subtraction(self):
        self.assertEqual(subtract_equals(*[Quantity('magnitude',v) for v in (Fraction(3,2),Fraction(3,2),Fraction(1,2),Fraction(1,2))])[0].value,1)
    def test_zero_remainder_convention(self): self.assertEqual(subtract_equals(*[Quantity('number',2)]*4)[0].value,0)
    def test_cross_kind(self):
        with self.assertRaises(ValueError): subtract_equals(Quantity('number',2),Quantity('magnitude',2),Quantity('number',1),Quantity('number',1))
    def test_unequal_premises(self):
        for row in [(2,3,1,1),(3,3,1,2)]:
            with self.assertRaises(ValueError): subtract_equals(*[Quantity('number',v) for v in row])
    def test_not_removable(self):
        with self.assertRaises(ValueError): subtract_equals(*[Quantity('number',v) for v in (1,1,2,2)])
    def test_invalid_quantity(self):
        for kind,value,error in [('other',1,ValueError),('number',Fraction(1,2),ValueError),('number',-1,ValueError),('number',True,TypeError),('magnitude',1.0,TypeError)]:
            with self.assertRaises(error): Quantity(kind,value)
    def test_definition_not_hypothesis(self):
        for a in ('accept','neutral','reject'): self.assertEqual(learner_status('definition',False,False,a),'meaning_only')
    def test_relative_labels(self):
        self.assertEqual(learner_status('proposition',True,False,'accept'),'relative_hypothesis')
        for a in ('neutral','reject'): self.assertEqual(learner_status('proposition',True,False,a),'postulate_relative_to_learner')
    def test_proved_flag_not_acceptance(self):
        for a in ('accept','neutral','reject'): self.assertEqual(learner_status('proposition',True,True,a),'declared_proved')
    def test_outside_classification(self): self.assertEqual(learner_status('proposition',False,False,'accept'),'outside_relative_classification')
    def test_invalid_policy(self):
        for args,error in [(('x',False,False,'accept'),ValueError),(('definition',True,False,'accept'),ValueError),(('proposition',False,True,'accept'),ValueError),(('proposition',1,False,'accept'),TypeError),(('proposition',True,False,'x'),ValueError)]:
            with self.assertRaises(error): learner_status(*args)
    def test_diagram_gap(self): self.assertEqual(diagram_gap(Fraction(999,1000),1),Fraction(1,1000))
    def test_invalid_diagram(self):
        with self.assertRaises(TypeError): diagram_gap(0.999,1)
        with self.assertRaises(ValueError): diagram_gap(-1,1)
    def test_oracles(self):
        r=enumerate_models()
        self.assertEqual(sum(x['pairs'] for x in r['definition_models']),340)
        self.assertEqual(sum(x['definitions'] for x in r['definition_models']),30)
        self.assertEqual(sum(x['empty_definitions'] for x in r['definition_models']),4)
        self.assertEqual(sum(x['oracle_mismatches'] for x in r['definition_models']+r['subtraction_models']),0)
        self.assertEqual([x['accepted'] for x in r['subtraction_models']],[21,21])

if __name__ == '__main__': unittest.main(verbosity=2)
