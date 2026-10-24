import itertools
import unittest
from syllogism import CONTRADICTORY, FIGURES, check, holds, models, refutes, report

class Tests(unittest.TestCase):
    def test_support_counts(self):
        self.assertEqual(len(list(models(False))), 128)
        self.assertEqual(len(list(models())), 109)
        self.assertEqual(len(set(models())), 109)

    def test_set_oracle_all_formulas(self):
        for support in models(False):
            sets = {name: {i for i, t in enumerate(support) if format(t, '03b')[pos] == '1'}
                    for name, pos in [('S', 2), ('M', 1), ('P', 0)]}
            for s, p in itertools.permutations('SMP', 2):
                expected = {'A': sets[s] <= sets[p], 'E': sets[s].isdisjoint(sets[p]),
                            'I': bool(sets[s] & sets[p]), 'O': bool(sets[s] - sets[p])}
                for kind in 'AEIO':
                    self.assertEqual(holds(kind, s, p, support), expected[kind])

    def test_contradictory_pairs_even_empty_terms(self):
        for support in models(False):
            for s, p in itertools.permutations('SMP', 2):
                for kind in 'AEIO':
                    self.assertNotEqual(holds(kind, s, p, support),
                                        holds(CONTRADICTORY[kind], s, p, support))
        # Contraries A/E are not contradictories: both true with empty subject.
        self.assertTrue(holds('A', 'S', 'P', (4,)))
        self.assertTrue(holds('E', 'S', 'P', (4,)))

    def test_valid_moods(self):
        self.assertEqual(report()['valid_moods'], {
            '1': ['AAA', 'AAI', 'AII', 'EAE', 'EAO', 'EIO'],
            '2': ['AEE', 'AEO', 'AOO', 'EAE', 'EAO', 'EIO'],
            '3': ['AAI', 'AII', 'EAO', 'EIO', 'IAI', 'OAO']})

    def test_two_negative_and_two_particular(self):
        for kinds in ('EO', 'IO'):
            count = 0
            for f in FIGURES:
                for a, b, c in itertools.product(kinds, kinds, 'AEIO'):
                    r = check(f, a + b + c)
                    self.assertFalse(r['valid'])
                    self.assertGreater(r['premise_models'], 0)
                    count += 1
            self.assertEqual(count, 48)

    def test_all_returned_countermodels(self):
        seen = 0
        for f in FIGURES:
            for letters in itertools.product('AEIO', repeat=3):
                r = check(f, ''.join(letters))
                self.assertGreater(r['premise_models'], 0)
                if not r['valid']:
                    w = r['first_countermodel']
                    self.assertIn(tuple(w), list(models()))
                    self.assertTrue(holds(letters[0], *FIGURES[f][0], w))
                    self.assertTrue(holds(letters[1], *FIGURES[f][1], w))
                    self.assertFalse(holds(letters[2], 'S', 'P', w))
                    seen += 1
        self.assertEqual(seen, 174)

    def test_refutation_and_existence_boundaries(self):
        self.assertTrue(refutes(1, 'AA', 'O')['valid'])
        self.assertFalse(refutes(1, 'AA', 'A')['valid'])
        self.assertTrue(refutes(1, 'EA', 'I')['valid'])
        self.assertFalse(check(2, 'AAA')['valid'])
        self.assertEqual(check(2, 'AAA')['first_countermodel'], [3, 6])
        self.assertTrue(check(3, 'AAI')['valid'])
        self.assertFalse(check(3, 'AAI', False)['valid'])
        # Nonempty universe with all three terms empty remains a legitimate countermodel.
        self.assertFalse(holds('I', 'S', 'P', ()))

    def test_invalid_inputs(self):
        for f in (0, 4, True, '1'):
            with self.assertRaises(ValueError): check(f, 'AAA')
        for mood in ('', 'AA', 'AAAA', 'AXA', None):
            with self.assertRaises(ValueError): check(1, mood)
        for support in ((0,), (8,), (True,)):
            with self.assertRaises(ValueError): holds('A', 'S', 'P', support)
        with self.assertRaises(ValueError): holds('Q', 'S', 'P', ())
        with self.assertRaises(ValueError): holds('A', 'X', 'P', ())
        with self.assertRaises(ValueError): refutes(1, 'AA', 'Q')

if __name__ == '__main__':
    unittest.main(verbosity=2)
