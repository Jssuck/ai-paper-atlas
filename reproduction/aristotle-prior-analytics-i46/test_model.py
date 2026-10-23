"""Original unit tests, including API boundary and countermodel tests."""
import unittest
from model import (atoms, subsets, scope_square, complement_inclusion,
                   quantifiers, joint_denial, abilities)

class ModelTests(unittest.TestCase):
    def test_wood_countermodel(self):
        q = scope_square(['white-log','black-log','stone'], ['white-log','black-log'], ['white-log'])
        self.assertIn('stone', q.B)
        self.assertNotIn('stone', q.C)
        self.assertIn('stone', q.D)
        self.assertNotIn('stone', q.A)
    def test_square_relations(self):
        q = scope_square(['a','b','c'], ['a','b'], ['a'])
        self.assertLessEqual(q.C,q.B)
        self.assertLessEqual(q.A,q.D)
        self.assertFalse(q.A & q.C)
        self.assertEqual(q.B & q.D,q.universe-q.applicable)
    def test_full_applicability(self):
        q=scope_square(['a','b'],['a','b'],['a'])
        self.assertEqual(q.B,q.C)
        self.assertEqual(q.A,q.D)
    def test_empty_domain(self):
        q=scope_square([],[],[])
        self.assertEqual(q.B,frozenset())
    def test_empty_applicability(self):
        q=scope_square(['a'],[],[])
        self.assertEqual(q.B&q.D,frozenset(['a']))
    def test_generators(self):
        q=scope_square((x for x in ['a','b']), (x for x in ['a']), (x for x in ['a']))
        self.assertEqual(q.A,frozenset(['a']))
    def test_duplicate_atoms(self):
        self.assertEqual(atoms(['a','a'],'x'),frozenset(['a']))
    def test_string_domain_rejected(self):
        with self.assertRaises(TypeError): scope_square('a',[],[])
    def test_invalid_atom_rejected(self):
        for bad in [[''],[1],[False],[None]]:
            with self.assertRaises(TypeError): atoms(bad,'x')
    def test_outside_universe_rejected(self):
        with self.assertRaises(ValueError): scope_square(['a'],['b'],[])
    def test_positive_outside_applicable_rejected(self):
        with self.assertRaises(ValueError): scope_square(['a'],[],['a'])
    def test_strict_complement_reversal(self):
        q=complement_inclusion(['x','y','z'],['x'],['x','y'])
        self.assertLess(q['B'],q['D'])
        self.assertFalse(q['D'] <= q['B'])
        self.assertEqual(q['A']&q['D'],frozenset(['y']))
    def test_equal_inclusion(self):
        q=complement_inclusion(['x'],['x'],['x'])
        self.assertEqual(q['B'],q['D'])
    def test_bad_inclusion(self):
        with self.assertRaises(ValueError): complement_inclusion(['x'],['x'],[])
    def test_mixed_quantifier_countermodel(self):
        q=quantifiers(['w','b'],['w','b'],['w'])
        self.assertTrue(q['not_all'])
        self.assertTrue(q['some_not'])
        self.assertFalse(q['all_not'])
    def test_empty_subject(self):
        q=quantifiers(['a'],[],[])
        self.assertTrue(q['all'])
        self.assertTrue(q['all_not'])
        self.assertFalse(q['some_not'])
    def test_quantifier_no_short_circuit_skips_validation(self):
        with self.assertRaises(ValueError): quantifiers(['a'],[],['outside'])
    def test_joint_denial_is_not_single_denial(self):
        self.assertEqual(joint_denial(['a','b'],['a'],['b']),frozenset())
        self.assertNotEqual(joint_denial(['a','b'],['a'],['b']),frozenset(['b']))
    def test_two_situations(self):
        q=abilities([True,False])
        self.assertTrue(q['can_walk'])
        self.assertTrue(q['can_not_walk'])
        self.assertFalse(q['not_can_walk'])
    def test_empty_accessibility(self):
        self.assertEqual(abilities([]),{'can_walk':False,'can_not_walk':False,'not_can_walk':True})
    def test_ability_strict_bool(self):
        for bad in [[True,1],['False'],'false']:
            with self.assertRaises(TypeError): abilities(bad)
    def test_subsets_and_invalid_late_values(self):
        self.assertEqual(len(list(subsets(['a','b']))),4)
        with self.assertRaises(TypeError): list(subsets(['a',None]))

if __name__ == '__main__': unittest.main(verbosity=2)
