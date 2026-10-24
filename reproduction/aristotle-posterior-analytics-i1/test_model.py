import unittest
from dataclasses import replace
from model import World, Ledger, Certificate, universal_truth, restricted_truth, derive, applicable, syntactic_check, semantic_check

class Tests(unittest.TestCase):
    def setUp(self):
        self.w = World(frozenset({'a','b'}), frozenset({'a'}), frozenset({'a'}))
        self.s = Ledger(frozenset({'P','Q'}), True, frozenset({'a'}), frozenset({'a'}))
    def test_explicit_application(self):
        self.assertNotIn('a', self.s.derived_q)
        after, cert = derive(self.s, 'a')
        self.assertIn('a', after.derived_q)
        self.assertTrue(semantic_check(self.w, self.s, cert))
        self.assertNotIn('a', self.s.derived_q)
    def test_missing_rule(self):
        with self.assertRaises(ValueError): derive(replace(self.s, accepts_rule=False), 'a')
    def test_missing_existence(self):
        with self.assertRaises(ValueError): derive(replace(self.s, registered=frozenset()), 'a')
    def test_missing_identification(self):
        with self.assertRaises(ValueError): derive(replace(self.s, recognizes_p=frozenset()), 'a')
    def test_missing_meaning(self):
        for meanings in (frozenset(), frozenset({'P'}), frozenset({'Q'})):
            with self.assertRaises(ValueError): derive(replace(self.s, meanings=meanings), 'a')
    def test_meaning_not_existence(self):
        s = Ledger(frozenset({'P','Q'}), True)
        self.assertFalse(applicable(s, 'a'))
    def test_same_name_different_id(self):
        labels = {'a':'this triangle','b':'this triangle'}
        self.assertEqual(labels['a'], labels['b'])
        with self.assertRaises(ValueError): derive(self.s, 'b')
    def test_wrong_identification(self):
        s = replace(self.s, registered=frozenset({'b'}), recognizes_p=frozenset({'b'}))
        after, cert = derive(s, 'b')
        self.assertTrue(syntactic_check(s, cert))
        self.assertIn('b', after.derived_q)
        self.assertFalse(semantic_check(self.w, s, cert))
    def test_false_rule_even_true_conclusion(self):
        w = World(frozenset({'a','b'}), frozenset({'a','b'}), frozenset({'a'}))
        _, cert = derive(self.s, 'a')
        self.assertFalse(universal_truth(w))
        self.assertFalse(semantic_check(w, self.s, cert))
    def test_restricted_not_universal(self):
        w = World(frozenset({'a','b'}), frozenset({'a','b'}), frozenset({'a'}))
        self.assertTrue(restricted_truth(w, frozenset({'a'})))
        self.assertFalse(universal_truth(w))
    def test_unknown_is_not_false(self):
        self.assertTrue('a' in self.w.q)
        self.assertNotIn('a', self.s.derived_q)
    def test_empty_extension_vacuity(self):
        w = World(frozenset({'a'}), frozenset(), frozenset())
        self.assertTrue(universal_truth(w))
        self.assertFalse(applicable(Ledger(frozenset({'P','Q'}),True), 'a'))
    def test_tampered_certificate(self):
        for cert in (Certificate('a', rule='reverse'),Certificate('a', premise='Q'),Certificate('a', conclusion='P')):
            self.assertFalse(syntactic_check(self.s, cert))
    def test_repeated_application_idempotent(self):
        after, _ = derive(self.s, 'a')
        twice, _ = derive(after, 'a')
        self.assertEqual(after, twice)
    def test_nonexistent_object(self):
        s = replace(self.s, registered=frozenset({'ghost'}), recognizes_p=frozenset({'ghost'}))
        _, cert = derive(s,'ghost')
        self.assertFalse(semantic_check(self.w,s,cert))
    def test_invalid_world(self):
        with self.assertRaises(ValueError): World(frozenset({'a'}),frozenset({'b'}),frozenset())

if __name__ == '__main__': unittest.main(verbosity=2)
