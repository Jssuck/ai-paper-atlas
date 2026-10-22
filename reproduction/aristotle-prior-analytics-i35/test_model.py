import itertools
import unittest
from model import (Atom,And,Inclusion,Step,InvalidCertificate,check,holds,
                   named_middle,linear_check,example,demo)

class KernelTests(unittest.TestCase):
    def test_positive_and_vocabulary_gap(self):
        facts,steps,expanded,t,m,a=example()
        self.assertTrue(check(facts,steps,Inclusion(t,a)))
        self.assertEqual(named_middle(expanded,t,a,[t,m.left,m.right,a]),[])
        self.assertEqual(named_middle(expanded,t,a,[m]),[m])
    def test_same_middle_is_required(self):
        a,b,c,d=map(Atom,'abcd'); facts={'p':Inclusion(a,b),'q':Inclusion(c,d)}
        with self.assertRaises(InvalidCertificate):
            check(facts,[Step(facts['p'],'given',fact='p'),Step(facts['q'],'given',fact='q'),Step(Inclusion(a,d),'trans',(0,1))],Inclusion(a,d))
    def test_reversal_is_not_given(self):
        a,b=map(Atom,'ab')
        with self.assertRaises(InvalidCertificate):
            check({'p':Inclusion(a,b)},[Step(Inclusion(b,a),'given',fact='p')],Inclusion(b,a))
        valuation={'a':False,'b':True}
        self.assertTrue(not holds(a,valuation) or holds(b,valuation))
        self.assertFalse(not holds(b,valuation) or holds(a,valuation))
        # A is empty, B nonempty: A subset B but not the reverse.
    def test_cycles_and_forward_references(self):
        a=Atom('a')
        for refs in [(0,0),(1,1),(-1,-1),(True,True)]:
            with self.assertRaises(InvalidCertificate):
                check({},[Step(Inclusion(a,a),'trans',refs)],Inclusion(a,a))
    def test_missing_and_forged_fact(self):
        a,b=map(Atom,'ab')
        for facts in [{},{'x':Inclusion(b,a)}]:
            with self.assertRaises(InvalidCertificate):check(facts,[Step(Inclusion(a,b),'given',fact='x')],Inclusion(a,b))
    def test_meet_needs_common_source(self):
        a,b,c,d=map(Atom,'abcd');facts={'p':Inclusion(a,b),'q':Inclusion(c,d)}
        with self.assertRaises(InvalidCertificate):
            check(facts,[Step(facts['p'],'given',fact='p'),Step(facts['q'],'given',fact='q'),Step(Inclusion(a,And(b,d)),'meet',(0,1))],Inclusion(a,And(b,d)))
    def test_projection_and_goal(self):
        a,b=map(Atom,'ab');c=Inclusion(And(a,b),a)
        self.assertTrue(check({},[Step(c,'project-left')],c))
        with self.assertRaises(InvalidCertificate):check({},[Step(c,'project-left')],Inclusion(a,b))
    def test_local_truth_tables(self):
        # Eight single-object valuations, a regression check, not the general proof.
        for a,b,c in itertools.product([False,True],repeat=3):
            implication=lambda x,y:not x or y
            if implication(a,b) and implication(b,c):self.assertTrue(implication(a,c))
            if implication(a,b) and implication(a,c):self.assertTrue(implication(a,b and c))
            self.assertTrue(implication(a and b,a))
            self.assertTrue(implication(a and b,b))
    def test_linear_identity(self):
        cert=[('transfer-alpha',1),('transfer-beta',1),('straight-angle',1)]
        self.assertTrue(linear_check(cert,{'euclidean-parallel-configuration','adjacent-straight-angle'}))
    def test_linear_rejects_missing_assumptions(self):
        with self.assertRaises(InvalidCertificate):linear_check([('transfer-alpha',1)],set())
    def test_linear_rejects_wrong_arithmetic_and_float(self):
        assumptions={'euclidean-parallel-configuration','adjacent-straight-angle'}
        for cert in [[('unknown',1)],[('transfer-alpha',1.0)],[('transfer-alpha',-1)],[]]:
            with self.assertRaises(InvalidCertificate):linear_check(cert,assumptions)
    def test_demo_negatives(self):
        self.assertEqual(len(demo()['rejected_cases']),4)

if __name__=='__main__':unittest.main(verbosity=2)
