import unittest
from fractions import Fraction as F
import condillac_model as m


class ModelTests(unittest.TestCase):
    def test_translation_and_solution(self):
        self.assertEqual(m.transfer(), (m.Aff(1,-1,-2), m.Aff(1,-2,3)))
        self.assertEqual(m.solve(m.transfer()), {'kind':'unique','point':(F(7),F(5))})
        self.assertEqual(m.oracle(m.transfer(),12), ((7,5),))
        self.assertTrue(m.feasible(7,5))

    def test_affine_arithmetic(self):
        self.assertEqual(2*(m.L-1), 2*m.L-2)
        self.assertEqual(3-m.R, m.Aff(-1,0,3))
        self.assertEqual(m.equation(3, m.L), m.Aff(0,-1,3))
        self.assertEqual((m.R+2).at(F(1,2),0), F(5,2))
        self.assertEqual(m.equation(m.R,3), m.Aff(1,0,-3))
        for bad in (1.0, True, '1'):
            with self.assertRaises(TypeError): m.Aff(c=bad)
        with self.assertRaises(TypeError): m.R*m.L
        with self.assertRaises(TypeError): m.R-True
        with self.assertRaises(TypeError): m.equation(m.R,True)
        with self.assertRaises(TypeError): m.holds((),True,0)
        with self.assertRaises(TypeError): m.holds([1],0,0)

    def test_reversible_certificate(self):
        operations = [('add',1,0,-1),('scale',1,-1),('add',0,1,1)]
        trace = m.certificate(m.transfer(), operations)
        self.assertEqual(trace[-1], (m.R-7,m.L-5))
        for rows in trace:
            self.assertTrue(m.equivalent(m.transfer(), rows))
        swapped = m.row_step(trace[-1], ('swap',0,1))
        self.assertTrue(m.equivalent(swapped, trace[-1]))
        self.assertEqual(m.row_step(swapped,('scale',0,F(2,3)))[0], (m.L-5)*F(2,3))
        for op in ((),('drop',0),('swap',0),('scale',0,0),('add',0,0,-1),('swap',-1,0),('swap',True,0)):
            with self.assertRaises(ValueError): m.row_step(m.transfer(),op)
        with self.assertRaises(TypeError): m.row_step(m.transfer(),('scale',0,1.5))

    def test_information_loss_and_mistakes(self):
        derived = (m.transfer()[1]-m.transfer()[0],)
        self.assertTrue(m.holds(derived,0,5))
        self.assertFalse(m.holds(m.transfer(),0,5))
        self.assertFalse(m.equivalent(derived,m.transfer()))
        for bad in ((m.R-m.L+2,m.transfer()[1]), (m.transfer()[0],m.R-2*m.L+2)):
            self.assertFalse(m.equivalent(bad,m.transfer()))
            self.assertFalse(m.holds(bad,7,5))

    def test_domain_and_degeneracy(self):
        self.assertEqual(m.solve(m.transfer(1,1,4))['point'], (F(13,3),F(7,3)))
        self.assertFalse(m.feasible(F(13,3),F(7,3)))
        self.assertEqual(m.oracle(m.transfer(1,1,4),10), ())
        self.assertEqual(m.solve(m.transfer(1,1,1))['kind'],'none')
        self.assertEqual(m.solve(m.transfer(0,0,1))['kind'],'infinite')
        self.assertEqual(m.solve(())['kind'],'infinite')
        self.assertTrue(m.equivalent((m.Aff(c=1),),(m.R,m.Aff(c=2))))
        self.assertFalse(m.equivalent((),(m.R,)))
        self.assertTrue(m.equivalent((m.R,2*m.R,m.Aff()),(m.R,)))
        self.assertFalse(m.feasible(-1,2))
        self.assertFalse(m.feasible(0,0))
        self.assertFalse(m.feasible(7,5,F(1,2),1))
        self.assertTrue(m.feasible(0,0,0,0))
        for bound in (-1,True,F(2)):
            with self.assertRaises(ValueError): m.oracle((),bound)

    def test_independent_not_sequential(self):
        self.assertEqual(m.solve(m.sequential())['point'],(F(4),F(2)))
        self.assertFalse(m.holds(m.sequential(),7,5))
        self.assertFalse(m.holds(m.transfer(),4,2))

    def test_bounded_direct_oracle(self):
        # Independent arithmetic on states, not Aff/canonical/solve.
        for a in range(3):
            for b in range(3):
                for k in range(5):
                    expected = tuple((r,l) for r in range(13) for l in range(13)
                                     if r-a == l+a and r+b == k*(l-b))
                    self.assertEqual(m.oracle(m.transfer(a,b,k),12),expected)
                    if k != 1:
                        l = F(2*a+(k+1)*b,k-1)
                        self.assertEqual(m.solve(m.transfer(a,b,k))['point'],(l+2*a,l))
                    else:
                        self.assertEqual(m.solve(m.transfer(a,b,k))['kind'], 'infinite' if a+b == 0 else 'none')

    def test_bounded_row_oracle(self):
        # 729 systems; preserve truth on 25 rational sample points each.
        rows = [m.Aff(a,b,c) for a in (-1,0,1) for b in (-1,0,1) for c in (-1,0,1)]
        samples = [F(x,2) for x in range(-2,3)]
        for a in rows:
            for b in rows:
                original = (a,b)
                changed = m.row_step(original,('add',0,1,F(2,3)))
                self.assertTrue(m.equivalent(original,changed))
                for r in samples:
                    for l in samples:
                        self.assertEqual(m.holds(original,r,l),m.holds(changed,r,l))

if __name__ == '__main__': unittest.main()
