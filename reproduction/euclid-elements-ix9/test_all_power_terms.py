from itertools import product
import unittest
from all_power_terms import PowerChain,power_chain


class TestPowerChain(unittest.TestCase):
    def test_square_and_cube_examples(self):
        self.assertEqual(power_chain(4,4,2),PowerChain((4,16,64,256),(2,4,8,16)))
        self.assertEqual(power_chain(8,4,3),PowerChain((8,64,512,4096),(2,4,8,16)))

    def test_short_lengths(self):
        self.assertEqual(power_chain(4,1,2),PowerChain((4,),(2,)))
        self.assertEqual(power_chain(8,2,3),PowerChain((8,64),(2,4)))
        self.assertEqual(power_chain(8,3,3),PowerChain((8,64,512),(2,4,8)))

    def test_missing_premise(self):
        # Same-ratio continuations not starting from unity need not preserve powers.
        self.assertNotEqual(8,2**2)
        self.assertTrue(2**2<8<3**2)  # (4,8,16,...) with ratio 2
        self.assertTrue(2**3<16<3**3) # (8,16,32,...) with ratio 2
        for args in ((2,3,2),(2,3,3),(4,3,3),(8,3,2)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                power_chain(*args)

    def test_invalid_domain_and_large_exact(self):
        for args in ((1,3,2),(1,3,3),(0,1,2),(4,0,2),(4,3,1),(8,1,3.0),(4,True,2)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                power_chain(*args)
        r=10**40+1
        self.assertEqual(power_chain(r**3,5,3).roots[-1],r**5)

    def test_grid(self):
        accepted=rejected=terms=0
        for degree,length in product((2,3),range(1,11)):
            bases={r**degree:r for r in range(2,65) if r**degree<=512}
            for q in range(2,513):
                if q not in bases:
                    with self.assertRaises(ValueError):
                        power_chain(q,length,degree)
                    rejected+=1
                    continue
                out=power_chain(q,length,degree)
                self.assertEqual(out,PowerChain(tuple(q**i for i in range(1,length+1)),
                                               tuple(bases[q]**i for i in range(1,length+1))))
                accepted+=1
                terms+=length
        self.assertEqual(accepted+rejected,10220)
        print(f'Grid: {accepted} accepted chains ({terms} certified terms); {rejected} rejected')
