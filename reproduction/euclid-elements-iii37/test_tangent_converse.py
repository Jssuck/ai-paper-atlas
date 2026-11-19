import unittest

from tangent_converse import DIAMETER, OFFSET, OFF_CIRCLE, Q, reference_tangents, sweep, verify


class ConverseTest(unittest.TestCase):
    def test_diameter(self):
        result = verify(*DIAMETER)
        self.assertEqual(result["branch"], "diameter")
        self.assertEqual(result["product"], 144)
        self.assertEqual(result["candidate_dot"], 0)

    def test_offset(self):
        result = verify(*OFFSET)
        self.assertEqual(result["branch"], "offset")
        self.assertEqual(result["squared_sides"], (9,25,34))
        self.assertNotEqual(result["reference"], OFFSET[-1])

    def test_both_contacts(self):
        f,r,d,c,a,b = OFFSET
        for contact in reference_tangents(f,r,d):
            self.assertNotEqual(verify(f,r,d,c,a,contact)["reference"], contact)

    def test_wrong_order(self):
        f,r,d,c,a,b = OFFSET
        with self.assertRaisesRegex(ValueError, "D-C-A"):
            verify(f,r,d,a,c,b)

    def test_wrong_square(self):
        with self.assertRaisesRegex(ValueError, "candidate square"):
            verify(*OFFSET[:-1], (0,5))

    def test_equal_length_off_circle(self):
        with self.assertRaisesRegex(ValueError, "must lie on circle"):
            verify(*OFF_CIRCLE)

    def test_irrational_reference_out_of_scope(self):
        with self.assertRaisesRegex(ValueError, "rational square root"):
            reference_tangents((0,0), 1, (2,0))

    def test_sweep(self):
        counts = sweep()
        self.assertGreater(counts["offset"], 0)
        self.assertGreater(counts["diameter"], 0)


if __name__ == "__main__":
    unittest.main()
