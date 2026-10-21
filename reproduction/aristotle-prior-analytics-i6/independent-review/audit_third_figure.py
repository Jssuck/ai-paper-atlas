"""Independent explicit-set oracle; no use of author's bitwise truth predicate."""
import itertools as it
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import third_figure as a

MEMBERS={0:(),1:('M',),2:('S',),3:('S','M'),4:('P',),5:('P','M'),6:('P','S'),7:('P','S','M')}
QS='AEIO'; TS=('P','S','M'); PS=('allow-empty','middle-nonempty','all-nonempty')
ALL=[s for n in range(1,9) for s in it.combinations(range(8),n)]
COUNTS={}
def check(ok, label):
    COUNTS[label]=COUNTS.get(label,0)+1
    if not ok: raise RuntimeError('independent mismatch: '+label)
def sets(s): return {x:{u for u in s if x in MEMBERS[u]} for x in TS}
def truth(q,x,y,s):
    d=sets(s); X,Y=d[x],d[y]
    if q=='A': return X<=Y
    if q=='E': return X.isdisjoint(Y)
    if q=='I': return not X.isdisjoint(Y)
    if q=='O': return bool(X-Y)
    raise ValueError(q)
def admissible(s,p):
    d=sets(s)
    return p=='allow-empty' or (bool(d['M']) if p=='middle-nonempty' else all(d.values()))
def premise(q,r,s): return truth(q,'M','P',s) and truth(r,'M','S',s)
def expected(q,r,c,p):
    return next((s for s in ALL if admissible(s,p) and premise(q,r,s) and not truth(c,'S','P',s)),None)
def throws(fn):
    try: fn()
    except (TypeError,ValueError): return True
    return False

def full_check():
    for s in ALL:
        for q,x,y in it.product(QS,TS,TS): check(a.truth(q,x,y,s)==truth(q,x,y,s),'set_truth')
        for p in PS: check(a.admissible(s,p)==admissible(s,p),'policy')
        rows=tuple(tuple(x in MEMBERS[u] for x in TS) for u in s)
        check(a.expand(s)==rows,'expand')
        check(a.compress(rows)==s,'compress')
        check(a.compress(rows+rows)==s,'compress_duplicates')
    for p in PS:
        check(a.supports(p)==tuple(s for s in ALL if admissible(s,p)),'support_order')
        for q,r,c in it.product(QS,repeat=3):
            w=expected(q,r,c,p)
            check(a.countermodel(q,r,c,p)==w,'minimal_countermodel')
            check(a.entails(q,r,c,p)==(w is None),'entailment')
            if w:
                check(premise(q,r,w) and not truth(c,'S','P',w),'witness_truth')
                check(not any(admissible(t,p) and premise(q,r,t) and not truth(c,'S','P',t) for t in ALL if len(t)<len(w)),'minimality')
    moods={'Darapti':('A','A','I'),'Felapton':('E','A','O'),'Disamis':('I','A','I'),'Datisi':('A','I','I'),'Bocardo':('O','A','O'),'Ferison':('E','I','O')}
    check(a.MOODS==moods,'mood_table')
    for name,(q,r,c) in moods.items():
        for s in ALL:
            applicable=premise(q,r,s) and (name not in ('Darapti','Felapton') or bool(sets(s)['M']))
            if applicable:
                w=a.proof_witness(name,s)
                check(w in s and 'M' in MEMBERS[w] and 'S' in MEMBERS[w] and (('P' in MEMBERS[w])==(c=='I')),'shared_route')
            else: check(throws(lambda:a.proof_witness(name,s)),'route_rejection')
    # Independently check compression over every sequence of up to three objects.
    rows=list(it.product((False,True),repeat=3))
    for n in (1,2,3):
        for seq in it.product(rows,repeat=n):
            s=a.compress(seq)
            before={x:{i for i,row in enumerate(seq) if row[j]} for j,x in enumerate(TS)}
            for q,x,y in it.product(QS,TS,TS):
                X,Y=before[x],before[y]
                v={'A':X<=Y,'E':X.isdisjoint(Y),'I':not X.isdisjoint(Y),'O':bool(X-Y)}[q]
                check(truth(q,x,y,s)==v,'sequence_truth_preservation')
    bads=[None,0,True,'7',(),[],(True,),(-1,),(8,),(1,1),[1.0],{'x':1}]
    for s in bads:
        for fn in [lambda s=s:a.truth('A','M','P',s),lambda s=s:a.premises('A','A',s),lambda s=s:a.admissible(s),lambda s=s:a.expand(s),lambda s=s:a.proof_witness('Darapti',s)]:
            check(throws(fn),'invalid_support')
    for q in [None,0,True,'','a','X',[],{}]:
        for fn in [lambda q=q:a.truth(q,'M','P',(7,)),lambda q=q:a.countermodel(q,'A','I'),lambda q=q:a.premises('A',q,(7,))]:check(throws(fn),'invalid_quantifier')
    for t in [None,0,True,'','X',[],{}]:check(throws(lambda t=t:a.truth('A',t,'P',(7,))),'invalid_term')
    for p in [None,0,True,'','X',[],{}]:
        for fn in [lambda p=p:a.supports(p),lambda p=p:a.admissible((7,),p),lambda p=p:a.countermodel('A','A','I',p)]:check(throws(fn),'invalid_policy')
    for x in [None,{},[],[(True,)],[(True,False,True,False)],[(1,False,True)],['xxx']]: check(throws(lambda x=x:a.compress(x)),'invalid_compress')
    for x in [None,0,[],{},'','Barbara']:check(throws(lambda x=x:a.proof_witness(x,(7,))),'invalid_route')

