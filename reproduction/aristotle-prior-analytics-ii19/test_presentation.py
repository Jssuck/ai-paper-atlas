"""Tests include a finite semantic oracle independent of graph traversal."""
import itertools
import unittest
from presentation import CHAIN, SEPARATED, closure, normalize, profile, witness


class PresentationTests(unittest.TestCase):
    def test_chain_certificate(self):
        self.assertEqual(witness(CHAIN, "F", "A"), ("F", "E", "D", "C", "B", "A"))
        self.assertEqual(len(closure(CHAIN)), 15)
        self.assertIsNone(witness(CHAIN, "A", "F"))

    def test_all_120_orders(self):
        for order in itertools.permutations(CHAIN):
            with self.subTest(order=order):
                self.assertEqual(closure(order), closure(CHAIN))
                self.assertEqual(profile(order)["prefix_target_available"], [False]*4+[True])

    def test_source_prefix_and_metrics(self):
        self.assertEqual(SEPARATED[:3], (("B", "A"), ("E", "D"), ("C", "B")))
        self.assertEqual(profile(CHAIN)["prefix_closure_sizes"], [1, 3, 6, 10, 15])
        self.assertEqual(profile(SEPARATED)["prefix_closure_sizes"], [1, 2, 4, 6, 15])
        self.assertEqual(profile(CHAIN)["adjacent_shared_term_pairs"], 4)
        self.assertEqual(profile(SEPARATED)["adjacent_shared_term_pairs"], 0)

    def test_repeated_term_insufficient(self):
        edges = (("B", "A"), ("B", "C"))
        self.assertIsNone(witness(edges, "A", "C"))
        self.assertIsNone(witness(edges, "C", "A"))
        # Explicit nonempty-set countermodel: B={0}, A={0,1}, C={0,2}.
        b, a, c = {0}, {0, 1}, {0, 2}
        self.assertTrue(b <= a and b <= c)
        self.assertFalse(a <= c)
        self.assertFalse(c <= a)

    def test_no_repeated_term_no_composition(self):
        edges = (("B", "A"), ("D", "C"))
        self.assertEqual(closure(edges), frozenset(edges))

    def test_empty_unknown_cycles_duplicates_generators(self):
        self.assertEqual(closure([]), frozenset())
        self.assertIsNone(witness(CHAIN, "X", "A"))
        self.assertIsNone(witness(CHAIN, "A", "A"))
        self.assertEqual(closure(iter(CHAIN)), closure(CHAIN))
        self.assertEqual(closure(CHAIN + CHAIN), closure(CHAIN))
        self.assertEqual(closure((("A", "B"), ("B", "A"))),
                         frozenset((("A", "B"), ("B", "A"))))
        self.assertEqual(witness((("A", "B"), ("B", "C"), ("A", "C")), "A", "C"), ("A", "C"))

    def test_invalid_edges(self):
        for bad in [("A",), ("A", "A"), ("", "B"), (1, "B"), "AB", ("A", "B", "C")]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                normalize([bad])

    def test_semantic_oracle_all_three_term_graphs(self):
        # 64 graphs x 6 queries, checked against 8 single-element membership worlds.
        # Inclusion constraints act independently on each element, so this is a
        # meaningful oracle for these finite graphs, not a historical experiment.
        terms = "ABC"
        pairs = list(itertools.permutations(terms, 2))
        for mask in range(64):
            edges = tuple(edge for i, edge in enumerate(pairs) if mask & (1 << i))
            models = [dict(zip(terms, bits)) for bits in itertools.product((False, True), repeat=3)
                      if all(not dict(zip(terms, bits))[s] or dict(zip(terms, bits))[p] for s, p in edges)]
            expected = frozenset((s, p) for s, p in pairs if all(not m[s] or m[p] for m in models))
            with self.subTest(mask=mask):
                self.assertEqual(closure(edges), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
