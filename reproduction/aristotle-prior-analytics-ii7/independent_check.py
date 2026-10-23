# Independent review: integer masks, no import of the implementation under review.
from itertools import product
import json
from pathlib import Path
base=Path(__file__).resolve().parent
expected=json.loads((base/'logs/run-normal.json').read_text())
for nonempty,label in [(False,'empty_terms_allowed'),(True,'all_terms_nonempty')]:
    counts={}
    total=0
    for n in range(1,5):
        full=(1<<n)-1
        for a,b,c in product(range(1 if nonempty else 0,1<<n),repeat=3):
            total+=1
            subset=lambda x,y: x&(~y&full)==0
            overlap=lambda x,y: (x&y)!=0
            outside=lambda x,y: (y&(~x&full))!=0
            pairs=[
                (subset(c,a) and subset(c,b) and c!=0,overlap(a,b)),
                (not overlap(a,c) and subset(c,b) and c!=0,outside(a,b)),
                (subset(c,a) and overlap(b,c),overlap(a,b)),
                (subset(c,b) and overlap(a,c),overlap(a,b)),
                (subset(c,b) and outside(a,c),outside(a,b)),
                (not overlap(a,c) and overlap(b,c),outside(a,b)),
                (subset(a,c) and overlap(a,b),overlap(c,b)),
                (subset(a,c) and overlap(a,b),overlap(b,c)),
                (subset(b,c) and overlap(a,b),overlap(a,c)),
                (subset(b,c) and outside(a,b),outside(a,c)),
                (outside(a,b) and subset(full^a,c),overlap(b,c)),
                (outside(a,b) and (b&(full^a)&c)!=0,overlap(b,c)),
                (subset(c,a) and subset(c,b),overlap(a,b)),
                (not overlap(a,c) and subset(c,b),outside(a,b)),
                (overlap(a,b) and subset(b,c),subset(c,a)),
                (outside(a,b) and subset(b,c),not overlap(a,c)),
                (outside(a,b) and not overlap(c,a),overlap(b,c)),
                (outside(a,b) and overlap(c,full^a),overlap(b,c))]
            for i,(prem,target) in enumerate(pairs):
                z=counts.setdefault(i,[0,0]);z[0]+=bool(prem);z[1]+=bool(prem and not target)
    names=['original_darapti_with_C_existence','original_felapton_with_C_existence','original_datisi','original_disamis','original_bocardo','original_ferison','major_universal_reverse_gives_converse_I','major_universal_reverse_semantic_target_I','minor_universal_reverse_recovers_I','minor_universal_reverse_recovers_O','negative_coverage_bridge_recovers_I','negative_shared_witness_bridge_recovers_I','invalid_darapti_without_existence','invalid_felapton_without_existence','invalid_recover_universal_A','invalid_recover_universal_E','invalid_negative_simple_conversion','invalid_independent_some_bridge']
    for i,name in enumerate(names):
        row=expected['regimes'][label]['rules'][name]
        if counts[i]!=[row['premise_models'],row['countermodels']]:
            raise RuntimeError((label,name,counts[i],row))
    if total!=expected['regimes'][label]['total_models']:raise RuntimeError('total mismatch')
    print(label,total,'all 18 premise/countermodel counts independently match')
print('PASS: bit-mask checker does not import model.py')
