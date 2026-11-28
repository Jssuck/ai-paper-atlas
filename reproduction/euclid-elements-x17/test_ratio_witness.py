from fractions import Fraction as F
from unittest import TestCase
from ratio_witness import Witness,divide


class TestX17(TestCase):
    def test_examples(self):
        self.assertEqual(divide(5,4),Witness(F(9),(F(1),F(4))))
        self.assertEqual(divide(3,2),Witness(F(5),None))
        self.assertEqual(divide(F(5,3),F(4,3)),Witness(F(1),(F(1,3),F(4,3))))
        self.assertEqual(divide(F(3,2),1),Witness(F(5,4),None))

    def test_invalid(self):
        for pair in [(2,2),(2,3),(2,0),(0,1),(2,-1),(2,1.0),(2,True)]:
            with self.assertRaises(ValueError):
                divide(*pair)

    def test_grid(self):
        valid=total=0
        for b in range(2,65):
            for a in range(1,b):
                candidates=[]
                # If gap is rational at integer inputs, its square is
                # integral, so gap and both doubled parts are integers.
                for u in range(1,b):
                    v=2*b-u
                    if u*v==a*a:
                        candidates.append((F(u,2),F(v,2)))
                self.assertLessEqual(len(candidates),1)
                result=divide(b,a)
                self.assertEqual(result.parts,candidates[0] if candidates else None)
                self.assertEqual(result.gap_squared+a*a,b*b)
                if candidates:
                    p,q=result.parts
                    self.assertEqual(p+q,b)
                    self.assertEqual(4*p*q,a*a)
                    self.assertEqual((q-p)**2,result.gap_squared)
                    valid+=1
                total+=1
        self.assertEqual((total,valid),(2016,54))
        print(f"Grid: {total} strict integer pairs; rational parts={valid}; irrational parts={total-valid}")

    def test_reverse_from_constructed_parts(self):
        for b,a in [(13,12),(17,8),(25,24)]:
            u,v=divide(b,a).parts
            self.assertEqual(divide(u+v,a).parts,(u,v))
            self.assertEqual((u+v)**2-4*u*v,(v-u)**2)
