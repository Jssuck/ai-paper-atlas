import unittest
from collections import Counter
from fractions import Fraction as Q
from arc_angles import Arc,compare_arcs,comparison,principal_turns


class ArcAngleTests(unittest.TestCase):
    def test_finite_multiple_grid(self):
        counts=Counter()
        turns=(Q(1,12),Q(1,6),Q(1,4),Q(1,2),Q(2,3),Q(3,4))
        for r in (Q(2,7),1,3):
            for u in turns:
                for v in turns:
                    a,b=Arc(r,u),Arc(r,v)
                    for m in range(1,13):
                        for n in range(1,13):
                            arc,center,inscribed=compare_arcs(a,b,m,n)
                            self.assertEqual(arc,center)
                            self.assertEqual(center,inscribed)
                            counts[arc]+=1
        self.assertEqual(sum(counts.values()),15552)
        self.assertEqual(counts,{-1:7533,0:486,1:7533})
        self.assertEqual(set(counts),{-1,0,1})

    def test_same_arc_half_angle_and_ratios(self):
        a,b=Arc(3,Q(1,6)),Arc(3,Q(1,4))
        for x,y in ((a.length_over_tau(),b.length_over_tau()),
                    (a.central_turns(),b.central_turns()),
                    (a.inscribed_turns(),b.inscribed_turns())):
            self.assertEqual(Q(x,y),Q(2,3))
        self.assertEqual(a.central_turns(),2*a.inscribed_turns())
        self.assertEqual(compare_arcs(a,b,3,2),(0,0,0))
        self.assertEqual(compare_arcs(a,b,4,2),(1,1,1))
        self.assertEqual(compare_arcs(a,b,2,2),(-1,-1,-1))

    def test_principal_fold_changes_comparison(self):
        a,b=Arc(1,Q(1,3)),Arc(1,Q(1,4))
        angles=(2*a.central_turns(),2*b.central_turns())
        self.assertEqual(angles,(Q(2,3),Q(1,2)))
        self.assertEqual(tuple(map(principal_turns,angles)),(Q(1,3),Q(1,2)))
        self.assertEqual(comparison(*angles,1,1),1)
        self.assertEqual(comparison(*map(principal_turns,angles),1,1),-1)

    def test_unequal_radius_breaks_ratio(self):
        a,b=Arc(1,Q(1,2)),Arc(2,Q(1,4))
        self.assertEqual(compare_arcs(a,b,1,1),(0,1,1))
        a,b=Arc(1,Q(1,4)),Arc(2,Q(1,4))
        self.assertEqual(compare_arcs(a,b,1,1),(-1,0,0))

    def test_unlike_angles_do_not_share_a_factor(self):
        a,b=Arc(1,Q(1,6)),Arc(1,Q(1,4))
        self.assertNotEqual(a.central_turns()/b.inscribed_turns(),
                            a.length_over_tau()/b.length_over_tau())

    def test_bounds(self):
        for r,t in ((0,Q(1,4)),(1,0),(1,1),(-1,Q(1,3))):
            with self.assertRaises(ValueError):
                Arc(r,t)
        with self.assertRaises(ValueError):
            comparison(1,2,0,3)


if __name__=='__main__':
    unittest.main()
