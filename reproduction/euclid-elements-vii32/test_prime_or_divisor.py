import unittest

from prime_or_divisor import Certificate, classify


def proper(n):
    return [j for j in range(2,n) if n%j == 0]


class TestClassification(unittest.TestCase):
    def test_prime_branch(self):
        self.assertEqual(classify(13),Certificate("prime-itself",13,(13,)))
        self.assertEqual(classify(2,largest=False),Certificate("prime-itself",2,(2,)))

    def test_composite_branch(self):
        self.assertEqual(classify(84),Certificate("VII.31",7,(84,42,21,7)))
        self.assertEqual(classify(84,largest=False),Certificate("VII.31",2,(84,2)))

    def test_independent_grid(self):
        primes = composites = 0
        for n in range(2,201):
            ds = proper(n)
            primes += not ds
            composites += bool(ds)
            for largest in (True,False):
                c = classify(n,largest=largest)
                self.assertEqual(c.branch,"VII.31" if ds else "prime-itself")
                self.assertEqual(c.path[0],n)
                self.assertEqual(c.path[-1],c.prime)
                self.assertFalse(proper(c.prime))
                self.assertEqual(n%c.prime,0)
                self.assertEqual(len(c.path)>1,bool(ds))
                for a,b in zip(c.path,c.path[1:]):
                    self.assertEqual(b,proper(a)[-1 if largest else 0])
                    self.assertIn(b,ds)
        self.assertEqual((primes,composites),(46,153))
        print(f"Exact grid: {primes} primes, {composites} composites, {2*composites} descent paths")

    def test_square(self):
        self.assertEqual(classify(49).path,(49,7))

    def test_input_boundary(self):
        for invalid in (1,0,-2,2.0,True):
            with self.subTest(invalid=invalid),self.assertRaises(ValueError):
                classify(invalid)
        with self.assertRaises(ValueError):
            classify(84,largest="yes")