def fault_checks():
    # Real isolated replacements; all originals are restored in finally clauses.
    faults=[]
    oldtruth=a._truth; oldadm=a._admissible; oldwit=a.proof_witness; oldcompress=a.compress
    replacements=[('A_direction',lambda q,x,y,s:oldtruth(q,y,x,s) if q=='A' else oldtruth(q,x,y,s)),
                  ('O_direction',lambda q,x,y,s:oldtruth(q,y,x,s) if q=='O' else oldtruth(q,x,y,s)),
                  ('E_as_I',lambda q,x,y,s:oldtruth('I',x,y,s) if q=='E' else oldtruth(q,x,y,s)),
                  ('I_as_A',lambda q,x,y,s:oldtruth('A',x,y,s) if q=='I' else oldtruth(q,x,y,s)),
                  ('A_imports_existence',lambda q,x,y,s:oldtruth(q,x,y,s) and any(x in MEMBERS[t] for t in s) if q=='A' else oldtruth(q,x,y,s)),
                  ('O_strong_some',lambda q,x,y,s:oldtruth(q,x,y,s) and oldtruth('I',x,y,s) if q=='O' else oldtruth(q,x,y,s))]
    try:
        for name,fn in replacements:
            a._truth=fn
            detected=any(a.truth(q,x,y,s)!=truth(q,x,y,s) for s in ALL for q,x,y in it.product(QS,TS,TS))
            if not detected: raise RuntimeError('undetected fault '+name)
            faults.append(name)
        a._truth=oldtruth
        for name,fn in [('ignore_existence',lambda s,p:True),('all_requires_only_M',lambda s,p:oldadm(s,'middle-nonempty') if p=='all-nonempty' else oldadm(s,p))]:
            a._admissible=fn
            if not any(a.admissible(s,p)!=admissible(s,p) for s in ALL for p in PS):raise RuntimeError(name)
            faults.append(name)
        a._admissible=oldadm
        for name,fn in [('witness_always_first',lambda name,s:s[0]),('witness_wrong_sign',lambda name,s:7)]:
            a.proof_witness=fn
            detected=False
            for mood,(q,r,c) in a.MOODS.items():
                for s in ALL:
                    if premise(q,r,s) and admissible(s,'middle-nonempty'):
                        w=a.proof_witness(mood,s)
                        if not(w in s and 'M' in MEMBERS[w] and 'S' in MEMBERS[w] and (('P' in MEMBERS[w])==(c=='I'))):detected=True
            if not detected:raise RuntimeError(name)
            faults.append(name)
        a.proof_witness=oldwit
        a.compress=lambda rows:(0,)
        if a.compress(((True,True,True),))==oldcompress(((True,True,True),)):raise RuntimeError('compress mutation survived')
        faults.append('erase_memberships')
    finally:
        a._truth=oldtruth;a._admissible=oldadm;a.proof_witness=oldwit;a.compress=oldcompress
        a.supports.cache_clear();a.countermodel.cache_clear()
    return faults

if __name__=='__main__':
    full_check(); f=fault_checks()
    result={'status':'PASS','checks':COUNTS,'total_checks':sum(COUNTS.values()),'detected_faults':f,'faults_detected':len(f),'scope':'Independent finite set-semantic check, not a proof of all historical claims or software correctness.'}
    print(json.dumps(result,ensure_ascii=False,indent=2))
