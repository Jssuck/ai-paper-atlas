from fractions import Fraction as F
from itertools import product
from unittest import TestCase
from ratio_witness import Witness,apply_medial


def kernel(n):
    k=2
    while k*k<=n:
        while n%(k*k)==0:
            n//=k*k
        k+=1
    return n


def signature(v):
    return kernel(v.numerator*v.denominator)


class TestX22(TestCase):
    def test_examples(self):
        self.assertEqual(apply_medial(6,2),Witness(F(3),F(3,2)))
        self.assertEqual(apply_medial(6,4),Witness(F(3,2),F(3,8)))
        self.assertEqual(apply_medial(F(16,15),F(2,3)),Witness(F(8,5),F(12,5)))
        self.assertEqual(apply_medial(F(3,2),F(3,5)),Witness(F(5,2),F(25,6)))

    def test_invalid(self):
        for args in [(1,2),(F(9,16),3),(4,3),(0,1),(1,0),(2,-1),(2,1.0),(True,1)]:
            with self.assertRaises(ValueError):
                apply_medial(*args)

    def test_grid(self):
        inputs=[F(p,r) for p,r in product(range(1,9),repeat=2)]
        accepted=0
        for q,b in product(inputs,repeat=2):
            tag=signature(q)
            if tag==1:
                with self.assertRaises(ValueError):
                    apply_medial(q,b)
                continue
            w=apply_medial(q,b)
            self.assertEqual(w.width_squared*b,q)
            self.assertEqual(w.width_to_base_squared*b,w.width_squared)
            self.assertEqual(signature(w.width_to_base_squared),tag)
            accepted+=1
        self.assertEqual(accepted,3328)
        print(f"Grid: {len(inputs)**2} ordered inputs; accepted={accepted}; square controls rejected={len(inputs)**2-accepted}")
