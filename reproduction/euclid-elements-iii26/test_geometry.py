import unittest
from fractions import Fraction as F
from geometry import Arc, make_arc, unit, dot, sub


class GeometryTests(unittest.TestCase):
    def test_minor(self):
        a=make_arc(t=F(1,2))
        self.assertEqual(a.sweep_key(),("minor",F(3,5)))
        self.assertEqual(a.half_sweep_cot(),2)

    def test_major(self):
        a=make_arc(t=-2)
        self.assertEqual(a.sweep_key(),("major",F(-3,5)))
        self.assertEqual(a.half_sweep_cot(),F(-1,2))

    def test_semicircle(self):
        a=make_arc(t=None)
        self.assertEqual(a.sweep_key(),("semicircle",-1))
        self.assertEqual(a.inscribed_cot((0,-1)),0)

    def test_opposite_arc_not_same(self):
        a=make_arc(t=F(1,2)); b=make_arc(t=F(1,2),ccw=False)
        self.assertEqual(a.sweep_key()[1],b.sweep_key()[1])
        self.assertFalse(a.congruent_to(b))

    def test_vertex_complement(self):
        a=make_arc(t=1)
        self.assertEqual(a.inscribed_cot((-1,0)),1)
        self.assertEqual(a.inscribed_cot((0,-1)),1)

    def test_major_vertex(self):
        a=make_arc(t=-1)
        self.assertEqual(a.inscribed_cot(unit(-F(1,2))),-1)

    def test_vertex_on_target_rejected(self):
        with self.assertRaises(ValueError):
            make_arc(t=1).inscribed_cot(unit(F(1,2)))

    def test_endpoint_rejected(self):
        with self.assertRaises(ValueError):
            make_arc().inscribed_cot((1,0))

    def test_offcircle_rejected(self):
        with self.assertRaises(ValueError):
            make_arc().contains_open((0,0))

    def test_zero_radius_rejected(self):
        with self.assertRaises(ValueError): make_arc(radius=0)

    def test_negative_radius_rejected(self):
        with self.assertRaises(ValueError): make_arc(radius=-1)

    def test_repeated_endpoint_rejected(self):
        with self.assertRaises(ValueError): make_arc(t=0)

    def test_float_rejected(self):
        with self.assertRaises(TypeError): make_arc(radius=1.0)
        with self.assertRaises(TypeError): make_arc(t=0.5)

    def test_bool_rejected(self):
        with self.assertRaises(TypeError): make_arc(radius=True)
        with self.assertRaises(TypeError): make_arc(center=(False,0))

    def test_bad_endpoint(self):
        with self.assertRaises(ValueError): Arc((0,0),1,(1,0),(1,1))

    def test_bad_orientation(self):
        with self.assertRaises(TypeError): make_arc(ccw=1)

    def test_bad_rotation(self):
        with self.assertRaises(ValueError): make_arc(rotation=(1,1))

    def test_equal_angle_unequal_radius(self):
        a=make_arc(radius=1,t=1); b=make_arc(radius=2,t=1)
        self.assertEqual(a.half_sweep_cot(),b.half_sweep_cot())
        self.assertFalse(a.congruent_to(b))

    def test_translation_rotation(self):
        a=make_arc(t=F(1,2));b=make_arc(t=F(1,2),center=(7,-2),rotation=unit(F(2,3)))
        self.assertTrue(a.congruent_to(b))
        self.assertEqual(a.map_point_to(b,a.end),b.end)
        self.assertEqual(a.map_point_to(b,a.center),b.center)

    def test_reflection(self):
        a=make_arc(t=1);b=make_arc(t=-1,ccw=False,center=(3,4))
        self.assertTrue(a.congruent_to(b))
        self.assertEqual(a.map_point_to(b,(0,-1)),(3,5))

    def test_mapping_bad_input(self):
        with self.assertRaises(TypeError): make_arc().map_point_to(make_arc(),(0.5,1))
        with self.assertRaises(ValueError): make_arc().map_point_to(make_arc(radius=2),(0,0))

    def test_extreme_exact_parameters(self):
        for t in (F(1,10**20),F(10**20),-F(1,10**20),-F(10**20)):
            a=make_arc(t=t)
            self.assertEqual(a.half_sweep_cot(),1/t)

    def test_supplementary_vertices(self):
        a=make_arc(t=F(1,2));b=make_arc(t=F(1,2),ccw=False)
        self.assertEqual(a.inscribed_cot((-1,0)),2)
        self.assertEqual(b.inscribed_cot(unit(F(1,4))),-2)

    def test_mixed_angle_types_not_equal_sweep(self):
        # Central angle 90 deg and inscribed angle 90 deg stand on 90/180 deg arcs.
        self.assertNotEqual(make_arc(t=1).sweep_key(),make_arc(t=None).sweep_key())


if __name__ == "__main__": unittest.main()
