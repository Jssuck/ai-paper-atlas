import unittest,copy
from fractions import Fraction as Q
from geometry import construct,verify,area,parameters
class Tests(unittest.TestCase):
    def test_default(self):self.assertEqual(verify(construct())['whole'],25)
    def test_complements(self):r=verify(construct());self.assertEqual(r['AG'],r['GE'])
    def test_overlap(self):r=verify(construct());self.assertEqual(r['AF']+r['CE']-r['gnomon'],r['CF'])
    def test_grid(self):
        for a in range(1,9):
            for b in range(1,9):
                r=verify(construct(a,b),a,b);self.assertEqual(r['whole']+r['CF'],2*r['AF']+r['DG'])
    def test_fraction(self):verify(construct(Q(2,3),Q(5,7)),Q(2,3),Q(5,7))
    def test_equal_cut(self):verify(construct(2,2),2,2)
    def test_rotated_scaled(self):verify(construct(3,2,(7,-3),(3,4),(-4,3)),3,2,(7,-3),(3,4),(-4,3))
    def test_reflected(self):verify(construct(v=(0,-1)),v=(0,-1))
    def test_zero(self):self.assertRaises(ValueError,construct,0,2)
    def test_negative(self):self.assertRaises(ValueError,construct,3,-2)
    def test_bool(self):self.assertRaises(ValueError,construct,True,2)
    def test_float(self):self.assertRaises(ValueError,construct,3.0,2)
    def test_zero_basis(self):self.assertRaises(ValueError,construct,u=(0,0))
    def test_unequal_basis(self):self.assertRaises(ValueError,construct,u=(2,0))
    def test_skew_basis(self):self.assertRaises(ValueError,construct,v=(1,1))
    def test_bad_point(self):self.assertRaises(ValueError,construct,origin=(0,))
    def test_schema(self):self.assertRaises(ValueError,verify,{'points':[]})
    def test_missing(self):c=construct();del c['points']['G'];self.assertRaises(ValueError,verify,c)
    def test_tamper(self):
        for name in construct()['points']:
            c=construct();x,y=c['points'][name];c['points'][name]=(x+Q(1,7),y);self.assertRaises(ValueError,verify,c)
    def test_bool_certificate(self):c=construct();c['points']['A']=(False,0);self.assertRaises(ValueError,verify,c)
if __name__=='__main__':unittest.main()
