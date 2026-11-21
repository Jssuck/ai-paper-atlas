from fractions import Fraction as Q
from itertools import product
from unittest import TestCase, main

from ratio_chains import reconstruct


def shoelace(polygon):
    total = sum(
        a[0] * b[1] - a[1] * b[0]
        for a, b in zip(polygon, polygon[1:] + polygon[:1], strict=True)
    )
    return abs(total) / 2


class TestVI14(TestCase):
    def test_number_example_and_auxiliary(self):
        r = reconstruct(6, 4, 2, 3)
        self.assertEqual((r.area_ab, r.area_bc, r.area_fe), (12, 12, 8))
        self.assertEqual((r.ratio_db_be, r.ratio_gb_bf), (Q(3, 2), Q(3, 2)))

    def test_unequal_input(self):
        r = reconstruct(6, 4, 2, 5)
        self.assertEqual((r.area_ab, r.area_bc, r.area_fe), (12, 20, 8))
        self.assertFalse(r.equal_areas)
        self.assertFalse(r.reciprocal_sides)

    def test_diagram_vertex_order(self):
        r = reconstruct(6, 4, 2, 3)
        self.assertEqual(r.ab_vertices, ((0, 0), (-6, 0), (-6, -2), (0, -2)))
        self.assertEqual(r.bc_vertices, ((0, 0), (4, 0), (4, 3), (0, 3)))
        self.assertEqual(r.fe_vertices, ((0, 0), (4, 0), (4, -2), (0, -2)))

    def test_oblique_nonunit_axes(self):
        r = reconstruct(6, 4, 2, 3, (2, 1), (-1, 2))
        self.assertEqual((r.area_ab, r.area_bc, r.area_fe), (60, 60, 40))
        self.assertEqual(r.ratio_gb_bf, Q(3, 2))

    def test_counterexamples_outside_equal_angle_hypothesis(self):
        rectangle = reconstruct(6, 4, 2, 3)
        # Use only BC from these separate constructions, retaining AB above.
        # Both directions below are unit vectors: the coefficients are lengths.
        tilted_same_products = reconstruct(6, 4, 2, 3, v=(Q(3, 5), Q(4, 5)))
        tilted_same_area = reconstruct(6, 4, 2, Q(15, 4), v=(Q(3, 5), Q(4, 5)))
        self.assertEqual(tilted_same_products.ratio_gb_bf, rectangle.ratio_db_be)
        self.assertNotEqual(tilted_same_products.area_bc, rectangle.area_ab)
        self.assertEqual(tilted_same_area.area_bc, rectangle.area_ab)
        self.assertNotEqual(tilted_same_area.ratio_gb_bf, rectangle.ratio_db_be)

    def test_reject_zero_or_negative_segments(self):
        for bad in (0, -1, Q(-3, 5)):
            for i in range(4):
                args = [6, 4, 2, 3]
                args[i] = bad
                with self.assertRaises(ValueError):
                    reconstruct(*args)

    def test_reject_collinear_and_inexact_inputs(self):
        for u, v in (((0, 0), (1, 0)), ((-2, -4), (3, 6))):
            with self.assertRaises(ValueError):
                reconstruct(6, 4, 2, 3, u, v)
        for bad in (True, 1.0, "1"):
            with self.assertRaises(TypeError):
                reconstruct(6, 4, 2, bad)

    def test_shoelace_ratios_across_1024_cases(self):
        grid = (Q(1, 3), Q(1, 2), Q(1), Q(2))
        axes = (((1, 0), (0, 1)), ((2, 1), (-1, 2)),
                ((-2, 1), (1, 2)), ((1, Q(1, 3)), (Q(2, 3), -1)))
        for x, y, z, w in product(grid, repeat=4):
            for u, v in axes:
                with self.subTest(x=x, y=y, z=z, w=w, u=u, v=v):
                    r = reconstruct(x, y, z, w, u, v)
                    a, b, c = map(shoelace, (r.ab_vertices, r.bc_vertices, r.fe_vertices))
                    self.assertEqual((a, b, c), (r.area_ab, r.area_bc, r.area_fe))
                    self.assertEqual((a / c, b / c), (r.ratio_db_be, r.ratio_gb_bf))
                    self.assertEqual(a == b, r.reciprocal_sides)

    def test_common_linear_transform_scales_areas_not_ratios(self):
        a = reconstruct(6, 4, 2, 3)
        b = reconstruct(6, 4, 2, 3, (2, 1), (1, -2))
        self.assertEqual((b.area_ab, b.area_bc, b.area_fe),
                         tuple(5 * v for v in (a.area_ab, a.area_bc, a.area_fe)))
        self.assertEqual((a.ratio_db_be, a.ratio_gb_bf), (b.ratio_db_be, b.ratio_gb_bf))


if __name__ == "__main__":
    main()
