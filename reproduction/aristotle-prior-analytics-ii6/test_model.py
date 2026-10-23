"""Independent direct elementwise oracle and edge cases; standard library only."""
import unittest
from model import A,E,I,O,Model,from_mask,models,rules,survey,VALID

class ModelTests(unittest.TestCase):
    def test_orientation_and_empty(self):
        x,y=frozenset({1,2}),frozenset({1})
        self.assertTrue(A(x,y)); self.assertFalse(A(y,x))
        self.assertTrue(O(y,x)); self.assertFalse(O(x,y))
        self.assertTrue(A(x,frozenset())); self.assertTrue(E(x,frozenset()))
        self.assertFalse(I(x,frozenset())); self.assertFalse(O(x,frozenset()))

    def test_elementwise_oracle_all_pairs(self):
        terms=[frozenset(i for i in range(3) if mask & (1<<i)) for mask in range(8)]
        for x in terms:
            for y in terms:
                self.assertEqual(A(x,y),all(t in x for t in y))
                self.assertEqual(E(x,y),all(t not in x for t in y))
                self.assertEqual(I(x,y),any(t in x for t in y))
                self.assertEqual(O(x,y),any(t not in x for t in y))

    def test_counts_and_type_bits(self):
        self.assertEqual(len(list(models())),255)
        self.assertEqual(len(list(models(True))),218)
        m=from_mask(255)
        self.assertEqual(m.a,frozenset({4,5,6,7}))
        self.assertEqual(m.b,frozenset({2,3,6,7}))
        self.assertEqual(m.c,frozenset({1,3,5,7}))

    def test_valid_and_invalid_classification(self):
        for flag in (False,True):
            report=survey(flag)
            for name,data in report['rules'].items():
                self.assertGreater(data['premise_models'],0,name)
                self.assertEqual(data['countermodels']==0,name in VALID,name)

    def test_minimality_against_all_smaller_models(self):
        for flag in (False,True):
            for name,data in survey(flag)['rules'].items():
                least=data['least_countermodel']
                if least is not None:
                    n=len(least['universe'])
                    for m in models(flag):
                        if len(m.universe)<n:
                            prem,goal=rules(m)[name]
                            self.assertFalse(prem and not goal,name)

    def test_distinct_existential_witnesses(self):
        m=Model(frozenset({0,1,2}),frozenset({0}),frozenset({1}),frozenset({2}))
        self.assertEqual(rules(m)['festino_independent_witnesses'],(True,False))
        self.assertEqual(m.a & m.not_b,frozenset({0}))
        self.assertEqual(m.c & m.not_b,frozenset({2}))

    def test_coverage_uses_same_witness(self):
        for m in models():
            if A(m.a,m.not_b) and O(m.b,m.c):
                for witness in m.c-m.b:
                    self.assertIn(witness,m.a & m.c)

    def test_compression_preserves_predicates(self):
        # All labelled universes of sizes 1..4: 8**n assignments, allowing repeats.
        from itertools import product
        for n in range(1,5):
            for types in product(range(8),repeat=n):
                u=frozenset(range(n))
                m=Model(u,*(frozenset(i for i,t in enumerate(types) if t&bit) for bit in (4,2,1)))
                q=from_mask(sum(1<<t for t in set(types)))
                self.assertEqual(rules(m),rules(q))

    def test_invalid_masks_and_flags(self):
        for bad in (True,False,1.0,'1',None):
            with self.assertRaises(TypeError): from_mask(bad)
        for bad in (-1,0,256):
            with self.assertRaises(ValueError): from_mask(bad)
        with self.assertRaises(TypeError): list(models(1))

    def test_invalid_models_and_terms(self):
        f=frozenset()
        with self.assertRaises(ValueError): Model(f,f,f,f)
        with self.assertRaises(ValueError): Model(frozenset({1}),frozenset({2}),f,f)
        with self.assertRaises(TypeError): Model({1},f,f,f)
        for fn in (A,E,I,O):
            with self.assertRaises(TypeError): fn([1],{1})
            with self.assertRaises(TypeError): fn({1},None)

if __name__=='__main__': unittest.main(verbosity=2)
