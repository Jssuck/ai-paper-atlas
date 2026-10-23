"""Independent II.11 audit: occupied Boolean types, no production imports.
Predicate is first; subject is second. Finite checks do not replace proofs.
"""
import itertools
import json
from pathlib import Path

KINDS = 'UEIO'
NEG = {'U': 'O', 'O': 'U', 'E': 'I', 'I': 'E'}

def need(ok, msg):
    if not ok:
        raise RuntimeError(msg)

def holds(atom, cells):
    kind, p, s = atom
    subject = [c for c in cells if (c >> s) & 1]
    hits = [bool((c >> p) & 1) for c in subject]
    return {'U': all(hits), 'E': not any(hits), 'I': any(hits),
            'O': any(not x for x in hits)}[kind]

def models():
    return [tuple(c for c in range(8) if mask & (1 << c)) for mask in range(1, 256)]

def nonempty(cells, term):
    return any((c >> term) & 1 for c in cells)

def entails(premises, goal, universe):
    return not any(all(holds(p, m) for p in premises) and not holds(goal, m) for m in universe)

def parse(text):
    need(len(text)==6 and text[1]=='(' and text[3]==',' and text[5]==')', 'atom syntax')
    return text[0], 'ABC'.index(text[2]), 'ABC'.index(text[4])

def validate_witness(witness, premises, goal, universe):
    bad=[m for m in universe if all(holds(p,m) for p in premises) and not holds(goal,m)]
    if not bad:
        need(witness is None,'spurious countermodel')
        return
    need(witness is not None,'missing countermodel')
    cells=tuple(witness['support'])
    expected=min(bad,key=lambda m:(len(m),sum(1<<c for c in m)))
    need(cells==expected,'not minimal canonical witness')
    for bit,name in enumerate('ABC'):
        need(witness[name]==[c for c in cells if (c>>bit)&1],'incorrect type encoding')

def compare_production():
    base=Path(__file__).resolve().parents[1]/'evidence'
    payloads=[json.loads((base/f'results-{mode}.json').read_text()) for mode in ['normal','optimized','double-optimized']]
    need(payloads[0]==payloads[1]==payloads[2],'production optimization mismatch')
    data=payloads[0]
    checked=0
    for policy in ['empty_allowed','all_terms_nonempty']:
        domain=models()
        if policy=='all_terms_nonempty': domain=[m for m in domain if all(nonempty(m,t) for t in range(3))]
        need(len(data[policy]['rows'])==128,'candidate count')
        for row in data[policy]['rows']:
            h,x,r,q,bg=map(parse,[row[k] for k in ['hypothesis','extra','internal_result','goal','known_background']])
            need(h==(NEG[q[0]],q[1],q[2]),'wrong hypothesis')
            need(bg==(NEG[r[0]],r[1],r[2]),'wrong background')
            iv=entails([h,x],r,domain); dv=entails([x,bg],q,domain)
            ic=sum(all(holds(a,m) for a in [h,x]) for m in domain)
            bc=sum(all(holds(a,m) for a in [x,bg]) for m in domain)
            need(row['internal_valid']==(iv and ic>0) and row['discharge_valid']==dv,'validity mismatch')
            need(row['internal_antecedent_models']==ic and row['background_models']==bc,'count mismatch')
            need(row['certificate']==(iv and ic>0 and dv and bc>0),'certificate mismatch')
            validate_witness(row['internal_countermodel'],[h,x],r,domain)
            validate_witness(row['discharge_countermodel'],[x,bg],q,domain)
            checked+=1
        for row in data['named_checks'][:-1]:
            ps=list(map(parse,row['premises'])); q=parse(row['conclusion'])
            need(row[policy]['valid']==entails(ps,q,domain),'named validity')
            validate_witness(row[policy]['countermodel'],ps,q,domain)
    mixed=data['named_checks'][-1]
    cells=mixed['model']['support']
    for bit,name in enumerate('ABC'):
        need(mixed['model'][name]==[c for c in cells if (c>>bit)&1],'mixed encoding')
    for key in ['I_A_B','O_A_B','U_C_A','I_C_B','E_C_B']:
        kind,p,s=key.split('_')
        need(mixed[key]==holds((kind,'ABC'.index(p),'ABC'.index(s)),cells),'mixed truth')
    return checked

def main():
    universe = models()
    policies = {'empty_terms_allowed': universe,
                'all_terms_nonempty': [m for m in universe if all(nonempty(m,t) for t in range(3))]}
    report = {'models': {k: len(v) for k,v in policies.items()}, 'policies': {}}
    for name, domain in policies.items():
        valid = []
        for k1,k2,k3 in itertools.product(KINDS, repeat=3):
            major, minor, goal = (k1,0,1), (k2,1,2), (k3,0,2)
            if entails([major,minor],goal,domain):
                valid.append(k1+k2+k3)
        expected = {'UUU','EUE','UII','EIO'}
        if name == 'all_terms_nonempty': expected |= {'UUI','EUO'}
        need(set(valid)==expected, ('moods',name,valid))
        # Each sound one-step inference supplies two reductio certificates:
        # one premise becomes hypothesis; other premise and negated result remain background.
        certificates=[]
        for mood in valid:
            major,minor,result=(mood[0],0,1),(mood[1],1,2),(mood[2],0,2)
            for hypothesis,background in [(major,minor),(minor,major)]:
                h,p,s=hypothesis
                target=(NEG[h],p,s)
                opposed=(NEG[result[0]],result[1],result[2])
                need(entails([background,opposed],target,domain), 'invalid reductio')
                need(any(holds(background,m) and holds(opposed,m) for m in domain),'vacuous background')
                certificates.append({'mood':mood,'hypothesis':hypothesis,'target':target})
        need({c['target'][0] for c in certificates}=={'E','I','O'},'target coverage')
        need(all(c['hypothesis'][0]!='O' for c in certificates),'O hypothesis found')
        report['policies'][name]={'moods':valid,'certificates':certificates,'candidate_moods_checked':64}
    # Original first-figure particular-affirmative route exposes existential assumption.
    eab,ubc,uac,iab=('E',0,1),('U',1,2),('U',0,2),('I',0,1)
    empty_counter = next(m for m in universe if holds(ubc,m) and holds(uac,m) and not holds(iab,m))
    need(not nonempty(empty_counter,2),'counterexample C should be empty')
    need(entails([ubc,uac],iab,[m for m in universe if nonempty(m,2)]),'C nonempty repair')
    need(entails([('I',1,2),uac],iab,universe),'particular minor repair')
    # Contrary assumptions: rejecting E yields I, not U; rejecting U yields O, not E.
    mixed = (2,3) # B has two members, only one in A.
    need(holds(('I',0,1),mixed) and holds(('O',0,1),mixed),'mixed witness')
    need(not holds(('U',0,1),mixed) and not holds(('E',0,1),mixed),'contrary failure')
    # A true I hypothesis plus true auxiliary cannot produce a genuinely false result.
    checked=0
    for m in universe:
        if holds(('I',0,1),m) and holds(('U',2,0),m):
            need(holds(('I',2,1),m),'true-premise preservation')
            checked+=1
    report['empty_C_counterexample_cells']=empty_counter
    report['mixed_counterexample_cells']=mixed
    report['true_I_hypothesis_models']=checked
    report['production_rows_compared']=compare_production()
    report['status']='PASS'
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
