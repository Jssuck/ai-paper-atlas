import unittest
from fractions import Fraction as Q
from extreme_mean import Root5,coerce,conjugate_root,cut,rectangle,signed_double_area


class ExtremeMeanTests(unittest.TestCase):
    def test_ten(self):
        x,y=cut(10)
        self.assertEqual((x,y),(Root5(-5,5),Root5(15,-5)))
        self.assertEqual(x*x,coerce(10)*y)
        self.assertEqual(x*x,Root5(150,-50))

    def test_exact_coordinate_grid(self):
        cases=0
        for numerator in (1,2,5,7,10,23,100):
            for denominator in (1,2,3,7,11):
                length=Q(numerator,denominator)
                total=coerce(length)
                x,y=cut(length)
                self.assertEqual((x.sign(),y.sign(),(x-y).sign()),(1,1,1))
                self.assertEqual(x+y,total)
                self.assertEqual(signed_double_area(rectangle(x,x)),
                                 signed_double_area(rectangle(total,y)))
                # VI.29 specialized: the applied rectangle on L+x has area L².
                self.assertEqual(signed_double_area(rectangle(total+x,x)),2*(total*total))
                common=signed_double_area(rectangle(total,x))
                self.assertEqual(signed_double_area(rectangle(total,total))-common,
                                 signed_double_area(rectangle(total,y)))
                self.assertEqual(signed_double_area(rectangle(total+x,x))-common,
                                 signed_double_area(rectangle(x,x)))
                m=length/2
                d=x+m
                self.assertEqual(d*d,coerce(m*m+length*length))
                cases+=1
        self.assertEqual(cases,35)

    def test_wrong_branch_and_swapping(self):
        length=coerce(10)
        x,y=cut(10)
        bad=conjugate_root(10)
        self.assertEqual((length+bad)*bad,length*length)
        self.assertEqual(bad.sign(),-1)
        self.assertEqual((length+bad).sign(),-1)
        self.assertNotEqual(y*y,length*x)
        self.assertEqual((y-x).sign(),-1)

    def test_exact_sign_distinguishes_close_values(self):
        self.assertEqual(Root5(161,-72).sign(),1)
        self.assertEqual(Root5(38,-17).sign(),-1)
        self.assertEqual(Root5(0,0).sign(),0)

    def test_reject_nonpositive(self):
        for length in (0,-1,Q(-3,4)):
            with self.assertRaises(ValueError):
                cut(length)


if __name__=='__main__':
    unittest.main()
