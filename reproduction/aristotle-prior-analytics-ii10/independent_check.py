#!/usr/bin/env python3
"""Independent quantified pointwise oracle; imports no production evaluator."""
import itertools
import json
from pathlib import Path

TERMS = 'ABC'
TYPES = tuple(itertools.product((False, True), repeat=3))
MOODS = {'Darapti':('A','A','I'), 'Disamis':('I','A','I'),
         'Datisi':('A','I','I'), 'Felapton':('E','A','O'),
         'Bocardo':('O','A','O'), 'Ferison':('E','I','O')}
RESULTS = {'Darapti':('E','E'), 'Disamis':('E','O'), 'Datisi':('O','E'),
           'Felapton':('A','E'), 'Bocardo':('A','O'), 'Ferison':('I','E')}

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def truth(k, pred, subj, points):
    pi, si = TERMS.index(pred), TERMS.index(subj)
    if k == 'A': return all(not p[si] or p[pi] for p in points)
    if k == 'E': return all(not (p[si] and p[pi]) for p in points)
    if k == 'I': return any(p[si] and p[pi] for p in points)
    if k == 'O': return any(p[si] and not p[pi] for p in points)
    raise ValueError(k)

def masks(policy):
    for flags in itertools.product((False,True), repeat=8):
        points = tuple(t for t,f in zip(TYPES,flags) if f)
        if not points: continue
        if policy=='C_nonempty' and not any(p[2] for p in points): continue
        if policy=='all_nonempty' and not all(any(p[i] for p in points) for i in range(3)): continue
        yield sum(1 << n for n,f in enumerate(flags) if f), points

def parse(s):
    return s[0],s[2],s[4]

def main():
    data = json.loads(Path(__file__).with_name('results.json').read_text())
    cases_checked = witnesses_checked = originals_checked = 0
    totals = {}
    for policy,record in data['policies'].items():
        universe = list(masks(policy))
        require(len(universe)==record['model_count'], policy+' universe size')
        rows = {r['id']:r for r in record['cases']}
        require(len(rows)==24, policy+' cases')
        for name,(major,minor,conclusion) in MOODS.items():
            original = [(mask,p) for mask,p in universe if truth(major,'A','C',p) and truth(minor,'B','C',p)]
            bad = [mask for mask,p in original if not truth(conclusion,'A','B',p)]
            saved = record['original_moods'][name]
            require((len(original),len(bad))==(saved['background_count'],saved['countermodels']), name+' original')
            originals_checked += 1
            for mode in ('contrary','contradictory'):
                replacement = ({'I':'O','O':'I'} if mode=='contrary' else {'I':'E','O':'A'})[conclusion]
                for side in ('BC','AC'):
                    idx = 0 if side=='BC' else 1
                    retained = (minor,'B','C') if idx==0 else (major,'A','C')
                    target = (major,'A','C') if idx==0 else (minor,'B','C')
                    key = f'{name}/{mode}/retain_{side}'
                    row = rows[key]
                    require(parse(row['retained'])==retained and parse(row['target'])==target and parse(row['replacement'])==(replacement,'A','B'), key+' metadata')
                    bg = [(mask,p) for mask,p in universe if truth(*retained,p) and truth(replacement,'A','B',p)]
                    coexist = [mask for mask,p in bg if truth(*target,p)]
                    require(len(bg)==row['background_count'] and len(coexist)==row['refutation_countermodels'], key+' counts')
                    require(len(bg)>0,key+' nonvacuity')
                    for reverse,label in ((False,'valid_target_pair_forms'),(True,'valid_reverse_pair_forms')):
                        pred,subj = target[1:] if not reverse else target[1:][::-1]
                        forms = [f'{k}({pred},{subj})' for k in 'AEIO' if all(truth(k,pred,subj,p) for _,p in bg)]
                        require(forms==row[label],key+' forms')
                    if mode=='contradictory':
                        result = RESULTS[name][idx],*target[1:]
                        require(parse(row['result'])==result,key+' result metadata')
                        bad_result = [mask for mask,p in bg if not truth(*result,p)]
                        require(len(bad_result)==row['result_countermodels']==0,key+' valid result')
                        exception = policy=='empty_allowed' and name in ('Darapti','Felapton')
                        require(bool(coexist)==exception,key+' refutation qualification')
                    else:
                        require(row['result'] is None and row['result_countermodels'] is None,key+' no claimed result')
                        require(bool(coexist) and not row['valid_target_pair_forms'],key+' contrary failure')
                    w=row['first_refutation_countermodel']
                    if coexist:
                        require(w['mask']==min(coexist),key+' least witness')
                        points = next(p for mask,p in universe if mask==w['mask'])
                        require(truth(*retained,points) and truth(replacement,'A','B',points) and truth(*target,points),key+' witness replay')
                        require(w['sets']=={x:[TYPES.index(p) for p in points if p[i]] for i,x in enumerate(TERMS)},key+' witness encoding')
                        witnesses_checked += 1
                    else: require(w is None,key+' absent witness')
                    cases_checked += 1
        totals[policy]={'models':len(universe),'cases':len(rows),'refuting_cases':sum(r['refutation_countermodels']==0 for r in rows.values())}
    # Modern wrong-term example: E(A,B) and A(B,C) do not imply E(B,C).
    points=((False,True,True),)
    require(truth('E','A','B',points) and truth('A','B','C',points) and not truth('E','B','C',points),'modern wrong-term countermodel')
    # Manually specified teaching examples, independent of model-mask iteration.
    positive=((True,True,True),(False,True,False))
    negative=((False,True,True),(True,True,False))
    for name,(a,b,c) in MOODS.items():
        points=positive if c=='I' else negative
        require(truth(a,'A','C',points) and truth(b,'B','C',points) and truth(c,'A','B',points),name+' common original example')
        require(truth('O' if c=='I' else 'I','A','B',points),name+' opposite particular coexistence')
    split=((False,True,True),(True,False,True))
    require(truth('E','A','B',split) and truth('I','B','C',split) and truth('O','A','C',split) and not truth('E','A','C',split),'Datisi no upgrade')
    require(truth('E','A','B',split) and truth('I','A','C',split) and truth('O','B','C',split) and not truth('E','B','C',split),'Disamis no upgrade')
    split2=((True,True,True),(False,False,True))
    require(truth('A','A','B',split2) and truth('I','B','C',split2) and truth('I','A','C',split2) and not truth('A','A','C',split2),'Ferison no upgrade')
    require(truth('A','A','B',split2) and truth('O','A','C',split2) and truth('O','B','C',split2) and not truth('E','B','C',split2),'Bocardo no upgrade')
    print(json.dumps({'status':'PASS','common_examples_checked':6,'nonupgrade_examples_checked':4,'independent_cases':cases_checked,'original_moods':originals_checked,'countermodels_replayed':witnesses_checked,'modern_wrong_term_checked':True,'policies':totals},indent=2))

if __name__=='__main__': main()
