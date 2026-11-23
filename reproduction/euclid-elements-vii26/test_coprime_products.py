from itertools import product
import unittest

from coprime_products import Step, prove


def common(a,b):
    return {k for k in range(2,min(a,b)+1) if a%k == b%k == 0}


class TestProducts(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(prove(45,75,26,77),(
            Step((45,75),26,3375),Step((45,75),77,3375),Step((26,77),3375,2002)))
        self.assertEqual(common(45,75),{3,5,15})
        self.assertEqual(common(3375,2002),set())
        self.assertNotEqual(26*77,1144)
        self.assertEqual(common(3375,1144),set())

    def test_both_groups_can_have_factors(self):
        self.assertTrue(common(4,8))
        self.assertTrue(common(9,15))
        self.assertEqual(prove(4,8,9,15)[-1],Step((9,15),32,135))

    def test_grid(self):
        count=accepted=0
        for a,b,c,d in product(range(2,11),repeat=4):
            valid = not any(common(x,y) for x,y in product((a,b),(c,d)))
            if valid:
                t = prove(a,b,c,d)
                self.assertEqual(tuple(s.product for s in t),(a*b,a*b,c*d))
                self.assertTrue(all(not common(s.product,s.against) for s in t))
                accepted += 1
            else:
                with self.assertRaises(ValueError):
                    prove(a,b,c,d)
                self.assertTrue(common(a*b,c*d))
            count += 1
        self.assertEqual(count,6561)
        print(f"Exact grid: {count} quadruples, {accepted} accepted, {count-accepted} rejected")

    def test_each_missing_cross_premise(self):
        fixtures = ((6,5,9,7),(6,5,7,9),(5,6,9,7),(5,6,7,9))
        for (a,b,c,d),idx in zip(fixtures,range(4)):
            failures = [i for i,(x,y) in enumerate(product((a,b),(c,d))) if common(x,y)]
            self.assertEqual(failures,[idx])
            self.assertEqual(common(a*b,c*d),{3})
            with self.assertRaises(ValueError):
                prove(a,b,c,d)

    def test_scope(self):
        for args in ((1,75,26,77),(45,75,0,77),(45,75,26,-77),(45.0,75,26,77)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                prove(*args)
