import unittest,copy
from geometry import Q,construct,verify,summary,area
GOOD=((0,0),(6,0),(0,4),Q(1,3))
class GeometryTests(unittest.TestCase):
    def test_known(self): self.assertEqual(summary(*GOOD),{'AE':'24','AD':'8','CE':'16'})
    def test_grid(self):
        count=0
        for A in [(0,0),(2,-3)]:
            for u in [(6,0),(3,4),(-4,3),(Q(1,2),0)]:
                for t in [Q(1,5),Q(1,3),Q(2,3),Q(4,5)]:
                    for sign in [-1,1]:
                        v=(-sign*(1-t)*u[1],sign*(1-t)*u[0]);c=construct(A,u,v,t)
                        self.assertTrue(verify(A,u,v,t,c));count+=1
        self.assertEqual(count,64)
    def test_rotated(self): self.assertEqual(summary((1,-2),(3,4),(-Q(12,5),Q(9,5)),Q(2,5)),{'AE':'15','AD':'6','CE':'9'})
    def test_reflection(self): self.assertEqual(summary((0,0),(6,0),(0,-4),Q(1,3)),{'AE':'24','AD':'8','CE':'16'})
    def test_fraction(self): self.assertEqual(summary((0,0),(Q(3,2),0),(0,1),Q(1,3)),{'AE':'3/2','AD':'1/2','CE':'1'})
    def test_not_ii2(self):
        with self.assertRaises(ValueError): construct((0,0),(6,0),(0,6),Q(1,3))
    def test_invalid_inputs(self):
        for args in [((0,0),(0,0),(0,1),Q(1,2)),((0,0),(6,0),(0,4),0),((0,0),(6,0),(0,4),1),((0,0),(6,0),(0,4),-1),((0,0),(6,0),(0,4),2),((0,0),(6,0),(1,4),Q(1,3)),((0,0),(6,0),(0,0),Q(1,3)),((0,0),(6,0),(0,2),Q(1,3)),((0,0),(6,0),(0,4),.333),((False,0),(6,0),(0,4),Q(1,3)),((0,),(6,0),(0,4),Q(1,3))]:
            with self.subTest(args=args):
                with self.assertRaises(ValueError): construct(*args)
                self.assertFalse(verify(*args,{}))
    def test_all_labels_bound(self):
        for label in 'ABCDEF':
            c=construct(*GOOD);p=c['points'][label];c['points'][label]=(p[0]+1,p[1]);self.assertFalse(verify(*GOOD,c))
    def test_regions_bound(self):
        for key in ['AE','AD','CE']:
            c=construct(*GOOD);c[key]=tuple(reversed(c[key]));self.assertFalse(verify(*GOOD,c))
    def test_equal_sum_not_enough(self):
        c=construct(*GOOD);c['AD']=tuple((x+1,y) for x,y in c['AD'])
        self.assertEqual(area(c['AE']),area(c['AD'])+area(c['CE']));self.assertFalse(verify(*GOOD,c))
    def test_points_container(self):
        for bad in [None,[],'ABCDEF',42]:
            c=construct(*GOOD);c['points']=bad;self.assertFalse(verify(*GOOD,c))
    def test_cert_container(self):
        for bad in [None,[],42,'x']: self.assertFalse(verify(*GOOD,bad))
    def test_keys(self):
        for key in ['points','AE','AD','CE']:
            c=construct(*GOOD);del c[key];self.assertFalse(verify(*GOOD,c))
        c=construct(*GOOD);c['extra']=0;self.assertFalse(verify(*GOOD,c))
    def test_region_container(self):
        for bad in [None,2,{},'AFEB',[],[(0,0)]*3]:
            c=construct(*GOOD);c['AE']=bad;self.assertFalse(verify(*GOOD,c))
    def test_point_coordinates(self):
        for bad in [None,1,'00',(0,), (0,0,0),(0.0,0),(True,0)]:
            c=construct(*GOOD);c['points']['A']=bad;self.assertFalse(verify(*GOOD,c))
    def test_list_coordinates(self):
        c=construct(*GOOD);c['points']={k:list(v) for k,v in c['points'].items()};self.assertTrue(verify(*GOOD,c))
    def test_swapped_square(self):
        c=construct(*GOOD);c['CE'],c['AD']=c['AD'],c['CE'];self.assertFalse(verify(*GOOD,c))
    def test_input_rebinding(self): self.assertFalse(verify((1,0),*GOOD[1:],construct(*GOOD)))
    def test_bad_parameter_type(self):
        for t in [True,'1/3',None,complex(1,0)]: self.assertFalse(verify(*GOOD[:3],t,construct(*GOOD)))
    def test_area_orientation(self):
        c=construct(*GOOD);self.assertEqual(area(c['CE']),area(tuple(reversed(c['CE']))))
    def test_determinism(self): self.assertEqual(construct(*GOOD),construct(*GOOD))
if __name__=='__main__': unittest.main()
