import unittest
from model import Atom, And, Not, Model, chain_certificate

A = Atom('A', 'quality', 'whole')
B = Atom('B', 'quality', 'whole')
C = Atom('C', 'quality', 'whole')
T = Atom('B', 'quality', 'teeth')


class Tests(unittest.TestCase):
    def test_chain_shape(self):
        self.assertTrue(chain_certificate((C, B), (B, A), (C, A)))

    def test_cross_aspect_rejected(self):
        self.assertFalse(chain_certificate((C, T), (B, A), (C, A)))

    def test_category_not_erased(self):
        b2 = Atom('B', 'relation', 'whole')
        self.assertFalse(chain_certificate((C, b2), (B, A), (C, A)))

    def test_wrong_conclusion(self):
        self.assertFalse(chain_certificate((C, B), (B, A), (A, C)))

    def test_shape_not_truth(self):
        m = Model({0}, {A: set(), B: {0}, C: {0}})
        self.assertTrue(chain_certificate((C, B), (B, A), (C, A)))
        self.assertFalse(m.includes(B, A))

    def test_refused_can_be_true(self):
        m = Model({0}, {A: {0}, B: {0}, C: {0}, T: {0}})
        self.assertFalse(chain_certificate((C, T), (B, A), (C, A)))
        self.assertTrue(m.includes(C, A))

    def test_conjunction(self):
        m = Model({0, 1}, {A: {0}, B: {0, 1}})
        self.assertEqual(m.extension(And(A, B)), frozenset({0}))

    def test_negation_scope(self):
        m = Model({0}, {A: {0}, B: set()})
        self.assertEqual(m.extension(Not(And(A, B))), frozenset({0}))
        self.assertEqual(m.extension(And(Not(A), Not(B))), frozenset())

    def test_witness_not_mergeable(self):
        m = Model({0, 1}, {A: {0}, B: {1}})
        self.assertTrue(m.some(A) and m.some(B))
        self.assertFalse(m.some(And(A, B)))

    def test_empty_domain(self):
        m = Model(set(), {A: set(), B: set()})
        self.assertTrue(m.includes(A, B))
        self.assertFalse(m.some(A))

    def test_missing_is_not_false(self):
        with self.assertRaises(KeyError):
            Model({0}, {A: {0}}).extension(Not(B))

    def test_unknown_expression(self):
        with self.assertRaises(TypeError):
            Model({0}, {}).extension('white animal')

    def test_invalid_labels(self):
        for args in [('', 'x', 'x'), ('x', None, 'x'), ('x', 'x', ' '), (1, 'x', 'x')]:
            with self.assertRaises(ValueError):
                Atom(*args)

    def test_out_of_domain(self):
        with self.assertRaises(ValueError):
            Model({0}, {A: {1}})

    def test_invalid_key(self):
        with self.assertRaises(TypeError):
            Model({0}, {'A': {0}})

    def test_invalid_certificate(self):
        for invalid in [(A,), [A, B], ('A', B), None]:
            with self.assertRaises(TypeError):
                chain_certificate(invalid, (B, A), (C, A))

    def test_label_identity(self):
        self.assertNotEqual(Atom('A', 'quality', 'whole'), Atom('a', 'quality', 'whole'))

    def test_input_copy(self):
        values = {0}
        m = Model({0, 1}, {A: values})
        values.add(1)
        self.assertEqual(m.extension(A), frozenset({0}))


if __name__ == '__main__':
    unittest.main(verbosity=2)
