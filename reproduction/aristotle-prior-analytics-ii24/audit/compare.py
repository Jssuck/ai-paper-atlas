"""Compare emitted JSON, with certificate predicates independently evaluated."""
import json,sys
from pathlib import Path
p=json.loads(Path(sys.argv[1]).read_text())
o=json.loads(Path(sys.argv[2]).read_text())
if p['exhaustive']['counts'] != o['counts']: raise RuntimeError('aggregate mismatch')
count=0
for row in p['examples']:
    a,b,c=map(set,(row['A'],row['B'],row['C']))
    n=row['domain_size']
    if any(not 0<=x<n for group in (a,b,c) for x in group): raise RuntimeError('domain')
    if 'D' in row:
        d=set(row['D'])
        checks={'observed':c<=b and d<=b and d<=a,'D_nonempty':bool(d),
                'some_B_is_A':bool(a.intersection(b)), 'all_B_is_A':b<=a,
                'all_C_is_A':c<=a,'C_covered_by_D':c<=d,'B_covered_by_D':b<=d}
    else:
        d1,d2=set(row['D1']),set(row['D2']); e=d1.union(d2)
        checks={'both_observed':c<=b and d1<=b and d2<=b and e<=a,
                'all_C_is_A':c<=a,'all_B_is_A':b<=a,
                'target_guaranteed_over_all_A':c<=e}
        if set(row['E_union'])!=e: raise RuntimeError('union mismatch')
    for key,value in checks.items():
        if row[key]!=value: raise RuntimeError((row['name'],key))
    count+=1
print(json.dumps({'counts_match':True,'independent_certificates':count,'mode':sys.flags.optimize},sort_keys=True))
