"""Independent quantifier oracle for the archived II.8 report.
No import of model.py; reference input is its saved report, not its evaluator.
"""
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TYPES = tuple(itertools.product((False, True), repeat=3))
INDEX = {'A': 0, 'B': 1, 'C': 2}
KINDS = ('U', 'E', 'I', 'O')
MOODS = {
    'Barbara': [('U','A','B'), ('U','B','C'), ('U','A','C')],
    'Celarent': [('E','A','B'), ('U','B','C'), ('E','A','C')],
    'Darii': [('U','A','B'), ('I','B','C'), ('I','A','C')],
    'Ferio': [('E','A','B'), ('I','B','C'), ('O','A','C')],
}
NEG = {'U':'O', 'E':'I', 'I':'E', 'O':'U'}
OTHER = {'U':'E', 'E':'U', 'I':'O', 'O':'I'}
RESULTS = {
 ('Barbara','contradictory','major'): ('O','B','C'),
 ('Barbara','contradictory','minor'): ('O','A','B'),
 ('Barbara','contrary','major'): ('E','B','C'),
 ('Barbara','contrary','minor'): ('O','A','B'),
 ('Celarent','contradictory','major'): ('O','B','C'),
 ('Celarent','contradictory','minor'): ('I','A','B'),
 ('Celarent','contrary','major'): ('E','B','C'),
 ('Celarent','contrary','minor'): ('I','A','B'),
 ('Darii','contradictory','major'): ('E','B','C'),
 ('Darii','contradictory','minor'): ('O','A','B'),
 ('Darii','contrary','major'): ('O','B','C'),
 ('Darii','contrary','minor'): None,
 ('Ferio','contradictory','major'): ('E','B','C'),
 ('Ferio','contradictory','minor'): ('I','A','B'),
 ('Ferio','contrary','major'): ('O','B','C'),
 ('Ferio','contrary','minor'): None,
}

def truth(objects, sentence):
    kind,p,s = sentence
    pairs = [(o[INDEX[p]], o[INDEX[s]]) for o in objects]
    if kind == 'U': return all(not subject or pred for pred,subject in pairs)
    if kind == 'E': return all(not (subject and pred) for pred,subject in pairs)
    if kind == 'I': return any(subject and pred for pred,subject in pairs)
    if kind == 'O': return any(subject and not pred for pred,subject in pairs)
    raise ValueError(kind)

def require(test, label):
    if not test: raise RuntimeError(label)

def accepted(objects, policy):
    if policy == 'empty_terms_allowed': return True
    if policy == 'C_nonempty': return any(o[2] for o in objects)
    if policy == 'all_terms_nonempty': return all(any(o[i] for o in objects) for i in range(3))
    raise ValueError(policy)

all_models = [subset for size in range(1,9) for subset in itertools.combinations(TYPES,size)]
report_bytes = (ROOT/'logs/run-normal.json').read_bytes()
report = json.loads(report_bytes)
for name in ('run-O.json','run-OO.json'):
    require((ROOT/'logs'/name).read_bytes() == report_bytes, name+' differs')
counts = {p: sum(accepted(m,p) for m in all_models) for p in report['model_counts']}
require(counts == report['model_counts'], 'model counts')
require(len(report['rows']) == 48, 'row count')
seen = set()
for row in report['rows']:
    key = row['mood'], row['mode'], row['keep']
    identity = key + (row['policy'],)
    require(identity not in seen, 'duplicate row')
    seen.add(identity)
    major,minor,conclusion = MOODS[row['mood']]
    retained,dropped = (major,minor) if row['keep']=='major' else (minor,major)
    kind,p,s=conclusion
    replacement=((NEG if row['mode']=='contradictory' else OTHER)[kind],p,s)
    target=(NEG[dropped[0]],*dropped[1:])
    stated=RESULTS[key]
    require(row['assumptions']==[list(replacement),list(retained)], 'assumptions')
    require(row['dropped_premise']==list(dropped), 'dropped')
    require(row['refutation_target']==list(target), 'target')
    require(row['stated_result']==(list(stated) if stated else None), 'result declaration')
    eligible=[m for m in all_models if accepted(m,row['policy']) and truth(m,replacement) and truth(m,retained)]
    require(len(eligible)==row['satisfying_models'] and eligible, 'nonvacuity/count')
    require(sum(not truth(m,target) for m in eligible)==row['refutation_counterexamples'], 'refutation count')
    failures=None if stated is None else sum(not truth(m,stated) for m in eligible)
    require(failures==row['stated_result_counterexamples'], 'result count')
    consequences=[(k,*dropped[1:]) for k in KINDS if all(truth(m,(k,*dropped[1:])) for m in eligible)]
    require(row['entailed_ordered_pair_results']==[list(s) for s in consequences], 'entailed language')
    for field,goal in [('first_refutation_countermodel',target),('first_stated_result_countermodel',stated)]:
        w=row[field]
        if w is None: continue
        objects=[tuple(bool(t & (1<<i)) for i in range(3)) for t in w['inhabited_types']]
        require(accepted(objects,row['policy']) and truth(objects,replacement) and truth(objects,retained) and not truth(objects,goal), 'witness replay')
        for name,i in INDEX.items():
            require(w[name]==[t for t in w['inhabited_types'] if t & (1<<i)], 'witness extensions')
for m in all_models:
    for major,minor,conclusion in MOODS.values():
        require(not(truth(m,major) and truth(m,minor)) or truth(m,conclusion), 'original mood')
print(json.dumps({'independent_rows_checked':len(seen),'counts':counts,
                  'all_counts_and_countermodels_match':True,'three_saved_modes_identical':True,
                  'report_sha256':hashlib.sha256(report_bytes).hexdigest()},sort_keys=True,indent=2))
