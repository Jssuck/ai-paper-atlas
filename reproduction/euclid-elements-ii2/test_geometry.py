import unittest,copy
from fractions import Fraction as Q
from geometry import construct,verify,summary,area,inputs

class GeometryTests(unittest.TestCase):
    a=((0,0),(6,0),(0,6),Q(1,3))
    def test_01_basic(self):self.assertEqual(summary(*self.a),{'square':'36','AF':'12','CE':'24'})
    def test_02_equal_split(self):self.assertEqual(summary((0,0),(4,0),(0,4),Q(1,2)),{'square':'16','AF':'8','CE':'8'})
    def test_03_rotated(self):self.assertEqual(summary((1,2),(4,6),(-3,5),Q(2,5)),{'square':'25','AF':'10','CE':'15'})
    def test_04_reflection(self):self.assertEqual(summary((1,2),(4,6),(5,-1),Q(2,5)),{'square':'25','AF':'10','CE':'15'})
    def test_05_fractional(self):self.assertEqual(summary((0,0),(Q(1,2),0),(0,Q(1,2)),Q(1,3)),{'square':'1/4','AF':'1/12','CE':'1/6'})
    def test_06_grid(self):
        n=0
        for u in [(1,0),(3,4),(-2,3),(Q(2,3),Q(-1,2))]:
            for sign in (-1,1):
                for tx,ty in [(0,0),(7,-11)]:
                    for t in [Q(1,7),Q(1,3),Q(1,2),Q(6,7)]:
                        A=(tx,ty);B=(tx+u[0],ty+u[1]);D=(tx-sign*u[1],ty+sign*u[0])
                        self.assertTrue(verify(A,B,D,t,construct(A,B,D,t)));n+=1
        self.assertEqual(n,64)
    def reject(self,A=(0,0),B=(6,0),D=(0,6),t=Q(1,3)):
        with self.assertRaises(ValueError):construct(A,B,D,t)
    def test_07_nonorthogonal(self):self.reject(D=(1,6))
    def test_08_unequal(self):self.reject(D=(0,3))
    def test_09_zero(self):self.reject(B=(0,0))
    def test_10_start(self):self.reject(t=0)
    def test_11_end(self):self.reject(t=1)
    def test_12_outside(self):self.reject(t=Q(3,2));self.reject(t=Q(-1,3))
    def test_13_float(self):self.reject(t=.5);self.reject(A=(0.,0))
    def test_14_boolean(self):self.reject(t=True);self.reject(D=(False,6))
    def test_15_badpoint(self):self.reject(A=(0,));self.reject(A='xy')
    def altered(self,change):
        c=construct(*self.a);change(c);self.assertFalse(verify(*self.a,c))
    def test_16_wrong_F(self):self.altered(lambda c:c['points'].__setitem__('F',(3,6)))
    def test_17_wrong_C(self):self.altered(lambda c:c['points'].__setitem__('C',(3,0)))
    def test_18_swap_equal_area(self):
        a=((0,0),(6,0),(0,6),Q(1,2));c=construct(*a);c['AF'],c['CE']=c['CE'],c['AF'];self.assertFalse(verify(*a,c))
    def test_19_duplicate_tile(self):self.altered(lambda c:c.__setitem__('CE',c['AF']))
    def test_20_reverse_tile(self):self.altered(lambda c:c.__setitem__('AF',c['AF'][::-1]))
    def test_21_missing(self):self.altered(lambda c:c.pop('CE'))
    def test_22_extra(self):self.altered(lambda c:c.__setitem__('extra',0))
    def test_23_bad_square(self):self.altered(lambda c:c.__setitem__('square',c['AF']))
    def test_24_invalid_certificate(self):self.assertFalse(verify(*self.a,None));self.assertFalse(verify(*self.a,{}))
    def test_25_not_segment_squares(self):self.assertNotEqual(6*6,2*2+4*4)
    def test_26_shoelace(self):self.assertEqual(area(((0,0),(0,3),(4,3),(4,0))),12)
    def test_27_invalid_input_verifier(self):self.assertFalse(verify((0,0),(6,0),(0,3),Q(1,3),construct(*self.a)))
    def test_28_wrong_binding(self):self.assertFalse(verify((0,0),(6,0),(0,6),Q(1,2),construct(*self.a)))
    def test_29_bad_points_container(self):
        for bad in [list('ABCDEF'),tuple('ABCDEF'),'ABCDEF',set('ABCDEF'),None]:
            self.altered(lambda c:c.__setitem__('points',bad))
if __name__=='__main__':unittest.main()
