"""Independent I.45 checks: object sets, not author's type-mask implementation."""
import itertools
import json
import unittest


def statement(kind, subject, predicate):
    if kind == 'A': return subject <= predicate
    if kind == 'E': return not (subject & predicate)
    if kind == 'I': return bool(subject & predicate)
    if kind == 'O': return bool(subject - predicate)
    raise ValueError(kind)


def models(n):
    subsets = [frozenset(i for i in range(n) if bits >> i & 1) for bits in range(1 << n)]
    yield from itertools.product(subsets, repeat=3)


def mood_truth(figure, mood, model):
    s, p, m = model
    pairs = {1: ((m,p),(s,m)), 2: ((p,m),(s,m)), 3: ((m,p),(m,s))}
    major, minor = pairs[figure]
    return (statement(mood[0],*major), statement(mood[1],*minor), statement(mood[2],s,p))


class IndependentChecks(unittest.TestCase):
    def test_author_semantics_crosscheck(self):
        import model as author
        for n in range(4):
            for sets in models(n):
                env=dict(zip(('S','P','M'),sets))
                for kind in 'AEIO':
                    for s,p in itertools.permutations(env,2):
                        self.assertEqual(author.holds(author.prop(kind,s,p),env),statement(kind,env[s],env[p]))
    def test_author_certificate_soundness(self):
        import model as author
        for name,(premises,steps,conclusion,nonempty) in author.demonstrations().items():
            self.assertTrue(author.verify(premises,steps,conclusion,nonempty),name)
            for n in range(4):
                for sets in models(n):
                    env=dict(zip(('S','P','M'),sets))
                    def value(p): return statement(p.kind,env[p.subject],env[p.predicate])
                    if all(env[t] for t in nonempty) and all(value(p) for p in premises): self.assertTrue(value(conclusion),name)
        for name,proof in author.indirect_demonstrations().items(): self.assertTrue(author.reductio(*proof),name)
    def test_author_rejects_bad_certificates(self):
        import model as a
        p=a.prop('A','S','P')
        for nonempty in ((),('P',)):
            with self.assertRaises(ValueError): a.convert(p,nonempty)
        with self.assertRaises(ValueError): a.convert(a.prop('O','S','P'),('S','P','M'))
        with self.assertRaises(ValueError): a.Step('convert',(True,),p)
        with self.assertRaises(ValueError): a.check_steps((p,),(a.Step('convert',(1,),p),))
        with self.assertRaises(ValueError): a.check_steps((a.prop('E','S','P'),),(a.Step('convert',(0,),a.prop('I','P','S')),))
        with self.assertRaises(ValueError): a.check_steps((),(),('X',))
        with self.assertRaises(ValueError): a.mood(True,'AAA')
        good=a.indirect_demonstrations()['Baroco']
        self.assertFalse(a.reductio(*good[:-1],a.prop('O','P','S')))
    def test_fourteen_moods(self):
        expected = {1: {'AAA','EAE','AII','EIO'},2:{'EAE','AEE','EIO','AOO'},3:{'IAI','AII','EIO','OAO'}}
        for fig in (1,2,3):
            valid = set()
            for mood in map(''.join,itertools.product('AEIO',repeat=3)):
                results = [not (a and b) or c for n in range(4) for model in models(n) for a,b,c in [mood_truth(fig,mood,model)]]
                if all(results): valid.add(mood)
            self.assertEqual(valid,expected[fig])
    def test_existential_third_figure(self):
        for mood in ('AAI','EAO'):
            for n in range(4):
                for model in models(n):
                    a,b,c=mood_truth(3,mood,model)
                    if model[2] and a and b: self.assertTrue(c)
        self.assertEqual(mood_truth(3,'AAI',(frozenset(),)*3),(True,True,False))
        self.assertEqual(mood_truth(3,'EAO',(frozenset(),)*3),(True,True,False))
    def test_simple_conversions(self):
        for n in range(4):
            for s,p,_ in models(n):
                for kind in 'EI': self.assertEqual(statement(kind,s,p),statement(kind,p,s))
    def test_partial_conversion(self):
        for n in range(4):
            for s,p,_ in models(n):
                if s and statement('A',s,p): self.assertTrue(statement('I',p,s))
        self.assertTrue(statement('A',frozenset(),frozenset({0})))
        self.assertFalse(statement('I',frozenset({0}),frozenset()))
    def test_illegal_simple_conversion(self):
        s,p=frozenset({0}),frozenset({0,1})
        self.assertTrue(statement('A',s,p));self.assertFalse(statement('A',p,s))
        self.assertTrue(statement('O',p,s));self.assertFalse(statement('O',s,p))
    def test_baroco_reductio(self):
        for n in range(4):
            for s,p,m in models(n):
                if statement('A',p,m) and statement('O',s,m):
                    self.assertFalse(statement('A',s,p))
                    self.assertTrue(statement('O',s,p))
    def test_bocardo_reductio(self):
        for n in range(4):
            for s,p,m in models(n):
                if statement('O',m,p) and statement('A',m,s):
                    self.assertFalse(statement('A',s,p))
                    self.assertTrue(statement('O',s,p))
    def test_camestres_conclusion_conversion(self):
        for n in range(4):
            for s,p,m in models(n):
                if statement('A',p,m) and statement('E',s,m):
                    self.assertTrue(statement('E',m,s))
                    self.assertTrue(statement('E',p,s))
                    self.assertTrue(statement('E',s,p))
    def test_disamis_conclusion_conversion(self):
        for n in range(4):
            for s,p,m in models(n):
                if statement('I',m,p) and statement('A',m,s):
                    self.assertTrue(statement('I',p,m))
                    self.assertTrue(statement('I',p,s))
                    self.assertTrue(statement('I',s,p))
    def test_two_particular_premisses_fail(self):
        # Different witnesses: some S is M, some M is P does not give some S is P.
        s,p,m=map(frozenset,({0},{1},{0,1}))
        self.assertTrue(statement('I',s,m));self.assertTrue(statement('I',m,p))
        self.assertFalse(statement('I',s,p))

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(IndependentChecks))
    print(json.dumps({'object_models':sum(8**n for n in range(4)), 'mood_model_checks':3*64*sum(8**n for n in range(4)), 'author_truth_comparisons':24*sum(8**n for n in range(4)), 'representation':'direct object subsets, n=0..3','finite_checks_are_not_general_proofs':True},sort_keys=True))
    raise SystemExit(0 if result.wasSuccessful() else 1)
