import unittest
from model import (checked_mask, every_instance, counterexample,
                   relative_partition, broadest_adequate, PerSeDeclarations)

class FiniteModelTests(unittest.TestCase):
    def test_inclusion(self):
        self.assertTrue(every_instance(3, 7, 3))
    def test_missing_object(self):
        self.assertEqual(counterexample(3, 1, 3, 2), (1, 0))
    def test_missing_later_time(self):
        self.assertEqual(counterexample(9, 1, 3, 2), (0, 1))
    def test_no_counterexample(self):
        self.assertIsNone(counterexample(9, 9, 3, 2))
    def test_empty_subject_vacuous(self):
        self.assertTrue(every_instance(0, 0, 6))
    def test_earliest_witness(self):
        self.assertEqual(counterexample(63, 0, 3, 2), (0, 0))
    def test_invalid_mask(self):
        for bad in (-1, 64, True, 1.5):
            with self.assertRaises(ValueError): every_instance(bad, 0, 6)
    def test_invalid_dimensions(self):
        for n, t in ((0, 2), (2, 0), (-1, 2), (True, 2)):
            with self.assertRaises(ValueError): counterexample(0, 0, n, t)
    def test_invalid_width(self):
        with self.assertRaises(ValueError): checked_mask(0, -1)
    def test_parity_partition(self):
        self.assertTrue(relative_partition(15, 5, 10, 4))
        self.assertFalse(every_instance(15, 5, 4))
        self.assertFalse(every_instance(15, 10, 4))
    def test_partition_overlap(self):
        self.assertFalse(relative_partition(15, 7, 10, 4))
    def test_partition_gap(self):
        self.assertFalse(relative_partition(15, 1, 10, 4))
    def test_outside_genus_ignored(self):
        self.assertTrue(relative_partition(3, 5, 6, 3))
    def test_triangle_level(self):
        self.assertEqual(broadest_adequate({'figure': 15, 'triangle': 7,
                                          'isosceles': 3}, 7, 4), ('triangle',))
    def test_empty_not_explanatory_candidate(self):
        self.assertEqual(broadest_adequate({'empty': 0}, 7, 4), ())
    def test_incomparable_maxima(self):
        self.assertEqual(broadest_adequate({'a': 3, 'b': 5}, 7, 3), ('a', 'b'))
    def test_coextensive_not_identified(self):
        self.assertEqual(broadest_adequate({'a': 3, 'b': 3}, 3, 2), ('a', 'b'))
    def test_omitted_broader_class(self):
        self.assertEqual(broadest_adequate({'isosceles': 3}, 7, 3), ('isosceles',))
    def test_no_truth_from_definition_label(self):
        d = PerSeDeclarations(frozenset({('triangle', 'line')}))
        self.assertEqual(d.senses('triangle', 'line'), ('definition-1',))
        self.assertFalse(every_instance(3, 1, 2))
    def test_reversed_definition_direction(self):
        d = PerSeDeclarations(subject_in_attribute_definition=frozenset({('number', 'odd')}))
        self.assertEqual(d.senses('number', 'odd'), ('definition-2',))
        self.assertEqual(d.senses('odd', 'number'), ())
    def test_four_senses_not_uniform_binary_relation(self):
        d = PerSeDeclarations(independent_subjects=frozenset({'substance'}))
        self.assertEqual(d.senses('substance', 'anything'), ('subsistence-3',))
    def test_cooccurrence_does_not_create_cause(self):
        self.assertTrue(every_instance(7, 7, 3))
        d = PerSeDeclarations()
        self.assertEqual(d.senses('walking', 'lightning'), ())
    def test_external_causal_declaration(self):
        d = PerSeDeclarations(causal_links=frozenset({('cut', 'death')}))
        self.assertEqual(d.senses('cut', 'death'), ('causal-4',))
    def test_invalid_class(self):
        with self.assertRaises(ValueError): broadest_adequate({'x': 8}, 7, 3)

if __name__ == '__main__':
    unittest.main()
