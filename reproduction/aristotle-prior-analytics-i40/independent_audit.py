"""Independent direct truth-vector oracle for I.40's modern teaching model.
Does not use production model generation or holds() to calculate expectations.
"""
import itertools
import json
import sys
import unittest
from model import Formula as F, Model, licensed, models, survey


def check(value, description):
    if not value:
        raise RuntimeError(description)


def oracle(bits, p, g):
    # Quantified definition, not production len(good) <= 1 implementation.
    unique = all(not (bits[x] and bits[y]) or x == y
                 for x in range(len(bits)) for y in range(len(bits)))
    return (bits[p], p == g, bits[g], unique)


def audit():
    formulas = (F.GOOD_P, F.IDENTITY, F.GOOD_G, F.AT_MOST_ONE_GOOD)
    counts = {'models': 0, 'formula_comparisons': 0, 'renaming_comparisons': 0,
              'rule_combinations': 0, 'applicable_licensed_rules': 0,
              'truth_pairs': dict.fromkeys(('00','01','10','11'), 0),
              'identity_Gg_premises': 0, 'Gp_Gg_unique_premises': 0,
              'empty_good_unique_true': 0}
    for n in range(1,5):
        for bits in itertools.product((False, True), repeat=n):
            ext = frozenset(i for i in range(n) if bits[i])
            for p in range(n):
                for g in range(n):
                    expected = oracle(bits,p,g)
                    m = Model(n,ext,p,g)
                    counts['models'] += 1
                    counts['truth_pairs'][f'{int(expected[0])}{int(expected[1])}'] += 1
                    counts['identity_Gg_premises'] += int(expected[1] and expected[2])
                    counts['Gp_Gg_unique_premises'] += int(expected[0] and expected[2] and expected[3])
                    if not any(bits):
                        check(expected[3], 'empty extension must satisfy at most one')
                        counts['empty_good_unique_true'] += 1
                    renamed = Model(n,frozenset(n-1-i for i in ext),n-1-p,n-1-g)
                    for f, truth in zip(formulas,expected):
                        check(m.holds(f) is truth, 'truth-vector disagreement')
                        check(renamed.holds(f) is truth, 'renaming disagreement')
                        counts['formula_comparisons'] += 1
                        counts['renaming_comparisons'] += 1
                    for selected in itertools.product((False,True),repeat=4):
                        hypotheses = frozenset(f for f, use in zip(formulas,selected) if use)
                        assumptions_true = all(t for t,use in zip(expected,selected) if use)
                        for source in (0,1):
                            for target in (0,1):
                                counts['rule_combinations'] += 1
                                accepted = licensed(formulas[source],formulas[target],hypotheses)
                                if accepted and expected[source] and assumptions_true:
                                    counts['applicable_licensed_rules'] += 1
                                    check(expected[target], 'licensed false conclusion')
    production = survey()
    for key in ('models','truth_pairs','identity_Gg_premises','Gp_Gg_unique_premises'):
        check(counts[key] == production[key], 'survey mismatch: '+key)
    check(counts['models']==346, 'enumeration size')
    return counts


class IndependentBoundaryTests(unittest.TestCase):
    def test_empty_good_is_at_most_one(self):
        self.assertTrue(Model(2,frozenset(),0,1).holds(F.AT_MOST_ONE_GOOD))
        self.assertFalse(Model(2,frozenset(),0,1).holds(F.GOOD_G))

    def test_two_members_violate_uniqueness(self):
        self.assertFalse(Model(3,frozenset({0,2}),0,2).holds(F.AT_MOST_ONE_GOOD))

    def test_distinct_goals_not_equivalent(self):
        self.assertEqual(oracle((True,True),0,1),(True,False,True,False))
        self.assertEqual(oracle((False,True),0,0),(False,True,False,True))

    def test_not_complete_even_if_target_assumed(self):
        # Logical consequence by assumption, but not a supported cross-goal rule.
        self.assertFalse(licensed(F.IDENTITY,F.GOOD_P,frozenset({F.GOOD_P})))
        self.assertFalse(licensed(F.GOOD_P,F.IDENTITY,frozenset({F.IDENTITY})))

    def test_false_assumption_does_not_certify_conclusion(self):
        m=Model(2,frozenset({0,1}),0,1)
        self.assertTrue(licensed(F.GOOD_P,F.IDENTITY,frozenset({F.GOOD_G,F.AT_MOST_ONE_GOOD})))
        self.assertFalse(m.holds(F.AT_MOST_ONE_GOOD))
        self.assertFalse(m.holds(F.IDENTITY))

    def test_model_validation(self):
        for args in ((True,frozenset(),0,0),(0,frozenset(),0,0),
                     (2,frozenset({True}),0,0),(2,frozenset({-1}),0,0),
                     (2,frozenset(),2,0),(2,frozenset(),0,0.0)):
            with self.assertRaises(ValueError):
                Model(*args)
        with self.assertRaises(TypeError):
            Model(2,[0],0,1)

    def test_formula_validation(self):
        with self.assertRaises(TypeError):
            Model(1,frozenset(),0,0).holds(None)
        for f in (F.GOOD_G,F.AT_MOST_ONE_GOOD,'G(p)',None):
            with self.assertRaises(ValueError):
                licensed(f,F.IDENTITY)
        for assumptions in ({F.GOOD_G},frozenset({'G(g)'}),None):
            with self.assertRaises(TypeError):
                licensed(F.IDENTITY,F.GOOD_P,assumptions)

    def test_generator_validates_on_iteration(self):
        for n in (0,-2,True,2.0):
            with self.assertRaises(ValueError):
                list(models(n))

    def test_no_duplicate_models(self):
        ms=list(models(4))
        keys={(m.n,m.good,m.p,m.g) for m in ms}
        self.assertEqual(len(ms),256)
        self.assertEqual(len(keys),256)

    def test_survey_rejects_unbounded_scope(self):
        for n in (0,7,True,1.5):
            with self.assertRaises(ValueError):
                survey(n)


if __name__=='__main__':
    if '--tests' in sys.argv:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    else:
        print(json.dumps(audit(),ensure_ascii=False,sort_keys=True,indent=2))
