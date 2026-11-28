from fractions import Fraction as F
from unittest import TestCase
from ratio_witness import Witness,construct


class TestX31(TestCase):
    def test_examples(self):
        self.assertEqual(construct(25,21),Witness(F(525),F(9261,25),F(21),F(21,25),F(4,25),True))
        self.assertEqual(construct(2,1),Witness(F(2),F(1,2),F(1),F(1,2),F(1,2),False))
        for a,b in [(25,21),(2,1)]:
            w=construct(a,b)
            v=construct(F(a,7),F(b,7))
            self.assertEqual(v.gap_commensurable,w.gap_commensurable)
            self.assertEqual(v.c_fourth,w.c_fourth/49)
            self.assertEqual(v.d_fourth,w.d_fourth/49)

    def test_grid(self):
        yes=no=excluded=0
        for a in range(2,65):
            for b in range(1,a):
                # A rational sqrt(x) for integer x must be an integer:
                # test sqrt(a*b) or sqrt(a*(a-b)) by extending square set.
                roots={i*i for i in range(1,a+1)}
                if a*b in roots:
                    with self.assertRaises(ValueError):
                        construct(a,b)
                    excluded+=1
                    continue
                w=construct(a,b)
                self.assertEqual(w.gap_commensurable,a*(a-b) in roots)
                self.assertEqual(w.d_over_c_squared*a,b)
                self.assertEqual(w.d_over_c_squared**2*w.c_fourth,w.d_fourth)
                self.assertEqual(w.d_fourth*w.c_fourth,w.rectangle_area**4)
                self.assertEqual(w.rectangle_area,b)
                self.assertEqual(w.gap_ratio_squared+w.d_over_c_squared,1)
                yes+=w.gap_commensurable
                no+=not w.gap_commensurable
        self.assertEqual((yes,no,excluded),(54,1904,58))
        print(f"Grid: {yes+no+excluded} ordered pairs; gap commensurable={yes}; gap incommensurable={no}; rejected={excluded}")

    def test_invalid(self):
        for args in [(4,1),(4,4),(1,2),(4,0),(4,-1),(4,1.0),(True,1)]:
            with self.assertRaises(ValueError):
                construct(*args)
