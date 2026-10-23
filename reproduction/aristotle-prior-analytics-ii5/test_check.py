"""Author tests; independent review is performed separately."""
import unittest
from check import Model, models, VALID, INVALID, check_schema, assumption_dependencies, run

class Checks(unittest.TestCase):
    def test_membership_models(self):
        ms = list(models())
        self.assertEqual(len(ms), 255)
        self.assertEqual(len({m.U for m in ms}), 255)
        self.assertEqual(sum(m.nonempty_terms() for m in ms), 218)
        for m in ms:
            self.assertTrue(m.U)
            self.assertTrue((m.A | m.B | m.C) <= m.U)

    def test_valid_schemas_both_domains(self):
        for nonempty in (False, True):
            domain = [m for m in models() if not nonempty or m.nonempty_terms()]
            for name, schema in VALID.items():
                with self.subTest(nonempty=nonempty, schema=name):
                    stats, failures = check_schema(domain, *schema)
                    self.assertGreater(stats['premise_models'], 0)
                    self.assertEqual(failures, [])

    def test_invalid_schemas_both_domains(self):
        for nonempty in (False, True):
            domain = [m for m in models() if not nonempty or m.nonempty_terms()]
            for name, schema in INVALID.items():
                with self.subTest(nonempty=nonempty, schema=name):
                    _, failures = check_schema(domain, *schema)
                    self.assertTrue(failures)

    def test_distinct_witnesses_explicit(self):
        m = Model(frozenset({0, 1, 2}), frozenset({0}), frozenset({1}), frozenset({2}))
        p, q = INVALID['separate_negative_witnesses_not_shared_witness']
        self.assertTrue(p(m))
        self.assertFalse(q(m))
        self.assertFalse(m.U-m.A <= m.B)

    def test_complement_reverse_is_not_implied(self):
        m = Model(frozenset({0, 1, 2}), frozenset({0}), frozenset({1}), frozenset({2}))
        self.assertTrue(m.B <= m.U-m.A)
        self.assertFalse(m.U-m.A <= m.B)
        self.assertEqual(m.A & m.B, m.B & m.A)

    def test_provenance(self):
        self.assertEqual(assumption_dependencies('derived', {'derived': ('given',), 'given': None}), {'given'})
        with self.assertRaises(ValueError):
            assumption_dependencies('x', {'x': ('y',), 'y': ('x',)})
        with self.assertRaises(KeyError):
            assumption_dependencies('missing', {})

    def test_full_report(self):
        r = run()
        self.assertEqual(r['model_counts'], {'nonempty_universe': 255, 'all_terms_nonempty': 218})
        self.assertTrue(r['dependency_demo']['cycle_refused'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
