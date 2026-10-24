"""Independent boolean-table oracle and explicit boundary tests. No assert statements."""
import unittest
from model import Model, categorical, modal, de_dicto, de_re, models, audit

def oracle(m, mode, kind, scope):
    sm = [[x in [i for i in range(m.n) if mask & (2**i)] for x in range(m.n)] for mask in m.s]
    pm = [[x in [i for i in range(m.n) if mask & (2**i)] for x in range(m.n)] for mask in m.p]
    def aggregate(bits):
        total = sum(bits)
        return total == len(bits) if mode == 'N' else total > 0 if mode == 'P' else 0 < total < len(bits)
    if scope == 'dc':
        bits = []
        for ss, pp in zip(sm, pm):
            intersection = sum(a and b for a, b in zip(ss, pp))
            difference = sum(a and not b for a, b in zip(ss, pp))
            bits.append({'A': difference == 0, 'E': intersection == 0,
                         'I': intersection > 0, 'O': difference > 0}[kind])
        return aggregate(bits)
    witnesses = [aggregate([pp[x] if kind in 'AI' else not pp[x] for pp in pm])
                 for x in range(m.n) if sm[0][x]]
    return sum(witnesses) == len(witnesses) if kind in 'AE' else sum(witnesses) > 0

class TestSemantics(unittest.TestCase):
    def test_01_independent_exhaustive_oracle(self):
        comparisons = 0
        count = 0
        for m in models():
            count += 1
            for mode in 'NPC':
                for kind in 'AEIO':
                    for scope, fn in [('dc', de_dicto), ('dr', de_re)]:
                        self.assertEqual(fn(m, mode, kind), oracle(m, mode, kind, scope), (m, mode, kind, scope))
                        comparisons += 1
        self.assertEqual(count, 4452)
        self.assertEqual(comparisons, 106848)
        print('Independent boolean-table oracle: 4452 models; 106848 comparisons; zero mismatches')

    def test_02_categorical_truth_values(self):
        self.assertEqual([categorical(k, 1, 3) for k in 'AEIO'], [True, False, True, False])
        self.assertEqual([categorical(k, 3, 1) for k in 'AEIO'], [False, False, True, True])

    def test_03_empty_subject(self):
        m = Model(1, (0,), (0,))
        self.assertTrue(de_dicto(m, 'N', 'A'))
        self.assertFalse(de_dicto(m.reverse(), 'N', 'I'))
        self.assertTrue(de_dicto(m, 'P', 'A'))
        self.assertFalse(de_dicto(m.reverse(), 'P', 'I'))

    def test_04_nonempty_actual_not_enough_for_necessary_particular(self):
        m = Model(1, (1, 0), (1, 0))
        self.assertTrue(de_dicto(m, 'N', 'A'))
        self.assertFalse(de_dicto(m.reverse(), 'N', 'I'))

    def test_05_cross_world_witness(self):
        m = Model(2, (1, 2), (1, 2))
        self.assertTrue(de_dicto(m, 'N', 'I'))
        self.assertFalse(de_re(m, 'N', 'I'))

    def test_06_necessary_de_re_negative_not_symmetric(self):
        m = Model(2, (1, 3), (2, 2))
        self.assertTrue(de_re(m, 'N', 'E'))
        self.assertFalse(de_re(m.reverse(), 'N', 'E'))

    def test_07_necessary_de_re_positive_not_symmetric(self):
        m = Model(1, (1, 0), (1, 1))
        self.assertTrue(de_re(m, 'N', 'I'))
        self.assertFalse(de_re(m.reverse(), 'N', 'I'))

    def test_08_possible_negative_not_outer_negative(self):
        m = Model(1, (1, 1), (1, 0))
        self.assertTrue(de_dicto(m, 'P', 'E'))
        self.assertFalse(not de_dicto(m, 'P', 'I'))

    def test_09_necessity_implies_broad_possibility_not_contingency(self):
        self.assertTrue(modal('N', [True, True]))
        self.assertTrue(modal('P', [True, True]))
        self.assertFalse(modal('C', [True, True]))

    def test_10_narrow_contingency_not_probability(self):
        self.assertTrue(modal('C', [True, False]))
        self.assertTrue(modal('C', [True]*99 + [False]))

    def test_11_de_re_contingent_E_not_convertible(self):
        m = Model(2, (1, 1), (3, 0))
        self.assertTrue(de_re(m, 'C', 'E'))
        self.assertFalse(de_re(m.reverse(), 'C', 'E'))

    def test_12_de_re_contingent_O_not_convertible(self):
        m = Model(1, (1, 1), (1, 0))
        self.assertTrue(de_re(m, 'C', 'O'))
        self.assertFalse(de_re(m.reverse(), 'C', 'O'))

    def test_13_quality_conversion_not_term_conversion(self):
        for m in models():
            self.assertEqual(de_re(m, 'C', 'A'), de_re(m, 'C', 'E'))
            self.assertEqual(de_re(m, 'C', 'I'), de_re(m, 'C', 'O'))

    def test_14_rule_counts(self):
        data = audit()
        self.assertEqual(data['models'], 4452)
        self.assertEqual(data['rule_checks_per_model'], 30)
        for mode in 'NP':
            for kind in 'EI':
                row = data['rules'][f'dc_{mode}{kind}_to_{mode}{kind}_reverse']
                self.assertGreater(row['premise_models'], 0)
                self.assertEqual(row['countermodels'], 0)
            self.assertEqual(data['rules'][f'dc_{mode}A_to_{mode}I_reverse_all_worlds_S_nonempty']['countermodels'], 0)
            self.assertGreater(data['rules'][f'dc_{mode}O_to_{mode}O_reverse']['countermodels'], 0)
        self.assertEqual(data['rules']['dc_CE_to_CE_reverse']['countermodels'], 0)
        self.assertGreater(data['rules']['dr_CO_to_CO_reverse']['countermodels'], 0)

    def test_15_invalid_models(self):
        for args in [(0, (0,), (0,)), (True, (0,), (0,)), (1, (), ()), (1, (0,), (0, 1)),
                     (1, (2,), (0,)), (1, (-1,), (0,)), (1, (True,), (0,)), (1, [0], [0])]:
            with self.assertRaises(ValueError): Model(*args)

    def test_16_invalid_operators(self):
        with self.assertRaises(ValueError): categorical('Z', 0, 0)
        with self.assertRaises(ValueError): modal('Z', [True])
        with self.assertRaises(ValueError): modal('N', [])
        with self.assertRaises(ValueError): de_re(Model(1, (0,), (0,)), 'N', 'AI')
        with self.assertRaises(ValueError): de_re(Model(1, (0,), (0,)), 'Z', 'A')

    def test_17_strict_contingency_A_not_weakening(self):
        m = Model(2, (1, 3), (1, 1))
        self.assertTrue(de_dicto(m, 'C', 'A'))
        self.assertTrue(all(m.s))
        self.assertFalse(de_dicto(m.reverse(), 'C', 'I'))

    def test_18_double_reversal(self):
        for m in models(): self.assertEqual(m.reverse().reverse(), m)

if __name__ == '__main__':
    unittest.main(verbosity=2)
