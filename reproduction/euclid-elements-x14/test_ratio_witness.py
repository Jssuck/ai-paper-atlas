from fractions import Fraction as F
from unittest import TestCase
from ratio_witness import classify,Witness


class TestX14(TestCase):
    def test_examples(self):
        self.assertEqual(classify(5,3,F(15,2),F(9,2)),Witness(F(16,25),F(4,5)))
        self.assertEqual(classify(3,2,F(9,2),3),Witness(F(5,9),None))
        self.assertEqual(classify(F(15,2),F(9,2),5,3),Witness(F(16,25),F(4,5)))

    def test_invalid(self):
        for data in [(5,3,5,4),(5,5,5,5),(3,5,3,5),(5,3,5,5),(5,0,5,0),
                     (5,3,5,3.0),(True,1,5,4)]:
            with self.assertRaises(ValueError):
                classify(*data)

    def test_grid(self):
        count = total = 0
        for a in range(2,33):
            squares = {r*r:r for r in range(1,a)}
            for b in range(1,a):
                expected = squares.get(a*a-b*b)
                for k in range(1,9):
                    q = classify(a,b,k*a,k*b)
                    self.assertEqual(q.remainder_to_larger_ratio,
                                     None if expected is None else F(expected,a))
                    self.assertEqual(q.remainder_square_ratio * (k*a)**2, (k*a)**2-(k*b)**2)
                    count += expected is not None
                    total += 1
        self.assertEqual((total,count),(3968,176))
        print(f"Grid: {total} ordered scale combinations; both commensurable={count}; neither={total-count}")

    def test_symbolic_irrational_scale(self):
        # This verifies the algebra in squared coordinates only, not an API input.
        for a,b in [(5,3),(3,2)]:
            square_scale = F(2)
            self.assertEqual((square_scale*a*a-square_scale*b*b)/(square_scale*a*a),
                             F(a*a-b*b,a*a))
