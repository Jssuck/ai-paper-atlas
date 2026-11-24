from itertools import product
import unittest

from named_part import Part, extract


def blocks(a, b):
    groups = [tuple(range(i,min(i+b,a))) for i in range(0,a,b)]
    if not groups or len(groups[-1]) != b:
        return None
    return len(groups)


class TestPart(unittest.TestCase):
    def test_transpose(self):
        self.assertEqual(extract(12,3),Part(3,4,3))
        self.assertEqual(extract(12,4),Part(4,3,4))

    def test_grid(self):
        admitted = 0
        for a,b in product(range(2,31),repeat=2):
            c = blocks(a,b)
            if c is None or c == 1:
                with self.assertRaises(ValueError):
                    extract(a,b)
            else:
                t = extract(a,b)
                self.assertEqual(t,Part(b,c,blocks(a,c)))
                self.assertEqual(t.reversed_count,b)
                admitted += 1
        print(f"Exact grid: 841 ordered pairs; {admitted} admitted, {841-admitted} rejected")

    def test_not_exact(self):
        self.assertEqual(divmod(14,3),(4,2))
        with self.assertRaises(ValueError):
            extract(14,3)

    def test_units(self):
        for a,b in ((12,12),(12,1),(1,1)):
            with self.assertRaises(ValueError):
                extract(a,b)
            self.assertEqual(extract(a,b,modern=True),Part(b,a//b,b))

    def test_invalid(self):
        for a,b in ((0,3),(12,0),(-12,3),(12,3.0),(12,True),(3,12)):
            with self.subTest(a=a,b=b),self.assertRaises(ValueError):
                extract(a,b,modern=True)
