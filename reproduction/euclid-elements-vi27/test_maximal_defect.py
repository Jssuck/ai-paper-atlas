import unittest
from fractions import Fraction as Q
from maximal_defect import area, construct, loss_pieces, shape


class MaximalDefectTests(unittest.TestCase):
    def test_worked(self):
        self.assertEqual([area(construct(10,t,2)[0]) for t in (2,5,8)],[32,50,32])
        self.assertEqual(loss_pieces(10,2,2),(30,12,18))

    def test_geometric_area_and_loss_grid(self):
        count=0
        for length in (3,10,Q(7,3)):
            for r in (1,2,Q(5,7)):
                length=Q(length)
                half=length/2
                for proportion in (Q(1,7),Q(1,3),Q(1,2),Q(2,3),Q(6,7)):
                    t=length*proportion
                    for skew in (0,Q(1,3),Q(-2,5)):
                        for rot in ((1,0),(0,1),(Q(3,5),Q(4,5))):
                            p,d=construct(length,t,r,skew,rot)
                            mirror=construct(length,length-t,r,skew,rot)[0]
                            middle=construct(length,half,r,skew,rot)[0]
                            unit=construct(length,Q(length,3),r,skew,rot)[1]
                            self.assertEqual(area(p),r*t*(length-t))
                            self.assertEqual(area(d),r*t*t)
                            self.assertEqual(area(d)/area(unit),Q(t,Q(length,3))**2)
                            self.assertEqual(area(p),area(mirror))
                            self.assertEqual(area(middle)-area(p),r*(half-t)**2)
                            upper,side,corner=loss_pieces(length,t,r,skew)
                            self.assertEqual(upper-side,corner)
                            self.assertEqual(corner,area(middle)-area(p))
                            count+=1
        self.assertEqual(count,405)

    def test_same_area_is_not_same_shape(self):
        applied,defect=construct(10,2,2,0)
        same_area=shape(8,1,0,0)
        self.assertEqual(area(defect),area(same_area))
        self.assertNotIn(Q(8,1),(Q(2,4),Q(4,2)))
        self.assertEqual(area(applied),32)

    def test_height_free_exceeds_bound(self):
        self.assertEqual(area(shape(8,7,0,0)),56)
        self.assertGreater(56,area(construct(10,5,2)[0]))

    def test_reject_degenerate(self):
        for args in ((10,0,2),(10,10,2),(10,5,0),(0,1,2)):
            with self.assertRaises(ValueError):
                construct(*args)


if __name__=='__main__':
    unittest.main()
