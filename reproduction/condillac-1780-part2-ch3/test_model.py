"""Authored tests: finite enumeration checks implementations, not historical claims."""
import itertools
import unittest
from dataclasses import replace
from model import (HypothesisSpace, Rule, HornSystem, ClosureResult, Derivation,
                   Vocabulary, aligned_dictionary, translation_preserves,
                   translate_atoms, inverse_dictionary, rename_rule, task_exact)


def powerset(items):
    items = tuple(items)
    return tuple(frozenset(combo) for k in range(len(items) + 1)
                 for combo in itertools.combinations(items, k))


def oracle_closure(universe, rules, seeds):
    # Definition-level finite intersection, not forward chaining.
    supersets = [candidate for candidate in powerset(universe)
                 if seeds <= candidate and all(not r.premises <= candidate or
                                                r.conclusion in candidate for r in rules)]
    return frozenset.intersection(*supersets)


class HypothesisTests(unittest.TestCase):
    def setUp(self):
        self.space = HypothesisSpace(('x', 'y', 'z'), (
            ('true', ('0', '0', '1')), ('twin', ('0', '0', '0')), ('other', ('1', '1', '1'))))

    def test_filter_exact(self):
        self.assertEqual(self.space.candidates([]), {'true', 'twin', 'other'})
        self.assertEqual(self.space.candidates([('x', '0')]), {'true', 'twin'})
        self.assertEqual(self.space.candidates([('x', '0'), ('z', '1')]), {'true'})

    def test_detect_not_identify(self):
        self.assertNotIn('other', self.space.candidates([('x', '0')]))
        self.assertFalse(self.space.distinguishes(('x', 'y')))
        self.assertTrue(self.space.distinguishes(('x', 'z')))
        duplicate = HypothesisSpace(('x',), (('a', ('0',)), ('b', ('0',))))
        self.assertFalse(duplicate.distinguishes(('x',)))

    def test_noise_budget(self):
        data = [('x', '1'), ('y', '0'), ('z', '1')]
        self.assertEqual(self.space.candidates(data), frozenset())
        self.assertEqual(self.space.candidates(data, 1), {'true', 'other'})
        self.assertEqual(self.space.candidates([('x', '1'), ('x', '1')], 1), {'other'})

    def test_truth_absent_and_noisy_singleton(self):
        missing = HypothesisSpace(('x', 'y'), (('bad', ('0', '0')),))
        self.assertEqual(missing.candidates([('x', '0')]), {'bad'})
        self.assertEqual(missing.candidates([('x', '0'), ('y', '1')]), set())
        self.assertEqual(self.space.candidates([('x', '1')]), {'other'})

    def test_filter_exhaustive(self):
        points = ('x', 'y', 'z')
        rows = tuple((str(i), row) for i, row in enumerate(itertools.product('01', repeat=3)))
        observations = tuple(itertools.product(points, '01'))
        sequences = ((),) + tuple((o,) for o in observations) + tuple(itertools.product(observations, repeat=2))
        count = 0
        for selected in powerset(range(8)):
            if not selected:
                continue
            hs = HypothesisSpace(points, tuple(rows[i] for i in sorted(selected)))
            for data in sequences:
                for budget in range(3):
                    expected = set()
                    for key, values in hs.rows:
                        predictions = dict(zip(points, values))
                        disagreements = [x for x, y in data if predictions[x] != y]
                        if len(disagreements) <= budget:
                            expected.add(key)
                    self.assertEqual(hs.candidates(data, budget), expected)
                    if data:
                        self.assertLessEqual(hs.candidates(data, budget), hs.candidates(data[:-1], budget))
                    count += 1
            for subset in powerset(points):
                signatures = [tuple(row[points.index(x)] for x in sorted(subset)) for _, row in hs.rows]
                self.assertEqual(hs.distinguishes(sorted(subset)), len(signatures) == len(set(signatures)))
                for truth, values in hs.rows:
                    data = tuple((x, values[points.index(x)]) for x in sorted(subset))
                    self.assertIn(truth, hs.candidates(data))
                    if hs.distinguishes(sorted(subset)):
                        self.assertEqual(hs.candidates(data), {truth})
        self.assertEqual(count, 32895)

    def test_validation_and_snapshot(self):
        points, rows = ['x'], [['h', ['0']]]
        hs = HypothesisSpace(points, rows)
        points.append('y'); rows[0][1][0] = '1'
        self.assertEqual(hs.candidates([('x', '0')]), {'h'})
        for bad in [True, -1, 1.0, '1']:
            with self.assertRaises(ValueError):
                hs.candidates([], bad)
        for bad in [[('unknown', '0')], [('x', '9'), ('unknown', '0')], [('x',)], 'x']:
            with self.assertRaises(ValueError):
                hs.candidates(bad)
        for points, rows in [((), ()), (('x', 'x'), (('a', ('0', '0')),)),
                             (('x',), (('a', ()),)), (('x',), (('a', ('0',)), ('a', ('1',))))]:
            with self.assertRaises(ValueError):
                HypothesisSpace(points, rows)
        with self.assertRaises(ValueError):
            hs.distinguishes(('unknown',))


