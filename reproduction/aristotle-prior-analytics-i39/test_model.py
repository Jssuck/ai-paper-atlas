import unittest
from model import Atom, Ref, And, Not, Definitions, Model


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.p, self.q = Atom('P'), Atom('Q')
        self.defs = Definitions({'both': And(self.p, self.q), 'also': Ref('both')})
        self.model = Model([0, 1], {'P': [0, 1], 'Q': [1]})

    def test_alias_chain(self):
        self.assertEqual(self.defs.expand(Ref('also')), And(self.p, self.q))
        self.assertEqual(self.model.extension(Ref('also'), self.defs), frozenset({1}))

    def test_definition_certificate(self):
        self.assertTrue(self.defs.equivalent_by_definition(Ref('both'), And(self.p, self.q)))
        self.assertFalse(self.defs.equivalent_by_definition(self.p, self.q))

    def test_incomplete_certificate(self):
        self.assertFalse(self.defs.equivalent_by_definition(And(self.p, self.q), And(self.q, self.p)))
        self.assertEqual(self.model.extension(And(self.p, self.q), self.defs), self.model.extension(And(self.q, self.p), self.defs))

    def test_complement(self):
        self.assertEqual(self.model.extension(Not(self.q), self.defs), frozenset({0}))

    def test_aeio(self):
        self.assertEqual([self.model.proposition(k, self.p, self.q, self.defs) for k in 'AEIO'], [False, False, True, True])

    def test_empty_domain(self):
        m = Model([], {'P': [], 'Q': []})
        self.assertEqual([m.proposition(k, self.p, self.q, self.defs) for k in 'AEIO'], [True, True, False, False])

    def test_missing_atom_not_false(self):
        with self.assertRaises(KeyError):
            Model([], {'P': []}).extension(And(self.p, Atom('absent')), self.defs)

    def test_undefined_reference(self):
        with self.assertRaises(KeyError):
            Definitions({'unused': Ref('absent')})

    def test_cycles(self):
        for d in ({'x': Ref('x')}, {'x': Ref('y'), 'y': Not(Ref('x'))}):
            with self.assertRaises(ValueError):
                Definitions(d)

    def test_bad_term_and_name(self):
        with self.assertRaises(TypeError):
            Definitions({'x': And(self.p, 'Q')})
        with self.assertRaises(ValueError):
            Atom(' ')

    def test_bad_domain_extensions(self):
        with self.assertRaises(TypeError):
            Model([True], {})
        with self.assertRaises(TypeError):
            Model([0, 1], {'P': [True]})
        with self.assertRaises(ValueError):
            Model([0], {'P': [1]})

    def test_generators_materialized_once(self):
        m = Model((x for x in range(2)), {'P': (x for x in range(2))})
        self.assertEqual(m.extension(self.p, Definitions({})), frozenset({0, 1}))

    def test_input_mutation_isolated(self):
        d = {'x': self.p}
        defs = Definitions(d)
        d['x'] = self.q
        ext = {'P': [0]}
        m = Model([0], ext)
        ext['P'].clear()
        self.assertEqual(defs.expand(Ref('x')), self.p)
        self.assertEqual(m.extension(self.p, defs), frozenset({0}))

    def test_invalid_query(self):
        with self.assertRaises(ValueError):
            self.model.proposition('X', self.p, self.q, self.defs)
        with self.assertRaises(KeyError):
            self.defs.expand(Ref('missing'))

    def test_explicit_checks_survive_optimization(self):
        from run_checks import check
        with self.assertRaises(RuntimeError):
            check(False, 'deliberate')


if __name__ == '__main__':
    unittest.main()
