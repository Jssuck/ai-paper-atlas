import unittest

from prime_divisor_descent import descend


def proper(n):
    return [d for d in range(2,n) if n%d == 0]


class TestDescent(unittest.TestCase):
    def test_paths(self):
        self.assertEqual(descend(84),(84,42,21,7))
        self.assertEqual(descend(84,"smallest"),(84,2))
        self.assertEqual(descend(84,"middle"),(84,12,4,2))

    def test_grid(self):
        prime_count = composite_count = paths = 0
        for n in range(2,201):
            oracle = proper(n)
            if not oracle:
                with self.assertRaisesRegex(ValueError,"composite"):
                    descend(n)
                prime_count += 1
                continue
            composite_count += 1
            for choice in ("largest","smallest","middle"):
                path = descend(n,choice)
                self.assertEqual(path[0],n)
                for a,b in zip(path,path[1:]):
                    ds = proper(a)
                    expected = ds[-1] if choice == "largest" else ds[0] if choice == "smallest" else ds[len(ds)//2]
                    self.assertEqual(b,expected)
                    self.assertGreater(a,b)
                    self.assertIn(b,oracle)
                self.assertFalse(proper(path[-1]))
                paths += 1
        self.assertEqual((prime_count,composite_count,paths),(46,153,459))
        print(f"Exact grid: {prime_count} primes, {composite_count} composites, {paths} paths")

    def test_square(self):
        self.assertEqual(descend(49),(49,7))
        self.assertEqual(descend(64),(64,32,16,8,4,2))

    def test_invalid(self):
        for n in (1,0,-84,True,84.0):
            with self.subTest(n=n),self.assertRaises(ValueError):
                descend(n)
        with self.assertRaises(ValueError):
            descend(84,"random")

    def test_prime_start(self):
        for p in (2,13,97):
            with self.subTest(p=p),self.assertRaisesRegex(ValueError,"composite"):
                descend(p)
