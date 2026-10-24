"""Independent finite oracle: bit violations rather than subset chains."""
import sys
from pathlib import Path
import unittest
from itertools import product
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from model import Slice, summarize, event_summary, continuation, enumerate_models

def to_set(mask):
    return frozenset(i for i in (0, 1) if mask >> i & 1)

def bit_row(a, b, c):
    return not (b & ~a), not (c & ~b), not (c & ~a)

class IndependentTests(unittest.TestCase):
    def test_all_traces_with_bit_violations(self):
        count = mismatch = both = failures = upgrade = nonall = 0
        for masks in product(range(4), repeat=6):
            rows = (bit_row(*masks[:3]), bit_row(*masks[3:]))
            expected = tuple(rows[0][j] and rows[1][j] for j in range(3))
            trace = (Slice(*(to_set(x) for x in masks[:3])), Slice(*(to_set(x) for x in masks[3:])))
            actual = summarize(trace)
            mismatch += tuple(actual[k] for k in ('major_all', 'minor_all', 'conclusion_all')) != expected
            self.assertEqual(actual['conclusion_failure_times'], [i for i in range(2) if not rows[i][2]])
            self.assertEqual(actual['premise_failure_times'], {'major':[i for i in range(2) if not rows[i][0]], 'minor':[i for i in range(2) if not rows[i][1]]})
            both += expected[0] and expected[1]
            failures += expected[0] and expected[1] and not expected[2]
            nonall += not expected[2]
            upgrade += rows[0][0] and rows[0][1] and not expected[2]
            count += 1
        self.assertEqual((count,mismatch,both,failures,nonall,upgrade), (4096,0,256,0,2800,448))
    def test_event_bit_oracle(self):
        for h, e in product(range(8), repeat=2):
            hs = tuple(bool(h >> i & 1) for i in range(3))
            es = tuple(bool(e >> i & 1) for i in range(3))
            r = event_summary(hs, es)
            self.assertEqual(r, {'conditional_all': not (h & ~e), 'event_all': e == 7, 'event_some': e != 0, 'trigger_some': h != 0})
    def test_reverse_implication_fails_with_nonempty_conclusion(self):
        f = frozenset
        r = summarize((Slice(f({0}), f({0}), f({0})), Slice(f({0}), f(), f({0}))))
        self.assertTrue(r['conclusion_all'])
        self.assertFalse(r['minor_all'])
    def test_failed_premise_identity_alternates(self):
        f = frozenset
        r = summarize((Slice(f(), f({0}), f({0})), Slice(f(), f(), f({0}))))
        self.assertEqual(r['premise_failure_times'], {'major':[0], 'minor':[1]})
        self.assertEqual(r['conclusion_failure_times'], [0,1])
    def test_condition_law_neither_permanence_nor_existence(self):
        r = event_summary((True, False), (True, False))
        self.assertTrue(r['conditional_all']); self.assertFalse(r['event_all'])
        r = event_summary((False, False), (False, False))
        self.assertTrue(r['conditional_all']); self.assertFalse(r['event_some'])
    def test_prefixes_at_boundary_and_remote_index(self):
        for n in range(12):
            p = (True,) * n
            for i in range(n):
                self.assertEqual(continuation(p, True, i), continuation(p, False, i))
            for i in (n, n+1, 10**30):
                self.assertTrue(continuation(p, True, i))
                self.assertFalse(continuation(p, False, i))
    def test_rejected_inputs(self):
        for args in (((),()), ((True,),()), ((1,), (True,))):
            with self.assertRaises(ValueError): event_summary(*args)
        with self.assertRaises(ValueError): summarize(())
        for i in (-1, True, 1.5):
            with self.assertRaises(ValueError): continuation((True,), False, i)
    def test_production_output_counts(self):
        r = enumerate_models()
        self.assertEqual(r['temporal_models'], {'traces':4096,'oracle_mismatches':0,'both_premises_all':256,'preservation_failures':0,'conclusion_not_all':2800,'contrapositive_failures':0,'snapshot_upgrade_counterexamples':448})
        self.assertEqual((r['event_cases'],r['event_oracle_mismatches']), (64,0))

if __name__ == '__main__': unittest.main(verbosity=2)
