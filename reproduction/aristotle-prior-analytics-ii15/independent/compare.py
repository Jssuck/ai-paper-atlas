#!/usr/bin/env python3
"""Compare production JSON against an independently implemented set oracle."""
import itertools
import json
import subprocess
import sys
from pathlib import Path
from audit import holds, check
ROOT = Path(__file__).resolve().parents[1]

def all_models():
    # Enumerate supports by cardinality, unlike production integer masks.
    result=[]
    for n in range(1,9):
        for support in itertools.combinations(range(8),n):
            result.append({name:set(t for t in support if t & bit) for name,bit in [('P',1),('M',2),('S',4)]})
    return result

def truth(prop,m):
    q,p,s=prop
    return holds(q,m[p],m[s])

def compare():
    production=json.loads(subprocess.check_output([sys.executable,*(['-'+sys.flags.optimize*'O'] if sys.flags.optimize else []),str(ROOT/'reproduce.py')],text=True))
    ms=all_models()
    check(len(ms)==255,'model count')
    checks=0
    for row in production['opposite_routes']:
        f,pair=row['figure'],row['pair']
        # Expected route direction determined separately from production rules.
        expected={2:{'UE':('E','P','S'),'EU':('E','P','S'),'UO':('O','P','S'),'OU':('O','S','P'),'IE':('O','S','P'),'EI':('O','P','S')},3:{'UE':('O','S','P'),'EU':('O','P','S'),'UO':('O','S','P'),'OU':('O','P','S'),'IE':('O','S','P'),'EI':('O','P','S')}}[f][pair]
        check(tuple(row['conclusion'])==expected,'conclusion direction')
        ps=row['premises']; c=expected
        need=('M',) if f==3 and pair in ('UE','EU') else ()
        for key,equal,nonempty in [('distinct_terms',False,need),('identified_extremes',True,('P','M','S')),('empty_terms_allowed',True,())]:
            bg=[m for m in ms if (not equal or m['P']==m['S']) and all(m[t] for t in nonempty)]
            sat=[m for m in bg if all(truth(p,m) for p in ps)]
            bad=[m for m in sat if not truth(c,m)]
            expected_values={'background_models':len(bg),'premise_models':len(sat),'semantic_entailment':not bad,'vacuous':not sat,'conclusion_false_in_background':sum(not truth(c,m) for m in bg)}
            for k,v in expected_values.items(): check(row[key][k]==v,f'{f}/{pair}/{key}/{k}')
            if row[key]['countermodel'] is not None:
                witness={k:set(v) for k,v in row[key]['countermodel'].items()}
                check(all(truth(p,witness) for p in ps) and not truth(c,witness),'countermodel replay')
            checks+=1
    for row in production['standard_rule_checks']:
        f,pair=row['figure'],row['pair']
        slots={1:[('P','M'),('M','S')],2:[('M','P'),('M','S')],3:[('P','M'),('S','M')]}[f]
        ps=[(q,*slot) for q,slot in zip(pair,slots)]
        sat=[m for m in ms if all(m.values()) and all(truth(p,m) for p in ps)]
        check(len(sat)==row['premise_models'],'standard premise count')
        check(all(truth(row['conclusion'],m) for m in sat),'generic rule soundness')
    for row, relation, exists in zip(production['subset_examples'],[False,True,True],[False,False,True]):
        bg=[m for m in ms if (not relation or m['S']<=m['P']) and (not exists or bool(m['S']))]
        sat=[m for m in bg if holds('U',m['M'],m['P']) and holds('E',m['M'],m['S'])]
        check(row['background_models']==len(bg),'subset background count')
        check(row['premise_models']==len(sat),'subset premise count')
        check(row['conclusion_false_in_background']==sum(not holds('E',m['P'],m['S']) for m in bg),'subset false count')
    check(len(production['standard_rule_checks'])==14,'14 standard moods')
    return {'independent_support_models':len(ms),'route_background_records_checked':checks,'generic_rule_records_checked':14,'subset_records_checked':3,'status':'passed','scope':'Comparison does not turn vacuous semantic entailment into a formal inference rule.'}

if __name__=='__main__':print(json.dumps(compare(),ensure_ascii=False,indent=2,sort_keys=True))
