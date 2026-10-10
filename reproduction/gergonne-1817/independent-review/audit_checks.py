"""Independent review: source fixtures, symbolic constraints and concrete objects.

Run from the package root: python independent-review/audit_checks.py
No installation, network, model-checker oracle, or downloaded code required.
"""
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import gergonne as impl
import reproduce

# Manually transcribed source expectations, not values produced by the software.
# D normalizes the source's reversed C. Original printed pages: 198, 213, 216, 219.
TABLE213 = {
    'H': 'HH HX HI HC HD XH XX XC IH CH DH DX DC'.split(),
    'X': 'HH HX HD XH XX XI XC XD IX CH CX CD DX DC'.split(),
    'I': 'HH XX II CD DC'.split(),
    'C': 'HH XH XX XC IC CH CX CI CC CD DC'.split(),
    'D': 'HH HX HD XX XD ID CD DX DI DC DD'.split(),
}
# p.216 actually prints CH in the N row. This is the corrected semantic
# table: p.217 explicitly prints reversed-C H, normalized here as DH.
TABLE216 = {
    'A': 'II IC CI CC'.split(),
    'N': 'HI HC IH DH'.split(),
    'a': 'XI XD IX II IC ID CX CI CC CD DI DD'.split(),
    'n': 'HX HI HC HD XI XD IH IX ID DH DX DI DD'.split(),
}
TABLE216_PRINTED = {**TABLE216, 'N': 'HI HC IH CH'.split()}
TABLE219 = {
    1: 'AAA NAN AAa Aaa NAn Nan'.split(),
    2: 'ANN AAa aAa NAn ANn Nan'.split(),
    3: 'NAN ANN ANn Ann NAn Nan'.split(),
    4: 'AAa aAa Aaa NAn nAn Nan'.split(),
}
TABLE198 = {'H': 'Nn', 'X': 'an', 'I': 'Aa', 'C': 'Aa', 'D': 'an'}
NAMES = ('P', 'M', 'G')
DIRECTIONS = {1: ((1, 2), (0, 1)), 2: ((2, 1), (1, 0)),
              3: ((2, 1), (0, 1)), 4: ((1, 2), (1, 0))}
ASSIGNMENTS = tuple(product((False, True), repeat=3))
INSIDE = tuple(a for a in ASSIGNMENTS if any(a))
NEGATION = dict(A='n', N='a', a='N', n='A')


def memberships():
    """Boolean tuples and combinations; no production Model or mask generator."""
    for size in range(8):
        yield from combinations(INSIDE, size)


def truth(kind, pair, objects):
    s, t = pair
    hits = sum(bool(x[s] and x[t]) for x in objects)
    misses = sum(bool(x[s] and not x[t]) for x in objects)
    return {'A': misses == 0, 'N': hits == 0, 'a': hits > 0, 'n': misses > 0}[kind]


def exact_relation(pair, objects):
    s, t = pair
    profile = (any(x[s] and not x[t] for x in objects),
               any(x[s] and x[t] for x in objects),
               any(x[t] and not x[s] for x in objects))
    return {(True, False, True): 'H', (True, True, True): 'X',
            (False, True, False): 'I', (False, True, True): 'C',
            (True, True, False): 'D'}[profile]


def source_triples():
    return {pair + tail for tail, pairs in TABLE213.items() for pair in pairs}


def source_valid():
    return {f'{f}:{word}' for f, words in TABLE219.items() for word in words}


def constraint_minimum(figure, word, nonempty=True):
    """SAT of premises plus denied conclusion, via witness obligations.

    Universals ban individual membership assignments. Each particular needs
    one surviving assignment, and nonempty semantics adds three obligations.
    There are no relations between objects, so obligations can be witnessed
    separately. This decision does not enumerate occupancy models or call the
    implementation's proposition/model/validity functions.
    """
    allowed = set(ASSIGNMENTS)
    obligations = []
    if nonempty:
        obligations.extend({a for a in ASSIGNMENTS if a[i]} for i in range(3))
    literals = list(zip(word[:2], DIRECTIONS[figure]))
    literals.append((NEGATION[word[2]], (0, 2)))
    for kind, (s, t) in literals:
        satisfying_region = {a for a in ASSIGNMENTS if a[s] and (a[t] if kind in 'Na' else not a[t])}
        if kind in 'AN':
            allowed.difference_update(satisfying_region)
        else:
            obligations.append(satisfying_region)
    if any(not (allowed & needed) for needed in obligations):
        return None
    # Exact minimum number of occupied regions satisfying all witness demands.
    for size in range(len(allowed) + 1):
        if any(all(set(chosen) & needed for needed in obligations)
               for chosen in combinations(allowed, size)):
            return size
    raise AssertionError('witness constraints inconsistent with satisfiability check')


