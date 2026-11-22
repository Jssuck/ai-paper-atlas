import unittest
from fractions import Fraction as Q
from equal_area import TRIANGLE, area, construct, rectangle, scale


class EqualAreaTests(unittest.TestCase):
    def test_worked(self):
        c=construct(6,area(TRIANGLE),27)
        self.assertEqual((c.height,c.transfer_base,c.output_base()),(2,Q(27,2),9))
        self.assertEqual(area(rectangle(c.base,c.height)),12)
        self.assertEqual(area(rectangle(c.transfer_base,c.height)),27)
        self.assertEqual(area(scale(TRIANGLE,Q(c.output_base(),c.base))),27)

    def test_irrational_width_exact_certificate(self):
        c=construct(6,12,6)
        self.assertEqual((c.transfer_base,c.output_base2,c.scale2),(3,18,Q(1,2)))
        self.assertIsNone(c.output_base())
        self.assertEqual(c.output_base2,c.base*c.transfer_base)
        self.assertEqual(c.scale2*area(TRIANGLE),6)

    def test_fraction_grid_and_placement(self):
        counts=[0,0,0]
        for b in (Q(1,2),2,6,11):
            for top in (Q(2,5),3,7):
                triangle=((0,0),(b,0),(Q(7,3),top))
                source=area(triangle)
                for k in (Q(1,3),Q(2,3),1,Q(3,2),3):
                    target=k*k*source
                    c=construct(b,source,target)
                    self.assertEqual(c.output_base(),b*k)
                    self.assertEqual(c.output_base2,b*c.transfer_base)
                    self.assertEqual(area(rectangle(b,c.height)),source)
                    self.assertEqual(area(rectangle(c.transfer_base,c.height)),target)
                    self.assertEqual(area(scale(triangle,k)),target)
                    counts[0 if k<1 else 1 if k==1 else 2]+=1
        self.assertEqual(counts,[24,12,24])

    def test_linear_control(self):
        wrong=Q(27,12)
        self.assertEqual(area(scale(TRIANGLE,wrong)),Q(243,4))
        self.assertNotEqual(area(scale(TRIANGLE,wrong)),27)

    def test_invalid(self):
        for case in ((0,12,27),(6,0,27),(6,12,-1)):
            with self.assertRaises(ValueError):
                construct(*case)


if __name__=='__main__':
    unittest.main()
