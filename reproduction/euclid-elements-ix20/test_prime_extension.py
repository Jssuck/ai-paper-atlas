from itertools import combinations
from math import lcm
import unittest
from prime_extension import Extension,extend_primes


class TestExtension(unittest.TestCase):
    def test_prime_branch(self):
        self.assertEqual(extend_primes([2,3,5]),Extension((2,3,5),30,31,31,1))

    def test_composite_branch(self):
        self.assertEqual(extend_primes([2,3,5,7,11,13]),
                         Extension((2,3,5,7,11,13),30030,30031,59,509))

    def test_smaller_than_max_and_duplicates(self):
        self.assertEqual(extend_primes([7,3,7]),Extension((3,7),21,22,2,11))

    def test_invalid(self):
        for given in ([],[1],[2,4],[True,3],[2.,3],[0],[-2]):
            with self.subTest(given=given),self.assertRaises(ValueError):
                extend_primes(given)

    def test_bounded_sieve_oracle(self):
        # Bound is product of all six available primes + 1 = 30031.
        bound=30031
        marked=bytearray(bound+1)
        for d in range(2,bound+1):
            if not marked[d]:
                for m in range(2*d,bound+1,d):
                    marked[m]=1
        primes=[p for p in range(2,bound+1) if not marked[p]]
        prime_cases=composite_cases=smaller=0
        pool=(2,3,5,7,11,13)
        for k in range(1,len(pool)+1):
            for given in combinations(pool,k):
                row=extend_primes(given)
                n=lcm(*given)+1
                p=next(p for p in primes if n%p==0)
                self.assertEqual(row,(Extension(given,n-1,n,p,n//p)))
                self.assertNotIn(p,given)
                self.assertTrue(all(n%q==1 for q in given))
                prime_cases+=n==p
                composite_cases+=n!=p
                smaller+=p<max(given)
        self.assertEqual(prime_cases+composite_cases,63)
        print(f"Grid: 63 subsets; {prime_cases} prime candidates; {composite_cases} composite candidates; {smaller} new primes below supplied maximum")
