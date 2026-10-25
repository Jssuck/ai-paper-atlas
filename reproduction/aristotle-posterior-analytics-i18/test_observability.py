"""Explicit unittest checks survive Python -O and -OO."""
import itertools
import unittest
from observability import bits, decoder, completions, run


class ObservationTests(unittest.TestCase):
    def test_exhaustive_against_all_total_decoders(self):
        checked = recoverable = 0
        for n in range(5):
            vectors = list(itertools.product((0, 1), repeat=n))
            for o in vectors:
                for t in vectors:
                    # Independent oracle searches every total map {0,1}->{0,1}.
                    exists = any(all(g[o[i]] == t[i] for i in range(n))
                                 for g in itertools.product((0, 1), repeat=2))
                    d = decoder(o, t)
                    self.assertEqual(d is not None, exists, (o, t))
                    if d is not None:
                        self.assertEqual(tuple(d[v] for v in o), t)
                    checked += 1
                    recoverable += exists
        self.assertEqual((checked, recoverable), (341, 105))

    def test_empty_and_unused_observation_value(self):
        self.assertEqual(decoder((), ()), {})
        self.assertEqual(decoder((0, 0), (1, 1)), {0: 1})
        self.assertIsNone(decoder((0, 0), (0, 1)))

    def test_channel_and_background_examples(self):
        x, y = (0, 0, 1, 1), (0, 1, 0, 1)
        self.assertIsNone(decoder(x, y))
        self.assertEqual(decoder(y, y), {0: 0, 1: 1})
        self.assertEqual(decoder((0, 1), (0, 1)), {0: 0, 1: 1})
        self.assertEqual(decoder(x, x), {0: 0, 1: 1})

    def test_sample_ambiguity_and_count(self):
        checked = ambiguous = 0
        for t in itertools.product((0, 1), repeat=4):
            for mask in itertools.product((0, 1), repeat=4):
                s = tuple(i for i, present in enumerate(mask) if present)
                candidates = completions(t, s)
                self.assertEqual(len(candidates), 2 ** (4 - len(s)))
                self.assertIn(t, candidates)
                self.assertEqual(len(candidates) == 1, len(s) == 4)
                checked += 1
                ambiguous += len(candidates) > 1
        self.assertEqual((checked, ambiguous), (256, 240))

    def test_positive_sample_not_universal(self):
        self.assertEqual(completions((1, 1), (0,)), [(1, 0), (1, 1)])
        self.assertEqual(completions((), ()), [()])

    def test_invalid_vectors(self):
        for bad in [(2,), (-1,), (True,), ('0',), (0.0,)]:
            with self.assertRaises(ValueError):
                bits(bad)
        with self.assertRaises(ValueError):
            decoder((0,), ())

    def test_invalid_samples(self):
        for sample in [(2,), (-1,), (0, 0), (True,), (0.0,)]:
            with self.assertRaises(ValueError):
                completions((0, 1), sample)

    def test_result_totals(self):
        r = run()
        self.assertEqual(r['total_pairs'], 341)
        self.assertEqual(r['total_recoverable'], 105)
        self.assertEqual(r['ambiguous_sample_target_checks'], 240)


if __name__ == '__main__':
    unittest.main(verbosity=2)
