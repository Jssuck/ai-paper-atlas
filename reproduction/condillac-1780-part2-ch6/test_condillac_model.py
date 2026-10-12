"""Unit and bounded exhaustive tests. Run via unittest, also under -O/-OO."""
import itertools
import unittest

import condillac_model as m


def dnf(names, bits):
    """Independent table-to-syntax helper; table uses False-before-True row order."""
    result = m.Const(False)
    for values, output in zip(itertools.product((False, True), repeat=len(names)), bits):
        if output:
            term = m.Const(True)
            for name, value in zip(names, values):
                term = m.And(term, m.Var(name) if value else m.Not(m.Var(name)))
            result = m.Or(result, term)
    return result


def tables(n):
    return tuple(itertools.product((False, True), repeat=2**n))


class ExpressionTests(unittest.TestCase):
    def test_truth_tables(self):
        for p, q in itertools.product((False, True), repeat=2):
            world = {"p": p, "q": q}
            cases = ((m.Const(True), True), (m.Var("p"), p),
                     (m.Not(m.Var("p")), not p),
                     (m.And(m.Var("p"), m.Var("q")), p and q),
                     (m.Or(m.Var("p"), m.Var("q")), p or q),
                     (m.Not(m.And(m.Var("p"), m.Not(m.Var("q")))), (not p) or q))
            for expr, expected in cases:
                self.assertEqual(m.evaluate(expr, world), expected)

    def test_empty_world_enumeration(self):
        self.assertEqual(m.enumerate_worlds(()), ({},))

    def test_world_order_and_count(self):
        worlds = m.enumerate_worlds(("q", "p"))
        self.assertEqual(len(worlds), 4)
        self.assertEqual(worlds[0], {"q": False, "p": False})
        self.assertEqual(worlds[-1], {"q": True, "p": True})

    def test_duplicate_and_empty_names(self):
        for names in (("p", "p"), ("",)):
            with self.assertRaises(ValueError):
                m.enumerate_worlds(names)
        with self.assertRaises(ValueError):
            m.Var("")

    def test_strict_booleans(self):
        for invalid in (0, 1, "true", None):
            with self.assertRaises(TypeError):
                m.Const(invalid)
            with self.assertRaises(TypeError):
                m.evaluate(m.Var("p"), {"p": invalid})

    def test_validate_short_circuited_branches(self):
        with self.assertRaises(ValueError):
            m.evaluate(m.And(m.Const(False), m.Var("missing")), {})
        with self.assertRaises(ValueError):
            m.evaluate(m.Or(m.Const(True), m.Var("missing")), {})

    def test_unsupported_ast(self):
        with self.assertRaises(TypeError):
            m.variables(m.Expr())
        with self.assertRaises(TypeError):
            m.Not(True)

    def test_all_small_dnf_tables(self):
        count = 0
        for n in range(3):
            names = tuple(f"p{i}" for i in range(n))
            for truth_table in tables(n):
                expr = dnf(names, truth_table)
                self.assertEqual(tuple(m.evaluate(expr, w) for w in m.enumerate_worlds(names)), truth_table)
                count += 1
        self.assertEqual(count, 22)


