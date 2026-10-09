"""Deterministic stdlib tests; each exhaustive scope has an asserted exact count."""
import itertools
import unittest
from peirce_finite import *


class ClassLogicTests(unittest.TestCase):
    def test_categorical_all_subject_predicate_pairs_n0_to_3(self):
        count = 0
        for n in range(4):
            u = frozenset(range(n))
            for s, p in itertools.product(powerset(u), repeat=2):
                q = categorical(s, p)
                self.assertEqual(q['A'], all(x in p for x in s))
                self.assertEqual(q['E'], all(x not in p for x in s))
                self.assertEqual(q['I'], any(x in p for x in s))
                self.assertEqual(q['O'], any(x not in p for x in s))
                self.assertEqual(q['A'], not q['O'])
                self.assertEqual(q['E'], not q['I'])
                if not s:
                    self.assertEqual(q, dict(A=True, E=True, I=False, O=False))
                count += 1
        self.assertEqual(count, 85)

    def test_boolean_laws_all_class_triples_n0_to_3(self):
        count = 0
        for n in range(4):
            u = frozenset(range(n))
            for a, b, c in itertools.product(powerset(u), repeat=3):
                self.assertEqual(a & (b | c), (a & b) | (a & c))
                self.assertEqual(a | (b & c), (a | b) & (a | c))
                self.assertEqual(u - (a | b), (u - a) & (u - b))
                self.assertEqual(u - (a & b), (u - a) | (u - b))
                self.assertEqual(a | (a & b), a)
                self.assertEqual(a & (a | b), a)
                count += 1
        self.assertEqual(count, 585)

    def test_expansion_all_256_ternary_boolean_functions(self):
        names = ('x', 'y', 'z')
        envs = list(assignments(names))
        checks = 0
        for table in itertools.product((False, True), repeat=8):
            def f(e):
                index = 4 * int(e['x']) + 2 * int(e['y']) + int(e['z'])
                return table[index]
            canonical = cnf_from_truth_function(names, f)
            for env in envs:
                self.assertEqual(eval_cnf(canonical, env), f(env))
                for variable in names:
                    self.assertEqual(shannon(f, variable, env), f(env))
                    checks += 1
        self.assertEqual(checks, 6144)

    def test_p39_elimination_rule_all_five_class_assignments_n0_to_2(self):
        count = 0
        for n in range(3):
            u = frozenset(range(n))
            for a, b, c, d, x in itertools.product(powerset(u), repeat=5):
                if a <= b | x and c <= d | (u - x):
                    self.assertTrue(a & c <= b | d)
                count += 1
        self.assertEqual(count, 1057)

    def test_m3_is_a_lattice_but_not_distributive(self):
        elements = ('0', 'a', 'b', 'c', '1')
        leq = lambda a, b: m3_meet(a, b) == a
        for a, b in itertools.product(elements, repeat=2):
            meet, join = m3_meet(a, b), m3_join(a, b)
            self.assertTrue(leq(meet, a) and leq(meet, b))
            self.assertTrue(leq(a, join) and leq(b, join))
            for x in elements:
                if leq(x, a) and leq(x, b):
                    self.assertTrue(leq(x, meet))
                if leq(a, x) and leq(b, x):
                    self.assertTrue(leq(join, x))
        self.assertEqual(m3_meet('a', m3_join('b', 'c')), 'a')
        self.assertEqual(m3_join(m3_meet('a', 'b'), m3_meet('a', 'c')), '0')


