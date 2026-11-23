from itertools import product
import unittest

from divisor_inherits_coprimality import Transfer, inherit, transfer


def common(a,b):
    return [d for d in range(2,min(a,b)+1) if a%d == b%d == 0]


class TestCoprime(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(inherit(35,12,5),(7,1))
        self.assertEqual(transfer(12,9,6,3),Transfer((2,2,3),4))

    def test_converse(self):
        self.assertEqual(common(4,9),[])
        self.assertEqual(common(12,9),[3])
        with self.assertRaisesRegex(ValueError,"coprime"):
            inherit(12,9,4)

    def test_grid(self):
        admissible = witnesses = 0
        for a,b,c in product(range(2,19),repeat=3):
            if a%c:
                continue
            ds = common(c,b)
            if not common(a,b):
                self.assertFalse(ds)
                self.assertEqual(inherit(a,b,c),(a//c,1))
                admissible += 1
            for d in ds:
                t = transfer(a,b,c,d)
                self.assertIn(d,common(a,b))
                self.assertEqual((d*t.a_over_d,d*t.divisions[2]),(a,b))
                witnesses += 1
        self.assertGreater(admissible,0)
        self.assertGreater(witnesses,0)
        print(f"Exact grid: {17**3} triples, {admissible} admissible triples, {witnesses} transfers")

    def test_invalid(self):
        for args in ((35,12,6),(12,9,4),(0,12,5),(35,12,5.0),(True,12,5)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                inherit(*args)
        for args in ((12,9,5,3),(12,9,6,4),(12,10,6,3)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                transfer(*args)

    def test_unit_and_reflexive(self):
        self.assertEqual(common(1,12),[])
        with self.assertRaises(ValueError):
            inherit(35,12,1)
        self.assertEqual(inherit(5,12,5),(1,1))
