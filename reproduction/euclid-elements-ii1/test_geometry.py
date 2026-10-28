import unittest,copy
from fractions import Fraction as Q
from geometry import construct,verify,summary,area
from cases import valid_cases,invalid_cases
class Geometry(unittest.TestCase):
    def setUp(self):self.args=((0,0),(6,0),(0,2),[Q(1,6),Q(1,2)]);self.c=construct(*self.args)
    def test_original(self):self.assertEqual(summary(*self.args),{'whole_area':'12','tile_areas':['2','4','6'],'tiles':3})
    def test_valid_family(self):
        for a in valid_cases():self.assertTrue(verify(*a,construct(*a)))
    def test_invalid_family(self):
        for a in invalid_cases():
            with self.assertRaises(ValueError):construct(*a)
    def test_no_cut(self):self.assertTrue(verify((0,0),(3,4),(-4,3),[],construct((0,0),(3,4),(-4,3),[])))
    def test_many_cuts(self):
        a=((0,0),(1,0),(0,1),[Q(i,100) for i in range(1,100)])
        self.assertEqual(summary(*a)['tiles'],100)
    def test_tiny(self):self.assertEqual(summary((0,0),(1,0),(0,Q(1,10**30)),[])['whole_area'],str(Q(1,10**30)))
    def test_missing_key(self):c=copy.deepcopy(self.c);del c['upper'];self.assertFalse(verify(*self.args,c))
    def test_extra_key(self):c=copy.deepcopy(self.c);c['area']=12;self.assertFalse(verify(*self.args,c))
    def test_missing_tile(self):c=copy.deepcopy(self.c);c['tiles']=c['tiles'][:-1];self.assertFalse(verify(*self.args,c))
    def test_duplicate_tile(self):c=copy.deepcopy(self.c);c['tiles']=(c['tiles'][0],)*3;self.assertFalse(verify(*self.args,c))
    def test_reverse_tiles(self):c=copy.deepcopy(self.c);c['tiles']=c['tiles'][::-1];self.assertFalse(verify(*self.args,c))
    def test_wrong_winding(self):c=copy.deepcopy(self.c);c['tiles']=tuple(r[::-1] for r in c['tiles']);self.assertFalse(verify(*self.args,c))
    def test_shift_lower(self):
        for i in range(4):
            c=copy.deepcopy(self.c);v=list(c['lower']);v[i]=(v[i][0]+1,v[i][1]);c['lower']=v;self.assertFalse(verify(*self.args,c))
    def test_shift_upper(self):
        for i in range(4):
            c=copy.deepcopy(self.c);v=list(c['upper']);v[i]=(v[i][0],v[i][1]+1);c['upper']=v;self.assertFalse(verify(*self.args,c))
    def test_tile_coordinates(self):
        for i in range(3):
            for j in range(4):
                for k in range(2):
                    c=copy.deepcopy(self.c);r=[list(p) for p in c['tiles'][i]];r[j][k]+=1;ts=list(c['tiles']);ts[i]=r;c['tiles']=ts;self.assertFalse(verify(*self.args,c))
    def test_bool_certificate(self):c=copy.deepcopy(self.c);v=list(c['lower']);v[0]=(False,0);c['lower']=v;self.assertFalse(verify(*self.args,c))
    def test_float_certificate(self):c=copy.deepcopy(self.c);v=list(c['upper']);v[0]=(0.0,2);c['upper']=v;self.assertFalse(verify(*self.args,c))
    def test_wrong_input_binding(self):self.assertFalse(verify((1,0),(7,0),(1,2),self.args[3],self.c))
    def test_wrong_cuts_binding(self):self.assertFalse(verify(*self.args[:3],[Q(1,3),Q(1,2)],self.c))
    def test_area_not_enough(self):c=copy.deepcopy(self.c);c['tiles']=(c['tiles'][2],c['tiles'][1],c['tiles'][0]);self.assertEqual(sum(area(r) for r in c['tiles']),12);self.assertFalse(verify(*self.args,c))
    def test_nonperpendicular_near(self):
        with self.assertRaises(ValueError):construct((0,0),(6,0),(Q(1,10**30),2),[])
if __name__=='__main__':unittest.main()