class HornTests(unittest.TestCase):
    def test_chain_and_idempotence(self):
        system = HornSystem(('a', 'b', 'c'), (Rule('bc', {'b'}, 'c'), Rule('ab', {'a'}, 'b')))
        result = system.close({'a'})
        self.assertEqual(result.atoms, {'a', 'b', 'c'})
        self.assertEqual([step.conclusion for step in result.steps], ['b', 'c'])
        self.assertTrue(system.verify_trace(result, {'a'}))
        again = system.close(result.atoms)
        self.assertEqual(again.atoms, result.atoms)
        self.assertEqual(again.steps, ())

    def test_conjunction(self):
        system = HornSystem(('a', 'b', 'c'), (Rule('ab-c', {'a', 'b'}, 'c'),))
        self.assertEqual(system.close({'a'}).atoms, {'a'})
        self.assertEqual(system.close({'a', 'b'}).atoms, {'a', 'b', 'c'})

    def test_unreachable(self):
        system = HornSystem(('a', 'b', 'c'), (Rule('ab', {'a'}, 'b'),))
        self.assertEqual(system.close({'a'}).atoms, {'a', 'b'})

    def test_cycles_and_empty_body(self):
        system = HornSystem(('a', 'b', 'c'), (Rule('ab', {'a'}, 'b'), Rule('ba', {'b'}, 'a')))
        self.assertEqual(system.close(set()).atoms, set())
        self.assertEqual(system.close({'a'}).atoms, {'a', 'b'})
        fact = HornSystem(('a',), (Rule('fact', set(), 'a'),))
        self.assertEqual(fact.close(set()).atoms, {'a'})
        empty = HornSystem((), ())
        self.assertTrue(empty.verify_trace(empty.close(set()), set()))

    def test_false_seed_and_sound_rules(self):
        system = HornSystem(('rain', 'wet', 'slip'), (Rule('r-w', {'rain'}, 'wet'), Rule('w-s', {'wet'}, 'slip')))
        true_atoms = frozenset()
        self.assertTrue(system.closed(true_atoms))
        result = system.close({'rain'})
        self.assertTrue(system.verify_trace(result, {'rain'}))
        self.assertEqual(result.atoms - true_atoms, {'rain', 'wet', 'slip'})

    def test_forged_trace(self):
        system = HornSystem(('a', 'b', 'c'), (Rule('ab', {'a'}, 'b'), Rule('bc', {'b'}, 'c')))
        good = system.close({'a'})
        forged = replace(good, steps=(Derivation('ab', ('c',), 'b'),) + good.steps[1:])
        with self.assertRaises(ValueError):
            system.verify_trace(forged, {'a'})
        for bad in [replace(good, seeds=frozenset()),
                    replace(good, steps=good.steps[::-1]),
                    replace(good, steps=good.steps + good.steps[:1]),
                    replace(good, steps=()),
                    ClosureResult(frozenset({'a'}), (), frozenset({'a'})),
                    replace(good, steps=(Derivation('missing', ('a',), 'b'),)),
                    replace(good, atoms=frozenset({'alien'}))]:
            with self.assertRaises(ValueError):
                system.verify_trace(bad, {'a'})

    def test_horn_exhaustive(self):
        atoms = ('a', 'b', 'c')
        all_rules = tuple(Rule(str(i), premise, conclusion) for i, (premise, conclusion)
                          in enumerate(itertools.product(powerset(atoms), atoms)))
        rule_sets = ((),) + tuple((r,) for r in all_rules) + tuple(itertools.combinations(all_rules, 2))
        cases = 0
        for rules in rule_sets:
            system = HornSystem(atoms, rules)
            closures = {}
            for seeds in powerset(atoms):
                result = system.close(seeds)
                self.assertEqual(result.atoms, oracle_closure(atoms, rules, seeds))
                self.assertLessEqual(seeds, result.atoms)
                self.assertLessEqual(len(result.steps), len(atoms) - len(seeds))
                self.assertTrue(system.verify_trace(result, seeds))
                self.assertEqual(system.close(result.atoms).atoms, result.atoms)
                self.assertEqual(HornSystem(atoms, rules[::-1]).close(seeds).atoms, result.atoms)
                closures[seeds] = result.atoms
                for truth in powerset(atoms):
                    if seeds <= truth and system.closed(truth):
                        self.assertLessEqual(result.atoms, truth)
                cases += 1
            for smaller, larger in itertools.product(closures, repeat=2):
                if smaller <= larger:
                    self.assertLessEqual(closures[smaller], closures[larger])
        self.assertEqual(cases, 2408)

    def test_validation_and_snapshot(self):
        body = {'a'}
        rule = Rule('r', body, 'b'); body.add('c')
        self.assertEqual(rule.premises, {'a'})
        for args in [(('a', 'a'), ()), (('a',), (rule,)),
                     (('a', 'b'), (rule, rule)), (('a',), ('bad',))]:
            with self.assertRaises(ValueError):
                HornSystem(*args)
        system = HornSystem(('a',), ())
        for bad in [{'x'}, 'a', [True], None]:
            with self.assertRaises(ValueError):
                system.close(bad)


