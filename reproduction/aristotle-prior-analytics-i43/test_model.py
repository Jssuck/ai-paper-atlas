import unittest
from model import Atom, And, Or, Not, Model, Certificate, project_component, verify_certificate, verify_components
W, L, P = map(Atom, ('W', 'L', 'P'))
D = And((L, P))

class Tests(unittest.TestCase):
    def model(self, w=(0,), l=(0,), p=(0,)):
        return Model((0, 1), {'W': w, 'L': l, 'P': p})
    def test_full_and_components(self):
        m = self.model()
        self.assertTrue(m.inclusion(W, D))
        self.assertTrue(verify_components(m, W, D, (Certificate(W,L), Certificate(W,P))))
    def test_missing_liquid(self):
        m = self.model(l=())
        self.assertTrue(m.inclusion(W,P)); self.assertFalse(m.inclusion(W,D))
    def test_reverse_missing(self):
        m = self.model(l=(0,1),p=(0,1))
        self.assertTrue(m.inclusion(W,D)); self.assertFalse(m.inclusion(D,W))
        self.assertFalse(m.definition(W,D))
    def test_vacuity(self):
        m = self.model(w=())
        self.assertTrue(m.inclusion(W,D)); self.assertFalse(m.definition(W,D))
    def test_empty_universe(self):
        m = Model((), {'W':(), 'L':(), 'P':()})
        self.assertTrue(m.definition(W,D))
    def test_counterexample_subject_required(self):
        m = self.model(p=(0,))
        self.assertEqual(m.counterexamples(W,P),frozenset())
        self.assertNotIn(1,m.counterexamples(W,P))
    def test_actual_counterexample(self):
        m = self.model(w=(0,1),p=(0,))
        self.assertEqual(m.counterexamples(W,P),frozenset((1,)))
    def test_matching_goal(self):
        self.assertFalse(verify_certificate(self.model(),Certificate(W,P),W,D))
    def test_duplicates_do_not_complete(self):
        self.assertFalse(verify_components(self.model(),W,D,(Certificate(W,P),)*2))
    def test_generator_certificates(self):
        self.assertTrue(verify_components(self.model(),W,D,(Certificate(W,x) for x in (L,P))))
    def test_positive_projection(self):
        self.assertEqual(project_component(And((D,W)),P),P)
    def test_no_disjunction_projection(self):
        with self.assertRaises(ValueError): project_component(Or((L,P)),P)
    def test_no_negation_projection(self):
        with self.assertRaises(ValueError): project_component(Not(D),P)
    def test_negated_conjunct_as_whole(self):
        self.assertEqual(project_component(And((L,Not(P))),Not(P)),Not(P))
    def test_unknown_name_not_short_circuited(self):
        with self.assertRaises(ValueError): self.model(l=()).extension(And((L,Atom('missing'))))
    def test_invalid_formula_and_model(self):
        with self.assertRaises(ValueError): self.model().extension(And((L,)))
        with self.assertRaises(ValueError): Model((0,),{'W':(1,)})
    def test_invalid_certificate_not_short_circuited(self):
        with self.assertRaises(ValueError): verify_components(self.model(),W,D,(Certificate(W,Atom('missing')),))
    def test_or_and_negation_countermodels(self):
        m = self.model(l=(0,),p=())
        self.assertTrue(m.inclusion(W,Or((L,P)))); self.assertFalse(m.inclusion(W,P))
        self.assertTrue(m.inclusion(W,Not(D))); self.assertFalse(m.inclusion(W,Not(L)))

if __name__ == '__main__': unittest.main(verbosity=2)
