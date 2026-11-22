import unittest
from fractions import Fraction as Q
from excess import applied,area,area_cells,polygon,solve


class OvershootTests(unittest.TestCase):
    def test_worked(self):
        c=solve(10,2,48)
        self.assertEqual((c.half,c.diagonal_base2,c.overshoot()),(5,49,2))
        cells=area_cells(c.half,2,2,Q(1,3))
        self.assertEqual(tuple(map(area,cells)),(50,20,20,8))
        self.assertEqual(sum(map(area,cells)),98)
        self.assertEqual(area(applied(10,2,2,Q(1,3))),48)

    def test_exact_coordinates_and_transfer_grid(self):
        count=0
        for length in (2,10,Q(7,3),Q(11,2)):
            for x in (Q(1,7),Q(1,2),2,5):
                for r in (1,2,Q(5,7)):
                    for slant in (0,Q(1,3),Q(-2,5)):
                        actual=area(applied(length,x,r,slant))
                        c=solve(length,r,actual)
                        self.assertEqual(c.overshoot(),x)
                        m=c.half
                        h,a,b,e=area_cells(m,x,r,slant)
                        self.assertEqual(h[2],e[0])
                        self.assertEqual(a[3],b[1])
                        self.assertEqual(area(a),area(b))
                        self.assertEqual(area(e),r*x*x)
                        self.assertEqual(sum(map(area,(a,b,e))),actual)
                        outer=polygon(m+x,r*(m+x),slant*(m+x))
                        self.assertEqual(area(outer),sum(map(area,(h,a,b,e))))
                        self.assertEqual(area(outer)-area(h),actual)
                        count+=1
        self.assertEqual(count,144)

    def test_radical_and_root_branches(self):
        c=solve(10,2,49)
        self.assertEqual(c.diagonal_base2,Q(99,2))
        self.assertIsNone(c.overshoot())
        self.assertGreater(c.diagonal_base2,c.half**2)
        for sign in (-1,1):
            self.assertEqual(c.radical_area(2,sign),(49,0))
        # Rational contrast: x=-5+7=2 or x=-5-7=-12; latter is outside domain.
        c=solve(10,2,48)
        x=c.overshoot()
        other=-2*c.half-x
        self.assertEqual((x,other),(2,-12))
        self.assertLess(other,-10)

    def test_no_deficit_style_upper_bound(self):
        c=solve(10,2,400)
        self.assertEqual(c.overshoot(),10)
        self.assertEqual(area(applied(10,10,2,0)),400)

    def test_invalid_input(self):
        for args in ((10,2,0),(10,2,-1),(10,0,1),(0,2,1)):
            with self.assertRaises(ValueError):
                solve(*args)


if __name__=='__main__':
    unittest.main()
