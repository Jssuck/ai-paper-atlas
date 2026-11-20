import unittest
from fractions import Fraction as Q
from hexagon import certificate, construct, grid, neg, norm2, sub


class HexagonTests(unittest.TestCase):
    def test_grid(self):
        self.assertEqual(grid(), (96,96,96))

    def test_auxiliary_intersections_and_antipodes(self):
        a,b,c,d,e,f = construct((1,0))
        self.assertEqual((a,b,f), (neg(d),neg(e),neg(c)))
        self.assertEqual((c,e), ((Q(1,2),Q(-1,2)),(Q(1,2),Q(1,2))))
        self.assertEqual(tuple((norm2(p),norm2(sub(p,d))) for p in (c,e)),
                         ((1,1),(1,1)))

    def test_nonaxis_direction_and_radius(self):
        result = certificate(construct((3,-4)),(3,-4))
        self.assertEqual(result["edges2"], (25,)*6)
        self.assertEqual(result["angle_dots"], (Q(-25,2),)*6)
        self.assertTrue(result["regular"])

    def test_wrong_radius_keeps_vertices_on_circle(self):
        v = construct((1,0),Q(12,19))
        result = certificate(v,(1,0))
        self.assertEqual(v[4],(Q(13,19),Q(8,19)))
        self.assertEqual(result["radii2"],(1,)*6)
        self.assertEqual(result["edges2"],
                         (Q(12,19),Q(676,361),Q(12,19))*2)
        self.assertFalse(result["regular"])

    def test_swap_preserves_point_set_not_polygon(self):
        a,b,c,d,e,f = construct((1,0))
        result = certificate((a,c,b,d,e,f),(1,0))
        self.assertTrue(result["on_circle"])
        self.assertFalse(result["ccw_steps"])
        self.assertFalse(result["regular"])

    def test_degenerate_auxiliary_or_input_circle(self):
        for aux in (0,4,5,-1):
            with self.subTest(aux=aux), self.assertRaises(ValueError):
                construct((1,0),aux)
        with self.assertRaises(ValueError):
            construct((0,0))

    def test_wrong_radius_can_permute_a_regular_point_set(self):
        # q=3 gives the SAME six points but in the wrong prescribed order.
        v = construct((1,0),3)
        result = certificate(v,(1,0))
        self.assertEqual(set(v),set(construct((1,0))))
        self.assertTrue(result["on_circle"])
        self.assertTrue(result["distinct"])
        self.assertFalse(result["ccw_steps"])
        self.assertFalse(result["regular"])

    def test_certificate_rejects_repeated_vertex(self):
        v = construct((1,0))
        result = certificate((v[0],v[0],*v[2:]),(1,0))
        self.assertTrue(result["on_circle"])
        self.assertFalse(result["distinct"])
        self.assertFalse(result["regular"])

    def test_algebraic_scope_is_not_intersection_existence(self):
        # q=2 has two real intersections; the normalized y=±1/sqrt(3)
        # is outside this demonstration's rational coefficient field.
        with self.assertRaisesRegex(ValueError,"rational-coefficient"):
            construct((1,0),2)


if __name__ == "__main__":
    unittest.main()
