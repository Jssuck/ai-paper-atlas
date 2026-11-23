from fractions import Fraction
import unittest

from unit_measures import Trace, measure


class TestMeasure(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(measure(3,4,12), Trace(3,4,12,3,(0,4,8,12),4,(0,3,6,9,12)))

    def test_grid(self):
        count = 0
        for x in range(2,19):
            for y in range(2,19):
                z = sum([y]*x)
                t = measure(x,y,z)
                # Compare the unit cells actually covered, without divmod.
                for cuts in (t.y_to_z_cuts,t.x_to_z_cuts):
                    cells = [i for start,end in zip(cuts,cuts[1:]) for i in range(start,end)]
                    self.assertEqual(cells,list(range(z)))
                self.assertEqual(tuple(b-a for a,b in zip(t.y_to_z_cuts,t.y_to_z_cuts[1:])),(y,)*x)
                self.assertEqual(tuple(b-a for a,b in zip(t.x_to_z_cuts,t.x_to_z_cuts[1:])),(x,)*y)
                self.assertEqual(Fraction(z,x),y)
                count += 1
        self.assertEqual(count,289)
        print("Exact grid:",count)

    def test_residual_and_wrong_count(self):
        for args in ((3,4,13),(3,4,16)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                measure(*args)

    def test_types_and_zero(self):
        for args in ((0,4,12),(3,0,12),(3,4,0),(3.0,4,12),(3,4,12.0),(True,4,4)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                measure(*args, modern=True)

    def test_modern_boundary(self):
        for args,cuts in (((1,4,4),(0,1,2,3,4)), ((3,1,3),(0,3)), ((1,1,1),(0,1))):
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    measure(*args)
                self.assertEqual(measure(*args,modern=True).x_to_z_cuts,cuts)


if __name__ == "__main__":
    unittest.main()
