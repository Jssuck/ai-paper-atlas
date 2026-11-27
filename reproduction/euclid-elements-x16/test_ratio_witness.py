from fractions import Fraction as F
from itertools import product
from unittest import TestCase
from ratio_witness import analyze


def conjugate_coefficient(x,y):
    a,b = x
    c,d = y
    # Multiply symbolic x by conjugate(y), then divide by norm(y).
    terms = [(a*c,0),(b*(-d)*2,0),(b*c,1),(a*(-d),1)]
    return F(sum(v for v,k in terms if k==1),c*c-2*d*d)


class TestX16(TestCase):
    def test_irrational_parts_rational_whole(self):
        self.assertEqual(analyze((1,1),(2,-1)),((3,0),(True,True,True)))
        self.assertEqual(analyze((2,-1),(1,1)),((3,0),(True,True,True)))

    def test_commensurable_and_scale(self):
        self.assertEqual(analyze((0,2),(0,3)),((0,5),(False,False,False)))
        self.assertEqual(analyze((F(1,3),F(1,3)),(F(2,3),F(-1,3))),
                         ((1,0),(True,True,True)))

    def test_invalid(self):
        for args in [((0,0),(1,0)),((1,-1),(1,0)),((2,-2),(1,0)),
                     ((1,0.5),(1,0)),((True,1),(1,0))]:
            with self.assertRaises(ValueError):
                analyze(*args)

    def test_grid(self):
        # Independent positivity via rational sqrt(2) bracket 7/5 < sqrt(2) < 10/7;
        # on this small coefficient grid both endpoint evaluations have same strict sign.
        points = []
        for a,b in product(range(-4,5),repeat=2):
            lo,hi = sorted((a+b*F(7,5),a+b*F(10,7)))
            self.assertTrue(lo>0 or hi<0 or (a,b)==(0,0))
            if lo>0:
                points.append((a,b))
        mixed = aligned = 0
        for x,y in product(points,repeat=2):
            w,status = analyze(x,y)
            expected_w = tuple(map(sum,zip(x,y)))
            self.assertEqual(w,expected_w)
            expected = tuple(conjugate_coefficient(p,q)!=0 for p,q in
                             ((x,y),(x,expected_w),(y,expected_w)))
            self.assertEqual(status,expected)
            self.assertIn(status,[(True,)*3,(False,)*3])
            mixed += status[0]
            aligned += not status[0]
        self.assertEqual((len(points),mixed,aligned),(40,1504,96))
        print(f"Grid: {len(points)} positive sides; {mixed+aligned} ordered pairs; all incommensurable={mixed}; all commensurable={aligned}")
