import unittest
from fractions import Fraction as F

from ratio_ops import (
    Amount, Ratio, alternate, corresponding, endpoint_ratios,
    grid, power_ratio, terms, transform,
)


class RatioOperationsTests(unittest.TestCase):
    def test_positive_exact_domain(self):
        for invalid in (False, 0, -1, 1.25):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                Amount(invalid, "length")
        with self.assertRaises(ValueError):
            Amount(1, "")

    def test_duplicate_and_triplicate(self):
        ts = terms(27, 18, 12, 8)
        self.assertEqual(power_ratio(ts[:3]).value, F(9, 4))
        self.assertEqual(power_ratio(ts).value, F(27, 8))
        self.assertNotEqual(power_ratio(ts[:3]).value, 2 * Ratio(*ts[:2]).value)

    def test_power_domain_and_arity(self):
        for malformed in (terms(1, 2), terms(9, 4, 2), terms(16, 8, 4, 2, 1)):
            with self.subTest(malformed=malformed), self.assertRaises(ValueError):
                power_ratio(malformed)

    def test_correspondence_and_alternate(self):
        p, q = Ratio(*terms(6, 4)), Ratio(*terms(9, 6))
        self.assertEqual(corresponding(p, q), ((p.leading, q.leading), (p.following, q.following)))
        self.assertEqual(tuple(r.value for r in alternate(p, q)), (F(2, 3), F(2, 3)))

    def test_alternate_cross_kind_rejected(self):
        p, q = Ratio(*terms(6, 4)), Ratio(*terms(9, 6, kind="area"))
        self.assertTrue(p.proportional_to(q))
        with self.assertRaises(ValueError):
            alternate(p, q)

    def test_inverse_and_conversion_are_distinct(self):
        p = Ratio(*terms(3, 2))
        self.assertEqual(transform(p, "inverse").value, F(2, 3))
        self.assertEqual(transform(p, "conversion").value, 3)
        self.assertEqual(transform(p, "composition").value, F(5, 2))
        self.assertEqual(transform(p, "separation").value, F(1, 2))

    def test_subtraction_needs_positive_excess(self):
        for p in (Ratio(*terms(2, 2)), Ratio(*terms(2, 3))):
            for op in ("separation", "conversion"):
                with self.subTest(p=p, op=op), self.assertRaises(ValueError):
                    transform(p, op)
        with self.assertRaises(ValueError):
            transform(Ratio(*terms(3, 2)), "unknown")

    def test_aligned_and_perturbed(self):
        p = terms(12, 6, 2)
        aligned = terms(18, 9, 3, kind="area")
        perturbed = terms(18, 6, 3, kind="area")
        for q, swapped in ((aligned, False), (perturbed, True)):
            self.assertEqual(tuple(r.value for r in endpoint_ratios(p, q, perturbed=swapped)), (6, 6))
            with self.assertRaises(ValueError):
                endpoint_ratios(p, q, perturbed=not swapped)

    def test_aligned_multi_link_and_invalid_chains(self):
        self.assertEqual(tuple(r.value for r in endpoint_ratios(terms(24, 12, 4, 1), terms(48, 24, 8, 2))), (24, 24))
        for left, right, swapped in (
            (terms(6, 3, 1), terms(6, 1), False),
            (terms(6, 3, 1), terms(6, 4, 1), False),
            (terms(24, 12, 4, 1), terms(48, 24, 8, 2), True),
            (terms(6, 3, 1), (Amount(6, "area"), Amount(3, "length"), Amount(1, "area")), False),
        ):
            with self.subTest(left=left, right=right, swapped=swapped), self.assertRaises(ValueError):
                endpoint_ratios(left, right, perturbed=swapped)

    def test_equal_link_ratios_allow_both_patterns(self):
        a, b = terms(4, 2, 1), terms(12, 6, 3)
        for swapped in (False, True):
            self.assertEqual(tuple(r.value for r in endpoint_ratios(a, b, perturbed=swapped)), (4, 4))

    def test_grid(self):
        self.assertEqual(grid(), (128, 56))


if __name__ == "__main__":
    unittest.main()