def parsed_literal(text):
    match = re.fullmatch(r'([ANan])\(([PMG]),([PMG])\)', text)
    if not match:
        raise ValueError(text)
    k, s, t = match.groups()
    return k, (NAMES.index(s), NAMES.index(t))


class IndependentAudit(unittest.TestCase):
    def test_01_membership_partition_and_source_54(self):
        all_patterns = list(memberships())
        nonempty = [o for o in all_patterns if all(any(a[t] for a in o) for t in range(3))]
        self.assertEqual(len(all_patterns), 128)
        self.assertEqual(len(nonempty), 109)
        triples = Counter(''.join(exact_relation(pair, o) for pair in ((1, 2), (0, 1), (0, 2)))
                          for o in nonempty)
        self.assertEqual(set(triples), source_triples())
        self.assertEqual(len(triples), 54)
        self.assertEqual(triples['XXX'], 26)
        self.assertEqual({''.join(impl.relation_triple(m)) for m in impl.models()}, source_triples())
        for objects in all_patterns:
            mask = sum(1 << (sum((1 << i) for i, yes in enumerate(a) if yes) - 1) for a in objects)
            m = impl.Model(mask)
            for s, t in product(range(3), repeat=2):
                for k in 'ANan':
                    self.assertEqual(truth(k, (s, t), objects),
                                     impl.Literal(k, NAMES[s], NAMES[t]).holds(m))

    def test_02_source_truth_and_composition_tables(self):
        fixture = json.loads((ROOT / 'source_tables.json').read_text())['section55']
        self.assertEqual(fixture['printed_premise_pairs_by_conclusion'], TABLE216_PRINTED)
        self.assertEqual(fixture['proposed_emended_premise_pairs_by_conclusion'], TABLE216)
        for relation, expected in TABLE198.items():
            for model in impl.models():
                if impl.relation(model.term('P'), model.term('G')) == relation:
                    self.assertEqual(''.join(k for k in 'ANan' if impl.Literal(k, 'P', 'G').holds(model)), expected)
        for kind, expected_pairs in TABLE216.items():
            derived = set()
            for a, b in product('HXICD', repeat=2):
                possible = {t[2] for t in source_triples() if t[:2] == a + b}
                self.assertTrue(possible)
                if all(kind in TABLE198[r] for r in possible):
                    derived.add(a + b)
            self.assertEqual(derived, set(expected_pairs))

    def test_03_symbolic_constraints_all_512_validity_cases(self):
        for nonempty in (True, False):
            valid = set()
            for f in range(1, 5):
                for letters in product('ANan', repeat=3):
                    word = ''.join(letters)
                    minimum = constraint_minimum(f, word, nonempty)
                    mood = impl.Mood(f, *word)
                    witness = impl.countermodel(mood, nonempty)
                    self.assertEqual(minimum is None, witness is None, (mood.id, nonempty))
                    if minimum is None:
                        valid.add(mood.id)
                    else:
                        self.assertEqual(len(witness.atoms), minimum, (mood.id, nonempty))
            self.assertEqual(valid, {m.id for m in impl.valid_moods(nonempty)})
            self.assertEqual(len(valid), 24 if nonempty else 15)
            if nonempty:
                self.assertEqual(valid, source_valid())
                self.assertEqual(valid, {m.id for m in impl.candidates() if not impl.rule59_violations(m)})

    def test_04_four_object_universe_independent_truth(self):
        # 16^3 = 4096 concrete triples, including empties; 15^3 = 3375 nonempty.
        # This is a crosscheck only, not the completeness proof.
        counterexamples = {False: set(), True: set()}
        for P, M, G in product(range(16), repeat=3):
            sets = [tuple(bool(bits & (1 << j)) for j in range(4)) for bits in (P, M, G)]
            objects = tuple(zip(*sets))
            values = {(k, pair): truth(k, pair, objects)
                      for k in 'ANan' for pair in ((1, 2), (0, 1), (2, 1), (1, 0), (0, 2))}
            for f, pairs in DIRECTIONS.items():
                for major, minor, conclusion in product('ANan', repeat=3):
                    if values[major, pairs[0]] and values[minor, pairs[1]] and not values[conclusion, (0, 2)]:
                        mid = f'{f}:{major}{minor}{conclusion}'
                        counterexamples[False].add(mid)
                        if all((P, M, G)):
                            counterexamples[True].add(mid)
        ids = {f'{f}:{a}{b}{c}' for f in range(1, 5) for a, b, c in product('ANan', repeat=3)}
        self.assertEqual(ids - counterexamples[True], source_valid())
        self.assertEqual(ids - counterexamples[False], {m.id for m in impl.valid_moods(False)})

    def test_05_every_published_countermodel_and_minimum(self):
        records = json.loads((ROOT / 'results' / 'invalid_countermodels_232.json').read_text())
        self.assertEqual(len(records), 232)
        self.assertEqual(len({r['id'] for r in records}), 232)
        for r in records:
            f, word = r['id'].split(':')
            terms = r['countermodel']['terms']
            universe = set().union(*map(set, terms.values()))
            objects = tuple(tuple(x in terms[t] for t in NAMES) for x in universe)
            self.assertTrue(all(terms[t] for t in NAMES))
            p1, p2 = DIRECTIONS[int(f)]
            self.assertTrue(truth(word[0], p1, objects))
            self.assertTrue(truth(word[1], p2, objects))
            self.assertFalse(truth(word[2], (0, 2), objects))
            self.assertEqual(len(universe), constraint_minimum(int(f), word))
        self.assertEqual(max(r['countermodel']['size'] for r in records), 3)

    def test_06_graph_reductions_and_four_certificates(self):
        record = reproduce.reductions_record()
        self.assertEqual(record['counts'], [24, 14, 11, 6, 2])
        self.assertEqual(record['six_closure_size'], 24)
        self.assertEqual([m.original_ascii for m in impl.SIX],
                         ['A A A', 'N A N', 'A ra a', 'N a n', 'rA n n', 'n rA n'])
        groups = record['with_conclusion_conversion_classes']
        edges = record['class_subsumption_edges']
        remaining = set(range(len(groups)))
        while remaining:
            roots = {i for i in remaining if not any(a in remaining and b == i for a, b in edges)}
            self.assertTrue(roots, 'subsumption graph contains a directed cycle')
            remaining -= roots
        certificates = record['four_reductio_certificates']
        self.assertEqual(len(certificates), 4)
        for c in certificates:
            major, minor, conclusion = map(parsed_literal, c['target_literals'])
            denied = parsed_literal(c['deny_conclusion'])
            self.assertEqual(denied, (NEGATION[conclusion[0]], conclusion[1]))
            available = {major, minor, denied}
            if c['simple_conversion']:
                before, after = map(parsed_literal, c['simple_conversion'].split(' -> '))
                self.assertIn(before, available)
                self.assertIn(before[0], 'Na')
                self.assertEqual(after, (before[0], before[1][::-1]))
                available.add(after)
            base1, base2 = map(parsed_literal, c['base_premises'])
            self.assertIn(base1, available)
            self.assertIn(base2, available)
            self.assertIn(base1[0], 'AN')
            self.assertEqual(base2[0], 'A')
            self.assertEqual(base1[1][0], base2[1][1])
            derived = parsed_literal(c['derived'])
            self.assertEqual(derived, (base1[0], (base2[1][0], base1[1][1])))
            contradicted = parsed_literal(c['contradicts_original_premise'])
            self.assertIn(contradicted, (major, minor))
            self.assertEqual(derived, (NEGATION[contradicted[0]], contradicted[1]))

    def test_07a_page216_printed_CH_is_not_a_valid_N_pair(self):
        # Nonempty M={m}, P={p}, G={m,p}: exact pair CH, but N(P,G) is false.
        objects = ((False, True, True), (True, False, True))
        self.assertEqual(exact_relation((1, 2), objects), 'C')
        self.assertEqual(exact_relation((0, 1), objects), 'H')
        self.assertFalse(truth('N', (0, 2), objects))
        self.assertIn('DH', TABLE216['N'])
        self.assertNotIn('CH', TABLE216['N'])

    def test_08_fresh_output_matches_published_results(self):
        with tempfile.TemporaryDirectory() as directory:
            fresh = Path(directory)
            reproduce.create_results(fresh)
            generated = {p.name: p.read_bytes() for p in fresh.iterdir()}
            self.assertEqual(set(generated), {
                'models_109.json', 'moods_256.json', 'invalid_countermodels_232.json',
                'relations_54.csv', 'relation_composition_25.csv', 'reductions.json',
                'original_examples.json', 'empty_term_boundary.json', 'summary.json'})
            for name, content in generated.items():
                self.assertEqual(content, (ROOT / 'results' / name).read_bytes(), name)
            reproduce.create_results(fresh)
            self.assertEqual(generated, {p.name: p.read_bytes() for p in fresh.iterdir()})

    def test_07_published_examples_retain_original_directions(self):
        examples = json.loads((ROOT / 'results' / 'original_examples.json').read_text())
        self.assertEqual(examples['section51']['premises'], ['A(G,M)', 'N(M,P)'])
        self.assertEqual(examples['section52']['premises'], ['A(M,G)', 'N(M,P)'])
        self.assertEqual(examples['section51']['relation_pairs'], ['DH', 'IH'])
        self.assertEqual(examples['section52']['relation_pairs'], ['CH', 'IH'])
        self.assertEqual(examples['section51']['entailed_conclusion_kinds'], ['N', 'n'])
        self.assertEqual(examples['section52']['entailed_conclusion_kinds'], [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
