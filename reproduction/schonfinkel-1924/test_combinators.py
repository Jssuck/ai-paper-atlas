import unittest
from dataclasses import FrozenInstanceError
from combinators import (Var, Comb, App, I, C, K, T, Z, S, app, step, normalize,
                         abstract, substitute, free_variables, finite_u,
                         StepLimitExceeded)


def terms_of_size(size, atoms):
    """All binary application trees with exactly size AST nodes."""
    if size == 1:
        return list(atoms)
    terms = []
    for left_size in range(1, size - 1):
        for left in terms_of_size(left_size, atoms):
            for right in terms_of_size(size - 1 - left_size, atoms):
                terms.append(App(left, right))
    return terms


class CombinatorTests(unittest.TestCase):
    def setUp(self):
        self.f, self.g, self.x, self.y = map(Var, ('f', 'g', 'x', 'y'))

    def nf(self, term):
        return normalize(term, 2000)[0]

    def test_original_rules(self):
        f, g, x, y = self.f, self.g, self.x, self.y
        for source, target in [(app(I,x),x), (app(C,x,y),x),
                               (app(T,f,x,y),app(f,y,x)),
                               (app(Z,f,g,x),app(f,app(g,x))),
                               (app(S,f,g,x),app(f,x,app(g,x)))]:
            self.assertEqual(step(source), target)

    def test_missing_arguments_and_partial_application(self):
        for comb, arity in [(I,1),(C,2),(T,3),(Z,3),(S,3)]:
            for count in range(arity):
                self.assertIsNone(step(app(comb,*([self.x]*count))))
        self.assertEqual(step(app(C,self.x,self.y,self.g)),app(self.x,self.g))
        self.assertEqual(self.nf(app(app(C,self.x),self.y)),self.x)

    def test_leftmost_outermost_and_full_normal_form(self):
        omega_body = app(S,I,I)
        omega = app(omega_body,omega_body)
        self.assertEqual(normalize(app(C,self.x,omega),1),(self.x,1))
        self.assertEqual(step(app(app(I,self.f),app(I,self.x))),
                         app(self.f,app(I,self.x)))
        self.assertEqual(self.nf(app(self.f,app(I,self.x))),app(self.f,self.x))

    def test_immutable_ast_and_alias(self):
        with self.assertRaises(FrozenInstanceError):
            self.x.name = 'changed'
        with self.assertRaises(FrozenInstanceError):
            App(I,self.x).argument = self.y
        with self.assertRaises(FrozenInstanceError):
            I.name = 'C'
        self.assertIs(K,C)
        with self.assertRaises(ValueError):
            Comb('K')

    def test_bracket_abstraction_rules(self):
        self.assertEqual(abstract('x',self.x),I)
        self.assertEqual(abstract('x',self.y),app(C,self.y))
        self.assertEqual(abstract('x',app(self.x,self.y)),app(S,I,app(C,self.y)))

    def test_exhaustive_finite_substitution_theorem(self):
        # Exhaustive only within this explicitly finite grammar; not a proof.
        atoms = (self.x,self.y,I,C,S)
        expressions = sum((terms_of_size(n,atoms) for n in (1,3,5)),[])
        replacements = (self.y,I,C,app(I,self.y),app(C,self.y))
        count = 0
        self.assertEqual(len(expressions),280)
        for expression in expressions:
            for replacement in replacements:
                with self.subTest(expression=str(expression),replacement=str(replacement)):
                    self.assertEqual(self.nf(app(abstract('x',expression),replacement)),
                                     self.nf(substitute(expression,'x',replacement)))
                    self.assertNotIn('x',free_variables(abstract('x',expression)))
                count += 1
        self.assertEqual(count,1400)
        print('Exhaustive finite substitution checks: 280 expressions × 5 replacements = 1400')

    def test_no_capture_and_shadow_like_names(self):
        # x replaced by y stays free: no lambda binders exist in this AST.
        expression = app(self.x,self.y)
        result = self.nf(app(abstract('x',expression),self.y))
        self.assertEqual(result,app(self.y,self.y))
        self.assertEqual(free_variables(result),frozenset({'y'}))
        self.assertEqual(substitute(Var('xx'),'x',self.y),Var('xx'))

    def test_original_elimination_identities_extensionally(self):
        f,g,x,y = self.f,self.g,self.x,self.y
        identities = [(I,app(S,C,C),(x,)),
                      (Z,app(S,app(C,S),C),(f,g,x)),
                      (T,app(S,app(Z,Z,S),app(C,C)),(f,x,y))]
        for primitive, derived, args in identities:
            self.assertEqual(self.nf(app(primitive,*args)),self.nf(app(derived,*args)))
            self.assertNotEqual(primitive,derived)  # not literal AST equality
        print('Original identities verified after fresh-variable arguments: I=SCC; Z=S(CS)C; T=S(ZZS)(CC)')

    def test_budget_and_exact_boundary(self):
        w = app(S,I,I)
        with self.assertRaises(StepLimitExceeded) as context:
            normalize(app(w,w),25)
        self.assertEqual(context.exception.steps,25)
        self.assertEqual(normalize(self.x,0),(self.x,0))
        self.assertEqual(normalize(app(I,self.x),1),(self.x,1))
        with self.assertRaises(StepLimitExceeded):
            normalize(app(I,self.x),0)
        with self.assertRaises(ValueError):
            normalize(self.x,-1)

    def test_finite_semantic_u(self):
        domain = (0,1,2)
        u = finite_u(domain)
        even = lambda n: n % 2 == 0
        odd = lambda n: n % 2 == 1
        self.assertTrue(u(even)(odd))
        self.assertFalse(u(even)(lambda n: n == 2))
        predicates = [lambda x,mask=mask: bool(mask & (1 << x)) for mask in range(8)]
        for f in predicates:
            for g in predicates:
                self.assertEqual(u(f)(g),not any(f(x) and g(x) for x in domain))
        with self.assertRaises(ValueError):
            finite_u(())
        print('Finite U checks: all 8 × 8 Boolean-predicate pairs on domain {0,1,2} = 64')


    def test_higher_order_u_with_distinct_domains(self):
        domain = (0,1,2)
        u_domain = finite_u(domain)
        all_predicates = tuple(lambda x,mask=mask: bool(mask & (1 << x))
                               for mask in range(8))
        restricted_predicates = (lambda x: True,)
        for label, predicates, expected in [('all eight',all_predicates,True),
                                             ('only constant True',restricted_predicates,False)]:
            u_predicates = finite_u(predicates)
            # A is a predicate ON predicates. Inner U quantifies over objects;
            # both outer U occurrences quantify over the selected predicate set.
            def a(f):
                incompatibility = u_domain(f)
                return u_predicates(incompatibility)(incompatibility)
            for f in predicates:
                self.assertEqual(a(f),not any(u_domain(f)(g) for g in predicates))
            encoded = u_predicates(a)(a)
            direct = all(any(u_domain(f)(g) for g in predicates) for f in predicates)
            self.assertEqual(encoded,direct)
            self.assertEqual(encoded,expected)
            print(f'Higher-order U: predicate domain {label}; encoded={encoded}; direct={direct}')


if __name__ == '__main__':
    unittest.main(verbosity=2)