class DefinitionTests(unittest.TestCase):
    def test_reorders_dependencies(self):
        system = m.DefinitionSystem(("p", "q"), (
            m.Definition("d2", m.Not(m.Var("d1"))),
            m.Definition("d1", m.And(m.Var("p"), m.Var("q"))),
        ))
        self.assertEqual(tuple(d.name for d in system.topological_definitions()), ("d1", "d2"))
        self.assertEqual(system.expand({"p": True, "q": False}),
                         {"p": True, "q": False, "d1": False, "d2": True})

    def test_expand_does_not_mutate_input(self):
        base = {"p": True}
        system = m.DefinitionSystem(("p",), (m.Definition("d", m.Var("p")),))
        expanded = system.expand(base)
        self.assertEqual(base, {"p": True})
        expanded["p"] = False
        self.assertEqual(base, {"p": True})

    def test_no_definitions(self):
        self.assertEqual(m.DefinitionSystem((), ()).worlds(), ({},))
        self.assertEqual(m.satisfying_extensions({}, ()), ({},))

    def test_reject_nonfresh_duplicate_unknown_and_cycle(self):
        bad = (
            (m.Definition("p", m.Const(True)),),
            (m.Definition("d", m.Const(True)), m.Definition("d", m.Const(False))),
            (m.Definition("d", m.Var("missing")),),
            (m.Definition("d", m.Not(m.Var("d"))),),
            (m.Definition("d", m.Var("e")), m.Definition("e", m.Var("d"))),
        )
        for definitions in bad:
            with self.subTest(definitions=definitions):
                with self.assertRaises(ValueError):
                    m.DefinitionSystem(("p",), definitions)

    def test_exact_primitive_domain(self):
        system = m.DefinitionSystem(("p",), ())
        for world in ({}, {"p": True, "extra": False}):
            with self.assertRaises(ValueError):
                system.expand(world)

    def test_cyclic_no_solution(self):
        self.assertEqual(m.satisfying_extensions({}, (m.Definition("d", m.Not(m.Var("d"))),)), ())

    def test_cyclic_multiple_solutions(self):
        equations = (m.Definition("d", m.Var("e")), m.Definition("e", m.Var("d")))
        self.assertEqual(m.satisfying_extensions({}, equations),
                         ({"d": False, "e": False}, {"d": True, "e": True}))

    def test_cyclic_can_have_unique_solution(self):
        # A syntactic dependency cycle alone does not imply nonuniqueness.
        equations = (m.Definition("d", m.And(m.Var("d"), m.Const(False))),)
        self.assertEqual(m.satisfying_extensions({}, equations), ({"d": False},))

    def test_old_name_equation_constrains_base(self):
        equations = (m.Definition("p", m.Const(True)),)
        self.assertEqual(m.satisfying_extensions({"p": False}, equations), ())
        self.assertEqual(m.satisfying_extensions({"p": True}, equations), ({"p": True},))

    def test_equation_oracle_rejects_bad_inputs(self):
        with self.assertRaises(ValueError):
            m.satisfying_extensions({}, (m.Definition("d", m.Var("p")),))
        with self.assertRaises(ValueError):
            m.satisfying_extensions({}, (m.Definition("d", m.Const(True)), m.Definition("d", m.Const(True))))
        with self.assertRaises(TypeError):
            m.satisfying_extensions({}, ("not an equation",))

    def test_bounded_exhaustive_expansion_and_conservativity(self):
        systems = world_cases = 0
        for n in range(3):
            names = tuple(f"p{i}" for i in range(n))
            worlds = m.enumerate_worlds(names)
            old_formulas = tuple(dnf(names, truth_table) for truth_table in tables(n))
            for first_table in tables(n):
                for second_table in tables(1):
                    definitions = (m.Definition("d1", dnf(names, first_table)),
                                   m.Definition("d2", dnf(("d1",), second_table)))
                    for input_order in (definitions, tuple(reversed(definitions))):
                        system = m.DefinitionSystem(names, input_order)
                        systems += 1
                        for index, world in enumerate(worlds):
                            expansion = system.expand(world)
                            self.assertEqual(m.satisfying_extensions(world, input_order), (expansion,))
                            self.assertEqual({name: expansion[name] for name in names}, world)
                            self.assertEqual(expansion["d1"], first_table[index])
                            self.assertEqual(expansion["d2"], second_table[int(first_table[index])])
                            for old_formula in old_formulas:
                                self.assertEqual(m.evaluate(old_formula, expansion), m.evaluate(old_formula, world))
                            world_cases += 1
        self.assertEqual(systems, 176)
        self.assertEqual(world_cases, 592)


