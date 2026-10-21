"""Print honest rule traces, a countermodel and bounded enumeration counts."""
import json
from itertools import product
from model import Proposition as P, derive, verify, models, nonempty_countermodel, quantity_countermodels

def main():
    shapes=[]
    for a,b in product('aeio',repeat=2):
        major,minor=P(a,'A','B'),P(b,'B','C');proof=derive(major,minor)
        if proof is not None and not verify(major,minor,proof):
            raise RuntimeError('generated certificate rejected')
        shapes.append({'major':a,'minor':b,'conclusion':proof[-1].formula.mode if proof else None,
                       'rules':[s.rule for s in proof] if proof else []})
    counts={'models':0,'aa_premises':0,'aa_failures':0,'aa_nonempty_premises':0,'aa_nonempty_failures':0,
            'bridge_universal_checks':0,'bridge_particular_checks':0}
    for n in (1,2):
        for m in models(n):
            counts['models']+=1
            p=m.evaluate(P('a','A','B')) and m.evaluate(P('a','B','C'))
            c=m.evaluate(P('a','A','C'))
            if p:
                counts['aa_premises']+=1;counts['aa_failures']+=not c
                if all(m.actual_set(t) for t in 'ABC'):
                    counts['aa_nonempty_premises']+=1;counts['aa_nonempty_failures']+=not c
            if m.quantify('a',m.possible_set('B'),'A'):
                for mode,name in (('a','universal'),('i','particular')):
                    if m.evaluate(P(mode,'B','C')):
                        counts['bridge_'+name+'_checks']+=1
                        if not m.evaluate(P(mode,'A','C')):
                            raise RuntimeError('bridge counterexample')
    m=nonempty_countermodel()
    print(json.dumps({'interpretation':'historical rule certificates versus a separate modern semantics',
                      'shapes':shapes,'quantity_countermodels':[{'worlds_ABC_masks':q.worlds,'particular_major':q.evaluate(P('i','A','B')),'universal_minor':q.evaluate(P('a','B','C')),'contingent_conclusions':[q.evaluate(P(c,'A','C')) for c in 'aeio']} for q in quantity_countermodels()],'countermodel':{'n':m.n,'worlds_ABC_masks':m.worlds,'actual':m.actual,
                       'premises':[m.evaluate(P('a','A','B')),m.evaluate(P('a','B','C'))],
                       'conclusion':m.evaluate(P('a','A','C'))},'bounded_counts':counts},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
