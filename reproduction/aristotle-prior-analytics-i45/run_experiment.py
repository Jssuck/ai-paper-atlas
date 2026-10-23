"""Actual finite observations; no general-theorem claim follows from counts."""
import json
from model import *

def require(condition,message):
    if not condition: raise RuntimeError(message)

def main():
    ms=list(models()); report={'models':len(ms),'all_terms_nonempty_models':sum(all(m[t] for t in TERMS) for m in ms)}
    mood_rows={}; total=0
    for name,(f,letters,ne) in MOODS.items():
        a,b,c=mood(f,letters); admitted=0; satisfied=0; failures=0
        for m in ms:
            if all(m[t] for t in ne):
                admitted+=1; total+=1
                if holds(a,m) and holds(b,m):
                    satisfied+=1; failures+=not holds(c,m)
        require(failures==0,name)
        mood_rows[name]={'admitted_models':admitted,'premises_true':satisfied,'failures':failures,'nonempty':list(ne)}
    report['moods']=mood_rows; report['mood_model_checks']=total
    report['direct_certificates']={name:verify(p,s,c,n) for name,(p,s,c,n) in demonstrations().items()}
    report['indirect_certificates']={name:reductio(*args) for name,args in indirect_demonstrations().items()}
    require(all(report['direct_certificates'].values()),'direct certificates')
    require(all(report['indirect_certificates'].values()),'indirect certificates')
    # Same conclusion, changed presentation. Premise equivalence for E/I only.
    pairs=[]
    for name,target in [('Celarent','Cesare'),('Ferio','Festino')]:
        f,l,ne=MOODS[name]; a,b,c=mood(f,l); changed=(convert(a),b)
        # target middle is old M; correct target pattern follows swapping E.
        pairs.append((name+' -> '+target,(a,b),changed,c,(),True))
    for name,target in [('Darii','Datisi'),('Ferio','Ferison')]:
        f,l,ne=MOODS[name]; a,b,c=mood(f,l); pairs.append((name+' -> '+target,(a,b),(a,convert(b)),c,(),True))
    a,b,c=mood(2,'EIO')
    pairs.append(('Festino -> Ferison',(a,b),(convert(a),convert(b)),c,(),True))
    for name in ('Ferison','Felapton'):
        f,l,ne=MOODS[name]; a,b,c=mood(f,l)
        pairs.append((name+' -> Festino',(a,b),(convert(a),convert(b,ne)),c,ne,name=='Ferison'))
    presentation={}
    for label,old,new,c,ne,equivalent in pairs:
        admitted=[m for m in ms if all(m[t] for t in ne)]
        eq=sum(all(holds(p,m) for p in old)==all(holds(p,m) for p in new) for m in admitted)
        implications=sum(not all(holds(p,m) for p in old) or all(holds(p,m) for p in new) for m in admitted)
        require(implications==len(admitted),label+' premise implication')
        if equivalent: require(eq==len(admitted),label)
        require(countermodel(new,c,ne) is None,label+' conclusion')
        presentation[label]={'admitted_models':len(admitted),'premise_equivalence_models':eq,'premise_implication_models':implications,'equivalence_claimed':equivalent,'conclusion_failures':0}
    conversion_checks=0
    for s in TERMS:
        for p in TERMS:
            if s==p: continue
            for k in ('A','E','I'):
                source=prop(k,s,p); ne=(s,) if k=='A' else ()
                target=convert(source,ne)
                for m in ms:
                    if all(m[t] for t in ne):
                        conversion_checks+=1
                        require(not holds(source,m) or holds(target,m),'conversion soundness')
    report['conversion_model_checks']=conversion_checks
    report['presentation_changes']=presentation
    def serial(m): return {t:sorted(m[t]) for t in TERMS}
    report['countermodels']={}
    for k in ('A','O'):
        m=countermodel((prop(k,'S','P'),),prop(k,'P','S'),TERMS)
        require(m is not None,'missing illegal conversion example')
        report['countermodels'][k+'_simple_conversion']=serial(m)
    for name in ('Darapti','Felapton'):
        f,l,ne=MOODS[name];a,b,c=mood(f,l);m=countermodel((a,b),c)
        require(m is not None,'missing existence example')
        report['countermodels'][name+'_without_existence']=serial(m)
    report['rejected_direct_attempts']={}
    for name in ('Baroco','Bocardo'):
        f,l,ne=MOODS[name];a,b,c=mood(f,l)
        o=a if a.kind=='O' else b
        try: convert(o,TERMS)
        except ValueError: report['rejected_direct_attempts'][name]='O conversion rejected'
        else: raise RuntimeError('O conversion unexpectedly accepted')
    print(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True))
if __name__=='__main__': main()
