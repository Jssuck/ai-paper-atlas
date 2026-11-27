from math import isqrt
import unittest

from perfect_number import perfect_number


def proper_divisors(n):
    found={1}
    for d in range(2,isqrt(n)+1):
        q,r=divmod(n,d)
        if not r:
            found.update((d,q))
    return found


class TestPerfectNumber(unittest.TestCase):
    def test_smallest(self):
        row=perfect_number(2)
        self.assertEqual((row.chain,row.mersenne,row.number),((1,2),3,6))
        self.assertEqual((row.pure_powers,row.mixed_powers),((1,2),(3,)))

    def test_composite_sum(self):
        for p,a,b in ((4,3,5),(11,23,89)):
            self.assertEqual((1<<p)-1,a*b)
            with self.assertRaises(ValueError):
                perfect_number(p)

    def test_domain(self):
        for p in (1,0,-1,True,3.0,21):
            with self.subTest(p=p),self.assertRaises(ValueError):
                perfect_number(p)

    def test_complete_bounded_grid(self):
        # Independent Eratosthenes sieve for all chain sums in the domain.
        top=(1<<20)-1
        sieve=bytearray(b"\1")*(top+1)
        sieve[:2]=b"\0\0"
        for d in range(2,isqrt(top)+1):
            if sieve[d]:
                sieve[d*d::d]=bytes((top-d*d)//d+1)
        accepted=[]
        probes=total_divisors=0
        for p in range(2,21):
            m=(1<<p)-1
            if not sieve[m]:
                with self.assertRaises(ValueError):
                    perfect_number(p)
                continue
            row=perfect_number(p)
            external=proper_divisors(row.number)
            self.assertEqual(sum(external),row.number)
            self.assertEqual(external,set(row.pure_powers)|set(row.mixed_powers))
            self.assertFalse(set(row.pure_powers)&set(row.mixed_powers))
            probes+=isqrt(row.number)-1
            total_divisors+=len(external)
            accepted.append(p)
        self.assertEqual(accepted,[2,3,5,7,13,17,19])
        print(f"Grid: 19 exponents; {len(accepted)} prime sums; {19-len(accepted)} composite sums; {total_divisors} proper divisors; {probes} paired probes")
