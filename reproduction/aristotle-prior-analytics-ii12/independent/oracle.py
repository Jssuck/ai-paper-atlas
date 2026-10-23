#!/usr/bin/env python3
"""Independent explicit-set oracle. Does not import production evaluator."""
from itertools import product
from pathlib import Path
import json
import unittest

KINDS='UEIO'
NEG={'U':'O','O':'U','E':'I','I':'E'}

def truth(model, proposition):
    kind, predicate, subject = proposition
    p,s=model[predicate],model[subject]
    if kind=='U': return s <= p
    if kind=='E': return not (s & p)
    if kind=='I': return bool(s & p)
    if kind=='O': return bool(s - p)
    raise ValueError(kind)

def models(nonempty=False):
    # All labelled universes of sizes 1,2,3. At most three existential
    # requirements occur in a two-premise counterexample.
    for n in range(1,4):
        subsets=[frozenset(i for i in range(n) if mask & (1<<i)) for mask in range(1<<n)]
        for values in product(subsets, repeat=3):
            if not nonempty or all(values):
                yield dict(zip('ABC',values))

def entails(premises, conclusion, nonempty=False):
    for m in models(nonempty):
        if all(truth(m,p) for p in premises) and not truth(m,conclusion):
            return False, m
    return True,None

def run():
    counts={}
    for nonempty in (False,True):
        rows=[]
        for q,p,r in product(KINDS,repeat=3):
            h=(NEG[q],'A','B'); prem=(p,'A','C'); result=(r,'C','B')
            ok,cm=entails((h,prem),result,nonempty)
            background=(NEG[r],'C','B')
            background_sat=any(truth(m,prem) and truth(m,background) for m in models(nonempty))
            target_ok,_=entails((prem,background),(q,'A','B'),nonempty)
            if ok and not target_ok: raise RuntimeError('unsound reductio')
            rows.append({'target':q,'premise':p,'result':r,'valid_internal':ok,'background_satisfiable':background_sat,'target_entailed':target_ok,
                         'counterexample':None if cm is None else {k:sorted(v) for k,v in cm.items()}})
        counts['nonempty' if nonempty else 'empty_allowed']={'models':sum(1 for _ in models(nonempty)), 'rows':rows,'valid_routes':sum(x['valid_internal'] and x['background_satisfiable'] for x in rows)}
    return counts

class Checks(unittest.TestCase):
    def test_four_routes(self):
        for q,p,r in [('U','U','O'),('I','U','E'),('E','E','O'),('O','E','E')]:
            for ne in (False,True):
                self.assertTrue(entails(((NEG[q],'A','B'),(p,'A','C')),(r,'C','B'),ne)[0])
                self.assertTrue(entails(((p,'A','C'),(NEG[r],'C','B')),(q,'A','B'),ne)[0])
    def test_wrong_strength(self):
        for ne in (False,True):
            self.assertFalse(entails((('I','A','B'),),('U','A','B'),ne)[0])
            self.assertFalse(entails((('O','A','B'),),('E','A','B'),ne)[0])
    def test_empty_background(self):
        m={'A':frozenset(),'B':frozenset(),'C':frozenset({0})}
        self.assertTrue(truth(m,('U','C','B')))
        self.assertTrue(truth(m,('E','C','B')))
    def test_particular_coexistence(self):
        m={'A':frozenset({0}),'B':frozenset({0,1}),'C':frozenset({0})}
        self.assertTrue(truth(m,('I','A','B')) and truth(m,('O','A','B')))
    def test_universal_background_stronger(self):
        self.assertTrue(entails((('U','A','C'),('U','C','B')),('U','A','B'))[0])
    def test_negations(self):
        for m in models():
            for q in KINDS:
                self.assertNotEqual(truth(m,(q,'A','B')),truth(m,(NEG[q],'A','B')))

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Checks)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():raise SystemExit(1)
    data=run()
    Path('oracle-results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:{'models':v['models'],'candidates':len(v['rows']),'valid_routes':v['valid_routes']} for k,v in data.items()},sort_keys=True))

# A separate pass covers every occupied unary type, including the outside type.
# Unlike production's bit tests, predicates are explicit sets of truth triples.
TRIPLES=list(product((False,True),repeat=3))
def support_models(policy):
    for occupancy in product((False,True),repeat=8):
        domain=[t for t,occupied in zip(TRIPLES,occupancy) if occupied]
        if not domain:continue
        model={name:frozenset(t for t in domain if t[i]) for i,name in enumerate('ABC')}
        if policy=='all_nonempty' and not all(model.values()):continue
        if policy=='B_nonempty' and not model['B']:continue
        ids=sorted(int(t[0])+2*int(t[1])+4*int(t[2]) for t in domain)
        yield model,ids

def independent_record(premises,conclusion,policy):
    relevant=[(m,ids) for m,ids in support_models(policy) if all(truth(m,p) for p in premises)]
    counters=[ids for m,ids in relevant if not truth(m,conclusion)]
    counters.sort(key=lambda x:(len(x),x))
    return {'valid':not counters,'premise_models':len(relevant),'countermodels':len(counters),'minimal_countermodel':counters[0] if counters else None}

if __name__=='__main__':
    production=json.loads((Path(__file__).resolve().parents[1]/'evidence/results-normal.json').read_text())
    comparisons=0
    for section in production['policies']:
        policy=section['policy']
        for row in section['rows']:
            for key,ps,c in [('internal',[row['hypothesis'],row['other']],row['result']),('external',[row['other'],row['known']],row['target'])]:
                expected=independent_record(ps,c,policy)
                if expected!=row[key]:raise RuntimeError((policy,key,row,expected))
                comparisons+=1
    for case in production['named_checks']:
        expected=independent_record(case['premises'],case['conclusion'],case['policy'])
        if any(case[k]!=v for k,v in expected.items()):raise RuntimeError((case,expected))
    print(json.dumps({'production_records_matched':comparisons,'named_checks_matched':len(production['named_checks']),'minimal_countermodels':'independently matched, cardinality then lexicographic'}))