class EliminationTests(unittest.TestCase):
    @staticmethod
    def canonical_clauses(names):
        # Each variable absent, positive or negative; includes empty clause.
        return tuple(frozenset((v, s == 1) for v, s in zip(names, row) if s)
                     for row in itertools.product((0, 1, -1), repeat=len(names)))

    def assert_projection(self, formula, names):
        count = 0
        for variable in names:
            projected, trace = eliminate(formula, variable)
            self.assertTrue(all(variable != v for c in projected for v, _ in c))
            remaining = tuple(v for v in names if v != variable)
            for env in assignments(remaining):
                expected = any(eval_cnf(formula, dict(env, **{variable: b}))
                               for b in (False, True))
                self.assertEqual(eval_cnf(projected, env), expected,
                                 (formula, variable, env, projected, trace))
                count += 1
        return count

    def test_all_512_cnf_subsets_of_two_variable_canonical_clauses(self):
        names = ('x', 'y')
        clauses = self.canonical_clauses(names)
        self.assertEqual(len(clauses), 9)
        checks, formulas = 0, 0
        for f in powerset(clauses):
            checks += self.assert_projection(f, names)
            formulas += 1
        self.assertEqual((formulas, checks), (512, 2048))

    def test_all_729_ordered_clause_pairs_on_three_variables(self):
        names = ('x', 'y', 'z')
        clauses = self.canonical_clauses(names)
        self.assertEqual(len(clauses), 27)
        checks, pairs = 0, 0
        for c, d in itertools.product(clauses, repeat=2):
            checks += self.assert_projection(frozenset((c, d)), names)
            pairs += 1
        self.assertEqual((pairs, checks), (729, 8748))

    def test_tautology_empty_formula_empty_clause_and_chain(self):
        self.assertEqual(normalize([clause('x', '~x')]), frozenset())
        self.assertTrue(eval_cnf(frozenset(), {}))
        self.assertFalse(eval_cnf(frozenset((clause(),)), {}))
        f = normalize([clause('~a', 'x'), clause('~x', 'b')])
        projected, trace = eliminate(f, 'x')
        self.assertEqual(projected, normalize([clause('~a', 'b')]))
        self.assertEqual(len(trace), 1)
        self.assert_projection(normalize([clause('x')]), ('x',))
        self.assert_projection(normalize([clause('~x')]), ('x',))

    def test_source_boole_p39_to_p41_and_p42_discrepancy(self):
        names = ('v', 'x', 'y', 'z', 'w')
        f = cnf_from_truth_function(names, boole_original)
        eliminated, _ = eliminate(f, 'v')
        six = boole_six_clauses()
        rows, projected_count, summary_count, mismatches = 0, 0, 0, []
        for env in assignments(('x', 'y', 'z', 'w')):
            expected = any(boole_original(dict(env, v=v)) for v in (False, True))
            self.assertEqual(eval_cnf(eliminated, env), expected)
            self.assertEqual(eval_cnf(six, env), expected)
            self.assertEqual(boole_exact_solution(env), expected)
            printed = boole_printed_summary(env)
            self.assertTrue(not expected or printed)
            projected_count += expected
            summary_count += printed
            if expected != printed:
                mismatches.append(tuple(int(env[v]) for v in ('x', 'y', 'z', 'w')))
            rows += 1
        self.assertEqual((rows, projected_count, summary_count), (16, 8, 11))
        self.assertEqual(mismatches, [(1, 0, 1, 1), (1, 1, 0, 0), (1, 1, 1, 1)])
        # No condition on y,z,w after also eliminating x, as stated on p41.
        eliminated_x, _ = eliminate(eliminated, 'x')
        self.assertTrue(all(eval_cnf(eliminated_x, e) for e in assignments(('y', 'z', 'w'))))


