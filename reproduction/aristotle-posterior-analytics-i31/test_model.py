"""Independent formula/bitmask checks; unittest checks remain active under -O/-OO."""
import itertools
import unittest
from model import compatible_models, report, mechanism

class Models(unittest.TestCase):
    def test_all_partial_boolean_assignments(self):
        # Independent oracle: each index is unknown, false or true.
        for n in range(8):
            for assignments in itertools.product((None, False, True), repeat=n):
                obs = [(i, v) for i, v in enumerate(assignments) if v is not None]
                got = compatible_models(n, obs)
                self.assertEqual(len(got), 2 ** assignments.count(None))
                oracle = {tuple(bool(mask & (1 << i)) for i in range(n))
                          for mask in range(2 ** n)
                          if all(bool(mask & (1 << i)) == v for i, v in obs)}
                self.assertEqual(set(got), oracle)
                self.assertEqual(report(n, obs)['universal_true_in_all_compatible_models'],
                                 all(v is True for v in assignments))
    def test_repeats_and_order(self):
        a = [(0, True), (2, False)]
        self.assertEqual(compatible_models(4, a), compatible_models(4, list(reversed(a)) * 6))
    def test_conflict(self):
        self.assertEqual(compatible_models(3, [(1, False), (1, True)]), ())
        r = report(3, [(1, False), (1, True)])
        self.assertFalse(r['consistent'])
        self.assertFalse(r['universal_true_in_all_compatible_models'])
        self.assertIsNone(r['countermodel'])
    def test_countermodel_is_real(self):
        for n in range(1, 9):
            for k in range(n):
                r = report(n, [(i, True) for i in range(k)])
                self.assertIsNotNone(r['countermodel'])
                self.assertFalse(all(r['countermodel']))
                self.assertTrue(all(r['countermodel'][i] for i in range(k)))
    def test_empty_domain_explicit(self):
        self.assertEqual(compatible_models(0, []), ((),))
        self.assertTrue(report(0, [])['universal_true_in_all_compatible_models'])
    def test_invalid_inputs(self):
        for n, obs in [(-1, []), (13, []), (True, []), (2.0, []), (2, [(2, True)]),
                       (2, [(-1, False)]), (2, [(True, True)]), (2, [(0, 1)]),
                       (2, [(0,)]), (2, ['xx'])]:
            with self.assertRaises(ValueError): compatible_models(n, obs)
    def test_mechanisms(self):
        for v in (False, True):
            self.assertEqual(mechanism('X', v, v), mechanism('Z', v, v))
        self.assertNotEqual(mechanism('X', True, False), mechanism('Z', True, False))
        self.assertEqual(mechanism('X', False, True), False)
        self.assertEqual(mechanism('Z', False, True), True)
        with self.assertRaises(ValueError): mechanism('?', False, True)
        with self.assertRaises(ValueError): mechanism('X', 1, True)

if __name__ == '__main__': unittest.main(verbosity=2)
