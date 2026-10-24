"""Independent finite-specification checks; no claims about explanatory truth."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import model
from fractions import Fraction
from itertools import product
import json
import unittest

COUNTS = {}
def as_set(mask, n):
    return set(i for i in range(n) if (mask // (2**i)) % 2)
def mask_of(values):
    return sum(2**i for i in values)

class IndependentChecks(unittest.TestCase):
    def test_all_report_fields(self):
        count = certs = 0
        for t,p,a,b in product(range(8), repeat=4):
            target, prop, left, right = (as_set(m,3) for m in (t,p,a,b))
            union = left.union(right)
            expected = dict(covered=target.issubset(union), all_parts_sound=union.issubset(prop),
                target_true=target.issubset(prop), missing_mask=mask_of(target-union),
                part_counterexamples_mask=mask_of(union-prop), outside_target_mask=mask_of(union-target),
                target_counterexamples_mask=mask_of(target-prop),
                extensional_certificate=target.issubset(union) and union.issubset(prop))
            self.assertEqual(model.coverage_report(t,p,(a,b),3),expected)
            count += 1
            certs += expected['extensional_certificate']
        COUNTS['coverage_reports']=count
        COUNTS['certificates']=certs
        self.assertEqual((count,certs),(4096,512))
    def test_all_multiroute_support(self):
        count=0
        labels=('T','I','B')
        for x,y,k in product(range(8),repeat=3):
            r1=[labels[i] for i in as_set(x,3)]
            r2=[labels[i] for i in as_set(y,3)]
            kept=[labels[i] for i in as_set(k,3)]
            expected=tuple(i for i,r in enumerate((r1,r2)) if all(v in kept for v in r))
            self.assertEqual(model.available_routes((r1,r2),kept),expected)
            count+=1
        COUNTS['two_route_support_cases']=count
    def test_named_candidates(self):
        count=0
        for a,b,p in product(range(8),repeat=3):
            classes={'first':a,'second':b,'empty':0}
            expected=tuple(name for name,m in classes.items() if all(i in as_set(p,3) for i in as_set(m,3)))
            self.assertEqual(model.extensional_candidates(classes,p,3),expected)
            count+=1
        COUNTS['candidate_cases']=count
    def test_rational_cross_products(self):
        values=sorted({Fraction(n,d) for n in range(1,4) for d in range(1,4)})
        count=valid=0
        for a,b,c,d in product(values,repeat=4):
            # Both ratio statements independently reduced to integer multiplication.
            cross1=(a.numerator*d.numerator*b.denominator*c.denominator == b.numerator*c.numerator*a.denominator*d.denominator)
            r=model.alternation(a,b,c,d)
            self.assertEqual(r,dict(premise=cross1,conclusion=cross1))
            count+=1; valid+=cross1
        COUNTS['rational_values']=len(values)
        COUNTS['rational_quadruples']=count
        COUNTS['rational_equalities']=valid
    def test_boundary_and_rejection(self):
        self.assertEqual(model.coverage_report(0,0,(),0)['extensional_certificate'],True)
        self.assertEqual(model.available_routes(((),('T',)),()),(0,))
        for index in range(4):
            for invalid in (0,-1,True,0.5,'1',None):
                args=[1,1,1,1]; args[index]=invalid
                with self.assertRaises(ValueError): model.alternation(*args)
        for bad in (-1,8,True):
            with self.assertRaises(ValueError): model.extensional_candidates({'x':bad},7,3)
    def test_recorded_production_result(self):
        recorded=json.loads((Path(__file__).resolve().parents[1]/'results.json').read_text())
        self.assertEqual(model.enumerate_models(),recorded)
        self.assertEqual(recorded['ratio_premises_true'],86)

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(IndependentChecks)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps(COUNTS,sort_keys=True))
    raise SystemExit(0 if result.wasSuccessful() else 1)
