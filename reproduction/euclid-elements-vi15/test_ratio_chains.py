from fractions import Fraction as Q
from itertools import product
from unittest import TestCase, main

from ratio_chains import reconstruct


def shoelace(polygon):
    return abs(sum(a[0]*b[1] - a[1]*b[0]
                   for a, b in zip(polygon, polygon[1:]+polygon[:1], strict=True))) / 2


def squared_distance(a, b):
    return sum((x-y)**2 for x, y in zip(a, b, strict=True))


class TestVI15(TestCase):
    def test_oblique_example(self):
        r = reconstruct(6, 4, 2, 3, v=(1, 1))
        self.assertEqual((r.area_abc, r.area_ade, r.area_bad), (6, 6, 4))
        self.assertEqual((r.ratio_ca_ad, r.ratio_ea_ab), (Q(3, 2), Q(3, 2)))

    def test_named_vertices(self):
        r = reconstruct(6, 4, 2, 3, v=(1, 1))
        self.assertEqual(r.abc_vertices, ((0, 0), (2, 2), (6, 0)))
        self.assertEqual(r.ade_vertices, ((0, 0), (-4, 0), (-3, -3)))
        self.assertEqual(r.bad_vertices, ((2, 2), (0, 0), (-4, 0)))

    def test_non_equal_and_order(self):
        r = reconstruct(6, 4, 2, 5)
        self.assertEqual((r.area_abc, r.area_ade, r.area_bad), (6, 10, 4))
        self.assertFalse(r.equal_areas)
        self.assertFalse(r.reciprocal_sides)
        self.assertEqual((r.ratio_ca_ad, r.ratio_ea_ab), (Q(3, 2), Q(5, 2)))
        # Equal-area example disproves using the uninverted second ratio.
        r = reconstruct(6, 4, 2, 3)
        self.assertNotEqual(r.ratio_ca_ad, 1 / r.ratio_ea_ab)

    def test_drop_equal_angle_ratios_sufficiency_fails(self):
        right = reconstruct(6, 4, 2, 3)
        tilted = reconstruct(6, 4, 2, 3, v=(Q(3, 5), Q(4, 5)))
        # Compare ABC from the right-angle model to ADE from the tilted model.
        self.assertEqual(right.ratio_ca_ad, tilted.ratio_ea_ab)
        self.assertEqual((right.area_abc, tilted.area_ade), (6, Q(24, 5)))

    def test_drop_equal_angle_ratios_necessity_fails(self):
        right = reconstruct(6, 4, 2, 3)
        tilted = reconstruct(6, 4, 2, Q(15, 4), v=(Q(3, 5), Q(4, 5)))
        self.assertEqual(right.area_abc, tilted.area_ade)
        self.assertEqual((right.ratio_ca_ad, tilted.ratio_ea_ab), (Q(3, 2), Q(15, 8)))

    def test_common_transform_scales_area_only(self):
        r = reconstruct(6, 4, 2, 3)
        s = reconstruct(6, 4, 2, 3, (2, 1), (1, -2))
        self.assertEqual((s.area_abc, s.area_ade, s.area_bad),
                         tuple(5*a for a in (r.area_abc, r.area_ade, r.area_bad)))
        self.assertEqual((s.ratio_ca_ad, s.ratio_ea_ab), (r.ratio_ca_ad, r.ratio_ea_ab))

    def test_reject_non_positive_coefficients(self):
        for i, bad in product(range(4), (0, -1, Q(-1, 3))):
            args = [6, 4, 2, 3]
            args[i] = bad
            with self.assertRaises(ValueError):
                reconstruct(*args)

    def test_reject_degenerate_or_inexact_inputs(self):
        for u, v in (((0, 0), (1, 0)), ((-2, -4), (3, 6))):
            with self.assertRaises(ValueError):
                reconstruct(6, 4, 2, 3, u, v)
        for bad in (True, 3.0, "3"):
            with self.assertRaises(TypeError):
                reconstruct(6, 4, 2, bad)

    def test_independent_shoelace_and_squared_lengths_1024_cases(self):
        grid = (Q(1, 3), Q(1, 2), Q(1), Q(2))
        axes = (((1, 0), (0, 1)), ((1, 0), (1, 1)), ((-2, 1), (1, 2)),
                ((1, Q(1, 3)), (Q(2, 3), -1)))
        for x, y, z, w in product(grid, repeat=4):
            for u, v in axes:
                with self.subTest(x=x, y=y, z=z, w=w, u=u, v=v):
                    r = reconstruct(x, y, z, w, u, v)
                    p, q, s = map(shoelace, (r.abc_vertices, r.ade_vertices, r.bad_vertices))
                    self.assertEqual((p, q, s), (r.area_abc, r.area_ade, r.area_bad))
                    a, b, c = r.abc_vertices
                    _, d, e = r.ade_vertices
                    self.assertEqual((p/s)**2, squared_distance(c, a)/squared_distance(a, d))
                    self.assertEqual((q/s)**2, squared_distance(e, a)/squared_distance(a, b))
                    self.assertEqual((p/s, q/s), (r.ratio_ca_ad, r.ratio_ea_ab))
                    self.assertEqual(r.equal_areas, r.reciprocal_sides)


if __name__ == "__main__":
    main()
