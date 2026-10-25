import unittest
from itertools import product
from model import all_of, none_of, status, evaluate, subsets, summarize


class ModelTests(unittest.TestCase):
    def test_predicate_direction(self):
        self.assertTrue(all_of({1}, {1, 2}))
        self.assertFalse(all_of({1, 2}, {1}))
        self.assertTrue(none_of({1}, {2}))

    def test_false_is_not_wholly_false(self):
        self.assertEqual(status('all', {1, 2}, {1}), 'partly_false')
        self.assertEqual(status('none', {1, 2}, {1}), 'partly_false')
        self.assertEqual(status('all', {1}, {2}), 'wholly_false')
        self.assertEqual(status('none', {1}, {1, 2}), 'wholly_false')

    def test_empty_subject_boundary(self):
        for q in ('all', 'none'):
            self.assertEqual(status(q, set(), {1}), 'true')
        self.assertTrue(all_of(set(), {1}))
        self.assertTrue(none_of(set(), {1}))

    def test_bad_quality_rejected(self):
        with self.assertRaises(ValueError):
            status('some', {1}, {1})

    def test_all_four_forms_valid_including_empty(self):
        for form in ('Barbara', 'Celarent', 'Cesare', 'Camestres'):
            for a, b, c in product(subsets(3), repeat=3):
                states, conclusion = evaluate(form, a, b, c)
                if states == ('true', 'true'):
                    self.assertTrue(conclusion, (form, a, b, c))

    def test_barbara_two_false_example(self):
        self.assertEqual(evaluate('Barbara', {1}, {2}, {3}),
                         (('wholly_false', 'wholly_false'), False))

    def test_barbara_true_major_example(self):
        self.assertEqual(evaluate('Barbara', {1, 3}, {2}, {3}),
                         (('true', 'wholly_false'), False))

    def test_extensional_counterexample_to_unqualified_minor_false(self):
        # No B is A does NOT alone entail that every candidate C fails on B.
        self.assertEqual(evaluate('Barbara', {1}, {2}, {2, 3}),
                         (('wholly_false', 'true'), False))

    def test_celarent_three_truth_patterns(self):
        examples = [({1, 2}, {1}, {2}, ('wholly_false', 'wholly_false')),
                    ({1}, {1}, {2}, ('true', 'wholly_false')),
                    ({1}, {1}, {1, 2}, ('partly_false', 'true'))]
        for a, b, c, expected in examples:
            self.assertEqual(evaluate('Celarent', a, b, c), (expected, False))

    def test_second_figure_no_two_wholly_false_nonempty(self):
        for a, b, c in product(subsets(4, True), repeat=3):
            if all_of(b, a):
                for form in ('Cesare', 'Camestres'):
                    self.assertNotEqual(evaluate(form, a, b, c)[0],
                                        ('wholly_false', 'wholly_false'))

    def test_second_figure_two_partly_false(self):
        for form in ('Cesare', 'Camestres'):
            self.assertEqual(evaluate(form, {1, 2, 3}, {1, 2}, {1}),
                             (('partly_false', 'partly_false'), False))

    def test_second_figure_either_single_false(self):
        for form in ('Cesare', 'Camestres'):
            profiles = summarize()['forms'][form]['false_conclusion_profiles']
            self.assertIn('true,wholly_false', profiles)
            self.assertIn('wholly_false,true', profiles)
            self.assertNotIn('true,true', profiles)

    def test_summary_counts_are_partition(self):
        s = summarize()
        self.assertEqual(s['triples_including_empty'], 512)
        self.assertEqual(s['nonempty_triples'], 343)
        # 12 disjoint ordered nonempty A,B pairs, 7 possible nonempty C.
        self.assertEqual(sum(s['forms']['Barbara']['false_conclusion_profiles'].values()), 84)
        # 19 nonempty B subset A pairs, 7 possible C.
        for f in ('Celarent', 'Cesare', 'Camestres'):
            self.assertEqual(sum(s['forms'][f]['false_conclusion_profiles'].values()), 133)
        for f in s['forms'].values():
            self.assertEqual(f['soundness_counterexamples'], 0)

    def test_witnesses_recompute(self):
        for form, data in summarize()['forms'].items():
            for key, w in data['witnesses'].items():
                states, conclusion = evaluate(form, set(w['A']), set(w['B']), set(w['C']))
                self.assertEqual(','.join(states), key)
                self.assertFalse(conclusion)


if __name__ == '__main__':
    unittest.main(verbosity=2)
