from fractions import Fraction as F
from unittest import TestCase
from ratio_witness import Witness,construct


class TestX33(TestCase):
    def test_examples(self):
        self.assertEqual(construct(9,2),Witness(F(7,9),F(9,2),F(9,2),F(9),F(9,2)))
        self.assertEqual(construct(F(3,2),F(1,3)),Witness(F(7,9),F(3,4),F(3,4),F(3,2),F(1,8)))
        self.assertEqual(construct(2,1),Witness(F(1,2),F(1),F(1),F(2),F(1,2)))

    def test_controls(self):
        for args in [(4,1),(4,3),(25,9),(2,2),(2,3),(1,0),(1,-1),(True,1),(2,1.0)]:
            with self.assertRaises(ValueError):
                construct(*args)

    def test_grid(self):
        passed=ratio_only=gap_only=both=0
        squares={r*r for r in range(1,65)}
        for h in range(2,65):
            for l in range(1,h):
                s,t=h*l in squares,h*(h-l) in squares
                if s or t:
                    with self.assertRaises(ValueError):
                        construct(h,l)
                    ratio_only+=s and not t
                    gap_only+=t and not s
                    both+=s and t
                else:
                    w=construct(h,l)
                    self.assertEqual(w.center*2,w.sum_squares)
                    self.assertEqual(w.sum_squares,h)
                    self.assertGreater(w.center**2,w.coefficient**2*w.radicand)
                    self.assertEqual(w.center**2-w.coefficient**2*w.radicand,F(h*l,4))
                    self.assertEqual(w.rectangle_squared,F(h*l,4))
                    self.assertEqual(w.radicand*h,h-l)
                    passed+=1
        self.assertEqual((passed,ratio_only,gap_only,both),(1904,54,54,4))
        print(f"Grid: {passed+ratio_only+gap_only+both}; accepted={passed}; only k square={ratio_only}; only 1-k square={gap_only}; both square={both}")
