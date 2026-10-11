"""Independent finite-set truth oracle, expected facts, and API guard tests."""
import itertools
import json
import unittest
import euler_cvii as e


def oracle(mood, subject, predicate):
    # Python sets, intentionally separate from the bit-based implementation.
    if mood == 'A': return subject <= predicate
    if mood == 'E': return subject.isdisjoint(predicate)
    if mood == 'I': return bool(subject & predicate)
    if mood == 'O': return bool(subject - predicate)
    raise ValueError(mood)


def assignments(n):
    universe = set(range(n))
    subsets = [set(i for i in universe if mask & (1 << i))
               for mask in range(1 << n)]
    for p, q, m in itertools.product(subsets, repeat=3):
        yield {'P': p, 'Q': q, 'M': m}


class ReproductionTests(unittest.TestCase):
    def test_euler_term_roles_and_figures(self):
        self.assertEqual(e.FIGURES, {1: (('M','Q'),('P','M')),
                                     2: (('Q','M'),('P','M')),
                                     3: (('M','Q'),('M','P')),
                                     4: (('Q','M'),('M','P'))})
        self.assertEqual(e.TERMS, {'P':1,'Q':2,'M':4})
        self.assertEqual(e.argument_truth(32,'AAA2'), (True,True,False))

    def test_support_counts_and_uniqueness(self):
        self.assertEqual(len(e.supports()), 255)
        self.assertEqual(len(e.supports(True)), 218)
        self.assertEqual(set(e.supports()), set(range(1, 256)))
        self.assertEqual(len(set(e.all_forms())), 256)
        self.assertEqual(e.supports(), tuple(sorted(e.supports(), key=lambda s:(s.bit_count(),s))))

    def test_known_valid_forms(self):
        modern = set('AAA1 AII1 EAE1 EIO1 AEE2 AOO2 EAE2 EIO2 AII3 EIO3 IAI3 OAO3 AEE4 EIO4 IAI4'.split())
        extra = set('AAI1 EAO1 AEO2 EAO2 AAI3 EAO3 AAI4 AEO4 EAO4'.split())
        for nonempty, expected in ((False, modern), (True, modern | extra)):
            actual = {f for f in e.all_forms() if e.minimum_countermodel(f, nonempty) is None}
            self.assertEqual(actual, expected)

    def test_every_countermodel_and_minimality(self):
        for nonempty in (False, True):
            models = e.supports(nonempty)
            for form in e.all_forms():
                cm = e.minimum_countermodel(form, nonempty)
                false_models = [s for s in models if e.argument_truth(s, form) == (True, True, False)]
                self.assertEqual(cm, false_models[0] if false_models else None)
                if cm is not None:
                    self.assertIn(cm, models)
                    self.assertEqual(e.argument_truth(cm, form), (True, True, False))
                    self.assertTrue(all(s.bit_count() >= cm.bit_count() for s in false_models))

    def test_independent_native_set_oracle_n_le_3(self):
        # Enumerate each interpretation over labeled universes, not supports.
        invalid = {False: set(), True: set()}
        for n in range(1, 4):
            for extensions in assignments(n):
                mask = 0
                for i in range(n):
                    t = sum(bit for term, bit in e.TERMS.items() if i in extensions[term])
                    mask |= 1 << t
                for mood, s, p in itertools.product(e.MOODS, e.TERMS, e.TERMS):
                    truth = oracle(mood, extensions[s], extensions[p])
                    self.assertEqual(e.holds(mask, mood, s, p), truth)
                    sb = sum(1 << i for i in extensions[s])
                    pb = sum(1 << i for i in extensions[p])
                    self.assertEqual(e.native_holds(n, mood, sb, pb), truth)
                for f in e.all_forms():
                    major, minor = e.FIGURES[int(f[3])]
                    a = oracle(f[0], *(extensions[t] for t in major))
                    b = oracle(f[1], *(extensions[t] for t in minor))
                    c = oracle(f[2], extensions['P'], extensions['Q'])
                    self.assertEqual(e.argument_truth(mask, f), (a,b,c))
                    if a and b and not c:
                        invalid[False].add(f)
                        if all(extensions.values()): invalid[True].add(f)
        for regime in (False, True):
            self.assertEqual(invalid[regime], {f for f in e.all_forms() if e.minimum_countermodel(f, regime) is not None})

    def test_filters_necessary_not_sufficient(self):
        counts = dict(zip(e.RULES, (64,64,96,96,32)))
        for rule in e.RULES:
            violating = [f for f in e.all_forms() if rule in e.violations(f)]
            self.assertEqual(len(violating), counts[rule])
            for f in violating:
                for regime in (False,True): self.assertIsNotNone(e.minimum_countermodel(f, regime))
        self.assertEqual(sum(not e.violations(f) for f in e.all_forms()), 48)
        self.assertEqual(e.violations('AAA2'), ())
        self.assertEqual(e.minimum_countermodel('AAA2'), 32)
        self.assertEqual(e.minimum_countermodel('AAA2', True), 96)
        self.assertIn('two_particular', e.violations('III3'))

    def test_empty_classes_and_existential_import(self):
        for s,p in itertools.product(e.TERMS, repeat=2):
            self.assertTrue(e.holds(1,'A',s,p))
            self.assertTrue(e.holds(1,'E',s,p))
            self.assertFalse(e.holds(1,'I',s,p))
            self.assertFalse(e.holds(1,'O',s,p))
        self.assertIsNotNone(e.minimum_countermodel('AAI1'))
        self.assertIsNone(e.minimum_countermodel('AAI1',True))

    def test_shared_singleton_n_le_4(self):
        for n in range(1,5):
            r=e.singleton_counts(n)
            self.assertEqual(r['assignments'], n*4**n)
            self.assertEqual(r['premise_pairs_true'], n*4**(n-1))
            for key in ('counterexamples','A_I_disagreements','E_O_disagreements'):
                self.assertEqual(r[key],0)
            # Independently exhaust same-name and distinct-name alternatives.
            for sets in assignments(n):
                p,q=sets['P'],sets['Q']
                for a in range(n):
                    name={a}
                    self.assertEqual(oracle('A',name,p),oracle('I',name,p))
                    self.assertEqual(oracle('E',name,p),oracle('O',name,p))
                    if a in p and a in q: self.assertTrue(p & q)

    def test_two_witnesses_and_non_denoting_name(self):
        p,q,m={0},{1},{0,1}
        self.assertTrue(oracle('I',m,p) and oracle('I',m,q))
        self.assertFalse(oracle('I',p,q))
        n=p=q=set()  # One-point universe {0}; these extensions are empty.
        self.assertTrue(oracle('A',n,p) and oracle('A',n,q))
        self.assertFalse(oracle('I',p,q))
        # |N| >= 1 suffices for these universal premises; |N| = 1 encodes a name.
        for size in range(1,4):
            for sets in assignments(size):
                n,p,q=sets['M'],sets['P'],sets['Q']
                if n and n <= p and n <= q: self.assertTrue(p & q)

    def test_malformed_inputs(self):
        for bad in (None, True, False, 0, -1, 256, 1.0, '1', []):
            with self.assertRaises(ValueError): e.cells(bad)
        for bad in ('', 'AAAA', 'AAA0', 'AAA5', 'aaa1', 'AA1', 1, None, ['A','A','A','1']):
            for fn in (e.validate_form,e.violations,e.minimum_countermodel):
                with self.assertRaises(ValueError): fn(bad)
        for bad in (None, '', 'AE', 'X', 1, []):
            with self.assertRaises(ValueError): e.holds(1,bad,'P','Q')
            with self.assertRaises(ValueError): e.native_holds(1,bad,0,0)
        for bad in (None,'S',[],1):
            with self.assertRaises(ValueError): e.holds(1,'A',bad,'P')
            with self.assertRaises(ValueError): e.holds(1,'A','P',bad)
        for bad in (None,0,1,'true',[]):
            with self.assertRaises(ValueError): e.supports(bad)
        for args in ((0,'A',0,0),(17,'A',0,0),(True,'A',0,0),(1,'A',2,0),(1,'A',0,-1),(1,'A',False,0)):
            with self.assertRaises(ValueError): e.native_holds(*args)
        for bad in (0,5,True,None,1.0):
            with self.assertRaises(ValueError): e.singleton_counts(bad)

    def test_saved_report_and_determinism(self):
        from pathlib import Path
        actual=e.report()
        self.assertEqual(actual,e.report())
        self.assertEqual(actual,json.loads(Path(__file__).with_name('results.json').read_text()))
        for key,valid,invalid in (('modern',15,33),('all_terms_nonempty',24,24)):
            r=actual['regimes'][key]
            self.assertEqual(r['valid_count'],valid)
            self.assertEqual(r['surviving_invalid_count'],invalid)
            for v in r['per_rule'].values(): self.assertEqual(v['valid_violating_forms'],0)

if __name__ == '__main__': unittest.main(verbosity=2)
