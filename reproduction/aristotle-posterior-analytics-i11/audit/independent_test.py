"""Independent finite audit: closed-model intersection, not graph reachability."""
import itertools
import pathlib
import sys
import unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from model import Literal, Rule, closure, support_status, neg, disj, cases_exhaustive

ATOMS = (Literal('p'), Literal('p', False), Literal('q'))
SUBSETS = tuple(frozenset(ATOMS[i] for i in range(3) if mask >> i & 1) for mask in range(8))
RULES = tuple(Rule(s, a) for s in SUBSETS for a in ATOMS)

def model_intersection(seed, rules):
    # Semantics: models are all supersets of seed satisfying each implication.
    models = [m for m in SUBSETS if seed <= m and all(not r.antecedents <= m or r.consequent in m for r in rules)]
    return frozenset.intersection(*models)

class IndependentAudit(unittest.TestCase):
    def test_closed_model_oracle(self):
        comparisons = 0
        for r1, r2 in itertools.product(RULES, repeat=2):
            for seed in SUBSETS:
                self.assertEqual(closure(seed, (r1, r2)), model_intersection(seed, (r1, r2)))
                comparisons += 1
        self.assertEqual(comparisons, 4608)
        print('closed-model comparisons:', comparisons)

    def test_monotonicity_and_idempotence(self):
        comparisons = 0
        for r1, r2 in itertools.product(RULES, repeat=2):
            results = {s: closure(s, (r1,r2)) for s in SUBSETS}
            for s in SUBSETS:
                self.assertEqual(closure(results[s], (r1,r2)), results[s])
                for t in SUBSETS:
                    if s <= t:
                        self.assertLessEqual(results[s], results[t])
                        comparisons += 1
        self.assertEqual(comparisons, 15552)
        print('monotonic seed pairs:', comparisons, '; idempotence cases: 4608')

    def test_support_not_truth(self):
        p, np, q = ATOMS
        for seed, expected in [((),(False,False)),((p,),(True,False)),((np,),(False,True)),((p,np),(True,True))]:
            self.assertEqual(support_status(closure(seed,()), 'p'), expected)
        self.assertEqual(closure((p,np),()), frozenset((p,np)))
        self.assertEqual(closure((p,np),(Rule(frozenset((p,)),q),)),frozenset((p,np,q)))
        self.assertNotIn(Literal('q',False),closure((p,), (Rule(frozenset((p,)),q),)))
        self.assertNotIn(np, closure((Literal('q',False),), (Rule(frozenset((p,)),q),)))
        self.assertNotIn(q,closure((np,), (Rule(frozenset((p,)),q),)))
        self.assertNotIn(q,closure((p,np),()))

    def test_k3_tables_separate_from_support(self):
        expected_neg={'T':'F','F':'T','U':'U'}
        expected_or={('F','F'):'F',('F','U'):'U',('F','T'):'T',('U','F'):'U',('U','U'):'U',('U','T'):'T',('T','F'):'T',('T','U'):'T',('T','T'):'T'}
        for v,w in expected_neg.items(): self.assertEqual(neg(v),w)
        for pair,result in expected_or.items(): self.assertEqual(disj(*pair),result)
        self.assertEqual([disj(v,neg(v)) for v in ('F','U','T')],['T','U','T'])
        self.assertEqual(neg(neg('U')),'U')

    def test_case_coverage(self):
        vals=('F','U','T')
        subsets=[{vals[i] for i in range(3) if mask>>i&1} for mask in range(8)]
        for allowed in subsets[1:]:
            for cases in subsets:
                self.assertEqual(cases_exhaustive(allowed,cases), all(v in cases for v in allowed))
        print('case coverage comparisons: 56')

    def test_identity_conjunction_and_validation(self):
        p,np,q=ATOMS
        rule=Rule(frozenset((p,np)),q)
        self.assertNotIn(q,closure((p,), (rule,)))
        self.assertIn(q,closure((p,np), (rule,)))
        self.assertIn(q,closure((),(Rule(frozenset(),q),)))
        self.assertNotIn(q,closure((Literal('p.other'),),(Rule(frozenset((p,)),q),)))
        for fn,args in [(Literal,('',)),(Literal,('p',1)),(neg,('B',)),(disj,('T','B')),(cases_exhaustive,((),('T',)))]:
            with self.assertRaises(ValueError): fn(*args)

if __name__=='__main__':
    unittest.main(verbosity=2)
