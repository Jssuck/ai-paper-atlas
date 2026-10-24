"""External reviewer: Boolean membership tables, independent of production oracle."""
import itertools
import json
import pathlib
import sys
import unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import model


def oracle(rows):
    # Each row is A-membership, B-membership, C-membership Boolean vectors.
    rels = []
    for a, b, c in rows:
        rels.append((all(not y or x for x,y in zip(a,b)),
                     all(not z or y for y,z in zip(b,c)),
                     all(not z or x for x,z in zip(a,c))))
    return dict(actual_ab=rels[0][0], actual_bc=rels[0][1], actual_ac=rels[0][2],
                necessary_ab=all(r[0] for r in rels), necessary_bc=all(r[1] for r in rels),
                necessary_ac=all(r[2] for r in rels),
                all_terms_nonempty=all(any(t) for row in rows for t in row))


def mask(bits):
    return sum(int(v)*2**i for i,v in enumerate(bits))


class ReviewTests(unittest.TestCase):
    def test_all_4096_membership_tables(self):
        counts = dict(models=0, nonempty=0, necessary=0, actual=0, bad_route=0, nonempty_bad_route=0)
        for bits in itertools.product((False,True), repeat=12):
            vectors=[bits[i:i+2] for i in range(0,12,2)]
            rows=(vectors[:3],vectors[3:])
            expected=oracle(rows)
            actual=model.evaluate(tuple(tuple(mask(v) for v in row) for row in rows))
            self.assertEqual(actual,expected)
            counts['models']+=1
            counts['nonempty']+=expected['all_terms_nonempty']
            necessary=expected['necessary_ab'] and expected['necessary_bc']
            current=expected['actual_ab'] and expected['actual_bc']
            counts['necessary']+=necessary
            counts['actual']+=current
            if necessary: self.assertTrue(expected['necessary_ac'])
            if current: self.assertTrue(expected['actual_ac'])
            bad=current and expected['necessary_ac'] and not necessary
            counts['bad_route']+=bad
            counts['nonempty_bad_route']+=bad and expected['all_terms_nonempty']
        self.assertEqual(counts,dict(models=4096,nonempty=729,necessary=256,actual=1024,bad_route=320,nonempty_bad_route=56))
        print('independent membership enumeration:',json.dumps(counts,sort_keys=True))

    def test_nonempty_necessary_conclusion_not_route(self):
        r=model.evaluate(((1,1,1),(1,2,1)))
        self.assertTrue(r['necessary_ac'] and r['actual_ab'] and r['actual_bc'] and r['all_terms_nonempty'])
        self.assertFalse(r['necessary_ab']); self.assertFalse(r['necessary_bc'])

    def test_nonempty_contrapositive_is_not_each_premise(self):
        r=model.evaluate(((1,1,1),(2,1,1)))
        self.assertFalse(r['necessary_ac']); self.assertFalse(r['necessary_ab'])
        self.assertTrue(r['necessary_bc'] and r['all_terms_nonempty'])

    def test_single_object_disappearing_middle(self):
        r=model.evaluate(((1,1,1),(1,0,1)),size=1)
        self.assertTrue(r['necessary_ac'] and r['necessary_ab'])
        self.assertFalse(r['necessary_bc'])

    def test_negative_control_by_membership(self):
        counts={k:dict(true=0,false=0) for k in 'AEIO'}
        admissible=0
        for bits in itertools.product((False,True),repeat=9):
            a,b,c=bits[:3],bits[3:6],bits[6:]
            if not (any(a) and any(b) and any(c)): continue
            if any(x and y for x,y in zip(a,b)) or any(y and z for y,z in zip(b,c)): continue
            admissible+=1
            vals={'A':all(not z or x for x,z in zip(a,c)), 'E':not any(x and z for x,z in zip(a,c)),
                  'I':any(x and z for x,z in zip(a,c)), 'O':any(z and not x for x,z in zip(a,c))}
            for k,v in vals.items():counts[k]['true' if v else 'false']+=1
        self.assertEqual(admissible,30)
        self.assertEqual(counts,model.negative_models()['conclusions'])
        for c in counts.values():self.assertGreater(c['true'],0);self.assertGreater(c['false'],0)

    def test_validation_and_scope(self):
        for size in (0,-1,True,1.5):
            with self.assertRaises(ValueError):model.evaluate(((0,0,0),),size)
        for worlds in ((), ((1,2),), ((-1,0,0),), ((0,0,4),), ((0,0,False),)):
            with self.assertRaises(ValueError):model.evaluate(worlds)
        self.assertEqual(model.evaluate(((1,1,1),(1,1,1))),model.evaluate(((1,1,1),)))
        self.assertEqual(model.examples()['same_extension_different_explanation']['essential_or_causal_status'], 'not represented; cannot be inferred')

if __name__=='__main__':unittest.main(verbosity=2)
