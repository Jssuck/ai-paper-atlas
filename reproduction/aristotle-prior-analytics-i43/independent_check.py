"""Independent bit-mask oracle and interface checks for the I.43 teaching model."""
import json
import unittest
from itertools import product
import model as author

W, L, P = map(author.Atom, ('W','L','P'))
D = author.And((L,P))

def subset(a,b):
    return (a & b) == a

def members(mask,n):
    return tuple(i for i in range(n) if (mask >> i) & 1)

def independent_counts():
    count = dict(models=0, background_reduction=0, local_not_whole=0, inclusion_not_definition=0)
    for n in range(5):
        for w,l,p in product(range(1<<n), repeat=3):
            count['models'] += 1
            whole = subset(w,l & p)
            local = subset(w,p)
            liquid = subset(w,l)
            if whole != (liquid and local): raise RuntimeError('mask conjunction')
            if liquid:
                count['background_reduction'] += 1
                if whole != local: raise RuntimeError('mask background')
            if (w == (l & p)) != (whole and subset(l & p,w)):
                raise RuntimeError('mask definition')
            if bool(w & ~p) == local: raise RuntimeError('mask witness')
            count['local_not_whole'] += local and not whole
            count['inclusion_not_definition'] += whole and w != (l & p)
            m = author.Model(range(n), {'W':members(w,n),'L':members(l,n),'P':members(p,n)})
            if m.inclusion(W,D) != whole: raise RuntimeError('author conjunction differs')
            if m.definition(W,D) != (w == (l & p)): raise RuntimeError('author definition differs')
            if m.counterexamples(W,P) != frozenset(members(w & ~p,n)):
                raise RuntimeError('author witness differs')
            if author.verify_components(m,W,D,(author.Certificate(W,x) for x in (L,P))) != whole:
                raise RuntimeError('author certificates differ')
    return count

class IndependentTests(unittest.TestCase):
    def setUp(self):
        self.m = author.Model((0,1), {'W':(0,), 'L':(0,), 'P':(0,)})
    def test_counts_and_oracle(self):
        type(self).checked_counts = independent_counts()
        self.assertEqual(self.checked_counts, dict(models=4681,background_reduction=1555,
                                                   local_not_whole=774,inclusion_not_definition=440))
    def test_same_witness(self):
        m=author.Model((0,1),{'W':(0,1),'L':(0,),'P':(1,)})
        self.assertTrue(m.extension(author.And((W,L))))
        self.assertTrue(m.extension(author.And((W,P))))
        self.assertFalse(m.extension(author.And((W,L,P))))
    def test_empty_domain(self):
        m=author.Model((), {'W':(),'L':(),'P':()})
        self.assertTrue(m.definition(W,D))
        self.assertFalse(m.extension(W))
    def test_missing_and_duplicate(self):
        c=author.Certificate(W,P)
        self.assertFalse(author.verify_components(self.m,W,D,(c,c)))
        self.assertFalse(author.verify_certificate(self.m,c,W,D))
    def test_syntax_is_not_equivalence(self):
        self.assertTrue(self.m.inclusion(W,author.And((P,L))))
        self.assertFalse(author.verify_certificate(self.m,author.Certificate(W,D),W,author.And((P,L))))
    def test_projection_boundaries(self):
        self.assertEqual(author.project_component(author.And((L,author.Not(P))),author.Not(P)),author.Not(P))
        for form in (author.Or((L,P)), author.Not(D)):
            with self.assertRaises(ValueError): author.project_component(form,P)
    def test_empty_evidence_invalid_goal(self):
        with self.assertRaises(ValueError): author.verify_components(self.m,author.Atom('missing'),D,())
        with self.assertRaises(ValueError): author.verify_components(self.m,W,author.And((L,)),())
    def test_mismatch_unknown_requested_name(self):
        with self.assertRaises(ValueError):
            author.verify_certificate(self.m,author.Certificate(W,P),W,author.Atom('missing'))
    def test_late_invalid_evidence(self):
        cs=(author.Certificate(W,L),author.Certificate(W,P),author.Certificate(W,author.Atom('missing')))
        with self.assertRaises(ValueError): author.verify_components(self.m,W,D,cs)
    def test_and_does_not_implement_empty_conjunction(self):
        with self.assertRaises(ValueError): self.m.extension(author.And(()))

if __name__ == '__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(IndependentTests))
    if not result.wasSuccessful(): raise SystemExit(1)
    print(json.dumps(IndependentTests.checked_counts,sort_keys=True))
    print('Independent bit-mask oracle checked each author model. Finite tests are not a general proof.')
