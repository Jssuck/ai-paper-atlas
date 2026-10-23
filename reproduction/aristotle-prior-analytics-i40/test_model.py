import unittest
from model import Formula as F, Model, licensed, models, survey


class TeachingModelTests(unittest.TestCase):
    def test_good_without_identity(self):
        m = Model(2, frozenset({0, 1}), 0, 1)
        self.assertTrue(m.holds(F.GOOD_P))
        self.assertTrue(m.holds(F.GOOD_G))
        self.assertFalse(m.holds(F.IDENTITY))

    def test_identity_without_good(self):
        m = Model(1, frozenset(), 0, 0)
        self.assertTrue(m.holds(F.IDENTITY))
        self.assertFalse(m.holds(F.GOOD_P))

    def test_unique_good_not_designated_good(self):
        m = Model(2, frozenset({0}), 0, 1)
        self.assertTrue(m.holds(F.AT_MOST_ONE_GOOD))
        self.assertFalse(m.holds(F.IDENTITY))
        self.assertFalse(m.holds(F.GOOD_G))

    def test_empty_good_is_at_most_one(self):
        m = Model(1, frozenset(), 0, 0)
        self.assertTrue(m.holds(F.AT_MOST_ONE_GOOD))
        self.assertFalse(m.holds(F.GOOD_G))

    def test_direct_preserves_goal(self):
        for f in (F.GOOD_P, F.IDENTITY):
            self.assertTrue(licensed(f, f))

    def test_no_unlicensed_goal_change(self):
        self.assertFalse(licensed(F.GOOD_P, F.IDENTITY))
        self.assertFalse(licensed(F.IDENTITY, F.GOOD_P))

    def test_equality_requires_bridge(self):
        self.assertTrue(licensed(F.IDENTITY, F.GOOD_P, frozenset({F.GOOD_G})))
        self.assertFalse(licensed(F.IDENTITY, F.GOOD_P, frozenset({F.AT_MOST_ONE_GOOD})))

    def test_reverse_requires_both_bridges(self):
        self.assertTrue(licensed(F.GOOD_P, F.IDENTITY,
                                 frozenset({F.GOOD_G, F.AT_MOST_ONE_GOOD})))
        for a in (F.GOOD_G, F.AT_MOST_ONE_GOOD):
            self.assertFalse(licensed(F.GOOD_P, F.IDENTITY, frozenset({a})))

    def test_assumptions_not_certified(self):
        m = Model(2, frozenset({0, 1}), 0, 1)
        assumptions = frozenset({F.GOOD_G, F.AT_MOST_ONE_GOOD})
        self.assertTrue(licensed(F.GOOD_P, F.IDENTITY, assumptions))
        self.assertFalse(all(m.holds(a) for a in assumptions))
        self.assertFalse(m.holds(F.IDENTITY))

    def test_invalid_domains(self):
        for n in (0, -1, True, 1.0):
            with self.assertRaises(ValueError):
                Model(n, frozenset(), 0, 0)

    def test_invalid_interpretations(self):
        for good, p, g in ((frozenset({2}), 0, 1), (frozenset(), -1, 0),
                            (frozenset(), 0, True)):
            with self.assertRaises(ValueError):
                Model(2, good, p, g)
        with self.assertRaises(TypeError):
            Model(2, {0}, 0, 1)

    def test_typed_formulas(self):
        with self.assertRaises(TypeError):
            Model(1, frozenset(), 0, 0).holds('p=g')
        with self.assertRaises(ValueError):
            licensed('good', F.IDENTITY)
        with self.assertRaises(TypeError):
            licensed(F.GOOD_P, F.IDENTITY, {'G(g)'})

    def test_model_counts(self):
        for n in range(1, 5):
            self.assertEqual(len(list(models(n))), n*n*2**n)
        self.assertEqual(survey()['models'], 346)

    def test_all_finite_rule_instances(self):
        fs = list(F)
        for n in range(1, 5):
            for m in models(n):
                for mask in range(16):
                    assumptions = frozenset(f for i, f in enumerate(fs) if mask & (1 << i))
                    for source in (F.GOOD_P, F.IDENTITY):
                        for target in (F.GOOD_P, F.IDENTITY):
                            if licensed(source, target, assumptions) and m.holds(source) and all(m.holds(a) for a in assumptions):
                                self.assertTrue(m.holds(target))

    def test_bounded_survey(self):
        for bound in (0, 7, True, 2.0):
            with self.assertRaises(ValueError):
                survey(bound)
        r = survey()
        self.assertEqual(r['identity_Gg_failures'], 0)
        self.assertEqual(r['Gp_Gg_unique_failures'], 0)
        self.assertTrue(all(r['truth_pairs'][pair] > 0 for pair in ('00','01','10','11')))


if __name__ == '__main__':
    unittest.main(verbosity=2)
