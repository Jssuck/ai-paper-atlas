from fractions import Fraction
from itertools import combinations
import unittest
from measures_later import Measurement,measure_later


class TestMeasurement(unittest.TestCase):
    def test_adjacent_and_far(self):
        self.assertEqual(measure_later(3,2,3),Measurement(9,27,3,3))
        self.assertEqual(measure_later(3,2,5),Measurement(9,243,27,3))

    def test_boundaries(self):
        for args in ((2,0,1),(2,2,2),(2,3,2),(1,1,3),(2.0,1,2),(True,1,2),(2,True,2)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                measure_later(*args)

    def test_integer_chain_without_unity(self):
        chain=(8,12,18,27)
        self.assertEqual({Fraction(y,x) for x,y in zip(chain,chain[1:])},{Fraction(3,2)})
        self.assertNotIn(0,{chain[j]%chain[i] for i,j in combinations(range(4),2)})

    def test_large(self):
        q=10**40+3
        self.assertEqual(measure_later(q,3,8).count,q**5)

    def test_grid(self):
        pairs=0
        for q in range(2,65):
            for i,j in combinations(range(1,13),2):
                m=measure_later(q,i,j)
                self.assertEqual((m.earlier,m.later),(q**i,q**j))
                self.assertEqual(Fraction(q**j,q**i),m.count)
                self.assertEqual(Fraction(q**(i+1),q**i),m.neighbor_count)
                pairs+=1
        self.assertEqual(pairs,4158)
        print(f'Grid: {pairs} exact earlier/later pairs, all divisible')
