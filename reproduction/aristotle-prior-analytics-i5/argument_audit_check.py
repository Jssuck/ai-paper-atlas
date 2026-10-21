#!/usr/bin/env python3
"""Independent argument audit; no imports from the author's implementation."""
import hashlib
import itertools
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
MAIN=HERE.parents[1] / 'papers' / 'ancient' / 'aristotle-prior-analytics-i5.zh-CN.md'
main_bytes=MAIN.read_bytes()
text=main_bytes.decode('utf-8')
Q='AEIO'
checks=0

def check(condition, message):
    global checks
    checks+=1
    if not condition:
        raise RuntimeError(message)

def truth(q, X, Y, U):
    # Object-level quantifiers, not the author's atom-bit or set evaluator.
    if q=='A': return all(x not in X or x in Y for x in U)
    if q=='E': return all(not (x in X and x in Y) for x in U)
    if q=='I': return any(x in X and x in Y for x in U)
    if q=='O': return any(x in X and x not in Y for x in U)
    raise ValueError(q)

def extensions(rows):
    U=tuple(range(len(rows)))
    sets=tuple(frozenset(i for i,r in enumerate(rows) if r[c]) for c in range(3))
    return U,sets

def signature(P,S,M,U):
    return ''.join('1' if truth(q,S,P,U) else '0' for q in Q)

def parse_model(raw):
    sets=tuple(frozenset(re.findall(r'[a-z]',s)) for s in re.findall(r'\{([^{}]*)\}',raw))
    check(len(sets)==3, 'table tuple arity')
    return sets

rows=[]
for line in text.splitlines():
    match=re.match(r'^\| ([AEIO]{2}) \| (.*?) \| (.*?) \|$',line)
    if not match: continue
    pair,left,right=match.groups()
    if not left.startswith('('): continue
    out={'pair':pair,'models':[]}
    for side,raw in [('left',left),('right',right)]:
        P,S,M=parse_model(raw)
        U=tuple(sorted(P|S|M))
        check(all((P,S,M)), f'{pair}/{side}: nonempty')
        check(truth(pair[0],P,M,U), f'{pair}/{side}: major')
        check(truth(pair[1],S,M,U), f'{pair}/{side}: minor')
        observed=signature(P,S,M,U)
        check(observed==('1010' if side=='left' else '0101'), f'{pair}/{side}: conclusion signature')
        atoms=sorted({''.join('1' if x in X else '0' for X in (P,S,M)) for x in U})
        out['models'].append({'side':side,'PSM_types':atoms,'premises':[True,True],'AEIO':observed})
    rows.append(out)
check(len(rows)==12,'12 failed premise pairs parsed')
check(set(r['pair'] for r in rows)==set(a+b for a in Q for b in Q)-{'EA','AE','EI','AO'},'failed premise coverage')

atoms=tuple(itertools.product((False,True),repeat=3))
models=[]
for n in range(1,9):
    for occupied in itertools.combinations(atoms,n):
        models.append(extensions(occupied))
check(len(models)==255,'all 255 supports')
expected={
    'allow-empty':{'AEE','AOO','EAE','EIO'},
    'all-nonempty':{'AEE','AEO','AOO','EAE','EAO','EIO'},
    'subject-nonempty':{'AEE','AEO','AOO','EAE','EAO','EIO'},
}
classifications={}
for policy in expected:
    eligible=[(U,(P,S,M)) for U,(P,S,M) in models if policy=='allow-empty' or (all((P,S,M)) if policy=='all-nonempty' else bool(S))]
    valid=[]
    premise_counts={}
    minimum_sizes={}
    for a,b in itertools.product(Q,repeat=2):
        satisfying=[(U,P,S,M) for U,(P,S,M) in eligible if truth(a,P,M,U) and truth(b,S,M,U)]
        premise_counts[a+b]=len(satisfying)
        check(bool(satisfying), f'{policy}/{a+b}: nonvacuous')
        for c in Q:
            failures=[len(U) for U,P,S,M in satisfying if not truth(c,S,P,U)]
            if failures: minimum_sizes[a+b+c]=min(failures)
            else: valid.append(a+b+c)
    check(set(valid)==expected[policy], f'{policy}: classification')
    for a,b in ('IE','OA'):
        check(all(truth('O',P,S,U) for U,(P,S,M) in eligible if truth(a,P,M,U) and truth(b,S,M,U)), f'{policy}/{a+b}: reversed conclusion')
    classifications[policy]={
        'support_count':len(eligible),
        'supports_by_size':dict(sorted(Counter(len(U) for U,_ in eligible).items())),
        'premise_support_counts':premise_counts,
        'valid_forward_moods':valid,
        'invalid_forward_count':len(minimum_sizes),
        'minimum_countermodel_size_histogram':dict(sorted(Counter(minimum_sizes.values()).items())),
        'minimum_countermodel_sizes':minimum_sizes,
    }