class EvidenceAndObservationTests(unittest.TestCase):
    def test_evidence_is_separate(self):
        system = m.DefinitionSystem(("p", "q"), (m.Definition("d", m.And(m.Var("p"), m.Var("q"))),))
        worlds = system.worlds()
        self.assertEqual(len(worlds), 4)
        self.assertFalse(m.entails(worlds, m.Var("p")))
        retained = m.filter_evidence(worlds, m.Var("d"))
        self.assertEqual(len(retained), 1)
        self.assertTrue(m.entails(retained, m.Var("p")))
        self.assertEqual(len(worlds), 4)

    def test_empty_evidence_is_vacuous_not_information(self):
        retained = m.filter_evidence(m.enumerate_worlds(("p",)), m.And(m.Var("p"), m.Not(m.Var("p"))))
        self.assertEqual(retained, ())
        self.assertTrue(m.entails(retained, m.Var("p")))
        self.assertTrue(m.entails(retained, m.Not(m.Var("p"))))

    def test_hidden_primitive_witness(self):
        result = m.analyze_observations(m.enumerate_worlds(("p", "q")), (m.Var("p"),), m.Var("q"))
        self.assertFalse(result.definable)
        self.assertEqual(result.witness, ({"p": False, "q": False}, {"p": False, "q": True}))
        self.assertEqual(result.table, ())

    def test_no_features_constant_target(self):
        result = m.analyze_observations(m.enumerate_worlds(("p",)), (), m.Const(True))
        self.assertTrue(result.definable)
        self.assertEqual(result.table, (((), True),))
        self.assertTrue(m.evaluate(m.observed_formula(result, ()), {}))

    def test_no_features_nonconstant_target(self):
        self.assertFalse(m.analyze_observations(m.enumerate_worlds(("p",)), (), m.Var("p")).definable)

    def test_empty_domain(self):
        result = m.analyze_observations((), (m.Var("p"),), m.Var("q"))
        self.assertTrue(result.definable)
        self.assertEqual(result.table, ())
        self.assertFalse(m.evaluate(m.observed_formula(result, ("f",)), {"f": True}))

    def test_partial_domain_and_unseen_signature(self):
        worlds = ({"p": True, "q": True},)
        result = m.analyze_observations(worlds, (m.Var("p"),), m.Var("q"))
        self.assertEqual(result.table, (((True,), True),))
        formula = m.observed_formula(result, ("f",))
        self.assertTrue(m.evaluate(formula, {"f": True}))
        self.assertFalse(m.evaluate(formula, {"f": False}))
        # The False above is a completion convention, not an empirical prediction.

    def test_duplicate_worlds_and_features(self):
        worlds = ({"p": True}, {"p": True}, {"p": False})
        result = m.analyze_observations(worlds, (m.Var("p"), m.Var("p")), m.Var("p"))
        self.assertEqual(result.table, (((False, False), False), ((True, True), True)))

    def test_inconsistent_vocabulary_and_unbound_names(self):
        with self.assertRaises(ValueError):
            m.analyze_observations(({"p": True}, {"q": False}), (), m.Const(True))
        with self.assertRaises(ValueError):
            m.analyze_observations(({"p": True},), (m.Var("missing"),), m.Var("p"))
        with self.assertRaises(ValueError):
            m.filter_evidence(({"p": True}, {}), m.Const(True))

    def test_invalid_observation_formula(self):
        failure = m.analyze_observations(m.enumerate_worlds(("p",)), (), m.Var("p"))
        with self.assertRaises(ValueError):
            m.observed_formula(failure, ())
        success = m.analyze_observations(m.enumerate_worlds(("p",)), (m.Var("p"),), m.Var("p"))
        with self.assertRaises(ValueError):
            m.observed_formula(success, ())
        malformed = m.ObservationAnalysis(True, (((True,), 1),), None)
        with self.assertRaises(ValueError):
            m.observed_formula(malformed, ("f",))
        duplicated = m.ObservationAnalysis(True, (((True,), True), ((True,), False)), None)
        with self.assertRaises(ValueError):
            m.observed_formula(duplicated, ("f",))

    def test_observation_formula_requires_typed_result(self):
        for invalid in (None, True, m.ObservationAnalysis(1, (), None)):
            with self.assertRaises(TypeError):
                m.observed_formula(invalid, ())

    def test_bounded_exhaustive_fiber_criterion(self):
        cases = 0
        for n in range(3):
            names = tuple(f"p{i}" for i in range(n))
            worlds = m.enumerate_worlds(names)
            all_tables = tables(n)
            syntax = {table: dnf(names, table) for table in all_tables}
            for number_features in range(3):
                for feature_tables in itertools.product(all_tables, repeat=number_features):
                    signatures = tuple(tuple(table[i] for table in feature_tables) for i in range(len(worlds)))
                    for target_table in all_tables:
                        # Independent finite oracle: enumerate all possible Boolean maps on the observed signatures.
                        distinct = tuple(sorted(set(signatures)))
                        possible = any(
                            all(dict(zip(distinct, outputs))[signature] == target_table[i]
                                for i, signature in enumerate(signatures))
                            for outputs in itertools.product((False, True), repeat=len(distinct))
                        )
                        result = m.analyze_observations(worlds, tuple(syntax[t] for t in feature_tables), syntax[target_table])
                        self.assertEqual(result.definable, possible)
                        if possible:
                            feature_names = tuple(f"f{i}" for i in range(number_features))
                            formula = m.observed_formula(result, feature_names)
                            for i, signature in enumerate(signatures):
                                self.assertEqual(m.evaluate(formula, dict(zip(feature_names, signature))), target_table[i])
                        else:
                            self.assertIsNotNone(result.witness)
                            first, second = result.witness
                            self.assertEqual(tuple(m.evaluate(syntax[t], first) for t in feature_tables),
                                             tuple(m.evaluate(syntax[t], second) for t in feature_tables))
                            self.assertNotEqual(m.evaluate(syntax[target_table], first), m.evaluate(syntax[target_table], second))
                        cases += 1
        self.assertEqual(cases, 4466)


