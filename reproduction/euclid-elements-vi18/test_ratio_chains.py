from fractions import Fraction as Q
from itertools import product
import unittest

from ratio_chains import direct_similarity, reconstruct, sub, dot, det


class VI18Tests(unittest.TestCase):
    C, D, F, E = (0, 0), (4, 0), (1, 3), (3, 2)
    A, B = (1, 1), (1, 7)

    def mapper(self):
        return direct_similarity(self.C, self.D, self.A, self.B)

    def test_worked_map(self):
        t = self.mapper()
        self.assertEqual((t(self.C), t(self.D)), (self.A,self.B))
        self.assertEqual((t(self.F), t(self.E)),
                         ((Q(-7,2),Q(5,2)), (-2,Q(11,2))))

    def test_two_angle_intersections(self):
        t = self.mapper()
        self.assertEqual(reconstruct(self.C,self.D,self.F,self.E,self.A,self.B),
                         (t(self.F),t(self.E)))

    def test_exact_grid(self):
        for x,y,m,n in product(range(-2,3), repeat=4):
            if (m,n) == (0,0):
                continue
            c,d,f,e = ((Q(x,3),Q(y,3)),(2,1),(-1,5),(3,4))
            a,b = (3,-1),(3+Q(m,2),-1+Q(n,2))
            t = direct_similarity(c,d,a,b)
            self.assertEqual(reconstruct(c,d,f,e,a,b), (t(f),t(e)))
            source, dest = (c,d,e,f), tuple(map(t,(c,d,e,f)))
            k = dot(sub(b,a),sub(b,a)) / Q(dot(sub(d,c),sub(d,c)))
            for i,j in [(0,1),(1,2),(2,3),(3,0),(0,2),(1,3)]:
                p,q = sub(source[j],source[i]),sub(dest[j],dest[i])
                self.assertEqual(dot(q,q),k*dot(p,p))
            for i,j,k0 in [(0,1,2),(1,2,3),(2,3,0),(3,0,1)]:
                self.assertEqual(det(sub(dest[j],dest[i]),sub(dest[k0],dest[i])),
                                 k*det(sub(source[j],source[i]),sub(source[k0],source[i])))

    def test_ordered_baseline(self):
        t = direct_similarity(self.C,self.D,self.B,self.A)
        self.assertEqual(t(self.F), (Q(11,2),Q(11,2)))
        self.assertEqual(t(self.E), (4,Q(5,2)))

    def test_reflection_is_not_the_direct_solution(self):
        t = self.mapper()
        g = t(self.F)
        reflected = (2-g[0],g[1])
        axis = sub(self.B,self.A)
        self.assertNotEqual(g,reflected)
        self.assertEqual(dot(sub(g,self.A),sub(g,self.A)),
                         dot(sub(reflected,self.A),sub(reflected,self.A)))
        self.assertEqual(det(axis,sub(g,self.A)), -det(axis,sub(reflected,self.A)))

    def test_zero_source_base(self):
        with self.assertRaises(ValueError):
            direct_similarity(self.C,self.C,self.A,self.B)

    def test_zero_destination_base(self):
        with self.assertRaises(ValueError):
            direct_similarity(self.C,self.D,self.A,self.A)

    def test_degenerate_triangle(self):
        with self.assertRaises(ValueError):
            reconstruct(self.C,self.D,(7,0),self.E,self.A,self.B)

    def test_inexact_input(self):
        with self.assertRaises(TypeError):
            self.mapper()((3,1.5))


if __name__ == "__main__":
    unittest.main()
