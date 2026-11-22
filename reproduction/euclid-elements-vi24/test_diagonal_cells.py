import unittest
from fractions import Fraction as Q
from diagonal_cells import (U,V,area,axis_square_ratios,cross,det_area,partition,point,
                            scale_match,sub)


class DiagonalCellTests(unittest.TestCase):
    def test_worked_example(self):
        full,*cells=partition(U,V,Q(1,3))
        self.assertEqual(tuple(map(area,(full,*cells))),(24,Q(8,3),Q(32,3),Q(16,3),Q(16,3)))
        self.assertEqual(cells[0][2],(Q(8,3),Q(4,3)))
        self.assertEqual(axis_square_ratios(cells[0],full),(Q(1,9),Q(1,9)))
        self.assertEqual(axis_square_ratios(cells[1],full),(Q(4,9),Q(4,9)))

    def test_grid_determinants_and_shape(self):
        trials=0
        for u,v in (((6,0),(2,4)),((2,4),(6,0)),((0,3),(-5,0)),((Q(5,3),2),(4,Q(-1,2)))):
            for t in (Q(1,7),Q(1,4),Q(1,3),Q(1,2),Q(2,3),Q(3,4),Q(6,7)):
                full,ll,ur,lr,ul=partition(u,v,t)
                self.assertEqual(ll[2],ur[0])
                self.assertEqual(ll[2],point(u,v,t,t))
                self.assertEqual(cross(sub(full[2],full[0]),sub(ll[2],full[0])),0)
                self.assertEqual(axis_square_ratios(ll,full),(t*t,t*t))
                self.assertEqual(axis_square_ratios(ur,full),((1-t)**2,(1-t)**2))
                self.assertEqual(axis_square_ratios(ll,ur),(Q(t,1-t)**2,)*2)
                self.assertEqual(scale_match(lr,full),t==Q(1,2))
                self.assertEqual(scale_match(ul,full),t==Q(1,2))
                self.assertEqual(sum(map(area,(ll,ur,lr,ul))),area(full))
                self.assertEqual(tuple(map(area,(full,ll,ur,lr,ul))),
                                 tuple(map(det_area,(full,ll,ur,lr,ul))))
                trials+=1
        self.assertEqual(trials,28)

    def test_off_diagonal_marked_correspondence(self):
        full,_,_,lr,ul=partition(U,V,Q(1,3))
        self.assertEqual(axis_square_ratios(lr,full),(Q(4,9),Q(1,9)))
        self.assertEqual(axis_square_ratios(ul,full),(Q(1,9),Q(4,9)))
        self.assertEqual(area(lr),area(ul))
        self.assertFalse(scale_match(lr,full) or scale_match(ul,full))

    def test_shifted_intersection(self):
        full,ll,ur,_,_=partition(U,V,Q(1,3),Q(1,2))
        self.assertEqual(ll[2],(3,2))
        self.assertNotEqual(cross(full[2],ll[2]),0)
        self.assertFalse(scale_match(ll,full) or scale_match(ur,full))

    def test_reject_degenerate_shapes_and_endpoint_cuts(self):
        for u,v,t in (((1,1),(2,2),Q(1,2)),((0,0),(1,0),Q(1,2)),(U,V,0),(U,V,1)):
            with self.assertRaises(ValueError):
                partition(u,v,t)


if __name__=='__main__':
    unittest.main()
