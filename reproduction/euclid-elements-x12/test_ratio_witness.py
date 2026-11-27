from fractions import Fraction as F
from itertools import product
from unittest import TestCase

from ratio_witness import Witness, combine


class TestX12(TestCase):
    def test_examples(self):
        self.assertEqual(combine(F(2,3),F(9,4),27),
                         Witness((18,27,12),F(1),(6,9,4),F(3)))
        self.assertEqual(combine(F(2,3),F(9,4),F(9,2)),
                         Witness((18,27,12),F(1,6),(6,9,4),F(1,2)))

    def test_orientation_and_symmetry(self):
        fwd = combine(F(2,3),F(9,4),27)
        rev = combine(F(4,9),F(3,2),27)
        self.assertEqual(rev.primitive_counts, fwd.primitive_counts[::-1])
        self.assertEqual(rev.primitive_measure, fwd.primitive_measure)
        self.assertEqual(combine(1,1,5),Witness((1,1,1),F(5),(1,1,1),F(5)))

    def test_grid(self):
        primitive_cases = 0
        for d,e,f,g in product(range(1,9),repeat=4):
            x, y = F(d,e), F(f,g)
            target = (x,F(1),1/y)
            cert = combine(x,y,1)
            # Independently use the first positive integral middle count
            # yielding two integral ends; raw e*f is always an upper bound.
            for middle in range(1,e*f+1):
                values = tuple(middle*t for t in target)
                if all(n.denominator == 1 for n in values):
                    break
            else:
                self.fail("search bound excluded all witnesses")
            self.assertEqual(cert.primitive_counts,values)
            self.assertEqual(cert.primitive_measure,F(1,middle))
            self.assertEqual(tuple(n*cert.product_measure for n in cert.product_counts),target)
            primitive_cases += cert.product_counts == cert.primitive_counts
        self.assertEqual(primitive_cases,3422)
        print(f"Grid: 4096 ordered representatives; no reduction={primitive_cases}; reduced={4096-primitive_cases}")

    def test_invalid(self):
        for args in [(0,1,1),(1,-1,1),(1,1,0),(True,1,1),(1,1.0,1),(1,1,0.5)]:
            with self.assertRaises(ValueError):
                combine(*args)