class LearningTests(unittest.TestCase):
    def setUp(self):
        self.rules = (m.Rule(frozenset(("sense",)), "compare"),
                      m.Rule(frozenset(("compare",)), "name"))

    def test_chain_and_reverse(self):
        plan = m.plan_learning(("sense",), self.rules)
        self.assertEqual(plan, ("compare", "name"))
        self.assertTrue(m.verify_order(("sense",), self.rules, plan).valid)
        report = m.verify_order(("sense",), self.rules, reversed(plan))
        self.assertFalse(report.valid)
        self.assertEqual(report.failure_index, 0)
        self.assertEqual(report.missing_alternatives, (frozenset(("compare",)),))

    def test_all_premises_required(self):
        rules = (m.Rule(frozenset(("a", "b")), "c"),)
        self.assertEqual(m.forward_closure(("a",), rules), frozenset(("a",)))
        self.assertFalse(m.verify_order(("a",), rules, ("c",)).valid)
        self.assertTrue(m.verify_order(("a", "b"), rules, ("c",)).valid)

    def test_alternative_rules(self):
        rules = (m.Rule(frozenset(("a", "b")), "c"), m.Rule(frozenset(("x",)), "c"))
        self.assertTrue(m.verify_order(("x",), rules, ("c",)).valid)

    def test_empty_premises_and_no_rules(self):
        self.assertEqual(m.plan_learning((), (m.Rule(frozenset(), "a"),)), ("a",))
        self.assertEqual(m.forward_closure(("a",), ()), frozenset(("a",)))

    def test_cycle_unseeded_seeded_and_self_loop(self):
        cycle = (m.Rule(frozenset(("a",)), "b"), m.Rule(frozenset(("b",)), "a"))
        self.assertEqual(m.forward_closure((), cycle), frozenset())
        self.assertEqual(m.plan_learning(("a",), cycle), ("b",))
        self.assertEqual(m.forward_closure(("a",), cycle), frozenset(("a", "b")))
        self.assertEqual(m.plan_learning((), (m.Rule(frozenset(("a",)), "a"),)), ())

    def test_not_every_reverse_fails(self):
        independent = (m.Rule(frozenset(("a",)), "b"), m.Rule(frozenset(("a",)), "c"))
        plan = m.plan_learning(("a",), independent)
        self.assertTrue(m.verify_order(("a",), independent, reversed(plan)).valid)

    def test_valid_does_not_mean_complete(self):
        report = m.verify_order(("sense",), self.rules, ("compare",))
        self.assertTrue(report.valid)
        self.assertNotEqual(report.known, m.forward_closure(("sense",), self.rules))

    def test_repeated_known_or_unlicensed_step(self):
        self.assertEqual(m.verify_order(("sense",), self.rules, ("sense",)).reason, "already known")
        self.assertFalse(m.verify_order(("sense",), self.rules, ("compare", "compare")).valid)
        report = m.verify_order((), (), ("unknown",))
        self.assertFalse(report.valid)
        self.assertEqual(report.missing_alternatives, ())

    def test_malformed_rules(self):
        with self.assertRaises(ValueError):
            m.Rule(frozenset(("",)), "a")
        with self.assertRaises(ValueError):
            m.Rule(frozenset(), "")
        with self.assertRaises(TypeError):
            m.forward_closure((), ("invalid",))

    def test_derivability_is_not_truth(self):
        rules = (m.Rule(frozenset(("p",)), "q"),)
        self.assertIn("q", m.forward_closure(("p",), rules))
        self.assertFalse(m.evaluate(m.Var("q"), {"p": True, "q": False}))

    def test_bounded_exhaustive_closure_and_plans(self):
        # All 256 rule sets on two names, with every premise subset and conclusion.
        names = ("a", "b")
        subsets = tuple(frozenset(name for name, bit in zip(names, bits) if bit)
                        for bits in itertools.product((False, True), repeat=2))
        possible_rules = tuple(m.Rule(premises, conclusion) for premises in subsets for conclusion in names)
        cases = order_cases = 0
        for rule_bits in itertools.product((False, True), repeat=len(possible_rules)):
            rules = tuple(rule for rule, bit in zip(possible_rules, rule_bits) if bit)
            for seeds in subsets:
                # Independent oracle: intersection of every closed superset of seeds.
                closed_sets = tuple(s for s in subsets if seeds <= s and
                                    all(not r.premises <= s or r.conclusion in s for r in rules))
                oracle = frozenset.intersection(*closed_sets)
                closure = m.forward_closure(seeds, rules)
                self.assertEqual(closure, oracle)
                plan = m.plan_learning(seeds, rules)
                report = m.verify_order(seeds, rules, plan)
                self.assertTrue(report.valid)
                self.assertEqual(report.known, closure)
                for length in range(3):
                    for order in itertools.permutations(names, length):
                        prior = set(seeds)
                        expected = True
                        for conclusion in order:
                            enabled = any(r.conclusion == conclusion and all(p in prior for p in r.premises) for r in rules)
                            if conclusion in prior or not enabled:
                                expected = False
                                break
                            prior.add(conclusion)
                        self.assertEqual(m.verify_order(seeds, rules, order).valid, expected)
                        order_cases += 1
                cases += 1
        self.assertEqual(cases, 1024)
        self.assertEqual(order_cases, 5120)


if __name__ == "__main__":
    unittest.main()
