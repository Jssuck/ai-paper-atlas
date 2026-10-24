"""Independent review checks. Run from reproduction root; no external packages."""
import itertools
import unittest
from model import Rule, closure, certificate_ok, truth_oracle, finite_chain


def bit_models(n, seeds, rules):
    # Independently encode implication by bit masks, not production set operations.
    models = []
    for world in range(1 << n):
        if world & seeds != seeds:
            continue
        if all(world & p != p or world & (1 << h) for p, h in rules):
            models.append(world)
    common = (1 << n) - 1
    for world in models:
        common &= world
    return common


class IndependentTests(unittest.TestCase):
    def test_all_three_atom_unary_models(self):
        names = ('A', 'B', 'C')
        candidates = [(1 << p, h) for p in range(3) for h in range(3)]
        count = 0
        for mask in range(512):
            raw = [r for i, r in enumerate(candidates) if mask & (1 << i)]
            rules = [Rule(frozenset(names[p] for p in range(3) if a & (1 << p)), names[h]) for a, h in raw]
            for seed in range(8):
                seeds = {names[i] for i in range(3) if seed & (1 << i)}
                actual, ranks, witness = closure(names, seeds, rules)
                bits = sum(1 << names.index(a) for a in actual)
                self.assertEqual(bits, bit_models(3, seed, raw))
                self.assertTrue(certificate_ok(names, seeds, rules, actual, ranks, witness))
                count += 1
        self.assertEqual(count, 4096)

    def test_all_two_atom_horn_models(self):
        names = ('A', 'B')
        candidates = [(p, h) for p in (1, 2, 3) for h in range(2)]
        count = 0
        for mask in range(64):
            raw = [r for i, r in enumerate(candidates) if mask & (1 << i)]
            rules = [Rule(frozenset(names[p] for p in range(2) if a & (1 << p)), names[h]) for a, h in raw]
            for seed in range(4):
                seeds = {names[i] for i in range(2) if seed & (1 << i)}
                actual = closure(names, seeds, rules)[0]
                self.assertEqual(sum(1 << names.index(a) for a in actual), bit_models(2, seed, raw))
                count += 1
        self.assertEqual(count, 256)

    def test_certificate_is_sound_subset_not_completeness(self):
        rules = [Rule(frozenset('A'), 'B')]
        self.assertTrue(certificate_ok('AB', 'A', rules, {'A'}, {'A':0}, {}))
        self.assertNotEqual(closure('AB', 'A', rules)[0], frozenset('A'))
        self.assertFalse(certificate_ok('AB', [], rules, {'A','B'}, {'A':1,'B':2}, {'A':0,'B':0}))

    def test_rank_not_shortest_or_confidence(self):
        rules = [Rule(frozenset('A'), 'B')]
        self.assertTrue(certificate_ok('AB', 'A', rules, {'A','B'}, {'A':0,'B':99}, {'B':0}))
        self.assertFalse(certificate_ok('AB', 'A', rules, {'A','B'}, {'A':0,'B':0}, {'B':0}))
        self.assertEqual(closure('AB', 'A', rules)[1]['B'], 1)

    def test_text_counterexample_and_bridge(self):
        a, b, c = {1}, {1,2}, {1}
        self.assertTrue(c <= a and c <= b)
        self.assertFalse(b <= a)
        sets = [set(i for i in range(3) if m & (1 << i)) for m in range(8)]
        cycles = 0
        for a,b,c in itertools.product(sets, repeat=3):
            if b <= c and c <= a:
                self.assertTrue(b <= a)
            if c <= a and a <= b:
                self.assertTrue(c <= b)
            if a <= b and b <= c and c <= a:
                self.assertEqual(a,b); self.assertEqual(b,c); cycles += 1
        self.assertEqual(cycles,8)

    def test_unrooted_loop_is_not_fact(self):
        rules = [Rule(frozenset('A'),'B'), Rule(frozenset('B'),'A')]
        common, models = truth_oracle('AB', [], rules)
        self.assertEqual(set(models), {frozenset(),frozenset('AB')})
        self.assertEqual(common, frozenset())
        self.assertEqual(closure('AB', 'A', rules)[0], frozenset('AB'))

    def test_boundary_not_infinite_theorem(self):
        for n in range(1, 33):
            for rooted in (False, True):
                atoms, seeds, rules = finite_chain(n, rooted)
                actual, ranks, witness = closure(atoms, seeds, rules)
                self.assertEqual(actual, frozenset(atoms) if rooted else frozenset())
                if rooted:
                    self.assertEqual(ranks['p0'], n-1)
                self.assertTrue(certificate_ok(atoms,seeds,rules,actual,ranks,witness))

    def test_empty_premises_are_explicitly_excluded(self):
        with self.assertRaises(ValueError):
            closure('A', [], [Rule(frozenset(), 'A')])
        self.assertEqual(closure('A', 'A', [])[0], frozenset('A'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
