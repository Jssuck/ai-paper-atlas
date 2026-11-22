import unittest
from common_measure import Step,backward_witness,common_divisors,greatest_measure,trace


class CommonMeasureTests(unittest.TestCase):
    def test_example_and_backward(self):
        rows=trace(84,30)
        self.assertEqual(rows,(Step(84,30,2,24),Step(30,24,1,6),Step(24,6,4,0)))
        self.assertEqual(backward_witness(rows),
                         (6,((24,6,4,1),(30,24,5,4),(84,30,14,5))))
        self.assertEqual(greatest_measure(84,30,True),6)

    def test_independent_divisors_grid(self):
        count=0
        for a in range(1,65):
            for b in range(1,65):
                rows=trace(a,b)
                g,rev=backward_witness(rows)
                divisors=common_divisors(a,b)
                self.assertEqual(g,max(divisors))
                self.assertEqual((a%g,b%g),(0,0))
                self.assertEqual(set(divisors),{k for k in range(1,g+1) if not g%k})
                for m in divisors:
                    self.assertTrue(all(row.r%m==0 for row in rows))
                    self.assertEqual(g%m,0)
                x,y,u,v=rev[-1]
                self.assertEqual((x,y),(max(a,b),min(a,b)))
                self.assertEqual((x,y),(g*u,g*v))
                count+=1
        self.assertEqual(count,4096)

    def test_first_exact(self):
        rows=trace(21,7)
        self.assertEqual(rows,(Step(21,7,3,0),))
        self.assertEqual(greatest_measure(21,7,True),7)
        self.assertEqual(greatest_measure(9,9,True),9)

    def test_ancient_and_modern_domains(self):
        for a,b,expected in ((35,22,1),(1,9,1),(1,1,1)):
            self.assertEqual(greatest_measure(a,b),expected)
            with self.assertRaises(ValueError):
                greatest_measure(a,b,True)

    def test_invalid_inputs(self):
        for args in ((0,7),(3,-1),(True,2),(4,2.0)):
            with self.assertRaises(ValueError):
                trace(*args)


if __name__=='__main__':
    unittest.main()
