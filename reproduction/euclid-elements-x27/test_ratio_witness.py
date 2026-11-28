from fractions import Fraction as F
from itertools import product
from unittest import TestCase
from ratio_witness import Witness,construct


class TestX27(TestCase):
    def test_examples(self):
        self.assertEqual(construct(2,3),Witness(F(6),F(27,2),F(3,2),F(3)))
        self.assertEqual(construct(3,2),Witness(F(6),F(8,3),F(2,3),F(2)))
        self.assertEqual(construct(F(2,3),F(8,5)),
                         Witness(F(16,15),F(768,125),F(12,5),F(8,5)))

    def test_invalid(self):
        for args in [(2,8),(F(9,16),1),(1,1),(0,1),(2,0),(-1,2),(1.0,2),(True,2)]:
            with self.assertRaises(ValueError):
                construct(*args)

    def test_grid(self):
        reps=[F(p,n) for p,n in product(range(1,9),repeat=2)]
        # Ratio terms for B²/A² and ab are <=64; terms of b³/a <=4096.
        squares={F(m*m,n*n) for m,n in product(range(1,65),repeat=2)}
        valid=0
        for a,b in product(reps,repeat=2):
            if b/a in squares:
                with self.assertRaises(ValueError):
                    construct(a,b)
                continue
            w=construct(a,b)
            self.assertNotIn(w.c_fourth,squares)
            self.assertNotIn(w.d_fourth,squares)
            self.assertEqual(w.d_over_c_squared*a,b)
            self.assertEqual(w.d_over_c_squared**2*w.c_fourth,w.d_fourth)
            self.assertEqual(w.c_fourth*w.d_fourth,w.rectangle_area**4)
            self.assertEqual(w.rectangle_area,b)
            valid+=1
        self.assertEqual(valid,3640)
        print(f"Grid: {len(reps)**2} ordered representatives; constructed={valid}; rejected={len(reps)**2-valid}")
