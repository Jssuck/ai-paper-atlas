import copy, unittest
from fractions import Fraction as Q
from geometry import *
from cases import legal_cases,illegal_cases
class Tests(unittest.TestCase):
    def test_example(self):
        c=make_certificate(example()); self.assertEqual(c['areas']['EBGK'],'4'); self.assertEqual(c['areas']['HKFD'],'4')
    def test_all_legal(self):
        for d in legal_cases(): self.assertTrue(verify(d,make_certificate(d)))
    def test_all_illegal(self):
        for d in illegal_cases():
            with self.assertRaises(ValueError): make_certificate(d)
    def test_off_diagonal(self):
        p=split((0,0),(6,0),(0,3),Q(1,3),Q(2,3))
        self.assertEqual(area([p[x] for x in 'EBGK']),8); self.assertEqual(area([p[x] for x in 'HKFD']),2)
    def test_not_congruent(self):
        p,_=validate(example())
        def sides(names):
            return sorted(sum(x*x for x in sub(p[names[(i+1)%4]],p[names[i]])) for i in range(4))
        self.assertEqual(sides('EBGK'),[Q(1),Q(1),Q(16),Q(16)])
        self.assertEqual(sides('HKFD'),[Q(4)]*4)
        self.assertNotEqual(sides('EBGK'),sides('HKFD'))
    def test_half(self): self.assertEqual(make_certificate(example(t=Q(1,2)))['areas']['EBGK'],'9/2')
    def test_negative_orientation(self): self.assertEqual(make_certificate(example(v=(0,-3)))['areas']['EBGK'],'4')
    def test_translation(self): self.assertEqual(make_certificate(example(A=(8,-4)))['areas'],make_certificate(example())['areas'])
    def test_shear(self): self.assertEqual(make_certificate(example(v=(3,3)))['areas'],make_certificate(example())['areas'])
    def test_tiny_internal(self): self.assertTrue(verify(example(t=Q(1,10**12)),make_certificate(example(t=Q(1,10**12)))))
    def test_boundary_start(self):
        with self.assertRaises(ValueError): make_certificate(example(t=Q(0)))
    def test_boundary_end(self):
        with self.assertRaises(ValueError): make_certificate(example(t=Q(1)))
    def test_missing(self): self.assertFalse(verify({},{}))
    def test_forged_area(self):
        d=example(); c=make_certificate(d); c['areas']['EBGK']='5'; self.assertFalse(verify(d,c))
    def test_forged_point(self):
        d=example(); c=make_certificate(d); c['points']['E']=['9','9']; self.assertFalse(verify(d,c))
    def test_rebind(self): self.assertFalse(verify(example(A=(1,0)),make_certificate(example())))
    def test_extra_certificate(self):
        d=example(); c=make_certificate(d); c['extra']=0; self.assertFalse(verify(d,c))
    def test_bool_certificate(self):
        d=example(); c=make_certificate(d); c['t']=True; self.assertFalse(verify(d,c))
    def test_diagonal_small_areas(self):
        c=make_certificate(example()); self.assertEqual(c['areas']['AEKH'],'2'); self.assertEqual(c['areas']['KGCF'],'8')
    def test_dissection(self):
        c=make_certificate(example()); a=c['areas']; self.assertEqual(Q(a['ABC']),Q(a['AEK'])+Q(a['KGC'])+Q(a['EBGK']))
    def test_scale(self): self.assertEqual(make_certificate(example(u=(12,0),v=(0,6)))['areas']['EBGK'],'16')
if __name__=='__main__': unittest.main()
