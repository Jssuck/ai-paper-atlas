"""Independent bit-mask oracle; does not call author enumerators or formulas for expected values."""
import json
import unittest
from model import Model


def objects(n, mask):
    return [i for i in range(n) if mask & (1 << i)]


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def oracle(n, a, b, f):
    # Object-by-object truth table, independent of the author's set inclusion methods.
    strong = all(not (b >> i & 1) or (a >> i & 1) for i in range(n))
    covered = 0
    weak = True
    for x in range(1 << n):
        if not (f >> x & 1):
            continue
        eligible = all(not (x >> i & 1) or (b >> i & 1) for i in range(n))
        if eligible:
            for i in range(n):
                if x >> i & 1:
                    covered |= 1 << i
                    if not (a >> i & 1):
                        weak = False
    return strong, weak, covered


def exhaustive():
    count = 0
    triples = 0
    weak_not_strong = 0
    covered_models = 0
    all_cases = some_cases = some_not_all = 0
    universal_a_families = 0
    for n in (1, 2, 3):
        top = 1 << n
        for b in range(top):
            for f in range(1 << top):
                equivalence_for_all_a = True
                coverage = None
                for a in range(top):
                    s, w, u = oracle(n, a, b, f)
                    m = Model(range(n), objects(n, a), objects(n, b),
                              (objects(n, x) for x in range(top) if f >> x & 1))
                    check(m.strong() == s, 'strong mismatch')
                    check(m.weak() == w, 'weak mismatch')
                    check(m.eligible_union() == frozenset(objects(n, u)), 'union mismatch')
                    check(m.covers_b() == (u == b), 'coverage mismatch')
                    equivalence_for_all_a &= s == w
                    coverage = u == b
                    count += 1
                    covered_models += int(coverage)
                    weak_not_strong += int(w and not s)
                check(equivalence_for_all_a == coverage, 'all-A iff coverage failed')
                universal_a_families += 1
            for a in range(top):
                m = Model(range(n), objects(n, a), objects(n, b))
                for c in range(top):
                    triples += 1
                    strong = all(not (b >> i & 1) or (a >> i & 1) for i in range(n))
                    minor_all = all(not (c >> i & 1) or (b >> i & 1) for i in range(n))
                    common = [i for i in range(n) if (b >> i & 1) and (c >> i & 1)]
                    if strong and minor_all:
                        check(m.all_chain(objects(n, c)) is True, 'all-chain failed')
                        all_cases += 1
                    else:
                        try:
                            m.all_chain(objects(n, c))
                        except ValueError:
                            pass
                        else:
                            raise RuntimeError('invalid all-chain accepted')
                    if strong and common:
                        witness = m.some_chain_witness(objects(n, c))
                        check(type(witness) is int and witness == min(common), 'bad witness')
                        check(a >> witness & 1, 'witness outside A')
                        some_cases += 1
                        some_not_all += int(any((c >> i & 1) and not (a >> i & 1) for i in range(n)))
                    else:
                        try:
                            m.some_chain_witness(objects(n, c))
                        except ValueError:
                            pass
                        else:
                            raise RuntimeError('invalid some-chain accepted')
    result = dict(family_models=count, triples=triples, weak_without_strong=weak_not_strong,
                  covered_models=covered_models, all_chain_cases=all_cases,
                  some_chain_cases=some_cases, some_not_all_cases=some_not_all,
                  universal_A_coverage_checks=universal_a_families)
    check(result == dict(family_models=16656, triples=584, weak_without_strong=2602,
                        covered_models=10884, all_chain_cases=84, some_chain_cases=103,
                        some_not_all_cases=32, universal_A_coverage_checks=2120), 'unexpected totals')
    print(json.dumps(result, sort_keys=True))


class IndependentTests(unittest.TestCase):
    def test_zero_witness(self):
        self.assertEqual(Model([0, 2], [0], [0]).some_chain_witness([0, 2]), 0)

    def test_noncontiguous_labels(self):
        m = Model([7, 40], [7], [7], [[7]])
        self.assertTrue(m.covers_b())
        self.assertEqual(m.some_chain_witness([7, 40]), 7)

    def test_generators_once_and_repeat(self):
        m = Model((x for x in [0, 1]), iter([0]), iter([0, 1]),
                  (iter(x) for x in [[0], [1]]))
        self.assertEqual(m.eligible_union(), {0, 1})
        self.assertFalse(m.weak())
        self.assertFalse(m.weak())
        self.assertTrue(m.covers_b())

    def test_duplicates_do_not_change_semantics(self):
        m = Model([0, 0, 1], [0, 0], [0], [[0], [0], []])
        self.assertTrue(m.weak())
        self.assertTrue(m.covers_b())

    def test_empty_b_and_family(self):
        m = Model([0], [], [], [])
        self.assertTrue(m.strong())
        self.assertTrue(m.weak())
        self.assertTrue(m.covers_b())
        self.assertTrue(m.all_chain([]))
        with self.assertRaises(ValueError):
            m.some_chain_witness([])

    def test_reject_invalid_elements_every_position(self):
        for bad in [True, False, -1, 0.0, '0', None, []]:
            for index in range(3):
                args = [[0], [], []]
                args[index] = [bad]
                with self.subTest(bad=repr(bad), index=index):
                    with self.assertRaises(TypeError):
                        Model(*args)
            with self.assertRaises(TypeError):
                Model([0], [], [], [[bad]])

    def test_outside_domain(self):
        for args in [([0], [1], []), ([0], [], [1]), ([0], [], [], [[1]])]:
            with self.assertRaises(ValueError):
                Model(*args)
        for method in [Model([0], [], []).all_chain, Model([0], [], []).some_chain_witness]:
            with self.assertRaises(ValueError):
                method([1])
            with self.assertRaises(TypeError):
                method([False])

    def test_noniterables(self):
        for value in [None, 0, '0', b'0']:
            with self.assertRaises(TypeError):
                Model(value, [], [])
            with self.assertRaises(TypeError):
                Model([0], [], [], value)

    def test_freeze_not_alias(self):
        d, a, b, x = [0, 1], [0], [0], [0]
        m = Model(d, a, b, [x])
        d.clear(); a.clear(); b.clear(); x.clear()
        self.assertEqual(m.domain, {0, 1})
        self.assertEqual(m.family, (frozenset({0}),))
        self.assertTrue(m.weak())

    def test_all_powerset_covers(self):
        m = Model([0, 1], [0], [0, 1], [[], [0], [1], [0, 1]])
        self.assertTrue(m.covers_b())
        self.assertFalse(m.strong())
        self.assertFalse(m.weak())


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(IndependentTests)
    outcome = unittest.TextTestRunner(verbosity=2).run(suite)
    if not outcome.wasSuccessful():
        raise SystemExit(1)
    exhaustive()
