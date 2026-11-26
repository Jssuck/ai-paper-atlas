import unittest
from dyad_doubling import Classification,classify,doubled_dyad


class TestDyadDoubling(unittest.TestCase):
    def test_boundary_and_controls(self):
        self.assertEqual(classify(2),Classification(0,1,(),()))
        self.assertEqual(classify(4),Classification(1,1,((2,2),),()))
        self.assertEqual(classify(12),Classification(1,3,((2,6),),((3,4),)))
        self.assertEqual(classify(9),Classification(0,9,(),((3,3),)))

    def test_doubling(self):
        self.assertEqual([doubled_dyad(k) for k in range(1,5)],[4,8,16,32])
        self.assertEqual(doubled_dyad(200),2**201)

    def test_invalid(self):
        for n in (1,0,-2,True,4.0):
            with self.subTest(n=n),self.assertRaises(ValueError):
                classify(n)
        for k in (0,-1,True,3.0):
            with self.subTest(k=k),self.assertRaises(ValueError):
                doubled_dyad(k)

    def test_bounded_product_oracle(self):
        limit=256
        pairs={n:[] for n in range(2,limit+1)}
        for a in range(2,limit+1):
            for b in range(a,limit+1):
                if a*b>limit:
                    break
                pairs[a*b].append((a,b))
        expected={doubled_dyad(k) for k in range(1,8)}
        only=0
        for n,p in pairs.items():
            found=classify(n)
            self.assertEqual(tuple(sorted(found.even_pairs+found.odd_factor_pairs)),tuple(p))
            self.assertEqual(found.even_pairs,tuple((a,b) for a,b in p if a%2==b%2==0))
            cert=bool(found.even_pairs) and not found.odd_factor_pairs
            self.assertEqual(cert,n in expected)
            if cert:
                self.assertEqual(found.odd_core,1)
                self.assertEqual(doubled_dyad(found.doublings),n)
                only+=1
        print(f"Grid: {len(pairs)} values; {sum(map(len,pairs.values()))} nonunit pairs; {only} even-times-even only")
