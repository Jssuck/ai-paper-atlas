"""Independent per-individual predicate oracle versus production set operations."""
from itertools import product
from pathlib import Path
import importlib.util
import json
import sys

root=Path(__file__).resolve().parents[1]
source=root/'relations.py'
spec=importlib.util.spec_from_file_location('production_under_review',source)
production=importlib.util.module_from_spec(spec)
spec.loader.exec_module(production)

def require(value,message):
    if not value:
        raise RuntimeError(message)

def oracle(a,b,c,d,u):
    rows=[(x in a,x in b,x in c,x in d) for x in u]
    every=lambda f: all(f(*r) for r in rows)
    return {
      'chain': (every(lambda a,b,c,d: (not c or b) and (not b or a) and (not a or c)), every(lambda a,b,c,d:a==b==c)),
      'negative_conversion': (every(lambda a,b,c,d:(not c or b) and not(a and b)),every(lambda a,b,c,d:not(a and c) and not(b and a) and not(c and a))),
      'negative_transfer': (every(lambda a,b,c,d:b==c and not(a and c)),every(lambda a,b,c,d:not(b and a))),
      'partition_transport': (every(lambda a,b,c,d:a==b and c==d and a!=c),every(lambda a,b,c,d:b!=d)),
      'complement_pair': (every(lambda a,b,c,d:a!=b and c!=d and a==c),every(lambda a,b,c,d:b==d)),
      'only_coverage': (every(lambda a,b,c,d:(not (b or c) or a) and (not a or b or c) and (not c or b)),every(lambda a,b,c,d:a==b)),
      'middle_transfer': (every(lambda a,b,c,d:(not c or a) and (not c or b) and (not b or c)),every(lambda a,b,c,d:not b or a))}

results=[]
for n in range(4):
    # Generate worlds by assigning each individual a four-predicate Boolean row,
    # independently of production.worlds() and its powerset construction.
    count=0
    totals={name:0 for name in production.RULES}
    for individual_rows in product(tuple(product((False,True),repeat=4)),repeat=n):
        terms=[frozenset(i for i,row in enumerate(individual_rows) if row[k]) for k in range(4)]
        u=frozenset(range(n))
        expected=oracle(*terms,u)
        actual=production.evaluate(*terms,u)
        require(expected==actual,'pointwise mismatch '+repr((n,terms,expected,actual)))
        for name,(p,q) in expected.items():
            require(not p or q,'theorem countermodel '+name)
            totals[name]+=int(p)
        count+=1
    results.append({'n':n,'worlds':count,'rule_pair_comparisons':count*7,'premise_models':totals})
prefs=0
for a,b,c,d in product(range(-3,4),repeat=4):
    # Independent rearrangement: bundle inequality iff (a-b) > (d-c).
    expected=(a-b>0 and d-c>0 and a-b>d-c,a-d>0)
    require(production.preference(a,b,c,d)==expected,'preference mismatch')
    prefs+=1
print(json.dumps({'status':'PASS','python':sys.version.split()[0],'optimize':sys.flags.optimize,'set_comparisons':results,'preference_comparisons':prefs,'imports':'production evaluate/preference only for system under test; expected results independently constructed'},indent=2))
