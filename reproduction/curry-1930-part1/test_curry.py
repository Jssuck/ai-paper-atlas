"""Regression tests, independent callable semantics, and negative checks."""
import random
import unittest
from curry import (
    Atom, App, B, C, W, K, I, app, parse, pretty, spine, atoms, step,
    normalize, normal, sequence, dot, dot_many, AXIOMS, AXIOM_TEXT,
    AXIOM_ARITIES, BW_P521_LITERAL, axioms_in_product_notation,
    Proof, InvalidProof, check, refl, sym, chain, congruence, applied,
    axiom, certify_step, certify_run, by_reduction, cbi_identity_proof,
    right_identity_proof, distribution_proof, associativity_proof,
    axiom_names_used, fresh_args, saturated_axiom_check, Step, Run, instantiate, substitute,
)


EXPECTED_ACTIONS = {
    "B": "x0 (x1 (x2 x3))", "C": "x0 (x1 x3 x2)",
    "W": "x0 (x1 x2 x2)", "K": "x0 x1", "I1": "x0 x1",
    "BC": "x0 x3 (x1 x2)", "BW": "x0 (x1 x2) (x1 x2)",
    "BK": "x0", "CC1": "x0 x1 x2", "CC2": "x0 x3 x2 x1",
    "CW": "x0 x2 x2 x1", "CK": "x0 x1", "WC": "x0 x1 x1",
    "WW": "x0 x1 x1 x1", "WK": "x0 x1", "I2": "x0 x1",
}


class Symbolic:
    """Independent callable interpreter: no root_contract/step/normal calls."""
    def __init__(self, term):
        self.term = term

    def __call__(self, other):
        if not isinstance(other, Symbolic):
            raise TypeError("residual combinator function: insufficient saturation")
        return Symbolic(App(self.term, other.term))


def denote(t):
    if isinstance(t, App):
        return denote(t.fn)(denote(t.arg))
    if t == B:
        return lambda f: lambda g: lambda x: f(g(x))
    if t == C:
        return lambda f: lambda x: lambda y: f(y)(x)
    if t == W:
        return lambda f: lambda x: f(x)(x)
    if t == K:
        return lambda x: lambda y: x
    return Symbolic(t)


