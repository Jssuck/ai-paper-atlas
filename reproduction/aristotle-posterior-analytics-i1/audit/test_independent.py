"""Independent diagnostics using explicit truth tables and boundary scenarios."""
import sys
import unittest
from pathlib import Path
from itertools import product
from dataclasses import replace
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from model import World, Ledger, Certificate, derive, applicable, universal_truth, restricted_truth, syntactic_check, semantic_check

class IndependentAudit(unittest.TestCase):
    def test_pointwise_truth_tables_domains_zero_to_four(self):
        comparisons = 0
        for n in range(5):
            ids = tuple(map(str, range(n)))
            for rows in product(tuple(product((False, True), repeat=3)), repeat=n):
                p = frozenset(i for i,row in zip(ids,rows) if row[0])
                q = frozenset(i for i,row in zip(ids,rows) if row[1])
                r = frozenset(i for i,row in zip(ids,rows) if row[2])
                w = World(frozenset(ids),p,q)
                u = not any(a and not b for a,b,_ in rows)
                v = not any(a and c and not b for a,b,c in rows)
                self.assertEqual(universal_truth(w),u)
                self.assertEqual(restricted_truth(w,r),v)
                self.assertFalse(u and not v)
                comparisons += 1
        self.assertEqual(comparisons,4681)
    def test_no_world_input_and_prior_output_preserved(self):
        s = Ledger(frozenset({'P','Q'}),True,frozenset({'a'}),frozenset({'a'}),frozenset({'old'}))
        after,c = derive(s,'a')
        self.assertEqual(after.derived_q,frozenset({'old','a'}))
        self.assertEqual(s.derived_q,frozenset({'old'}))
        true_world = World(frozenset({'a'}),frozenset({'a'}),frozenset({'a'}))
        false_world = World(frozenset({'a'}),frozenset({'a'}),frozenset())
        self.assertTrue(semantic_check(true_world,s,c))
        self.assertFalse(semantic_check(false_world,s,c))
        self.assertEqual(derive(s,'a'),(after,c))
    def test_false_identification_true_conclusion_rejected(self):
        s=Ledger(frozenset({'P','Q'}),True,frozenset({'a'}),frozenset({'a'}))
        w=World(frozenset({'a'}),frozenset(),frozenset({'a'}))
        _,c=derive(s,'a')
        self.assertTrue(universal_truth(w))
        self.assertTrue(syntactic_check(s,c))
        self.assertFalse(semantic_check(w,s,c))
    def test_same_display_name_does_not_transfer_support(self):
        s=Ledger(frozenset({'P','Q'}),True,frozenset({'id-1','id-2'}),frozenset({'id-1'}))
        self.assertTrue(applicable(s,'id-1'))
        self.assertFalse(applicable(s,'id-2'))
        with self.assertRaises(ValueError): derive(s,'id-2')
        self.assertFalse(syntactic_check(s,Certificate('id-2')))
    def test_certificates_check_support_not_execution_history(self):
        s=Ledger(frozenset({'P','Q'}),True,frozenset({'a'}),frozenset({'a'}))
        self.assertEqual(s.derived_q,frozenset())
        self.assertTrue(syntactic_check(s,Certificate('a')))
        self.assertFalse(syntactic_check(replace(s,accepts_rule=False),Certificate('a')))
    def test_all_gate_combinations(self):
        for meaning_p,meaning_q,rule,exists,identified in product((False,True),repeat=5):
            meanings=frozenset(x for x,yes in [('P',meaning_p),('Q',meaning_q)] if yes)
            s=Ledger(meanings,rule,frozenset({'a'}) if exists else frozenset(),frozenset({'a'}) if identified else frozenset())
            expected=all((meaning_p,meaning_q,rule,exists,identified))
            self.assertEqual(applicable(s,'a'),expected)
            if expected:
                after,_=derive(s,'a');self.assertIn('a',after.derived_q)
            else:
                with self.assertRaises(ValueError):derive(s,'a')

if __name__=='__main__':unittest.main(verbosity=2)
