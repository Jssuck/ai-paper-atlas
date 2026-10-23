"""Independent set-based audit of the declared classical three-term semantics.
No production code is imported. Exhaustive finite checks are not general proofs.
"""
import itertools
import json
from pathlib import Path

FORMS = tuple((q,p,s) for q in 'UEIO' for p in 'ABC' for s in 'ABC' if p != s)
NEG = {'U':'O','O':'U','E':'I','I':'E'}

def truth(form, sets):
    q,p,s = form
    P,S = sets[p],sets[s]
    return {'U': S <= P, 'E': not (S & P), 'I': bool(S & P), 'O': bool(S - P)}[q]

def models(nonempty=False):
    result=[]
    for mask in range(1,256):
        occupied=[v for v in range(8) if mask & (1 << v)]
        sets={letter: {v for v in occupied if v & (1 << bit)} for bit,letter in enumerate('ABC')}
        if not nonempty or all(sets.values()):
            result.append((mask,sets))
    return result

def run():
    report={}
    for policy in (False,True):
        ms=models(policy)
        bits={f:sum(1<<i for i,(_,s) in enumerate(ms) if truth(f,s)) for f in FORMS}
        full=(1<<len(ms))-1
        for f in FORMS:
            dual=(NEG[f[0]],f[1],f[2])
            if bits[dual] != (full ^ bits[f]):
                raise RuntimeError('Contradictory pair not Boolean complements')
        checked=0
        for p,k,t in itertools.product(FORMS, repeat=3):
            direct=(bits[p]&bits[k]&~bits[t]) == 0
            reduction=(bits[p]&(full^bits[t])&bits[k]) == 0
            if direct != reduction:
                raise RuntimeError('Conditional transposition mismatch')
            checked+=1
        # U(A,C) & U(B,C) => I(A,B) needs C nonempty.
        bad=[mask for mask,s in ms if truth(('U','A','C'),s) and truth(('U','B','C'),s) and not truth(('I','A','B'),s)]
        report['all_nonempty' if policy else 'empty_terms_allowed']={
            'models':len(ms),'complement_checks':len(FORMS),'conditional_transposition_checks':checked,
            'universal_shared_subject_to_overlap_countermodels':bad,
        }
    if report['empty_terms_allowed']['models']!=255 or report['all_nonempty']['models']!=218:
        raise RuntimeError('Model enumeration count mismatch')
    if not report['empty_terms_allowed']['universal_shared_subject_to_overlap_countermodels']:
        raise RuntimeError('Missing empty-subject countermodel')
    if report['all_nonempty']['universal_shared_subject_to_overlap_countermodels']:
        raise RuntimeError('Unexpected nonempty-subject countermodel')
    # Independent checks of teaching boundaries, not source-text adjudication.
    all_models=models(False)
    def entails(prems,c):
        return all(not all(truth(p,s) for p in prems) or truth(c,s) for _,s in all_models)
    special={
      'same_figure_direct': entails(['UAC','IBC'],'IAB'),
      'same_figure_reductio_internal': entails(['ICB','EAB'],'OAC'),
      'I_conversion': all(truth('IBC',s)==truth('ICB',s) for _,s in all_models),
      'erase_background_fails': not entails(['UAC'],'UAB'),
      'I_O_coexist': any(truth('IAB',s) and truth('OAB',s) for _,s in all_models),
      'AB_nonempty_not_enough': any(s['A'] and s['B'] and not s['C'] and truth('UAC',s) and truth('UBC',s) and not truth('IAB',s) for _,s in all_models),
    }
    if not all(special.values()): raise RuntimeError('Special boundary check failed')
    report['boundary_checks']=special
    return report


# Independent transcription of the fifteen explicit/similar chapter routes.
EXPECTED = [
 ('F1_E_positive_fixed',1,2,'EAB','UCA','ECB','ICB'),
 ('F1_O_positive_fixed',1,2,'OAB','UCA','OCB','UCB'),
 ('F1_E_negative_fixed',1,2,'EAB','ECA','UCB','OCB'),
 ('F1_O_negative_fixed',1,2,'OAB','ECA','ICB','ECB'),
 ('F1_I_both_universal',1,3,'IAB','UBC','UAC','EAC'),
 ('F1_I_A_particular',1,3,'IAB','UBC','IAC','EAC'),
 ('F1_I_B_particular',1,3,'IAB','IBC','UAC','OAC'),
 ('F2_U',2,1,'UAB','UAC','UCB','OCB'),
 ('F2_I',2,1,'IAB','UAC','ICB','ECB'),
 ('F2_E',2,1,'EAB','EAC','UCB','OCB'),
 ('F2_O',2,1,'OAB','EAC','ICB','ECB'),
 ('F3_U',3,1,'UAB','UCB','UAC','OAC'),
 ('F3_I',3,1,'IAB','ICB','UAC','OAC'),
 ('F3_E',3,2,'EAB','UCB','ECA','ICA'),
 ('F3_O',3,2,'OAB','ICB','ECA','IAC'),
]

def production_audit(production_result):
    def sig(x): return x['kind']+x['pred']+x['subj']
    def neg(f): return NEG[f[0]]+f[1:]
    checked=0
    for policy, data in production_result['policies'].items():
        ms=models(policy=='all_terms_nonempty')
        if policy=='C_nonempty': ms=[(m,s) for m,s in ms if s['C']]
        if len(ms)!=data['model_count']: raise RuntimeError('model count mismatch')
        if len(data['routes'])!=15: raise RuntimeError('route count mismatch')
        for record,ex in zip(data['routes'],EXPECTED):
            name,fi,fd,t,p,k,r=ex
            if (record['name'],record['internal_figure'],record['direct_figure'],*[sig(record[x]) for x in ('target','fixed','background','internal_result')])!=ex:
                raise RuntimeError('route transcription mismatch')
            if sig(record['hypothesis'])!=neg(t): raise RuntimeError('bad hypothesis')
            def witness(mask):
                if mask is None:return None
                s=dict(ms)[mask]
                return {'mask':mask,'domain_types':[v for v in range(8) if mask&(1<<v)],'extensions':{a:sorted(s[a]) for a in 'ABC'}}
            def smallest(bad):return min(bad,key=lambda m:(len([v for v in range(8) if m&(1<<v)]),m),default=None)
            for label, prems, conclusion in [('internal',[p,neg(t)],r),('direct',[p,k],t),('reverse_refutation',[p,neg(t)],neg(k))]:
                good=[m for m,s in ms if all(truth(f,s) for f in prems)]
                bad=[m for m,s in ms if m in good and not truth(conclusion,s)]
                want={'valid':not bad,'premise_models':len(good),'countermodels':len(bad),'smallest_countermodel':witness(smallest(bad))}
                if record[label]!=want:raise RuntimeError(f'{name} {policy} {label} mismatch')
                checked+=1
            overlap=[m for m,s in ms if truth(k,s) and truth(r,s)]
            want={'incompatible':not overlap,'overlap_models':len(overlap),'smallest_overlap':witness(smallest(overlap))}
            if record['conflict']!=want:raise RuntimeError('conflict mismatch')
            checked+=1
    return {'route_records':45,'implication_or_conflict_checks':checked}

if __name__=='__main__':
    import sys
    result=run()
    if len(sys.argv)>1:
        result['production_comparison']=production_audit(json.loads(Path(sys.argv[1]).read_text()))
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))