class TranslationTests(unittest.TestCase):
    def setUp(self):
        self.a = Vocabulary((('rain', 'rain'), ('wet', 'wet'), ('dry', 'dry')))
        self.b = Vocabulary((('rain', 'lluvia'), ('wet', 'mojado'), ('dry', 'seco')))
        self.correct = aligned_dictionary(self.a, self.b)
        self.wrong = {'rain': 'lluvia', 'wet': 'seco', 'dry': 'mojado'}

    def test_correct_dictionary(self):
        self.assertTrue(translation_preserves(self.a, self.b, self.correct))
        for meanings in powerset(self.a.meanings):
            self.assertEqual(self.b.decode(translate_atoms(self.a.encode(meanings), self.correct)), meanings)

    def test_wrong_dictionary(self):
        self.assertFalse(translation_preserves(self.a, self.b, self.wrong))
        inverse = inverse_dictionary(self.wrong)
        self.assertEqual(translate_atoms(translate_atoms({'wet'}, self.wrong), inverse), {'wet'})
        self.assertEqual(self.b.decode(translate_atoms({'wet'}, self.wrong)), {'dry'})

    def test_wrong_dictionary_closure(self):
        rule = Rule('r-w', {'rain'}, 'wet')
        source = HornSystem(tuple(self.a.words), (rule,))
        genuine = HornSystem(tuple(self.b.words), (rename_rule(rule, self.correct),))
        transported_wrong = HornSystem(tuple(self.b.words), (rename_rule(rule, self.wrong),))
        left = translate_atoms(source.close({'rain'}).atoms, self.wrong)
        self.assertNotEqual(left, genuine.close(translate_atoms({'rain'}, self.wrong)).atoms)
        self.assertEqual(left, transported_wrong.close(translate_atoms({'rain'}, self.wrong)).atoms)

    def test_dictionary_inverse_validation(self):
        with self.assertRaises(ValueError):
            inverse_dictionary({'a': 'x', 'b': 'x'})
        self.assertEqual(inverse_dictionary({}), {})
        for bad in [{'rain': 'lluvia'}, dict(self.correct, extra='seco'),
                    dict(self.correct, wet='alien')]:
            self.assertFalse(translation_preserves(self.a, self.b, bad))
        with self.assertRaises(ValueError):
            translate_atoms({'alien'}, self.correct)

    def test_noninjective_closure_counterexample(self):
        source = HornSystem(('a', 'b', 'c', 'd'), (Rule('ab', {'a'}, 'b'), Rule('cd', {'c'}, 'd')))
        dictionary = {'a': 'x', 'b': 'y', 'c': 'x', 'd': 'z'}
        target = HornSystem(('x', 'y', 'z'), tuple(rename_rule(r, dictionary) for r in source.rules))
        self.assertEqual(translate_atoms(source.close({'a'}).atoms, dictionary), {'x', 'y'})
        self.assertEqual(target.close({'x'}).atoms, {'x', 'y', 'z'})

    def test_renaming_exhaustive(self):
        meanings = ('a', 'b', 'c')
        semantic = HornSystem(meanings, (Rule('ab', {'a'}, 'b'), Rule('bc', {'b'}, 'c')))
        count = 0
        for wa, wb in itertools.product(itertools.permutations(('A', 'B', 'C')),
                                        itertools.permutations(('X', 'Y', 'Z'))):
            a, b = Vocabulary(tuple(zip(meanings, wa))), Vocabulary(tuple(zip(meanings, wb)))
            a_rules = tuple(rename_rule(r, dict(a.entries)) for r in semantic.rules)
            source = HornSystem(wa, a_rules)
            for outputs in itertools.permutations(wb):
                d = dict(zip(wa, outputs))
                self.assertEqual(translation_preserves(a, b, d), d == aligned_dictionary(a, b))
                target = HornSystem(wb, tuple(rename_rule(r, d) for r in a_rules))
                inverse = inverse_dictionary(d)
                for seeds in powerset(wa):
                    self.assertEqual(translate_atoms(translate_atoms(seeds, d), inverse), seeds)
                    self.assertEqual(translate_atoms(source.close(seeds).atoms, d),
                                     target.close(translate_atoms(seeds, d)).atoms)
                count += 1
        self.assertEqual(count, 216)

    def test_vocabulary_snapshot_and_validation(self):
        entries = [['a', 'A']]
        vocabulary = Vocabulary(entries); entries[0][1] = 'B'
        self.assertEqual(vocabulary.encode({'a'}), {'A'})
        for entries in [(('a', 'A'), ('b', 'A')), (('a', 'A'), ('a', 'B')), (('', 'A'),)]:
            with self.assertRaises(ValueError):
                Vocabulary(entries)
        with self.assertRaises(ValueError):
            aligned_dictionary(self.a, Vocabulary((('alien', 'word'),)))


