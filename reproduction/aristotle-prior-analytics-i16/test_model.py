import unittest
from model import Model, examples, models


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.e = examples()

    def test_positive_n_validation(self):
        for n in (0, -1, True, 1.0, '1'):
            with self.assertRaises(ValueError): Model(n, ((0, 0, 0),))

    def test_world_structure_validation(self):
        for worlds in ((), [], ((0, 0),), ([0, 0, 0],), ((0, 0, 0, 0),)):
            with self.assertRaises(ValueError): Model(1, worlds)

    def test_mask_validation(self):
        for mask in (-1, 2, True, 0.0, '0'):
            with self.assertRaises(ValueError): Model(1, ((mask, 0, 0),))

    def test_actual_validation(self):
        for actual in (-1, 1, True, 0.0):
            with self.assertRaises(ValueError): Model(1, ((0, 0, 0),), actual)

    def test_query_validation(self):
        m = self.e['empty_subject']
        for args in (('D', 'A', 'K'), ('A', 'D', 'K'), ('A', 'B', 'bad'), ('A', 'B', 'K', 'many')):
            with self.assertRaises(ValueError): m.modal(*args)
        with self.assertRaises(ValueError): m.categorical('A', 'B', 'bad')
        for w in (-1, 1, True, 0.0):
            with self.assertRaises(ValueError): m.mask('A', w)
        with self.assertRaises(ValueError): m.jointly_possible('A', 'B', 1)

    def test_empty_subject(self):
        m = self.e['empty_subject']
        for mode in ('K', 'N+', 'N-', 'M+', 'M-'):
            self.assertTrue(m.modal('A', 'C', mode))
            self.assertFalse(m.modal('A', 'C', mode, 'some'))
        self.assertTrue(m.categorical('A', 'C', 'A'))
        self.assertTrue(m.categorical('A', 'C', 'E'))
        self.assertFalse(m.categorical('A', 'C', 'I'))
        self.assertFalse(m.categorical('A', 'C', 'O'))

    def test_actual_index_changes_subject(self):
        a = Model(1, ((0, 0, 0), (1, 1, 1)), 0)
        b = Model(1, a.worlds, 1)
        self.assertFalse(a.modal('A', 'C', 'K', 'some'))
        self.assertTrue(b.modal('A', 'C', 'K', 'some'))
        self.assertTrue(b.categorical('A', 'C', 'I'))

    def test_direct_all_and_some(self):
        m = Model(2, ((1, 3, 3), (2, 3, 3)))
        for q in ('all', 'some'):
            self.assertTrue(m.modal('A', 'B', 'K'))
            self.assertTrue(m.modal('B', 'C', 'N+', q))
            self.assertTrue(m.modal('A', 'C', 'K', q))

    def test_direct_not_actual_or_necessary(self):
        m = Model(1, ((0, 1, 1), (1, 1, 1)))
        self.assertTrue(m.modal('A', 'B', 'K'))
        self.assertTrue(m.modal('B', 'C', 'N+'))
        self.assertFalse(m.categorical('A', 'C', 'A'))
        self.assertFalse(m.modal('A', 'C', 'N+'))
        self.assertFalse(m.modal('A', 'C', 'N-'))

    def test_local_positive_reverse_failure_nonempty(self):
        m = self.e['local_positive_not_possible']
        self.assertTrue(all(m.mask(t) for t in ('A', 'B', 'C')))
        self.assertTrue(m.modal('A', 'B', 'N+'))
        self.assertTrue(m.modal('B', 'C', 'K'))
        self.assertFalse(m.modal('A', 'C', 'M+'))
        self.assertFalse(m.stable_positive('A', 'B'))

    def test_stable_positive_not_strong(self):
        m = self.e['stable_positive_not_strong']
        self.assertTrue(m.stable_positive('A', 'B'))
        self.assertTrue(m.modal('B', 'C', 'K'))
        self.assertTrue(m.modal('A', 'C', 'N+'))
        self.assertFalse(m.modal('A', 'C', 'K'))

    def test_stable_positive_not_actual(self):
        m = self.e['stable_positive_not_actual']
        self.assertTrue(m.stable_positive('A', 'B'))
        self.assertTrue(m.modal('B', 'C', 'K'))
        self.assertTrue(m.modal('A', 'C', 'M+'))
        self.assertFalse(m.categorical('A', 'C', 'A'))

    def test_symmetric_negative_nonempty_not_necessary(self):
        m = self.e['symmetric_negative_not_necessary']
        self.assertTrue(all(m.mask(t) for t in ('A', 'B', 'C')))
        self.assertTrue(m.symmetric_negative('A', 'B'))
        self.assertTrue(m.modal('B', 'C', 'K'))
        self.assertTrue(m.categorical('A', 'C', 'E'))
        self.assertTrue(m.modal('A', 'C', 'M-'))
        self.assertFalse(m.modal('A', 'C', 'N-'))
        self.assertTrue(m.mask('A', 1) & m.mask('B', 1))

    def test_symmetric_negative_not_strong(self):
        m = self.e['symmetric_negative_not_strong']
        self.assertTrue(m.symmetric_negative('A', 'B'))
        self.assertTrue(m.modal('B', 'C', 'K'))
        self.assertTrue(m.modal('A', 'C', 'N-'))
        self.assertFalse(m.modal('A', 'C', 'K'))

    def test_one_way_negative_no_conversion(self):
        m = self.e['one_way_negative_not_actual']
        self.assertTrue(m.modal('A', 'B', 'N-'))
        self.assertFalse(m.modal('B', 'A', 'N-'))
        self.assertTrue(m.modal('B', 'C', 'K'))
        self.assertFalse(m.categorical('A', 'C', 'E'))

    def test_world_disjointness_not_symmetric_anchor(self):
        m = Model(1, ((1, 0, 1), (0, 1, 1)))
        self.assertTrue(all(not (a & b) for a, b, _ in m.worlds))
        self.assertTrue(m.modal('B', 'C', 'K'))
        self.assertFalse(m.symmetric_negative('A', 'B'))
        self.assertFalse(m.categorical('A', 'C', 'E'))

    def test_negative_minor_counterpair(self):
        for name, endpoint in (('negative_minor_positive_endpoint', 'N+'),
                               ('negative_minor_negative_endpoint', 'N-')):
            m = self.e[name]
            self.assertTrue(m.modal('A', 'B', 'K'))
            self.assertTrue(m.modal('B', 'C', 'N-'))
            self.assertTrue(m.modal('A', 'C', endpoint))
            self.assertFalse(m.modal('A', 'C', 'K'))

    def test_particular_major_counterpair(self):
        for name, endpoint in (('particular_major_no_positive_endpoint', 'N-'),
                               ('particular_major_positive_endpoint', 'N+')):
            m = self.e[name]
            self.assertTrue(m.modal('A', 'B', 'N+', 'some'))
            self.assertTrue(m.modal('B', 'C', 'K'))
            self.assertTrue(m.modal('A', 'C', endpoint))

    def test_pointwise_not_joint(self):
        m = self.e['pointwise_not_joint']
        self.assertTrue(m.modal('A', 'C', 'K'))
        self.assertFalse(m.jointly_possible('A', 'C'))
        self.assertFalse(m.jointly_possible('A', 'C', False))

    def test_same_witness_required(self):
        m = self.e['different_witnesses']
        self.assertTrue(m.modal('A', 'C', 'M+', 'some'))
        self.assertTrue(m.modal('A', 'C', 'M-', 'some'))
        self.assertFalse(m.modal('A', 'C', 'K', 'some'))

    def test_contingency_not_term_conversion(self):
        m = Model(1, ((0, 1, 1), (1, 1, 1)))
        self.assertTrue(m.modal('A', 'B', 'K'))
        self.assertFalse(m.modal('B', 'A', 'K', 'some'))
        # Switching the sign presentation of K adds no new condition;
        # switching predicate and subject is a different operation.

    def test_single_world_contingency_requires_empty_subject(self):
        for m in models(1, 1):
            self.assertEqual(m.modal('A', 'C', 'K'), m.mask('C') == 0)
            self.assertFalse(m.modal('A', 'C', 'K', 'some'))

    def test_small_exhaustive_theorems(self):
        count = 0
        for m in models(1):
            count += 1
            for q, quality in (('all', 'E'), ('some', 'O')):
                if m.modal('A', 'B', 'K') and m.modal('B', 'C', 'N+', q):
                    self.assertTrue(m.modal('A', 'C', 'K', q))
                if m.stable_positive('A', 'B') and m.modal('B', 'C', 'K', q):
                    self.assertTrue(m.modal('A', 'C', 'M+', q))
                if m.symmetric_negative('A', 'B') and m.modal('B', 'C', 'K', q):
                    self.assertTrue(m.categorical('A', 'C', quality))
                    self.assertTrue(m.modal('A', 'C', 'M-', q))
        self.assertEqual(count, 128)

    def test_generator_validation_and_size(self):
        for args in ((0,), (True,), (1, 0), (1, True)):
            with self.assertRaises(ValueError): next(models(*args))
        self.assertEqual(sum(1 for _ in models(1, 1)), 8)

if __name__ == '__main__':
    unittest.main()
