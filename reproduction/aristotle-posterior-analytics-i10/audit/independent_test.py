"""Independent review tests: extensional semantics and declared-role boundaries."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from model import definition_holds, has_instance, Quantity, subtract_equals, learner_status, diagram_gap

class IndependentTests(unittest.TestCase):
    def test_unique_extension_and_witness(self):
        # Different oracle: binary strings and direct equality of truth values.
        checked=0
        for n in range(1,6):
            for q in range(2**n):
                qv=tuple(int(c) for c in f'{q:0{n}b}')
                extensions=[]
                for p in range(2**n):
                    pv=tuple(int(c) for c in f'{p:0{n}b}')
                    expected=all(u==v for u,v in zip(pv,qv))
                    self.assertEqual(definition_holds(p,q,n), expected)
                    if expected: extensions.append(p)
                    checked+=1
                self.assertEqual(extensions,[q])
                self.assertEqual(has_instance(q,n),any(qv))
                self.assertTrue(definition_holds(0,0,n))
                self.assertFalse(has_instance(0,n))
        self.assertEqual(checked,1364)
    def test_typed_subtraction_exhaustive(self):
        # Cross-multiplied rational oracle, not producer's a==b comparison.
        count=0
        for kind,den in [('number',1),('magnitude',3)]:
            vals=[Fraction(x,den) for x in range(5)]
            for a,b,c,d in product(vals,repeat=4):
                eq1=a.numerator*b.denominator==b.numerator*a.denominator
                eq2=c.numerator*d.denominator==d.numerator*c.denominator
                ok=eq1 and eq2 and a>=c and b>=d
                if ok:
                    x,y=subtract_equals(*(Quantity(kind,v) for v in (a,b,c,d)))
                    self.assertEqual(x.value+c,a)
                    self.assertEqual(y.value+d,b)
                    self.assertEqual(x,y)
                else:
                    with self.assertRaises(ValueError):
                        subtract_equals(*(Quantity(kind,v) for v in (a,b,c,d)))
                count+=1
        self.assertEqual(count,1250)
    def test_all_cross_type_signatures(self):
        for kinds in product(('number','magnitude'),repeat=4):
            if len(set(kinds))==1: continue
            with self.assertRaises(ValueError):
                subtract_equals(*(Quantity(k,v) for k,v in zip(kinds,(2,2,1,1))))
    def test_policy_full_valid_matrix(self):
        attitudes=['accept','neutral','reject']
        for a in attitudes:
            self.assertEqual(learner_status('definition',False,False,a),'meaning_only')
            self.assertEqual(learner_status('proposition',False,False,a),'outside_relative_classification')
            self.assertEqual(learner_status('proposition',True,True,a),'declared_proved')
            expected='relative_hypothesis' if a=='accept' else 'postulate_relative_to_learner'
            self.assertEqual(learner_status('proposition',True,False,a),expected)
            with self.assertRaises(ValueError): learner_status('proposition',False,True,a)
            for d,p in [(True,False),(False,True),(True,True)]:
                with self.assertRaises(ValueError): learner_status('definition',d,p,a)
    def test_mask_boundaries_and_types(self):
        for n in (1,8):
            self.assertTrue(definition_holds(2**n-1,2**n-1,n))
            for p in (-1,2**n):
                with self.assertRaises(ValueError): has_instance(p,n)
        for x in (True,False,1.0,'1',None):
            with self.assertRaises(TypeError): has_instance(x,2)
        for n in (0,9,-1):
            with self.assertRaises(ValueError): definition_holds(0,0,n)
    def test_quantities_and_flags(self):
        for x in (True,False,0.5,'1',None):
            with self.assertRaises(TypeError): Quantity('number',x)
            with self.assertRaises(TypeError): diagram_gap(x,1)
        for x in (0,1,0.5,'1',None):
            with self.assertRaises(TypeError): learner_status('proposition',x,False,'accept')
        with self.assertRaises(ValueError): Quantity('number',Fraction(1,3))
        with self.assertRaises(TypeError): subtract_equals(1,1,0,0)
    def test_diagram_only_gap(self):
        for a,b in product(range(6),repeat=2):
            x,y=Fraction(a,3),Fraction(b,3)
            self.assertEqual(diagram_gap(x,y),Fraction(max(a,b)-min(a,b),3))
            self.assertEqual(diagram_gap(x,y),diagram_gap(y,x))
        self.assertEqual(diagram_gap(Fraction(999,1000),1),Fraction(1,1000))
        with self.assertRaises(ValueError): diagram_gap(-1,1)

if __name__=='__main__': unittest.main(verbosity=2)
