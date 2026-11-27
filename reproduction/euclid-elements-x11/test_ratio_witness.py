from fractions import Fraction as F
from unittest import TestCase
from ratio_witness import Witness, transfer


class TestX11(TestCase):
    def test_pair_local_witnesses(self):
        self.assertEqual(transfer(F(9,4),F(18,8),4,10),
                         Witness(F(9,4),(3,2),F(2),F(5)))
        self.assertEqual(transfer(F(4,9),F(4,9),6,15),
                         Witness(F(4,9),(2,3),F(2),F(5)))
        self.assertEqual(transfer(1,1,4,10), Witness(F(1),(1,1),F(4),F(10)))

    def test_equal_irrational(self):
        self.assertEqual(transfer(2,F(4,2),4,10), Witness(F(2),None,None,None))

    def test_unequal_or_invalid(self):
        for args in [(F(9,4),F(25,4)), (F(9,4),F(4,9)), (2,3), (0,0),
                     (2,2,0,1), (2,2,1,-1), (2,2.0), (True,1)]:
            with self.assertRaises(ValueError):
                transfer(*args)

    def test_grid(self):
        # Complete for squared ratio representatives p,q <=64:
        # reduced integral side counts cannot exceed 8.
        squares = {F(m*m,n*n): F(m,n) for m in range(1,9) for n in range(1,9)}
        b,d = F(13,7), F(41,5)
        yes = 0
        for p in range(1,65):
            for q in range(1,65):
                x = F(p,q)
                cert = transfer(x,F(7*p,7*q),b,d)
                if x in squares:
                    yes += 1
                    r = squares[x]
                    m,n = r.numerator,r.denominator
                    self.assertEqual(cert.counts,(m,n))
                    self.assertEqual(n*cert.left_measure,b)
                    self.assertEqual(n*cert.right_measure,d)
                    self.assertEqual(m*cert.left_measure,r*b)
                    self.assertEqual(m*cert.right_measure,r*d)
                else:
                    self.assertEqual(cert,Witness(x,None,None,None))
        self.assertEqual(yes,180)
        print(f"Grid: 4096 ordered representatives; witnesses={yes}; neither={4096-yes}")
