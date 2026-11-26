import unittest
from odd_half import OddHalf,even_factor_counts,odd_half_witness


class TestOddHalf(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(odd_half_witness(18),OddHalf(9,2))
        self.assertEqual(even_factor_counts(18),(((3,6),(9,2)),()))

    def test_mixed_and_even_even_can_coexist(self):
        self.assertEqual(even_factor_counts(12),(((3,4),),((2,6),(6,2))))
        self.assertEqual(even_factor_counts(4),((),((2,2),)))

    def test_unit_and_false_premises(self):
        self.assertEqual(even_factor_counts(2),((),()))
        for n in (2,4,12,9,1,0,-6,True,6.0):
            with self.subTest(n=n),self.assertRaises(ValueError):
                odd_half_witness(n)

    def test_large_exact_witness(self):
        d=10**100+1
        self.assertEqual(odd_half_witness(2*d),OddHalf(d,2))

    def test_independent_product_grouping(self):
        limit=256
        odd=set(range(3,limit+1,2))
        even=set(range(2,limit+1,2))
        grouped={n:([],[]) for n in range(2,limit+1)}
        for divisor in range(2,limit+1):
            for count in sorted(even):
                n=divisor*count
                if n>limit:
                    break
                grouped[n][0 if divisor in odd else 1].append((divisor,count))
        accepted=mixed_pairs=even_pairs=0
        for n,(mixed,ee) in grouped.items():
            self.assertEqual(even_factor_counts(n),(tuple(mixed),tuple(ee)))
            if mixed and not ee:
                w=odd_half_witness(n)
                self.assertIn((w.odd_divisor,w.even_count),mixed)
                accepted+=1
            else:
                with self.assertRaises(ValueError):
                    odd_half_witness(n)
            mixed_pairs+=len(mixed)
            even_pairs+=len(ee)
        print(f"Grid: {len(grouped)} values; {accepted} mixed-only witnesses; {mixed_pairs} mixed pairs; {even_pairs} even-even pairs")
