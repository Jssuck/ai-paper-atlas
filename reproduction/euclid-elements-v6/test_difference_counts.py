from fractions import Fraction
import unittest

from difference_counts import Quantity, finite_grid, make_inputs, reconstruct


class DifferenceTests(unittest.TestCase):
    def test_unit(self):
        c = reconstruct(*make_inputs(3, 7, 4, 3))
        self.assertEqual((c.remainder_count, c.branch), (1, "unit"))

    def test_strict(self):
        c = reconstruct(*make_inputs(Fraction(2, 3), Fraction(5, 4), 7, 3))
        self.assertEqual((c.remainder_count, c.branch), (4, "strict"))
        self.assertEqual(tuple(r.value for r in c.remainders), (Fraction(8, 3), 5))

    def test_rebuilt_wholes(self):
        inputs = make_inputs(2, 7, 8, 3)
        c = reconstruct(*inputs)
        self.assertEqual(c.rebuilt_wholes, inputs[1])
        self.assertEqual(c.remainders, c.auxiliaries)

    def test_preserved_kind(self):
        result = reconstruct(*make_inputs(3, 7, 4, 3))
        self.assertEqual(tuple(q.kind for q in result.remainders), ("length", "area"))

    def test_compensating_errors(self):
        base, whole, cut = make_inputs(2, 3, 5, 3)
        with self.assertRaisesRegex(ValueError, "counts differ"):
            reconstruct(base, (whole[0], Quantity(18, "area")),
                        (cut[0], Quantity(12, "area")))

    def test_cut_only_mismatch(self):
        base, whole, cut = make_inputs(2, 3, 5, 3)
        with self.assertRaisesRegex(ValueError, "counts differ"):
            reconstruct(base, whole, (cut[0], Quantity(12, "area")))

    def test_non_integer(self):
        base, whole, cut = make_inputs(2, 3, 5, 3)
        with self.assertRaisesRegex(ValueError, "strict integer"):
            reconstruct(base, whole, (Quantity(5, "length"), cut[1]))

    def test_nonproper(self):
        for m, n in ((3, 3), (3, 4)):
            with self.subTest(m=m, n=n), self.assertRaisesRegex(ValueError, "positive remainder"):
                reconstruct(*make_inputs(2, 3, m, n))

    def test_one_is_not_input_multiple(self):
        with self.assertRaisesRegex(ValueError, "strict integer"):
            reconstruct(*make_inputs(2, 3, 3, 1))

    def test_type_checks(self):
        base, whole, cut = make_inputs(2, 3, 5, 3)
        with self.assertRaisesRegex(ValueError, "same kind"):
            reconstruct(base, whole, (cut[0], Quantity(9, "length")))
        with self.assertRaises(TypeError):
            Quantity(0.5, "length")

    def test_grid(self):
        self.assertEqual(finite_grid(), (54, 135, 189))


if __name__ == "__main__":
    unittest.main()
