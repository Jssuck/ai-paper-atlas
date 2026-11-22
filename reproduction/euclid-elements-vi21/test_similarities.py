import unittest
from fractions import Fraction as Q
from similarities import (corner_dots, distance2, label_map, reorder, squared_scale,
                          transform, worked, wrong_angle_pair, wrong_ratio_pair)


class CorrespondenceTests(unittest.TestCase):
    def test_worked_composition(self):
        c,a,b,ca,cb=worked()
        ab=label_map(ca,cb)
        self.assertEqual(ab,(1,0,2))
        self.assertEqual(squared_scale(c,a,ca),4)
        self.assertEqual(squared_scale(c,b,cb),Q(1,4))
        self.assertEqual(squared_scale(a,b,ab),Q(1,16))
        for x,y in zip(a, (b[j] for j in ab)):
            self.assertEqual(y,(-3+Q(x[1]-1,4),5+Q(x[0]-10,4)))

    def test_scalene_wrong_fixed_map(self):
        c,a,b,ca,cb=worked()
        self.assertIsNone(squared_scale(a,b,(0,1,2)))
        self.assertEqual(squared_scale(a,b,label_map(ca,cb)),Q(1,16))

    def test_grid_rotations_reflections_and_labels(self):
        shapes=(((0,0),(4,0),(1,2)),((0,0),(4,0),(4,2),(0,2)),
                ((0,0),(3,0),(5,2),(2,4),(-1,2)))
        count=reverse=0
        for c in shapes:
            n=len(c)
            for ka,kb in ((1,Q(1,2)), (Q(3,2),Q(5,3)), (2,2)):
                for oa in range(n):
                    ca=tuple((oa+i)%n for i in range(n))
                    for ob in range(n):
                        for step in (-1,1):
                            cb=tuple((ob+step*i)%n for i in range(n))
                            a=reorder(transform(c,ka,(0,1),(10,1),1),ca)
                            b=reorder(transform(c,kb,(Q(3,5),Q(4,5)),(-3,5),step),cb)
                            sab=squared_scale(a,b,label_map(ca,cb))
                            self.assertEqual(sab,Q(kb,ka)**2)
                            self.assertEqual(sab,squared_scale(c,b,cb)/Q(squared_scale(c,a,ca)))
                            count+=1
                            reverse+=(step==-1)
        self.assertEqual((count,reverse),(300,150))

    def test_equal_angles_without_proportional_sides(self):
        a,b=wrong_ratio_pair()
        self.assertEqual(corner_dots(a),corner_dots(b))
        self.assertEqual(corner_dots(a),(0,0,0,0))
        self.assertIsNone(squared_scale(a,b,(0,1,2,3)))

    def test_equal_side_ratios_without_equal_angles(self):
        a,b=wrong_angle_pair()
        for i in range(4):
            self.assertEqual(distance2(a[i-1],a[i]),distance2(b[i-1],b[i]))
        self.assertNotEqual(corner_dots(a),corner_dots(b))
        self.assertIsNone(squared_scale(a,b,(0,1,2,3)))

    def test_reject_nonboundary_mapping(self):
        with self.assertRaises(ValueError):
            label_map((0,2,1,3),(0,1,2,3))


if __name__=='__main__':
    unittest.main()
