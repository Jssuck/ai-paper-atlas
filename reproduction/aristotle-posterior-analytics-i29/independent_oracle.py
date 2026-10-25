"""Independent review: explicit element sets, never imports model.py."""
from itertools import product
from pathlib import Path
import contextlib
import hashlib
import io
import json
import platform
from datetime import datetime, timezone

BASE = Path(__file__).parent

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def universe_sets(n):
    return [frozenset(i for i, included in enumerate(bits) if included)
            for bits in product((False, True), repeat=n)]

def included(x, y):
    return all(e in y for e in x)

def enumeration(max_n):
    out = dict(endpoint_pairs=0, middle_candidates=0, ordered_middle_pairs=0,
               equal=0, comparable_distinct=0, incomparable=0,
               nonempty_subject_pairs=0, overlap_failures=0,
               empty_subject_disjoint_pairs=0, conclusion_failures=0,
               candidate_count_failures=0)
    strict_checked = 0
    for n in range(max_n+1):
        sets=universe_sets(n)
        for a,b in product(sets, repeat=2):
            out['endpoint_pairs']+=1
            mids=[m for m in sets if included(b,m) and included(m,a)]
            expected=2**len(a-b) if included(b,a) else 0
            out['candidate_count_failures']+=len(mids)!=expected
            out['middle_candidates']+=len(mids)
            strict=[m for m in mids if m!=a and m!=b]
            strict_expected=max(0,expected-2) if a!=b else 0
            require(len(strict)==strict_expected,'strict count')
            strict_checked+=1
            for d,h in product(mids,repeat=2):
                out['ordered_middle_pairs']+=1
                kind='equal' if d==h else ('comparable_distinct' if included(d,h) or included(h,d) else 'incomparable')
                out[kind]+=1
                out['conclusion_failures']+=not included(b,a)
                if b:
                    out['nonempty_subject_pairs']+=1
                    out['overlap_failures']+=not any(e in h for e in d)
                elif not any(e in h for e in d):
                    out['empty_subject_disjoint_pairs']+=1
    return out, strict_checked

def negative(max_n):
    out=dict(assignments=0,celarent_premises=0,cesare_premises=0,both_routes=0,invalid_conclusions=0)
    for n in range(max_n+1):
        for a,b,d,h in product(universe_sets(n),repeat=4):
            c=all(x not in a for x in d) and included(b,d)
            s=all(x not in h for x in a) and included(b,h)
            q=all(x not in a for x in b)
            out['assignments']+=1
            out['celarent_premises']+=c
            out['cesare_premises']+=s
            out['both_routes']+=c and s
            out['invalid_conclusions']+=(c or s) and not q
    return out

def check_notebook():
    doc=json.loads((BASE/'i29_teaching.ipynb').read_text())
    namespace={'__name__':'__independent_notebook_review__'}
    cells=0
    for c in doc['cells']:
        if c['cell_type']!='code': continue
        cells+=1
        stdout=io.StringIO()
        with contextlib.redirect_stdout(stdout):
            exec(compile(''.join(c['source']),f'notebook-review-{cells}','exec'),namespace)
        recorded=''.join(''.join(o['text']) for o in c['outputs'] if o['output_type']=='stream' and o['name']=='stdout')
        require(stdout.getvalue()==recorded,'saved notebook stdout differs')
        require(c['execution_count']==cells,'execution count')
    return {'cells':cells,'saved_stdout_matches':True,'method':'read-only sequential exec; not Jupyter kernel'}

if __name__=='__main__':
    stored=json.loads((BASE/'results.json').read_text())
    small,_=enumeration(4)
    negsmall=negative(3)
    require(small==stored['set_enumeration'],'published set counts')
    require(negsmall==stored['negative_enumeration'],'published negative counts')
    expanded,strict=enumeration(5)
    negexpanded=negative(4)
    for key in ('conclusion_failures','overlap_failures','candidate_count_failures'):
        require(expanded[key]==0,key)
    require(negexpanded['invalid_conclusions']==0,'negative invalid')
    result={'review_utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),
            'independent_representation':'explicit frozensets and element quantification; no model import for oracle',
            'published_counts_match':True,'expanded_sets_n0_to5':expanded,
            'strict_candidate_checks':strict,'expanded_negative_n0_to4':negexpanded,
            'notebook_replay':check_notebook()}
    print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))
