import unittest
from itertools import product
from prime_descent import Stage,descend_prime


class TestDescent(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(descend_prime(12,3,3),(Stage(3,1728,576),Stage(2,144,48),Stage(1,12,4)))

    def test_missing_and_invalid_premises(self):
        for args in ((12,3,5),(6,2,4),(1,4,2),(3,0,2),(3,4,1),(True,3,2)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                descend_prime(*args)

    def test_composite_and_multiplicity_controls(self):
        self.assertEqual(divmod(6**2,4),(9,0))
        self.assertEqual(divmod(6,4),(1,2))
        self.assertEqual(descend_prime(6,2,2)[-1].quotient,3)
        self.assertEqual(descend_prime(6,2,2)[0].quotient%2,0)
        self.assertNotEqual(descend_prime(6,2,2)[-1].quotient%2,0)

    def test_single_and_large(self):
        self.assertEqual(descend_prime(3,1,3),(Stage(1,3,1),))
        q=3*(10**40+1)
        self.assertEqual(descend_prime(q,5,3)[0].quotient,q**5//3)

    def test_grid(self):
        # Independent sieve, then mark each prime's multiples in base range.
        primes=set(range(2,65))
        for d in range(2,65):
            primes.difference_update(range(d*d,65,d))
        support={q:set() for q in range(2,65)}
        for p in primes:
            for q in range(p,65,p):
                support[q].add(p)
        accepted = rejected = stage_count = 0
        for q,k,p in product(range(2,65),range(1,9),sorted(primes)):
            if p not in support[q]:
                with self.assertRaises(ValueError):
                    descend_prime(q,k,p)
                self.assertNotEqual(pow(q,k,p),0)
                rejected+=1
                continue
            rows=descend_prime(q,k,p)
            self.assertEqual(rows,tuple(Stage(e,q**e,q**e//p) for e in range(k,0,-1)))
            self.assertTrue(all(row.quotient*p==row.power for row in rows))
            accepted+=1
            stage_count+=len(rows)
        self.assertEqual(accepted+rejected,63*8*18)
        print(f"Grid: {accepted} certificates, {stage_count} witnessed stages, {rejected} nondividing primes rejected")