class PrecisionTests(unittest.TestCase):
    def test_breadth_is_not_precision(self):
        worlds = ('w1', 'w2', 'w3', 'w4')
        task = dict(zip(worlds, ('safe', 'safe', 'unsafe', 'unsafe')))
        small = dict(zip(worlds, ('A', 'A', 'B', 'B')))
        larger = dict(zip(worlds, ('X', 'Y', 'X', 'Z')))
        self.assertTrue(task_exact(worlds, small, task))
        self.assertFalse(task_exact(worlds, larger, task))
        self.assertEqual(len(set(small.values())), 2)
        self.assertEqual(len(set(larger.values())), 3)

    def test_precision_refinement_exhaustive(self):
        worlds = ('a', 'b', 'c')
        maps = tuple(dict(zip(worlds, values)) for values in itertools.product('012', repeat=3))
        for labels, task in itertools.product(maps, repeat=2):
            expected = all(labels[x] != labels[y] or task[x] == task[y]
                           for x, y in itertools.product(worlds, repeat=2))
            self.assertEqual(task_exact(worlds, labels, task), expected)
            if expected:
                for finer in maps:
                    refines = all(finer[x] != finer[y] or labels[x] == labels[y]
                                  for x, y in itertools.product(worlds, repeat=2))
                    if refines:
                        self.assertTrue(task_exact(worlds, finer, task))

    def test_precision_validation(self):
        for labels, task in [({}, {'a': 'yes'}), ({'a': 'L'}, {}),
                              ({'a': 'L', 'b': 'M'}, {'a': 'yes'})]:
            with self.assertRaises(ValueError):
                task_exact(('a',), labels, task)


if __name__ == '__main__':
    unittest.main(verbosity=2)
