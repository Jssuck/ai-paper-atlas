import unittest
from fractions import Fraction as Q
from similar_side_areas import TEMPLATE,area,area_three,dot,place,projection,sub,triangle


class SideAreaTests(unittest.TestCase):
    def test_worked(self):
        a,b,c=triangle(2,1)
        self.assertEqual((a,b,c),((Q(9,5),Q(12,5)),(0,0),(5,0)))
        self.assertEqual(projection(a,b,c),(Q(9,5),0))
        self.assertEqual(area_three(a,b,c,((0,0),(1,0),(1,1),(0,1))),(9,16,25))

    def test_grid_and_projection_ratios(self):
        count=0
        for u,v in ((2,1),(3,1),(3,2),(4,3),(5,2),(7,4)):
            for factor in (Q(1,3),1,Q(5,4)):
                a,b,c=triangle(u,v,factor)
                for rot in ((1,0),(0,1),(Q(3,5),Q(4,5))):
                    a1,b1,c1=tuple((x*rot[0]-y*rot[1]+4,x*rot[1]+y*rot[0]-2) for x,y in (a,b,c))
                    d=projection(a1,b1,c1)
                    ab,ac,bc=sub(b1,a1),sub(c1,a1),sub(c1,b1)
                    self.assertEqual(dot(ab,ac),0)
                    self.assertEqual(dot(sub(d,a1),bc),0)
                    e=Q(dot(sub(d,b1),bc),dot(bc,bc))
                    self.assertTrue(0<e<1)
                    self.assertEqual(Q(dot(ab,ab),dot(bc,bc)),e)
                    self.assertEqual(Q(dot(ac,ac),dot(bc,bc)),1-e)
                    for sign in (-1,1):
                        for shape in (TEMPLATE,((0,0),(1,0),(Q(1,5),Q(2,3)))):
                            on_ab,on_ac,on_bc=area_three(a1,b1,c1,shape,sign)
                            self.assertEqual(Q(on_ab,on_bc),e)
                            self.assertEqual(Q(on_ac,on_bc),1-e)
                            self.assertEqual(on_ab+on_ac,on_bc)
                            count+=1
        self.assertEqual(count,216)

    def test_right_but_wrong_shape(self):
        a,b,c=triangle(2,1)
        square=((0,0),(1,0),(1,1),(0,1))
        unit_triangle=((0,0),(1,0),(0,1))
        p,q,r=area_three(a,b,c,square)
        alien_area=area(place(unit_triangle,b,c))
        self.assertEqual((p+q,r,alien_area),(25,25,Q(25,2)))

    def test_same_shape_but_not_right(self):
        a,b,c=(1,1),(0,0),(4,0)
        self.assertNotEqual(dot(sub(b,a),sub(c,a)),0)
        p,q,r=area_three(a,b,c)
        self.assertNotEqual(p+q,r)

    def test_reject_degenerate(self):
        with self.assertRaises(ValueError):
            triangle(1,1)
        with self.assertRaises(ValueError):
            place(TEMPLATE,(1,1),(1,1))


if __name__=='__main__':
    unittest.main()
