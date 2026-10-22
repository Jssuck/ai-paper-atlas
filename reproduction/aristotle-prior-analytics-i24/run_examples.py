import json
from fractions import Fraction
import model as m


def main():
    out={'scope':'Three figures; categorical AEIO, not modal syllogisms or a full proof checker.', 'policies':{}}
    for policy in m.POLICIES:
        rows=m.census(policy)
        valid=[f"{r['mood']}-{r['figure']}" for r in rows if r['valid']]
        failures=[]
        for r in rows:
            if not r['valid']: continue
            x,y,z=r['mood']
            if not (x in 'AI' or y in 'AI'): failures.append('affirmative')
            if not (x in 'AE' or y in 'AE'): failures.append('universal')
            if z in 'AE' and not (x in 'AE' and y in 'AE'): failures.append('universal conclusion')
        out['policies'][policy]={'model_count':len(m.models(policy)), 'mood_count':len(rows), 'valid_count':len(valid),'valid_moods':valid,'necessary_condition_failures':failures}
    out['examples']=[m.classify(f,mode,p) for f,mode,p in ((1,'III','all_terms_nonempty'),(2,'EEE','all_terms_nonempty'),(2,'AAA','all_terms_nonempty'),(3,'AAI','allow_empty_terms'),(3,'AAI','all_terms_nonempty'),(3,'AAA','all_terms_nonempty'),(1,'AAA','allow_empty_terms'))]
    # Musical pleasure S, pleasure M, commendable P: one other pleasure is P,
    # all musical pleasure is pleasure, but no musical pleasure is P.
    mask=(1<<5)|(1<<6)
    out['music']={'mask':mask,'domain':sorted(m.domain(mask)), 'extensions':{t:sorted(m.extension(mask,t)) for t in m.TERMS}, 'some_pleasure_commendable':m.proposition(mask,'I','M','P'),'all_music_pleasure':m.proposition(mask,'A','S','M'),'all_music_commendable':m.proposition(mask,'A','S','P')}
    out['subtraction']=m.equal_remainders(Fraction(9,2),Fraction(9,2),Fraction(1,3),Fraction(1,3))
    out['subtraction']['remainders']=list(map(str,out['subtraction']['remainders']))
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
