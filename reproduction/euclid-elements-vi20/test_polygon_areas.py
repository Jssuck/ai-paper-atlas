import unittest
from fractions import Fraction as Q
from polygon_areas import (CONCAVE, double_polygon, double_triangle, fan, grid,
                           intersection, side_squares, worked, worked_map)


class PolygonRatioTests(unittest.TestCase):
    def test_worked_fans(self):
        p,q = worked()
        a,b,c,d,e = p
        self.assertEqual(fan(p),((e,a,b),(e,b,c),(e,c,d)))
        self.assertEqual(tuple(double_triangle(*piece) for piece in fan(p)), (16,12,11))
        self.assertEqual(tuple(double_triangle(*piece) for piece in fan(q)),
                         (36,27,Q(99,4)))
        self.assertEqual(Q(double_polygon(q),double_polygon(p)),Q(9,4))
        self.assertEqual((double_polygon(p), double_polygon(q)),(39,Q(351,4)))

    def test_original_proof_two_junctions(self):
        (a,b,c,d,e),(f,g,h,k,l)=worked()
        m,n=intersection(a,c,b,e),intersection(f,h,g,l)
        self.assertEqual(m,(Q(20,7),Q(8,7)))
        self.assertEqual(n,(Q(65,7),Q(9,7)))
        self.assertEqual(n,worked_map(m))
        m2,n2=intersection(b,d,e,c),intersection(g,k,l,h)
        self.assertEqual(m2,(Q(80,23),Q(60,23)))
        self.assertEqual(n2,(Q(163,23),Q(51,23)))
        self.assertEqual(n2,worked_map(m2))

    def test_reject_nonproper_crossing(self):
        with self.assertRaises(ValueError):
            intersection((0,0),(1,1),(1,1),(2,0))

    def test_grid_piecewise_and_whole_invariant(self):
        count = reflected = 0
        for p,q,k,ref in grid():
            sign=-1 if ref else 1
            ap,aq = double_polygon(p),double_polygon(q)
            fp = tuple(double_triangle(*x) for x in fan(p))
            fq = tuple(double_triangle(*x) for x in fan(q))
            self.assertTrue(all(x>0 for x in fp))
            self.assertEqual((sum(fp),sum(fq)),(ap,aq))
            self.assertEqual(len(fp),len(p)-2)
            self.assertEqual(len(fp),len(fq))
            self.assertEqual(aq,sign*k*k*ap)
            self.assertEqual(abs(aq)/abs(ap),Q(side_squares(q)[0],side_squares(p)[0]))
            for t1,t2,x,y in zip(fan(p),fan(q),fp,fq):
                self.assertEqual(side_squares(t2),tuple(k*k*z for z in side_squares(t1)))
                self.assertEqual(y,sign*k*k*x)
                self.assertEqual(Q(x,ap),Q(y,aq))
            count += 1
            reflected += ref
        self.assertEqual((count,reflected),(144,72))

    def test_concave_anchor_warning(self):
        terms=tuple(double_triangle(*t) for t in fan(CONCAVE,0))
        self.assertEqual(terms,(16,-4,8))
        self.assertEqual(sum(terms),double_polygon(CONCAVE))
        self.assertEqual(sum(terms),20)
        self.assertEqual(sum(map(abs,terms)),28)

    def test_area_ratio_does_not_imply_similarity(self):
        p,q=((0,0),(4,0),(4,1),(0,1)),((0,0),(4,0),(5,1),(1,1))
        self.assertEqual(double_polygon(p),double_polygon(q))
        self.assertEqual(side_squares(p)[0],side_squares(q)[0])
        self.assertNotEqual(side_squares(p)[1],side_squares(q)[1])


if __name__=='__main__':
    unittest.main()
