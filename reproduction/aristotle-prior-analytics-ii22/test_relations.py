"""Regression checks with explicit unittest checks, active under -O / -OO."""
import unittest
from relations import evaluate, census, worlds, preference, preference_census

F = frozenset


class RelationsTests(unittest.TestCase):
    def test_enumeration_and_counts(self):
        # Independent local membership counts: 2,4,3,2,2,3,3 allowed
        # types respectively; free fourth term doubles all 3-term counts.
        bases = {'chain': 4, 'negative_conversion': 8, 'negative_transfer': 6,
                 'partition_transport': 2, 'complement_pair': 2,
                 'only_coverage': 6, 'middle_transfer': 6}
        for n in (0, 1, 2, 3):
            result = census(n)
            self.assertEqual(result['worlds'], 16 ** n)
            self.assertEqual(len(set(worlds(n))), 16 ** n)
            for name, base in bases.items():
                self.assertEqual(result['rules'][name]['premise_models'], base ** n)
                self.assertEqual(result['rules'][name]['violations'], 0)

    def test_chain_requires_reverse_link(self):
        a, b, c, d, u = F({0, 1}), F({0}), F({0}), F(), F({0, 1})
        self.assertTrue(c <= b <= a)
        self.assertNotEqual(a, b)
        self.assertFalse(evaluate(a, b, c, d, u)['chain'][0])

    def test_negative_is_not_equality_or_complement(self):
        a, b, c, d, u = F({0}), F({1}), F({1}), F(), F({0, 1, 2})
        self.assertEqual(evaluate(a, b, c, d, u)['negative_conversion'], (True, True))
        self.assertNotEqual(a, b)
        self.assertNotEqual(b, u - a)

    def test_partition_coverage_is_essential(self):
        a, b, c, d, u = F(), F({0}), F(), F(), F({0})
        self.assertTrue(a.isdisjoint(b) and c.isdisjoint(d) and a == c)
        self.assertNotEqual(b, d)
        self.assertFalse(evaluate(a, b, c, d, u)['complement_pair'][0])

    def test_partition_exclusivity_is_essential(self):
        a, b, c, d, u = F({0}), F(), F({0}), F({0}), F({0})
        self.assertTrue(a | b == u and c | d == u and a == c)
        self.assertNotEqual(b, d)
        self.assertFalse(evaluate(a, b, c, d, u)['complement_pair'][0])

    def test_only_coverage_is_essential(self):
        a, b, c, d, u = F({0, 1}), F({0}), F({0}), F(), F({0, 1})
        self.assertTrue(b | c <= a and c <= b)
        self.assertNotEqual(a, b)
        self.assertFalse(evaluate(a, b, c, d, u)['only_coverage'][0])

    def test_middle_reverse_link_is_essential(self):
        a, b, c, d, u = F({0}), F({0, 1}), F({0}), F(), F({0, 1})
        self.assertTrue(c <= a and c <= b)
        self.assertFalse(b <= a)
        self.assertFalse(evaluate(a, b, c, d, u)['middle_transfer'][0])

    def test_preference_hidden_assumption(self):
        self.assertEqual(preference(3, 0, 2, 4), (True, False))
        self.assertEqual(preference(2, 0, 1, 2), (True, False))
        for a in range(1, 6):
            for d in range(1, 6):
                premise, conclusion = preference(a, -a, -d, d)
                self.assertEqual(premise, conclusion)
        result = preference_census()
        self.assertEqual(result['unrestricted']['assignments'], 2401)
        self.assertGreater(result['unrestricted']['violations'], 0)
        self.assertEqual(result['symmetric_positive']['premise_models'], 10)
        self.assertEqual(result['symmetric_positive']['violations'], 0)

    def test_input_guards(self):
        with self.assertRaises(TypeError):
            evaluate(set(), F(), F(), F(), F())
        with self.assertRaises(ValueError):
            evaluate(F({0}), F(), F(), F(), F())
        for invalid in (-1, 1.0, True):
            with self.assertRaises(ValueError):
                list(worlds(invalid))


if __name__ == '__main__':
    unittest.main(verbosity=2)
