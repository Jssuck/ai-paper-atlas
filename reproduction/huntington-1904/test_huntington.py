"""Regression tests plus independently written small-domain reference checks."""
import unittest
from itertools import product
from huntington import *


def direct_first_closed(K, s, t):
    """Independent direct formulas for a CLOSED signature, no AST/Check objects."""
    zero=[z for z in K if all(s[a,z]==a for a in K)]
    one=[z for z in K if all(t[a,z]==a for a in K)]
    return {
        'Ia':True, 'Ib':True, 'IIa':bool(zero), 'IIb':bool(one),
        'IIIa':all(s[a,b]==s[b,a] for a,b in product(K,repeat=2)),
        'IIIb':all(t[a,b]==t[b,a] for a,b in product(K,repeat=2)),
        'IVa':all(s[a,t[b,d]]==t[s[a,b],s[a,d]] for a,b,d in product(K,repeat=3)),
        'IVb':all(t[a,s[b,d]]==s[t[a,b],t[a,d]] for a,b,d in product(K,repeat=3)),
        'V':len(zero)!=1 or len(one)!=1 or all(any(s[a,b]==one[0] and t[a,b]==zero[0] for b in K) for a in K),
        'VI':len(K)>1}


class HuntingtonTests(unittest.TestCase):
    def test_all_ten_first_original_witnesses(self):
        for target,m in first_original_models().items():
            with self.subTest(target=target): self.assertEqual(failed(first(m)),[target])

    def test_all_seven_second_original_witnesses(self):
        for target,m in second_original_models().items():
            with self.subTest(target=target): self.assertEqual(failed(second(m)),target.split(','))

    def test_all_six_third_original_witnesses(self):
        for target,m in third_original_models().items():
            with self.subTest(target=target): self.assertEqual(failed(third(m)),[target])

    def test_external_outputs_are_not_domain_members(self):
        m=first_original_models()['Ia']
        self.assertNotIn('outside',m.elements)
        self.assertEqual(m.op('+',1,1),'outside')
        with self.assertRaises(OutsideOperand): m.op('+','outside',0)

    def test_guards_do_not_assume_closure(self):
        a=first(first_original_models()['Ia'])
        b=first(first_original_models()['Ib'])
        for c in (a,b):
            self.assertGreater(c['IVa'].skipped+c['IVb'].skipped,0)
            self.assertTrue(c['IVa'].holds and c['IVb'].holds)

    def test_first_complement_vacuity(self):
        for label in ('IIa','IIb','IIIa','IIIb'):
            r=first(first_original_models()[label])['V']
            self.assertTrue(r.holds); self.assertEqual(r.checked,0)
            self.assertIn('vacuous',r.note)

    def test_original_relation_exempts_equal_bound(self):
        m=second_original_models()['1']; c=second(m)
        self.assertFalse(m.le(0,0)); self.assertFalse(m.le(1,1))
        self.assertTrue(c['4'].holds and c['5'].holds)
        self.assertEqual(c['9'].checked,0)

    def test_original_nontransitivity(self):
        m=second_original_models()['3']
        self.assertTrue(m.le(2,4) and m.le(4,3))
        self.assertFalse(m.le(2,3))

    def test_original_nonassociativity(self):
        m=third_original_models()['C']; f=lambda a,b:m.op('+',a,b)
        self.assertEqual(f(f(2,4),3),3)
        self.assertEqual(f(2,f(4,3)),1)

    def test_missing_subset_labels(self):
        self.assertEqual(mask_label(9),'u014')
        self.assertEqual(mask_label(6),'u023')
        self.assertEqual(len(fourteen_domain()),14)
        self.assertNotIn(6,fourteen_domain()); self.assertNotIn(9,fourteen_domain())

    def test_joint_failure_and_reduced_independence(self):
        c=second(second_original_models()['6,7'])
        self.assertEqual(failed(c),['6','7'])
        self.assertEqual(failed({k:v for k,v in c.items() if k!='6'}),['7'])
        self.assertEqual(failed({k:v for k,v in c.items() if k!='7'}),['6'])

    def test_fourteen_union_guarded_associativity(self):
        m=third_original_models()['F']; c=third(m)
        self.assertEqual(m.op('+',1,8),9)
        self.assertTrue(c['C'].holds)
        self.assertGreater(c['C'].skipped,0)
        self.assertFalse(c['F'].holds)

    def test_multiple_complements_never_choose_only_first(self):
        m=second_original_models()['9']; comps=relation_complements(m,0,1)
        self.assertEqual(set(comps[3]),{2,4})
        self.assertFalse(second(m)['9'].holds)
        op=third_original_models()['H']; oc=operation_complements(op,0,1)
        self.assertEqual(set(oc[3]),{2,4})
        # Original explicit witness: a=4,b=3,bar_b=2; no nonzero shared lower element.
        self.assertNotEqual(op.op('+',4,2),2)
        self.assertEqual([x for x in op.elements if op.op('+',4,x)==4 and op.op('+',3,x)==3],[0])
        self.assertFalse(third(op)['H'].holds)

    def test_third_H_original_antecedent_has_D(self):
        # Three-element closed semilattice with two minimal points and one top.
        K=(0,1,2); m=Algebra(K,{'+':{(a,b):(a if a==b else 2) for a,b in product(K,repeat=2)}})
        c=third(m)
        self.assertTrue(c['A'].holds and c['B'].holds and c['E'].holds and c['G'].holds)
        self.assertFalse(c['D'].holds)
        self.assertEqual(c['H'].checked,0)
        self.assertIn('A,D,E,G',c['H'].note)

    def test_projection_nonunique_bounds_convention(self):
        m=third_original_models()['B']; c=third(m)
        self.assertEqual(identities(m,'+'),[0,1])
        self.assertTrue(c['G'].holds and c['H'].holds)
        self.assertGreater(c['H'].checked,0)

    def test_modern_saturated_addition_only_A_fails(self):
        self.assertEqual(failed(third(teaching_saturated_addition())),['A'])

    def test_powersets_all_three_presentations(self):
        for bits in range(1,5):
            m=powerset_algebra(bits)
            for check in (first(m),second(induced_relation(m)),third(m)):
                self.assertEqual(failed(check),[])

    def test_singleton_nontriviality(self):
        m=powerset_algebra(0)
        self.assertEqual(failed(first(m)),['VI'])
        self.assertEqual(failed(second(induced_relation(m))),['10'])
        self.assertEqual(failed(third(m)),['J'])

    def test_reconstruction_from_relation(self):
        for bits in range(1,5):
            m=powerset_algebra(bits); K=m.elements; R=induced_relation(m).le
            comps=relation_complements(induced_relation(m),0,(1<<bits)-1)
            for a,b in product(K,repeat=2):
                join=[j for j in K if R(a,j) and R(b,j) and all(not(R(a,u) and R(b,u)) or R(j,u) for u in K)]
                meet=[j for j in K if R(j,a) and R(j,b) and all(not(R(u,a) and R(u,b)) or R(u,j) for u in K)]
                self.assertEqual(join,[a|b]); self.assertEqual(meet,[a&b])
                self.assertEqual(comps[comps[a][0]|comps[b][0]],[a&b])

    def test_closed_first_crosscheck_all_257_pairs(self):
        for n in (1,2):
            K=tuple(range(n)); pairs=tuple(product(K,repeat=2))
            for values in product(K,repeat=2*n*n):
                s=dict(zip(pairs,values[:n*n])); t=dict(zip(pairs,values[n*n:]))
                self.assertEqual({k:v.holds for k,v in first(Algebra(K,{'+':s,'*':t})).items()},direct_first_closed(K,s,t))

    def test_bounded_complete_counts(self):
        result=small_enumeration()
        self.assertEqual([(x['checked'],x['valid']) for x in result['first']],[(1,0),(256,2)])
        self.assertEqual([(x['checked'],x['valid']) for x in result['second']],[(2,0),(16,2),(512,0)])
        self.assertEqual([(x['checked'],x['valid']) for x in result['third']],[(1,0),(16,2),(19683,0)])

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError): Algebra((),{})
        with self.assertRaises(ValueError): Algebra((0,0),{})
        with self.assertRaises(ValueError): Algebra((0,1),{'+':{(0,0):0}})
        with self.assertRaises(ValueError): Relation((0,),{(0,1)})
        with self.assertRaises(ValueError): table((0,1),[(0,1)])
        for bad in (-1,7,1.5,True):
            with self.assertRaises(ValueError): powerset_algebra(bad)


if __name__=='__main__': unittest.main()
