"""Behavioral, algebraic, negative and independent semantic tests."""
import ast
import inspect
import itertools
import random
import unittest
import model
from model import (Catalog, Observation, Concept, Rule, Theory, Step, attend,
                   compare, reflect, equivalence_classes, imagine, closure,
                   verify_certificate, semantic_oracle, subset_syllogism)


def catalog():
    return Catalog(("color", "shape", "material"),
                   (("red", "blue"), ("round", "square"), ("wood", "metal")),
                   (("a", ("red", "round", "wood")),
                    ("b", ("red", "round", "metal")),
                    ("c", ("blue", "square", "wood"))))


def atoms_of(steps):
    return {step.atom for step in steps}


class ObservationTests(unittest.TestCase):
    def setUp(self):
        self.c = catalog()
        self.a = attend(self.c, "a", ("color", "shape"))
        self.b = attend(self.c, "b", ("color", "shape"), "recalled")
        self.c_obs = attend(self.c, "c", ("color",))

    def test_projection_and_recalled_provenance(self):
        self.assertEqual(self.a.attributes, (("color", "red"), ("shape", "round")))
        self.assertEqual(self.b.provenance, "recalled")
        self.assertEqual(compare(self.c, self.a, self.b, "color"), "equal")
        self.assertEqual(attend(self.c, "a", ()).attributes, ())

    def test_unknown_is_not_equality_or_difference(self):
        self.assertEqual(compare(self.c, self.a, self.b, "material"), "unknown")
        self.assertEqual(compare(self.c, self.a, self.c_obs, "shape"), "unknown")
        self.assertEqual(compare(self.c, self.a, self.c_obs, "color"), "different")
        self.assertEqual(compare(self.c, self.c_obs, self.a, "color"), "different")

    def test_reflection_and_hidden_feature(self):
        self.assertEqual(reflect(self.c, self.a, self.b, ("color", "material")),
                         (("color", "equal"), ("material", "unknown")))
        self.assertEqual(equivalence_classes(self.c, ("color", "shape")), (("a", "b"), ("c",)))
        self.assertEqual(equivalence_classes(self.c, self.c.features), (("a",), ("b",), ("c",)))
        full_a = attend(self.c, "a", self.c.features)
        full_b = attend(self.c, "b", self.c.features, "recalled")
        self.assertEqual(compare(self.c, full_a, full_b, "material"), "different")
        self.assertEqual(reflect(self.c, self.a, self.b, ()), ())

    def test_all_feature_subsets_are_equivalence_relations_and_refine(self):
        names = tuple(name for name, _ in self.c.objects)
        partitions = {}
        for bits in itertools.product((False, True), repeat=len(self.c.features)):
            selected = tuple(f for f, bit in zip(self.c.features, bits) if bit)
            groups = equivalence_classes(self.c, selected)
            relation = {(a, b) for group in groups for a in group for b in group}
            partitions[frozenset(selected)] = relation
            self.assertEqual(set(itertools.chain.from_iterable(groups)), set(names))
            for a in names:
                self.assertIn((a, a), relation)
                for b in names:
                    self.assertEqual((a, b) in relation, (b, a) in relation)
                    for c in names:
                        if (a, b) in relation and (b, c) in relation:
                            self.assertIn((a, c), relation)
        for first, first_rel in partitions.items():
            for second, second_rel in partitions.items():
                if first <= second:
                    self.assertTrue(second_rel <= first_rel)
        self.assertEqual(equivalence_classes(self.c, ()), (("a", "b", "c"),))

    def test_imagination_product_and_witnesses(self):
        observations = (attend(self.c, "a", ("color", "shape")),
                        attend(self.c, "c", ("color", "shape"), "recalled"))
        concepts = imagine(self.c, observations, ("color", "shape"))
        self.assertEqual(len(concepts), 4)
        lookup = {x.attributes: x.witnesses for x in concepts}
        self.assertEqual(lookup[(("color", "red"), ("shape", "round"))], ("a", "b"))
        self.assertEqual(lookup[(("color", "red"), ("shape", "square"))], ())
        self.assertEqual(lookup[(("color", "blue"), ("shape", "round"))], ())
        self.assertEqual(lookup[(("color", "blue"), ("shape", "square"))], ("c",))
        for concept in concepts:
            expected = tuple(name for name, vals in self.c.objects
                             if dict(zip(self.c.features, vals)).items() >= dict(concept.attributes).items())
            self.assertEqual(concept.witnesses, expected)
        self.assertEqual(len(imagine(self.c, (observations[0], observations[0]), ("color",))), 1)

    def test_empty_catalog(self):
        empty = Catalog(("x",), (("v",),), ())
        self.assertEqual(equivalence_classes(empty, ()), ())
        with self.assertRaises(ValueError):
            attend(empty, "missing", ("x",))

    def test_invalid_catalogs(self):
        bad = [([], (), ()), (("x", "x"), (("a",), ("a",)), ()),
               ((), (), ()), (("x",), (), ()), (("x",), ((),), ()),
               (("x",), (("a", "a"),), ()), (("x",), (("a",),), (("o", ("b",)),)),
               (("x",), (("a",),), (("o", ("a",)), ("o", ("a",)))),
               (("x",), (("a",),), (("o", ()),)), (("x",), (("a",),), (("o",),)),
               (("x",), (("a",),), (("o", (1,)),))]
        for args in bad:
            with self.subTest(args=args), self.assertRaises(ValueError):
                Catalog(*args)

    def test_invalid_observations_and_calls(self):
        bad_calls = [lambda: attend(self.c, "missing", ("color",)),
                     lambda: attend(self.c, "a", ["color"]),
                     lambda: attend(self.c, "a", ("color", "color")),
                     lambda: attend(self.c, "a", ("missing",)),
                     lambda: attend(self.c, "a", (), "dreamed"),
                     lambda: attend(None, "a", ()),
                     lambda: compare(self.c, None, self.b, "color"),
                     lambda: compare(self.c, self.a, self.b, "missing"),
                     lambda: compare(self.c, Observation("a", (("color", "blue"),), "current"), self.b, "color"),
                     lambda: reflect(self.c, self.a, None, ()),
                     lambda: imagine(self.c, (), ("color",)),
                     lambda: imagine(self.c, (self.a,), ()),
                     lambda: imagine(self.c, [self.a], ("color",)),
                     lambda: Observation(" a", (), "current"),
                     lambda: Observation("a", (("color", "red"), ("color", "red")), "current"),
                     lambda: Observation("a", (("color",),), "current"),
                     lambda: Concept((), ("a", "a"))]
        for call in bad_calls:
            with self.subTest(call=call), self.assertRaises(ValueError):
                call()

    def test_imagination_budget(self):
        features = tuple(f"f{i}" for i in range(5))
        domains = tuple(("0", "1", "2", "3", "4", "5", "6", "7") for _ in features)
        c = Catalog(features, domains, tuple((f"o{i}", (str(i),) * 5) for i in range(8)))
        observations = tuple(attend(c, name, features) for name, _ in c.objects)
        with self.assertRaisesRegex(ValueError, "budget"):
            imagine(c, observations, features)


