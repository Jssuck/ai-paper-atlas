import unittest
import induction as m


class InductionTests(unittest.TestCase):
    def test_subset_direction(self):
        self.assertTrue(m.subset(1, 3))
        self.assertFalse(m.subset(3, 1))

    def test_complete_transfer(self):
        x = m.countermodel('complete', 3, 7, 3, 3)
        self.assertTrue(x['observations'] and x['classification'] and x['coverage'] and x['universal'])

    def test_missing_coverage(self):
        x = m.countermodel('incomplete', 2, 1, 3, 1)
        self.assertTrue(x['observations'] and x['classification'] and x['particular'])
        self.assertFalse(x['coverage'] or x['universal'])
        self.assertEqual(x['missed_failures'], [1])

    def test_missing_observation(self):
        x = m.countermodel('unobserved', 1, 0, 1, 1)
        self.assertTrue(x['classification'] and x['coverage'])
        self.assertFalse(x['observations'] or x['universal'])

    def test_empty_sample(self):
        x = m.countermodel('empty', 1, 0, 1, 0)
        self.assertTrue(x['observations'] and x['classification'])
        self.assertFalse(x['particular'])

    def test_empty_domain_universal_not_existential(self):
        x = m.countermodel('empty universe', 0, 0, 0, 0)
        self.assertTrue(x['universal'] and x['coverage'])
        self.assertFalse(x['particular'])

    def test_classification_not_minimally_required(self):
        x = m.countermodel('extra cases', 2, 3, 1, 3)
        self.assertTrue(x['coverage'] and x['observations'] and x['universal'])
        self.assertFalse(x['classification'])

    def test_coverage_not_required_for_accidental_truth(self):
        x = m.countermodel('accident', 2, 3, 3, 1)
        self.assertTrue(x['universal'])
        self.assertFalse(x['coverage'])

    def test_full_enumeration(self):
        r = m.experiment()
        self.assertEqual(r['worlds'], sum(8**n for n in range(5)))
        self.assertEqual(r['coverage_iff_forall_A']['pairs'], sum(4**n for n in range(5)))
        self.assertTrue(all(x['violations'] == 0 for x in r['rules'].values()))
        self.assertGreater(r['weak_observation_classification']['false_universal'], 0)

    def test_runtime_check_not_optimized_away(self):
        with self.assertRaises(RuntimeError):
            m.require(False, 'deliberate failure')

    def test_invalid_bounds(self):
        for value in (-1, 7, True, 1.5):
            with self.assertRaises(ValueError):
                m.experiment(value)


if __name__ == '__main__':
    unittest.main(verbosity=2)
