from fractions import Fraction as F
from unittest import TestCase
from ratio_witness import Witness,construct


class TestX34(TestCase):
    def test_examples(self):
        self.assertEqual(construct(2,F(1,2)),Witness(F(2),F(1),F(8),F(1),F(8),False,True))
        self.assertEqual(construct(2,F(2,5)),Witness(F(5,2),F(3,2),F(10),F(1),F(15),False,False))
        for k in (F(1,2),F(2,5)):
            self.assertEqual(construct(F(2,3),k).rectangle_area,F(1,3))

    def test_controls(self):
        for args in [(1,F(1,4)),(1,F(3,4)),(1,F(9,25)),(0,F(1,2)),
                     (1,0),(1,1),(1,2),(1,0.5),(True,F(1,2))]:
            with self.assertRaises(ValueError):
                construct(*args)

    def test_grid(self):
        squares={i*i for i in range(1,65)}
        yes=no=outside=0
        for h in range(2,65):
            for l in range(1,h):
                k=F(l,h)
                if h*l in squares or h*(h-l) in squares:
                    with self.assertRaises(ValueError):
                        construct(1,k)
                    outside+=1
                    continue
                w=construct(1,k)
                self.assertGreater(w.center_squared,w.offset_squared)
                self.assertEqual(w.center_squared-w.offset_squared,w.rectangle_area**2)
                self.assertEqual(w.sum_squared*k,1)
                self.assertEqual(4*w.center_squared*w.offset_squared,w.cross_term_squared)
                # Each input pair also encodes the offset radical (1−k)/k;
                # its rationality differs from that of the cross term.
                self.assertEqual(w.cross_term_rational,h*(h-l) in squares)
                self.assertEqual(w.offset_rational,l*(h-l) in squares)
                yes+=l*(h-l) in squares
                no+=l*(h-l) not in squares
        self.assertEqual((yes,no,outside),(104,1800,112))
        print(f"Grid: {yes+no+outside}; accepted={yes+no}; excluded={outside}; rational offset={yes}; irrational offset={no}")
