import unittest
from model import Model, powerset


class ModelTests(unittest.TestCase):
    def test_strong_and_weak(self):
        m = Model({0, 1}, {0, 1}, {0}, ({0}, {0, 1}))
        self.assertTrue(m.strong())
        self.assertTrue(m.weak())
        self.assertEqual(m.eligible_union(), {0})

    def test_missing_coverage_counterexample(self):
        m = Model({0, 1, 2}, {0}, {0, 1}, ({0}, {1, 2}))
        self.assertTrue(m.weak())
        self.assertFalse(m.strong())
        self.assertFalse(m.covers_b())
        c = {1, 2}
        self.assertTrue(c & m.b)
        self.assertFalse(c & m.a)

    def test_coverage_detects_failure(self):
        m = Model({0, 1}, {0}, {0, 1}, ({0}, {1}))
        self.assertTrue(m.covers_b())
        self.assertFalse(m.weak())
        self.assertFalse(m.strong())

    def test_empty_family_vacuity(self):
        m = Model({0}, set(), {0})
        self.assertTrue(m.weak())
        self.assertFalse(m.strong())

    def test_empty_b(self):
        m = Model({0}, set(), set(), (set(), {0}))
        self.assertTrue(m.weak())
        self.assertTrue(m.strong())
        self.assertTrue(m.covers_b())

    def test_all_chain(self):
        self.assertTrue(Model({0, 1, 2}, {0, 1, 2}, {0, 1}).all_chain({0}))

    def test_empty_c_all_not_some(self):
        m = Model({0}, {0}, {0})
        self.assertTrue(m.all_chain(set()))
        with self.assertRaises(ValueError):
            m.some_chain_witness(set())

    def test_some_not_all(self):
        m = Model({0, 1}, {0}, {0})
        self.assertEqual(m.some_chain_witness({0, 1}), 0)
        self.assertFalse({0, 1} <= m.a)
        with self.assertRaises(ValueError):
            m.all_chain({0, 1})

    def test_some_major_insufficient_even_all_minor(self):
        m = Model({0, 1}, {0}, {0, 1})
        self.assertTrue(m.a & m.b)
        self.assertTrue({1} <= m.b)
        self.assertFalse({1} & m.a)
        with self.assertRaises(ValueError):
            m.some_chain_witness({1})

    def test_generators_materialized(self):
        m = Model(iter([0, 1]), iter([0]), iter([0]), (iter(x) for x in [[0], [1]]))
        self.assertTrue(m.weak())
        self.assertTrue(m.weak())
        self.assertTrue(m.covers_b())

    def test_input_not_mutated_or_aliased(self):
        a = {0}
        family = [{0}]
        m = Model({0, 1}, a, {0}, family)
        a.clear()
        family[0].clear()
        self.assertEqual(m.a, {0})
        self.assertEqual(m.family, (frozenset({0}),))

    def test_invalid_model_values(self):
        for args, exception in [(([], [], []), ValueError), (([0], [1], []), ValueError),
                                (([0], [], [1]), ValueError), (([0], [], [], [[1]]), ValueError),
                                (([False], [], []), TypeError), (([0], ['0'], []), TypeError),
                                (([0], [], [], [0]), TypeError), (([0], [], [], None), TypeError),
                                (('0', [], []), TypeError), (([-1], [], []), TypeError)]:
            with self.subTest(args=args):
                with self.assertRaises(exception):
                    Model(*args)

    def test_invalid_c(self):
        m = Model({0}, {0}, {0})
        for method in (m.all_chain, m.some_chain_witness):
            with self.assertRaises(ValueError):
                method({1})
            with self.assertRaises(TypeError):
                method({True})

    def test_powerset(self):
        self.assertEqual(powerset({0, 1}), (frozenset(), frozenset({0}), frozenset({1}), frozenset({0, 1})))
        with self.assertRaises(TypeError):
            powerset({True})


if __name__ == '__main__':
    unittest.main(verbosity=2)