check([classifications[p]['support_count'] for p in expected]==[255,218,240],'all three support counts')

# A second route enumerates all labelled one- to four-object domains, including
# repeated types, and compares resulting classifications without compression.
raw_results={}
for policy in expected:
    found=set()
    count=0
    compressions=0
    for n in range(1,5):
        for assignment in itertools.product(atoms,repeat=n):
            U,(P,S,M)=extensions(assignment)
            if policy=='all-nonempty' and not all((P,S,M)): continue
            if policy=='subject-nonempty' and not S: continue
            count+=1
            V,(Pc,Sc,Mc)=extensions(tuple(sorted(set(assignment))))
            for X,Y,Xc,Yc in ((P,M,Pc,Mc),(S,M,Sc,Mc),(S,P,Sc,Pc),(P,S,Pc,Sc)):
                for q in Q:
                    check(truth(q,X,Y,U)==truth(q,Xc,Yc,V), 'compression truth preservation')
                    compressions+=1
            for a,b,c in itertools.product(Q,repeat=3):
                if truth(a,P,M,U) and truth(b,S,M,U) and not truth(c,S,P,U):
                    found.add(a+b+c)
    valid=set(''.join(t) for t in itertools.product(Q,repeat=3))-found
    check(valid==expected[policy], f'{policy}: labelled-domain agreement')
    raw_results[policy]={'labelled_models_1_through_4':count,'compression_truth_comparisons':compressions,'valid_moods':sorted(valid)}

# Additional explicit models used in the explanation and exercises.
for pair,M in [('EI',{'b'}),('AO',{'a'})]:
    P,S,U={'a'},{'a','b'},{'a','b'}
    check(truth(pair[0],P,M,U) and truth(pair[1],S,M,U),'particular premise example')
    check(truth('O',S,P,U) and not truth('E',S,P,U),'particular cannot strengthen E')
check(truth('O',{'a','b'},{'a'},{'a','b'}) and not truth('O',{'a'},{'a','b'},{'a','b'}),'O not convertible')
for pair,P,M in [('EA',{'a'},{'b'}),('AE',{'a'},{'a'})]:
    S,U=set(),{'a','b'}
    check(truth(pair[0],P,M,U) and truth(pair[1],S,M,U),'empty S satisfies universal premises')
    check(truth('E',S,P,U) and not truth('O',S,P,U),'empty S prevents weakening')

# Read the published data as an output artifact, not an oracle. Its values are
# checked against independently calculated results and direct witnesses.
published=json.loads((HERE / 'report.json').read_text(encoding='utf-8'))
compared=0
for policy,ours in classifications.items():
    theirs=published['policies'][policy]
    check(theirs['support_count']==ours['support_count'], 'published support count')
    check(set(theirs['valid_moods'])==set(ours['valid_forward_moods']), 'published valid list')
    for mood,row in theirs['results'].items():
        compared+=1
        a,b,c=mood
        check(row['valid']==(mood in ours['valid_forward_moods']), 'published validity')
        check(row['premise_support_count']==ours['premise_support_counts'][a+b], 'published premise count')
        check(row['countermodel_size']==ours['minimum_countermodel_sizes'].get(mood), 'published minimal size')
        if row['valid']:
            check(row['countermodel'] is None, 'no countermodel for valid mood')
            continue
        raw=row['countermodel']
        U,P,S,M=(frozenset(raw[k]) for k in ('universe','P','S','M'))
        check(bool(U) and all(X<=U for X in (P,S,M)), 'published concrete universe')
        check(len(U)==row['countermodel_size'], 'published concrete size')
        check(policy!='all-nonempty' or all((P,S,M)), 'published nonempty policy')
        check(policy!='subject-nonempty' or bool(S), 'published S policy')
        check(truth(a,P,M,U) and truth(b,S,M,U) and not truth(c,S,P,U), 'published concrete countermodel')
check(compared==192, '192 published classification rows')

report={
    'method':'independent direct object quantification; no author implementation imported',
    'main_sha256':hashlib.sha256(main_bytes).hexdigest(),
    'audit_checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'published_report_sha256':hashlib.sha256((HERE / 'report.json').read_bytes()).hexdigest(),
    'python_version':sys.version.split()[0],
    'checks':checks,'published_classification_rows_verified':compared,'table_models':rows,'support_enumeration':classifications,
    'raw_labelled_domain_crosscheck':raw_results,
    'result':'PASS',
}
print(json.dumps(report,ensure_ascii=False,indent=2))