class SyntaxTests(unittest.TestCase):
    def test_left_association(self):
        self.assertEqual(parse("BXY"), app(B, Atom("X"), Atom("Y")))
        self.assertNotEqual(parse("x y z"), parse("x (y z)"))

    def test_parentheses_and_whitespace(self):
        self.assertEqual(parse(" ( B\n x ) (y z) "), app(B, Atom("x"), parse("y z")))
        self.assertEqual(spine(parse("B x y z u")), (B, tuple(map(Atom, "xyzu"))))

    def test_i_is_expansion(self):
        self.assertEqual(parse("I"), app(W, K))
        self.assertNotIn(Atom("i"), atoms(I))
        with self.assertRaises(ValueError):
            Atom("I")

    def test_invalid_parser(self):
        for text in ("", " ", "()", "(x", "x)", "x$y", "x.y", "(())", "x( )"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse(text)

    def test_round_trip(self):
        for text in ("B(B(BW)W)(BC)", "I x", "foo bar", "x0 (x12 y_z)", "B2"):
            self.assertEqual(parse(pretty(parse(text))), parse(text))
        self.assertNotEqual(parse("B2"), sequence("B", 2))


class ReductionTests(unittest.TestCase):
    def test_primitive_rules(self):
        for source, target, rule in (("B x y z", "x (y z)", "B"),
                                     ("C x y z", "x z y", "C"),
                                     ("W x y", "x y y", "W"),
                                     ("K x y", "x", "K")):
            with self.subTest(rule=rule):
                s = step(parse(source))
                self.assertEqual((s.after, s.rule, s.path), (parse(target), rule, ()))
                self.assertEqual(check(certify_step(s)), (parse(source), parse(target)))

    def test_partial_application_is_normal(self):
        for text in ("B", "B x", "B x y", "C x y", "W x", "K x", "I", "B I"):
            with self.subTest(text=text):
                self.assertIsNone(step(parse(text)))

    def test_i_trace_uses_w_and_k(self):
        result = normalize(parse("I x"))
        self.assertEqual([s.rule for s in result.steps], ["W", "K"])
        self.assertEqual(result.end, Atom("x"))

    def test_overapplication(self):
        self.assertEqual(step(parse("B x y z u")).after, parse("x (y z) u"))
        self.assertEqual(step(parse("K x y z")).after, parse("x z"))

    def test_context_in_argument(self):
        s = step(parse("f (I x)"))
        self.assertEqual(s.path, (1,))
        self.assertEqual(s.after, parse("f (K x x)"))
        check(certify_step(s))

    def test_context_in_function_before_argument(self):
        s = step(parse("f (I x) (I y)"))
        self.assertEqual(s.path, (0, 1))
        check(certify_step(s))

    def test_outermost_discards_divergence(self):
        self.assertEqual(normal(parse("K x (W W W)")), Atom("x"))

    def test_self_loop_is_not_normal(self):
        omega = parse("W W W")
        s = step(omega)
        self.assertIsNotNone(s)
        self.assertEqual(s.after, omega)
        run = normalize(omega)
        self.assertEqual((run.status, len(run.steps), run.cycle_start, run.cycle_length),
                         ("cycle", 1, 0, 1))
        check(certify_run(run))

    def test_fuel_and_cycle_status(self):
        self.assertEqual(normalize(parse("I x"), 0).status, "fuel_exhausted")
        self.assertEqual(normalize(parse("x"), 0).status, "normal")
        self.assertEqual(normalize(parse("I x"), 1).status, "fuel_exhausted")
        self.assertEqual(normalize(parse("I x"), 2).status, "normal")
        run = normalize(parse("W W W"), 7, detect_cycles=False)
        self.assertEqual((run.status, len(run.steps)), ("fuel_exhausted", 7))
        for fuel in (-1, 1.5, True):
            with self.assertRaises(ValueError):
                normalize(I, fuel)

    def test_normal_helper_rejects_inconclusive(self):
        with self.assertRaises(ValueError):
            normal(parse("W W W"))


class SequenceTests(unittest.TestCase):
    def test_exact_definitions_and_index_boundary(self):
        self.assertEqual(sequence("B", 0), I)
        self.assertEqual(sequence("B", 1), B)
        self.assertEqual(sequence("B", 2), app(B, B, B))
        for kind, base in (("C", C), ("W", W), ("K", K)):
            self.assertEqual(sequence(kind, 1), base)
            self.assertEqual(sequence(kind, 3), app(B, app(B, base)))
        for kind, n in (("B", -1), ("C", 0), ("W", 0), ("K", 0), ("Q", 1), ("BC", 1), ("B", True)):
            with self.subTest(kind=kind, n=n), self.assertRaises(ValueError):
                sequence(kind, n)

    def test_b_sequence_action(self):
        f, g = Atom("f"), Atom("g")
        for n in range(7):
            xs = fresh_args(n)
            lhs = app(sequence("B", n), f, g, *xs)
            rhs = app(f, app(g, *xs))
            self.assertEqual(normal(lhs), rhs)
            check(by_reduction(lhs, rhs))

    def test_c_w_k_sequence_actions(self):
        for n in range(1, 7):
            xs = fresh_args(n + 2)
            cases = (
                (app(sequence("C", n), *xs), app(xs[0], *xs[1:n], xs[n+1], xs[n])),
                (app(sequence("W", n), *xs[:-1]), app(xs[0], *xs[1:n], xs[n], xs[n])),
                (app(sequence("K", n), *xs[:-1]), app(xs[0], *xs[1:n])),
            )
            for lhs, rhs in cases:
                self.assertEqual(normal(lhs), rhs)
                check(by_reduction(lhs, rhs))

    def test_sequence_lifting_identity(self):
        # II.B.1 Satz 5, B_m(B_n X) = B_(m+n)X, finite index instances.
        x = Atom("x")
        for m in range(5):
            for n in range(5):
                lhs = app(sequence("B", m), app(sequence("B", n), x))
                rhs = app(sequence("B", m+n), x)
                self.assertEqual(normal(lhs), normal(rhs))


class AxiomTests(unittest.TestCase):
    def test_all_sixteen_symbolic_actions(self):
        self.assertEqual(len(AXIOMS), 16)
        for name, arity in AXIOM_ARITIES.items():
            with self.subTest(name=name):
                a, b = saturated_axiom_check(name, arity)
                self.assertEqual(a.end, parse(EXPECTED_ACTIONS[name]))
                self.assertEqual(check(axiom(name)), AXIOMS[name])

    def test_independent_callable_semantics(self):
        for name, arity in AXIOM_ARITIES.items():
            with self.subTest(name=name):
                for side in AXIOMS[name]:
                    got = denote(app(side, *fresh_args(arity)))
                    self.assertIsInstance(got, Symbolic)
                    self.assertEqual(got.term, parse(EXPECTED_ACTIONS[name]))

    def test_product_notation_matches_each_side(self):
        # Independent p.534–535 transcription, not equality of the two sides.
        for name, sides in axioms_in_product_notation().items():
            for expanded, product in zip(AXIOMS[name], sides):
                self.assertEqual(check(by_reduction(expanded, product)), (expanded, product))

    def test_bw_p521_literal_anomaly(self):
        lhs, rhs = BW_P521_LITERAL
        xs = fresh_args(3)
        self.assertEqual(normal(app(lhs, *xs)), parse("x0 (x1 x2) (x1 x2)"))
        self.assertEqual(normal(app(rhs, *xs)), parse("x0 (x1 (B x0)) (x1 x2)"))
        self.assertNotEqual(normal(app(lhs, *xs)), normal(app(rhs, *xs)))
        self.assertNotEqual(rhs, AXIOMS["BW"][1])

    def test_insufficient_saturation_rejected(self):
        with self.assertRaises(ValueError):
            saturated_axiom_check("I2", 1)


class ProofTests(unittest.TestCase):
    def test_equality_properties(self):
        x = Atom("x")
        p = Proof("W", (K, x))
        q = Proof("K", (x, x))
        r = chain(p, q)
        self.assertEqual(check(r), (app(I, x), x))
        self.assertEqual(check(sym(r)), (x, app(I, x)))
        self.assertEqual(check(congruence(refl(Atom("f")), r)), (parse("f (I x)"), parse("f x")))
        self.assertEqual(check(applied(r, Atom("z"))), (parse("I x z"), parse("x z")))

    def test_reject_bad_certificates(self):
        bad = (
            Proof("eta", (parse("B I"), I)),
            Proof("axiom", ("invented",)),
            Proof("B", (Atom("x"),)),
            Proof("refl", ("not a term",)),
            Proof("trans", premises=(refl(B), refl(C))),
            Proof("app", premises=(refl(B),)),
            Proof("K", (B, C), (refl(B),)),
        )
        for p in bad:
            with self.subTest(rule=p.rule), self.assertRaises(InvalidProof):
                check(p)

    def test_reject_forged_trace(self):
        with self.assertRaises(InvalidProof):
            certify_step(Step(parse("K x y"), Atom("y"), "K", ()))
        with self.assertRaises(InvalidProof):
            certify_step(Step(parse("W x y"), Atom("x"), "K", ()))
        with self.assertRaises(InvalidProof):
            certify_run(Run(B, C, (), "normal"))
        good = step(parse("I x"))
        with self.assertRaises(InvalidProof):
            certify_run(Run(B, good.after, (good,), "normal"))

    def test_bi_i_boundary(self):
        self.assertEqual(normal(app(B, I)), app(B, I))
        self.assertEqual(normal(I), I)
        self.assertNotEqual(normal(app(B, I)), normal(I))
        with self.assertRaises(ValueError):
            by_reduction(app(B, I), I)
        x, y = fresh_args(2)
        self.assertEqual(normal(app(B, I, x, y)), normal(app(I, x, y)))
        self.assertEqual(check(axiom("I2")), (app(B, I), I))

    def test_cbi_and_right_identity_proofs(self):
        p = cbi_identity_proof()
        self.assertEqual(check(p), (app(C, B, I), I))
        self.assertEqual(axiom_names_used(p), frozenset(("I1", "I2")))
        x = Atom("x")
        self.assertEqual(check(right_identity_proof(x)), (dot(x, I), x))

    def test_associativity_proof_and_boundary(self):
        x, y, z, u = map(Atom, "xyzu")
        lhs, rhs = dot(dot(x, y), z), dot(x, dot(y, z))
        self.assertNotEqual(normal(lhs), normal(rhs))
        self.assertEqual(normal(app(lhs, u)), normal(app(rhs, u)))
        self.assertEqual(normal(app(lhs, u)), parse("x (y (z u))"))
        p = associativity_proof(x, y, z)
        self.assertEqual(check(p), (lhs, rhs))
        self.assertEqual(axiom_names_used(p), frozenset(("B",)))

    def test_distribution_proof(self):
        x, y = map(Atom, "xy")
        p = distribution_proof(x, y)
        self.assertEqual(check(p), (app(B, dot(x, y)), dot(app(B, x), app(B, y))))

    def test_theorem_instantiation_with_divergent_arguments(self):
        omega = parse("W W W")
        self.assertEqual(check(right_identity_proof(omega)), (dot(omega, I), omega))
        self.assertEqual(check(distribution_proof(omega, omega)),
                         (app(B, dot(omega, omega)), dot(app(B, omega), app(B, omega))))
        self.assertEqual(check(associativity_proof(omega, omega, omega)),
                         (dot(dot(omega, omega), omega), dot(omega, dot(omega, omega))))

    def test_substitution_is_simultaneous_and_protects_primitives(self):
        x, y = Atom("x"), Atom("y")
        self.assertEqual(substitute(app(x, y), {x: y, y: B}), app(y, B))
        with self.assertRaises(ValueError):
            instantiate(axiom("I2"), {B: C})
        self.assertEqual(check(instantiate(Proof("K", (x, y)), {x: parse("W W W")})),
                         (parse("K (W W W) y"), parse("W W W")))

    def test_bounded_random_traces_are_certified(self):
        rng = random.Random(1930)
        def term(depth):
            if depth == 0 or rng.random() < .4:
                return rng.choice((B, C, W, K, Atom("x"), Atom("y")))
            return app(term(depth - 1), term(depth - 1))
        for _ in range(250):
            t = term(4)
            self.assertEqual(parse(pretty(t)), t)
            run = normalize(t, 30)
            self.assertEqual(check(certify_run(run)), (t, run.end))


if __name__ == "__main__":
    unittest.main(verbosity=2)