class ReasoningTests(unittest.TestCase):
    def test_intermediates_make_conclusion_explicit(self):
        theory = Theory(("p", "q", "r"), ("p",),
                        (Rule("qr", ("q",), "r"), Rule("pq", ("p",), "q")))
        proof = closure(theory)
        self.assertEqual(proof, (Step("p"), Step("q", "pq"), Step("r", "qr")))
        self.assertTrue(verify_certificate(theory, proof, "r"))
        self.assertEqual(semantic_oracle(theory), (("p", "q", "r"), 1))

    def test_missing_bridge_and_cycle_without_facts(self):
        missing = Theory(("p", "q", "r"), ("p",), (Rule("qr", ("q",), "r"),))
        self.assertEqual(atoms_of(closure(missing)), {"p"})
        self.assertEqual(semantic_oracle(missing), (("p",), 3))
        cycle = Theory(("p", "q"), (), (Rule("pq", ("p",), "q"), Rule("qp", ("q",), "p")))
        self.assertEqual(closure(cycle), ())
        self.assertEqual(semantic_oracle(cycle), ((), 2))

    def test_conjunction_and_empty_antecedent(self):
        t = Theory(("p", "q", "r"), ("p",), (Rule("and", ("p", "q"), "r"),))
        self.assertEqual(atoms_of(closure(t)), {"p"})
        seeded = Theory(("p", "q"), (), (Rule("seed", (), "p"), Rule("pq", ("p",), "q")))
        proof = closure(seeded)
        self.assertEqual(atoms_of(proof), {"p", "q"})
        self.assertTrue(verify_certificate(seeded, proof, "q"))
        self.assertEqual(semantic_oracle(seeded), (("p", "q"), 1))
        self.assertEqual(closure(Theory((), (), ())), ())
        self.assertEqual(semantic_oracle(Theory((), (), ())), ((), 1))

    def test_proof_checker_rejects_forgery_and_cycles(self):
        t = Theory(("p", "q", "r"), ("p",),
                   (Rule("pq", ("p",), "q"), Rule("qr", ("q",), "r")))
        invalid = [(Step("r"),), (Step("r", "qr"),),
                   (Step("p"), Step("r", "pq")), (Step("p"), Step("q", "missing")),
                   (Step("p"), Step("p")), (Step("undeclared"),),
                   (Step("p"), Step("r", "qr"), Step("q", "pq"))]
        for proof in invalid:
            with self.subTest(proof=proof):
                self.assertFalse(verify_certificate(t, proof, "r"))
        self.assertFalse(verify_certificate(t, (Step("p"),), "r"))
        self.assertTrue(verify_certificate(t, (Step("p"),), "p"))
        cyc = Theory(("p", "q"), (), (Rule("pq", ("p",), "q"), Rule("qp", ("q",), "p")))
        self.assertFalse(verify_certificate(cyc, (Step("p", "qp"), Step("q", "pq")), "q"))

    def test_exhaustive_two_atom_theories_against_independent_oracle(self):
        atoms = ("p", "q")
        subsets = [tuple(a for a, bit in zip(atoms, bits) if bit)
                   for bits in itertools.product((False, True), repeat=2)]
        candidates = tuple(Rule(f"r{i}", premises, conclusion)
                           for i, (premises, conclusion) in enumerate(itertools.product(subsets, atoms)))
        count = 0
        for enabled in itertools.product((False, True), repeat=len(candidates)):
            rules = tuple(rule for rule, bit in zip(candidates, enabled) if bit)
            for facts in subsets:
                t = Theory(atoms, facts, rules)
                proof = closure(t)
                expected, models = semantic_oracle(t)
                self.assertGreater(models, 0)
                self.assertEqual(atoms_of(proof), set(expected), msg=repr(t))
                for atom in expected:
                    self.assertTrue(verify_certificate(t, proof, atom), msg=repr(t))
                count += 1
        self.assertEqual(count, 1024)

    def test_seeded_three_atom_theories_and_rule_order(self):
        rng = random.Random(1780)
        atoms = ("p", "q", "r")
        for _ in range(200):
            facts = tuple(a for a in atoms if rng.choice((False, True)))
            rules = tuple(Rule(f"r{i}", tuple(a for a in atoms if rng.choice((False, True))), rng.choice(atoms))
                          for i in range(rng.randrange(9)))
            t = Theory(atoms, facts, rules)
            expected, _ = semantic_oracle(t)
            self.assertEqual(atoms_of(closure(t)), set(expected))
            self.assertEqual(atoms_of(closure(Theory(atoms, facts, tuple(reversed(rules))))), set(expected))
            enlarged = Theory(atoms, atoms, rules)
            self.assertTrue(atoms_of(closure(t)) <= atoms_of(closure(enlarged)))

    def test_bad_theories_and_certificates(self):
        bad = [lambda: Rule("", (), "p"), lambda: Rule("r", ("p", "p"), "q"),
               lambda: Theory(("p", "p"), (), ()), lambda: Theory(("p",), ("q",), ()),
               lambda: Theory(("p",), (), (Rule("r", (), "q"),)),
               lambda: Theory(("p",), (), (Rule("r", ("q",), "p"),)),
               lambda: Theory(("p",), (), (Rule("r", (), "p"), Rule("r", (), "p"))),
               lambda: Theory(("p",), (), ("not a rule",)),
               lambda: Theory(tuple(str(i) for i in range(13)), (), ()),
               lambda: Step("p", 1), lambda: closure(None), lambda: semantic_oracle(None),
               lambda: verify_certificate(Theory(("p",), (), ()), (), "q"),
               lambda: verify_certificate(Theory(("p",), (), ()), ("p",), "p"),
               lambda: verify_certificate(Theory(("p",), (), ()), [], "p")]
        for call in bad:
            with self.subTest(call=call), self.assertRaises(ValueError):
                call()

    def test_subset_syllogism_including_vacuity(self):
        universe = ("a", "b", "c")
        sets = tuple(tuple(x for x, bit in zip(universe, bits) if bit)
                     for bits in itertools.product((False, True), repeat=3))
        for a, b, c in itertools.product(sets, repeat=3):
            result = subset_syllogism(universe, a, b, c)
            self.assertTrue(result["implication"])
        vacant = subset_syllogism(universe, (), ("a",), universe)
        self.assertTrue(vacant["premises"])
        self.assertTrue(vacant["conclusion"])
        self.assertFalse(vacant["small_nonempty"])
        with self.assertRaises(ValueError):
            subset_syllogism(universe, ("outside",), (), ())

    def test_no_optimizable_assert_statements_and_oracle_independence(self):
        tree = ast.parse(inspect.getsource(model))
        self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(tree)))
        oracle = ast.parse(inspect.getsource(semantic_oracle))
        calls = {node.func.id for node in ast.walk(oracle) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
        self.assertNotIn("closure", calls)
        self.assertNotIn("verify_certificate", calls)


if __name__ == "__main__":
    unittest.main(verbosity=2)