class RelationTests(unittest.TestCase):
    def test_all_four_operations_against_quantified_oracle_n0_to_2(self):
        count = 0
        for n in range(3):
            for r, s in itertools.product(all_relations(n), repeat=2):
                universe = tuple(range(n))
                oracle = {
                    'compose': frozenset((x, z) for x in universe for z in universe
                        if any((x, y) in r.pairs and (y, z) in s.pairs for y in universe)),
                    'regressive': frozenset((x, z) for x in universe for z in universe
                        if all((x, y) not in r.pairs or (y, z) in s.pairs for y in universe)),
                    'progressive': frozenset((x, z) for x in universe for z in universe
                        if all((y, z) not in s.pairs or (x, y) in r.pairs for y in universe)),
                    'transadd': frozenset((x, z) for x in universe for z in universe
                        if any((x, y) not in r.pairs and (y, z) not in s.pairs for y in universe))}
                for operation, expected in oracle.items():
                    self.assertEqual(getattr(r, operation)(s).pairs, expected)
                self.assertEqual(r.compose(s).converse(), s.converse().compose(r.converse()))
                self.assertEqual(r.regressive(s).converse(), s.converse().progressive(r.converse()))
                self.assertEqual(r.progressive(s).converse(), s.converse().regressive(r.converse()))
                self.assertEqual(r.transadd(s).converse(), s.converse().transadd(r.converse()))
                count += 1
        self.assertEqual(count, 261)

    def test_p55_eight_distribution_equalities_and_composition_association_n0_to_2(self):
        count = 0
        for n in range(3):
            for a, b, c in itertools.product(all_relations(n), repeat=3):
                self.assertEqual((a | b).compose(c), a.compose(c) | b.compose(c))
                self.assertEqual(a.compose(b | c), a.compose(b) | a.compose(c))
                self.assertEqual((a & b).progressive(c), a.progressive(c) & b.progressive(c))
                self.assertEqual(a.progressive(b | c), a.progressive(b) & a.progressive(c))
                self.assertEqual((a | b).regressive(c), a.regressive(c) & b.regressive(c))
                self.assertEqual(a.regressive(b & c), a.regressive(b) & a.regressive(c))
                self.assertEqual((a & b).transadd(c), a.transadd(c) | b.transadd(c))
                self.assertEqual(a.transadd(b & c), a.transadd(b) | a.transadd(c))
                self.assertEqual(a.compose(b).compose(c), a.compose(b.compose(c)))
                count += 1
        self.assertEqual(count, 4105)

    def test_four_variance_rules_all_nested_relation_pairs_n0_to_2(self):
        count = 0
        for n in range(3):
            relations = tuple(all_relations(n))
            nested = tuple((a, b) for a in relations for b in relations if a <= b)
            for (a, b), (c, d) in itertools.product(nested, repeat=2):
                self.assertTrue(a.compose(c) <= b.compose(d))
                self.assertTrue(b.regressive(c) <= a.regressive(d))
                self.assertTrue(a.progressive(d) <= b.progressive(c))
                self.assertTrue(b.transadd(d) <= a.transadd(c))
                count += 1
        self.assertEqual(count, 6571)

    def test_corrected_classification_and_identity_all_relations_n0_to_3(self):
        count = 0
        for n in range(4):
            for r in all_relations(n):
                flags, neg = r.classify(), (~r).classify()
                self.assertEqual(flags['concurrent'], not flags['opponent'])
                self.assertEqual(flags['alio_relative'], not flags['self_relative'])
                for name in ('concurrent', 'opponent', 'self_relative', 'alio_relative'):
                    self.assertEqual(flags['negative_of_' + name], neg[name])
                self.assertEqual(r.converse().converse(), r)
                self.assertEqual(~(~r), r)
                self.assertEqual(r.compose(Relation.identity(n)), r)
                self.assertEqual(Relation.identity(n).compose(r), r)
                count += 1
            zero, top = Relation.zero(n).classify(), Relation.top(n).classify()
            self.assertTrue(zero['concurrent'] and zero['alio_relative'])
            self.assertTrue(top['negative_of_concurrent'] and top['negative_of_alio_relative'])
        self.assertEqual(count, 531)

    def test_counterexamples_are_actual_counterexamples(self):
        # Different intermediate witnesses make the right-hand side larger.
        r = Relation(3, frozenset(((0, 0), (0, 1))))
        s = Relation(3, frozenset(((0, 2),)))
        t = Relation(3, frozenset(((1, 2),)))
        self.assertNotEqual(r.compose(s & t), r.compose(s) & r.compose(t))
        self.assertEqual(r.compose(s & t).pairs, frozenset())
        self.assertEqual((r.compose(s) & r.compose(t)).pairs, frozenset(((0, 2),)))
        # forall x exists y is not exists y forall x.
        diagonal = Relation.identity(2)
        self.assertTrue(all(any((x, y) in diagonal.pairs for y in range(2)) for x in range(2)))
        self.assertFalse(any(all((x, y) in diagonal.pairs for x in range(2)) for y in range(2)))
        # Do not transplant ordinary associativity to arbitrary mixtures.
        a = Relation.top(2)
        b = Relation.identity(2)
        c = Relation.top(2)
        self.assertEqual(a.regressive(b).compose(c), Relation.zero(2))
        self.assertEqual(a.regressive(b.compose(c)), Relation.top(2))

    def test_input_validation(self):
        for n in (-1, 0.5, True):
            with self.assertRaises(ValueError):
                Relation(n, frozenset())
        with self.assertRaises(ValueError):
            Relation(2, frozenset(((2, 0),)))
        with self.assertRaises(ValueError):
            Relation(2, frozenset(((True, 0),)))
        for method in ('compose', 'regressive', 'progressive', 'transadd', '__or__', '__and__', '__le__'):
            with self.assertRaises(ValueError):
                getattr(Relation.zero(1), method)(Relation.zero(2))


class EqualityPatternTests(unittest.TestCase):
    def test_p48_counts_and_independent_stirling_recurrence(self):
        expected = (1, 1, 2, 5, 15, 52, 203, 877)
        self.assertEqual(bell_numbers(7), expected)
        self.assertEqual(tuple(len(equality_patterns(n)) for n in range(8)), expected)
        self.assertEqual(set(equality_patterns(3)),
                         {(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (0, 1, 2)})

    def test_patterns_from_all_tuples_n0_to_4_arity0_to_5(self):
        count = 0
        for n in range(5):
            for arity in range(6):
                actual = set()
                for row in itertools.product(range(n), repeat=arity):
                    actual.add(equality_pattern(row))
                    count += 1
                expected = {p for p in equality_patterns(arity) if max(p, default=-1) < n}
                self.assertEqual(actual, expected)
        self.assertEqual(count, 1799)


if __name__ == '__main__':
    unittest.main(verbosity=2)
