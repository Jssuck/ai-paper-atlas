from itertools import product
import unittest

from commute_products import Trace, commute, exact_measure, modern


class TestCommute(unittest.TestCase):
    def test_fixture(self):
        self.assertEqual(commute(3,4),Trace(3,4,12,12,3,4,4))
        self.assertEqual(commute(4,3),Trace(4,3,12,12,4,3,3))

    def test_grid(self):
        count = 0
        for a,b in product(range(2,21), repeat=2):
            t = commute(a,b)
            # Enumerate ordered pairs and transpose coordinates independently.
            grid = set(product(range(a),range(b)))
            mirror = {(j,i) for i,j in grid}
            self.assertEqual(mirror,set(product(range(b),range(a))))
            self.assertEqual((t.ab,t.ba),(len(grid),len(mirror)))
            self.assertEqual((t.first_measure_count,t.transferred_measure_count,t.second_measure_count),
                             (a,b,b))
            count += 1
        self.assertEqual(count,361)
        print("Exact grid:",count)

    def test_measure_controls(self):
        for args in ((3,13,4),(3,15,4),(4,12,4)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                exact_measure(*args)

    def test_historical_domain(self):
        for args in ((1,4),(4,0),(0,0),(-1,4),(3.0,4),(True,4)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                commute(*args)

    def test_modern_boundary(self):
        for (a,b), expected in (((1,4),4),((4,1),4),((0,4),0),((4,0),0),((0,0),0)):
            self.assertEqual(modern(a,b),(expected,expected))
        with self.assertRaises(ValueError):
            modern(-1,4)


if __name__ == "__main__":
    unittest.main()
