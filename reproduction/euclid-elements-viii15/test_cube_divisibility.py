from fractions import Fraction
from itertools import product
import unittest
from cube_divisibility import Trace, inspect, from_cubes


def count(x,y):
    q,r=divmod(y,x)
    return None if r else q


class TestCubes(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(inspect(4,12),Trace((16,48,144),(64,192,576,1728),(3,1),3,(3,3,3),27))
        self.assertEqual(from_cubes(4,12),3)
        self.assertIsNone(from_cubes(12,4))

    def test_grid(self):
        yes=0
        for c,d in product(range(1,41),repeat=2):
            t=inspect(c,d,modern=True)
            a,h,k,b=t.cubes
            self.assertEqual(t.squares,(c**2,c*d,d**2))
            self.assertEqual(Fraction(b,a),Fraction(d,c)**3)
            self.assertEqual(t.side_count,count(c,d))
            self.assertEqual(t.adjacent_counts,tuple(count(x,y) for x,y in zip(t.cubes,t.cubes[1:])))
            self.assertEqual(t.endpoint_count,count(a,b))
            self.assertEqual(from_cubes(c,d,modern=True),count(c,d))
            yes += t.side_count is not None
        self.assertEqual(yes,158)
        print(f"Exact grid: 1600 side pairs, {yes} measure, {1600-yes} do not")

    def test_joyce_extra_premise(self):
        t=inspect(2,6)
        self.assertEqual(t.cubes,(8,24,72,216))
        self.assertEqual(t.squares[-1],36)
        self.assertEqual(t.squares[-1]%t.cubes[0],4)
        self.assertEqual(from_cubes(2,6),3)

    def test_no_and_big(self):
        self.assertEqual(inspect(4,6).cubes,(64,96,144,216))
        self.assertIsNone(from_cubes(4,6))
        self.assertEqual(inspect(4,6).squares[-1],36)
        c=10**60+1
        self.assertEqual(from_cubes(c,11*c),11)
        self.assertIsNone(from_cubes(c,11*c+1))

    def test_scope(self):
        self.assertEqual(from_cubes(1,3,modern=True),3)
        self.assertEqual(from_cubes(7,7,modern=True),1)
        for sides in ((0,2),(-2,3),(True,4),(2.0,4),(1,3),(7,7)):
            with self.subTest(sides=sides),self.assertRaises(ValueError):
                inspect(*sides)
