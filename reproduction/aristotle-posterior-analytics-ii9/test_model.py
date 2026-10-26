import unittest
from model import *

class TeachingModelTests(unittest.TestCase):
    atoms = frozenset('abc')
    chain = ((frozenset('a'), 'b'), (frozenset('b'), 'c'))
    cycle = ((frozenset('a'), 'b'), (frozenset('b'), 'a'))
    def test_empty_language(self):
        self.assertEqual(derive(set(), set(), ()), (frozenset(), ()))
    def test_assumption_is_retained(self):
        self.assertEqual(derive(self.atoms, {'a'}, ())[0], frozenset('a'))
    def test_chain(self):
        self.assertEqual(derive(self.atoms, {'a'}, self.chain)[0], self.atoms)
    def test_reverse_order_still_closes(self):
        self.assertEqual(derive(self.atoms, {'a'}, self.chain[::-1])[0], self.atoms)
    def test_unrooted_cycle(self):
        self.assertEqual(derive(self.atoms, set(), self.cycle)[0], frozenset())
    def test_rooted_cycle(self):
        self.assertEqual(derive(self.atoms, {'a'}, self.cycle)[0], frozenset('ab'))
    def test_self_loop(self):
        self.assertEqual(derive(self.atoms, set(), ((frozenset('a'),'a'),))[0], frozenset())
    def test_conjunction_requires_all(self):
        self.assertNotIn('c', derive(self.atoms, {'a'}, ((frozenset('ab'),'c'),))[0])
    def test_conjunction_with_both(self):
        self.assertIn('c', derive(self.atoms, {'a','b'}, ((frozenset('ab'),'c'),))[0])
    def test_valid_certificate(self):
        _, cert = derive(self.atoms, {'a'}, self.chain)
        self.assertTrue(check_certificate(self.atoms, {'a'}, self.chain, cert, 'c'))
    def test_circular_certificate_rejected(self):
        self.assertFalse(check_certificate(self.atoms, set(), self.cycle, ((0,'b'),(1,'a')), 'a'))
    def test_future_premise_rejected(self):
        self.assertFalse(check_certificate(self.atoms, {'a'}, self.chain, ((1,'c'),(0,'b')), 'c'))
    def test_wrong_head_rejected(self):
        self.assertFalse(check_certificate(self.atoms, {'a'}, self.chain, ((0,'c'),), 'c'))
    def test_bad_index_rejected(self):
        self.assertFalse(check_certificate(self.atoms, {'a'}, self.chain, ((-1,'c'),), 'c'))
    def test_bool_index_rejected(self):
        self.assertFalse(check_certificate(self.atoms, {'a'}, self.chain, ((False,'b'),), 'b'))
    def test_duplicate_step_rejected(self):
        self.assertFalse(check_certificate(self.atoms, {'a'}, self.chain, ((0,'b'),(0,'b')), 'b'))
    def test_target_outside_language(self):
        self.assertFalse(check_certificate(self.atoms, {'a'}, (), (), 'z'))
    def test_base_is_not_independently_proven(self):
        self.assertTrue(check_certificate(self.atoms, {'a'}, (), (), 'a'))
        self.assertFalse(check_certificate(self.atoms, set(), (), (), 'a'))
    def test_invalid_base(self):
        with self.assertRaises(ValueError): derive(self.atoms, {'z'}, ())
    def test_empty_body_forbidden(self):
        with self.assertRaises(ValueError): derive(self.atoms, set(), ((frozenset(),'a'),))
    def test_outside_head(self):
        with self.assertRaises(ValueError): derive(self.atoms, set(), ((frozenset('a'),'z'),))
    def test_extensional_definition_without_existence(self):
        self.assertEqual(definition_case({0}, set(), set()), {'same_extension':True,'unit_exists':False,'description_exists':False})
    def test_extensional_definition_with_existence(self):
        self.assertTrue(definition_case({0}, {0}, {0})['unit_exists'])
    def test_existence_does_not_give_definition(self):
        self.assertFalse(definition_case({0,1}, {0}, {1})['same_extension'])
    def test_outside_extension(self):
        with self.assertRaises(ValueError): definition_case(set(), {0}, set())
    def test_exhaustive_oracle(self):
        x = experiment()
        self.assertEqual(x['base_system_instances'],4096)
        self.assertEqual(x['semantic_mismatches'],0)
        self.assertEqual(x['equal_pairs'],31)
        self.assertEqual(x['equal_empty_pairs'],5)

if __name__ == '__main__': unittest.main()
