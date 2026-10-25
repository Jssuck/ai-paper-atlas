import itertools
import unittest
import model


def oracle(kind, subject, predicate):
    if kind == 'A': return all(x in predicate for x in subject)
    if kind == 'E': return all(x not in predicate for x in subject)
    if kind == 'I': return any(x in predicate for x in subject)
    if kind == 'O': return any(x not in predicate for x in subject)
    raise ValueError(kind)


class ModelTests(unittest.TestCase):
    def test_empty_semantics(self):
        self.assertEqual([model.proposition(k, set(), {1}) for k in 'AEIO'], [True, True, False, False])

    def test_unknown_kind(self):
        with self.assertRaises(ValueError): model.proposition('X', set(), set())

    def test_invalid_world(self):
        for value in (-1, 256, True, 1.0):
            with self.assertRaises(ValueError): model.terms(value)

    def test_invalid_figure(self):
        with self.assertRaises(ValueError): model.premises(4, 'AAA', set(), set(), set())

    def test_invalid_mood(self):
        with self.assertRaises(ValueError): model.premises(1, 'AA', set(), set(), set())

    def test_each_cell(self):
        for cell in range(8):
            s, p, m = model.terms(1 << cell)
            self.assertEqual(tuple(bool(t) for t in (s, p, m)), tuple(bool(cell & b) for b in (1,2,4)))

    def test_quantified_oracle(self):
        for w in range(256):
            terms = model.terms(w)
            for a, b in itertools.product(terms, repeat=2):
                for kind in 'AEIO': self.assertEqual(model.proposition(kind,a,b), oracle(kind,a,b))

    def test_e_i_conversion(self):
        for w in range(256):
            s,p,_=model.terms(w)
            for k in 'EI': self.assertEqual(model.proposition(k,s,p),model.proposition(k,p,s))

    def test_a_not_simple_conversion(self):
        self.assertTrue(model.proposition('A',{1},{1,2}))
        self.assertFalse(model.proposition('A',{1,2},{1}))

    def test_barbara_celarent(self):
        for mood in ('AAA','EAE'):
            self.assertTrue(model.evaluate(1,mood)['valid_in_enumeration'])

    def test_modern_valid_lists(self):
        expected={1:['AAA','AII','EAE','EIO'],2:['AEE','AOO','EAE','EIO'],3:['AII','EIO','IAI','OAO']}
        for f in expected:
            self.assertEqual([m for m in model.MOODS if model.evaluate(f,m)['valid_in_enumeration']],expected[f])

    def test_nonempty_valid_lists(self):
        expected={1:['AAA','AAI','AII','EAE','EAO','EIO'],2:['AEE','AEO','AOO','EAE','EAO','EIO'],3:['AAI','AII','EAO','EIO','IAI','OAO']}
        for f in expected:
            self.assertEqual([m for m in model.MOODS if model.evaluate(f,m,True)['valid_in_enumeration']],expected[f])

    def test_no_figure2_affirmative(self):
        for policy in (False,True):
            for mood in model.MOODS:
                if mood[2] in 'AI': self.assertFalse(model.evaluate(2,mood,policy)['valid_in_enumeration'])

    def test_no_figure3_universal(self):
        for policy in (False,True):
            for mood in model.MOODS:
                if mood[2] in 'AE': self.assertFalse(model.evaluate(3,mood,policy)['valid_in_enumeration'])

    def test_stored_counterexamples(self):
        for policy in (False,True):
            for f in (1,2,3):
                for mood in model.MOODS:
                    result=model.evaluate(f,mood,policy)
                    w=result['first_counterexample']
                    if w is not None:
                        s,p,m=model.terms(w)
                        if policy: self.assertTrue(all((s,p,m)))
                        self.assertTrue(model.premises(f,mood,s,p,m))
                        self.assertFalse(model.proposition(mood[2],s,p))
                    self.assertGreater(result['premise_worlds'],0)

    def test_darapti_existence(self):
        self.assertFalse(model.evaluate(3,'AAI')['valid_in_enumeration'])
        self.assertTrue(model.evaluate(3,'AAI',True)['valid_in_enumeration'])

    def test_reductions(self):
        for w in range(256): self.assertTrue(all(model.reductions(*model.terms(w)).values()))

    def test_three_element_independent_enumeration(self):
        sets=[{i for i in range(3) if mask & (1<<i)} for mask in range(8)]
        for policy in (False,True):
            failed={(f,mood):False for f in (1,2,3) for mood in model.MOODS}
            for s,p,m in itertools.product(sets,repeat=3):
                if policy and not all((s,p,m)): continue
                pairs={1:((m,p),(s,m)),2:((p,m),(s,m)),3:((m,p),(m,s))}
                for (f,mood) in failed:
                    major,minor=pairs[f]
                    if oracle(mood[0],*major) and oracle(mood[1],*minor) and not oracle(mood[2],s,p):
                        failed[f,mood]=True
            for (f,mood),bad in failed.items():
                self.assertEqual(not bad,model.evaluate(f,mood,policy)['valid_in_enumeration'])

if __name__ == '__main__': unittest.main()
