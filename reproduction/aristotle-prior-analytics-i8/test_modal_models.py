import unittest
from modal_models import (Model, MOODS, categorical, necessary, rigid_witnesses,
                          witnesses, premises, conclusion, propositions, exposition,
                          two_world_models, run_report)

class Tests(unittest.TestCase):
    def test_empty_domain(self):
        for n in (0, -1, True, 1.5, '2'):
            with self.assertRaises(ValueError): Model(n, ((0, 0, 0),))
    def test_world_structure(self):
        for worlds in ((), [], ((0, 0),), ([0, 0, 0],), (None,)):
            with self.assertRaises(ValueError): Model(2, worlds)
    def test_masks(self):
        for mask in (-1, 4, True, '1', 0.5):
            with self.assertRaises(ValueError): Model(2, ((mask, 0, 0),))
    def test_bad_world_indices(self):
        m = Model(1, ((1, 1, 1),))
        for w in (-1, 1, True, '0'):
            with self.assertRaises(ValueError): categorical(m, w, 'A', 'S', 'P')
    def test_bad_terms(self):
        m = Model(1, ((1, 1, 1),))
        for term in ('X', '', None, 0):
            with self.assertRaises(ValueError): necessary(m, 'A', term, 'P')
            with self.assertRaises(ValueError): necessary(m, 'A', 'S', term)
    def test_bad_kind(self):
        m = Model(1, ((1, 1, 1),))
        for kind in ('Z', '', None, 0):
            with self.assertRaises(ValueError): necessary(m, kind, 'S', 'P')
    def test_bad_rigid_kind(self):
        m = Model(1, ((1, 1, 1),))
        for kind in ('A', 'E', None, 0):
            with self.assertRaises(ValueError): rigid_witnesses(m, kind, 'S', 'P')
    def test_bad_witness_kind(self):
        with self.assertRaises(ValueError): witnesses(Model(1, ((1, 1, 1),)), 0, 'A', 'S', 'P')
    def test_vacuity(self):
        m = Model(1, ((0, 0, 0),))
        self.assertTrue(necessary(m, 'A', 'S', 'P'))
        self.assertTrue(necessary(m, 'E', 'S', 'P'))
        self.assertFalse(necessary(m, 'I', 'S', 'P'))
        self.assertFalse(necessary(m, 'O', 'S', 'P'))
    def test_switching_I(self):
        m = Model(2, ((1, 3, 0), (2, 3, 0)))
        self.assertTrue(necessary(m, 'I', 'S', 'P'))
        self.assertEqual(rigid_witnesses(m, 'I', 'S', 'P'), ())
    def test_switching_O(self):
        m = Model(2, ((2, 3, 0), (1, 3, 0)))
        self.assertTrue(necessary(m, 'O', 'S', 'P'))
        self.assertEqual(rigid_witnesses(m, 'O', 'S', 'P'), ())
    def test_positive_rigid(self):
        m = Model(2, ((3, 1, 0), (1, 3, 0)))
        self.assertEqual(rigid_witnesses(m, 'I', 'S', 'P'), (0,))
    def test_negative_rigid(self):
        m = Model(2, ((2, 3, 0), (0, 1, 0)))
        self.assertEqual(rigid_witnesses(m, 'O', 'S', 'P'), (0,))
    def test_baroco_exposition(self):
        m = Model(2, ((0, 1, 2), (0, 2, 1)))
        self.assertTrue(premises(m, 'Baroco'))
        self.assertTrue(conclusion(m, 'Baroco'))
        self.assertEqual(exposition(m, 'Baroco'), (0, 1))
    def test_bocardo_exposition(self):
        m = Model(2, ((2, 3, 1), (1, 3, 2)))
        self.assertTrue(premises(m, 'Bocardo'))
        self.assertTrue(conclusion(m, 'Bocardo'))
        self.assertEqual(exposition(m, 'Bocardo'), (0, 1))
    def test_exposition_rejects_false_premises(self):
        with self.assertRaises(ValueError): exposition(Model(1, ((0, 0, 0),)), 'Baroco')
    def test_exposition_rejects_wrong_mood(self):
        with self.assertRaises(ValueError): exposition(Model(1, ((1, 1, 1),)), 'Barbara')
    def test_unknown_mood(self):
        for name in ('Unknown', None, 0):
            with self.assertRaises(ValueError): propositions(name)
    def test_policy_validation(self):
        with self.assertRaises(ValueError): premises(Model(1, ((1, 1, 1),)), 'Barbara', 1)
    def test_enumeration_bound(self):
        for n in (0, 4, True, '2'):
            with self.assertRaises(ValueError): next(two_world_models(n))
    def test_nonempty_requirement(self):
        m = Model(1, ((0, 0, 0), (0, 0, 0)))
        for name in ('Darapti', 'Felapton'):
            self.assertTrue(premises(m, name))
            self.assertFalse(conclusion(m, name))
            self.assertFalse(premises(m, name, True))
    def test_O_not_convertible(self):
        m = Model(2, ((1, 3, 0), (1, 3, 0)))
        self.assertTrue(necessary(m, 'O', 'S', 'P'))
        self.assertFalse(necessary(m, 'O', 'P', 'S'))
    def test_mixed_necessary_major(self):
        m = Model(1, ((1, 1, 1), (0, 1, 0)))
        self.assertTrue(necessary(m, 'A', 'M', 'P'))
        self.assertTrue(categorical(m, 0, 'A', 'S', 'M'))
        self.assertFalse(necessary(m, 'A', 'S', 'P'))
    def test_mixed_necessary_minor(self):
        m = Model(1, ((1, 1, 1), (0, 1, 1)))
        self.assertTrue(categorical(m, 0, 'A', 'M', 'P'))
        self.assertTrue(necessary(m, 'A', 'S', 'M'))
        self.assertFalse(necessary(m, 'A', 'S', 'P'))
    def test_all_fourteen_moods_and_witnesses(self):
        report = run_report()
        self.assertEqual(report['models'], 4096)
        self.assertEqual(len(report['mood_results']), 14)
        for name, _, _, _, _, needs_existence in MOODS:
            row = report['mood_results'][name]
            self.assertGreater(row['premise_models_middle_nonempty'], 0)
            self.assertEqual(row['failures_middle_nonempty'], 0)
            if needs_existence: self.assertGreater(row['failures_free'], 0)
            else: self.assertEqual(row['failures_free'], 0)
        self.assertGreater(report['necessary_without_rigid_witness']['I'], 0)
        self.assertGreater(report['necessary_without_rigid_witness']['O'], 0)
        self.assertEqual(report['rigid_implies_necessary_failures'], 0)
    def test_enumeration_singleton(self):
        self.assertEqual(sum(1 for _ in two_world_models(1)), 64)
    def test_multiple_worlds(self):
        m = Model(1, ((1, 1, 1),) * 3)
        self.assertTrue(necessary(m, 'I', 'S', 'P'))
        self.assertEqual(rigid_witnesses(m, 'I', 'S', 'P'), (0,))

if __name__ == '__main__': unittest.main(verbosity=2)
