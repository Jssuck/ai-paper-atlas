import unittest
from fractions import Fraction as Q
from apply_deficit import applied,area,diagonal_cells,radical_area_terms,remaining,residual_shape,solve


class DeficitApplicationTests(unittest.TestCase):
    def test_worked(self):
        sol=solve(10,2,32)
        self.assertEqual((sol.half,sol.maximum,sol.residual,sol.gap2),(5,50,18,9))
        self.assertEqual(sol.rational_cuts(),(2,8))
        self.assertEqual([area(applied(10,2,t)) for t in sol.rational_cuts()],[32,32])
        self.assertEqual(area(residual_shape(3,2)),18)

    def test_rational_grid(self):
        count=equal=0
        for length in (3,10,Q(7,3),Q(11,2)):
            for r in (1,2,Q(5,7)):
                for fraction in (Q(1,7),Q(1,3),Q(1,2),Q(2,3),Q(6,7)):
                    t=length*fraction
                    for skew in (0,Q(1,3),Q(-2,5)):
                        target=area(applied(length,r,t,skew))
                        sol=solve(length,r,target)
                        roots=sol.rational_cuts()
                        self.assertIn(t,roots)
                        self.assertEqual(roots,tuple(sorted({t,length-t})))
                        for cut in roots:
                            p,d=applied(length,r,cut,skew),remaining(length,r,cut,skew)
                            self.assertGreater(min(cut,length-cut),0)
                            self.assertEqual(area(p),target)
                            self.assertEqual(area(d),r*cut*cut)
                            self.assertEqual((p[1],p[2]),(d[0],d[3]))
                            self.assertEqual(area(residual_shape(abs(sol.half-cut),r,skew)),sol.residual)
                        equal+=len(roots)==1
                        count+=1
        self.assertEqual((count,equal),(180,36))

    def test_irrational_exact_certificate(self):
        sol=solve(10,2,49)
        self.assertEqual(sol.gap2,Q(1,2))
        self.assertGreater(sol.gap2,0)
        self.assertLess(sol.gap2,sol.half**2)
        self.assertIsNone(sol.rational_cuts())
        for sign in (-1,1):
            self.assertEqual(radical_area_terms(sol.half,sol.gap2,2,sign),(49,0))
        self.assertEqual(2*sol.gap2,sol.residual)

    def test_diagonal_cells_complements_and_gnomon(self):
        cases=0
        for half in (Q(3,2),5,Q(7,3)):
            for r in (1,2,Q(5,7)):
                for ratio in (Q(1,7),Q(1,3),Q(3,5)):
                    gap=half*ratio
                    small,lower,upper,large=diagonal_cells(half,gap,r)
                    self.assertEqual(small[2],large[0])
                    self.assertEqual(area(lower),area(upper))
                    self.assertEqual(area(small),r*gap**2)
                    whole=area(residual_shape(half,r))
                    self.assertEqual(sum(map(area,(small,lower,upper,large))),whole)
                    self.assertEqual(sum(map(area,(lower,upper,large))),whole-area(small))
                    cases+=1
        self.assertEqual(cases,27)

    def test_maximum_unique_cut(self):
        sol=solve(10,2,50)
        self.assertEqual((sol.gap2,sol.rational_cuts()),(0,(5,)))
        self.assertEqual(area(applied(10,2,5)),50)

    def test_reject_impossible_or_degenerate(self):
        for fixture in ((10,2,51),(10,2,0),(10,0,2),(0,2,2),(10,2,-1)):
            with self.assertRaises(ValueError):
                solve(*fixture)


if __name__=='__main__':
    unittest.main()
