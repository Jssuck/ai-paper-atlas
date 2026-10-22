"""Independent object-wise oracle; bounded checks do not prove the theorem."""
import itertools
import json
import sys
import unittest
from model import Atom, Ref, And, Not, Definitions, Model


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def holds(term, obj, atoms, definitions):
    """Interpret original syntax per object without calling expand/extension."""
    if isinstance(term, Atom):
        return obj in atoms[term.name]
    if isinstance(term, Ref):
        return holds(definitions[term.name], obj, atoms, definitions)
    if isinstance(term, And):
        return holds(term.left, obj, atoms, definitions) and holds(term.right, obj, atoms, definitions)
    if isinstance(term, Not):
        return not holds(term.child, obj, atoms, definitions)
    raise TypeError('invalid oracle syntax')


def oracle(kind, subject, predicate, domain, atoms, definitions):
    # Inputs here are preconstructed valid finite models, not a validator.
    pairs = [(holds(subject, x, atoms, definitions), holds(predicate, x, atoms, definitions)) for x in domain]
    if kind == 'A':
        return all(not s or p for s, p in pairs)
    if kind == 'E':
        return all(not (s and p) for s, p in pairs)
    if kind == 'I':
        return any(s and p for s, p in pairs)
    if kind == 'O':
        return any(s and not p for s, p in pairs)
    raise ValueError(kind)


class BoundaryTests(unittest.TestCase):
    def test_separate_namespaces(self):
        defs = Definitions({'x': Atom('P')})
        m = Model([0, 1], {'x': [0], 'P': [1]})
        self.assertEqual(m.extension(Atom('x'), defs), frozenset({0}))
        self.assertEqual(m.extension(Ref('x'), defs), frozenset({1}))
        self.assertFalse(defs.equivalent_by_definition(Atom('x'), Ref('x')))

    def test_unknown_atom_after_empty_subject(self):
        for kind in 'AEIO':
            with self.assertRaises(KeyError):
                Model([], {'P': []}).proposition(kind, Atom('P'), Atom('absent'), Definitions({}))

    def test_unknown_atom_after_empty_and(self):
        with self.assertRaises(KeyError):
            Model([], {'P': []}).extension(And(Atom('P'), Atom('absent')), Definitions({}))

    def test_all_refs_validated(self):
        for d in ({'unused': Ref('lost')}, {'a': Ref('b'), 'b': Ref('a')}, {'unused': And(Atom('P'), Ref('lost'))}):
            with self.assertRaises((ValueError, KeyError)):
                Definitions(d)

    def test_ref_unknown_at_query(self):
        with self.assertRaises(KeyError):
            Model([], {}).extension(Ref('lost'), Definitions({}))

    def test_atom_checked_at_query_not_definition(self):
        defs = Definitions({'unused': Atom('not_provided')})
        self.assertEqual(Model([], {'P': []}).extension(Atom('P'), defs), frozenset())
        with self.assertRaises(KeyError):
            Model([], {'P': []}).extension(Ref('unused'), defs)

    def test_boolean_rejected(self):
        for domain, ext in (([False], {}), ([0], {'P': [False]})):
            with self.assertRaises(TypeError):
                Model(domain, ext)

    def test_negative_ints_and_duplicates(self):
        m = Model([-1, -1, 0], {'P': [-1, -1]})
        self.assertEqual(m.extension(Not(Atom('P')), Definitions({})), frozenset({0}))

    def test_evidence_is_read_only_mapping(self):
        defs = Definitions({'x': Atom('P')})
        with self.assertRaises(TypeError):
            defs.definitions['x'] = Atom('Q')
        m = Model([0], {'P': [0]})
        with self.assertRaises(TypeError):
            m.extensions['P'] = frozenset()

    def test_invalid_ast_even_unused(self):
        for term in (Not(None), And(Atom('P'), 7)):
            with self.assertRaises(TypeError):
                Definitions({'x': term})

    def test_no_commutativity_certificate(self):
        p, q = Atom('P'), Atom('Q')
        self.assertFalse(Definitions({}).equivalent_by_definition(And(p, q), And(q, p)))

    def test_require_not_optimized_away(self):
        with self.assertRaises(RuntimeError):
            require(False, 'deliberate')


def run():
    p, q, r = Atom('P'), Atom('Q'), Atom('R')
    definitions = {'both': And(p, q), 'outside': Not(p), 'nested': And(Ref('both'), Not(r)), 'alias': Ref('nested')}
    defs = Definitions(definitions)
    terms = [p, q, r, Ref('both'), Ref('outside'), Ref('nested'), Ref('alias'), And(q, p), Not(And(Ref('both'), r))]
    models = ext_checks = truth_checks = 0
    for n in range(4):
        domain = tuple(range(n))
        subsets = [tuple(x for x in domain if bits & (1 << x)) for bits in range(1 << n)]
        for pv, qv, rv in itertools.product(subsets, repeat=3):
            atoms = {'P': pv, 'Q': qv, 'R': rv}
            m = Model(domain, atoms)
            models += 1
            for t in terms:
                expected = frozenset(x for x in domain if holds(t, x, atoms, definitions))
                require(m.extension(t, defs) == expected, 'independent extension mismatch')
                ext_checks += 1
            for s, t, kind in itertools.product(terms, terms, 'AEIO'):
                require(m.proposition(kind, s, t, defs) == oracle(kind, s, t, domain, atoms, definitions), 'independent truth mismatch')
                truth_checks += 1
    print(json.dumps({'models_domain_0_to_3': models, 'terms': len(terms), 'independent_extension_comparisons': ext_checks, 'independent_truth_comparisons': truth_checks, 'result': 'pass', 'scope': 'bounded object-wise oracle on valid finite input; not a general proof or natural-language equivalence check'}, indent=2))


if __name__ == '__main__':
    if '--tests' in sys.argv:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    else:
        run()
