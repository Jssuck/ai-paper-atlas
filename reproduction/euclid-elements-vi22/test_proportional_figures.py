import unittest
from fractions import Fraction as Q
from proportional_figures import area, compare, fourth, grid, isosceles, right_345, side2, square, third


class ProportionsTests(unittest.TestCase):
    def test_worked_pair_families(self):
        figures=(square(2),square(3),isosceles(4),isosceles(6))
        values=tuple(map(area,figures))
        self.assertEqual(values,(4,9,8,18))
        self.assertTrue(compare(*values))
        self.assertTrue(compare(2,3,4,6))
        self.assertEqual((third(2,3),third(4,6)),(Q(9,2),9))

    def test_both_directions_in_grid(self):
        count=0
        for a,b,c,d,shapes in grid():
            p,q,r,s=map(area,shapes)
            self.assertEqual((a*a,b*b,c*c,d*d),tuple(side2(v,0) for v in shapes))
            self.assertTrue(compare(a,b,c,d))
            self.assertTrue(compare(p,q,r,s))
            self.assertTrue(compare(a,third(a,b),c,third(c,d)))
            self.assertEqual(Q(p,q),Q(a,third(a,b)))
            self.assertEqual(Q(r,s),Q(c,third(c,d)))
            d_new=fourth(a,b,c)
            self.assertEqual(d_new,d)
            self.assertTrue(compare(a,b,c,d_new))
            self.assertEqual(Q(s,r),Q(d_new,c)**2)
            count+=1
        self.assertEqual(count,270)

    def test_wrong_fourth_is_rejected_by_area_ratio(self):
        expected=fourth(2,3,4)
        self.assertEqual(expected,6)
        for proposed in (5,7):
            self.assertFalse(compare(2,3,4,proposed))
            self.assertFalse(compare(4,9,8,area(isosceles(proposed))))

    def test_wrong_corresponding_base(self):
        r,s=right_345(4),right_345(6)
        self.assertTrue(compare(4,9,area(r),area(s)))
        self.assertEqual(side2(s,1),100)  # hypotenuse, not the leg matching side 0
        self.assertFalse(compare(2,3,4,10))

    def test_nonsimilar_figures_break_both_directions(self):
        thin=((0,0),(3,0),(3,1),(0,1))
        self.assertTrue(compare(2,3,4,6))
        self.assertFalse(compare(4,area(thin),8,18))
        skew=((0,0),(4,0),(5,3),(1,3))
        self.assertEqual(area(skew),12)
        rectangle=((0,0),(9,0),(9,3),(0,3))
        self.assertTrue(compare(4,9,area(skew),area(rectangle)))
        self.assertFalse(compare(2,3,4,9))

    def test_positive_domain(self):
        for operation,args in ((third,(0,6)),(fourth,(2,3,-4)),(compare,(1,2,0,4))):
            with self.assertRaises(ValueError):
                operation(*args)


if __name__=='__main__':
    unittest.main()
