import unittest
from fractions import Fraction as Q
from same_diagonal import U,V,area,construct,cross,grid,side_ratios2,sub


class SameDiagonalTests(unittest.TestCase):
    def test_worked(self):
        a,b,c,d,e,f,g,h,k=construct(U,V,Q(1,2),Q(1,3))
        self.assertEqual((f,h,k),((Q(11,3),Q(4,3)),(Q(8,3),Q(4,3)),(2,0)))
        self.assertEqual(side_ratios2(a,b,d,e,g),(Q(1,4),Q(1,9)))
        self.assertEqual(cross(sub(c,a),sub(f,a)),-4)

    def test_exact_collinearity_and_ratio_grid(self):
        counts=[0,0,0]
        for u,v,s,t,origin in grid():
            a,b,c,d,e,f,g,h,k=construct(u,v,s,t,origin)
            col=cross(sub(c,a),sub(f,a))
            self.assertEqual(col,(t-s)*cross(u,v))
            self.assertEqual(cross(sub(c,a),sub(h,a)),0)
            self.assertEqual(cross(sub(h,g),sub(f,g)),0)
            self.assertEqual(cross(sub(k,h),sub(d,a)),0)
            self.assertEqual(side_ratios2(a,b,d,e,g),(s*s,t*t))
            self.assertEqual(side_ratios2(a,b,d,k,g),(t*t,t*t))
            self.assertEqual(area((a,e,f,g)),s*t*area((a,b,c,d)))
            self.assertEqual(col==0,s==t)
            self.assertEqual(h==f,s==t)
            counts[0 if s<t else 1 if s==t else 2]+=1
        self.assertEqual(counts,[80,40,80])

    def test_equal_area_does_not_force_same_diagonal(self):
        a,b,c,d,e,f,g,_,_=construct(U,V,Q(1,2),Q(1,8))
        i,_,_,_,j,m,n,_,_=construct(U,V,Q(1,4),Q(1,4))
        self.assertEqual(area((a,e,f,g)),area((i,j,m,n)))
        self.assertNotEqual(cross(sub(c,a),sub(f,a)),0)
        self.assertEqual(cross(sub(c,a),sub(m,a)),0)

    def test_angle_alone_does_not_force_equal_scales(self):
        a,b,_,d,e,_,g,_,_=construct(U,V,Q(1,3),Q(1,2))
        self.assertEqual(cross(sub(e,a),sub(b,a)),0)
        self.assertEqual(cross(sub(g,a),sub(d,a)),0)
        first,second=side_ratios2(a,b,d,e,g)
        self.assertNotEqual(first,second)

    def test_degenerate_or_noninterior(self):
        for args in (((0,0),V,Q(1,2),Q(1,2)),(U,(12,0),Q(1,2),Q(1,2)),
                     (U,V,0,Q(1,2)),(U,V,Q(1,2),1)):
            with self.assertRaises(ValueError):
                construct(*args)


if __name__=='__main__':
    unittest.main()
