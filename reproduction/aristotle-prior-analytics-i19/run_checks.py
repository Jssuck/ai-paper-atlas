"""Bounded enumeration. Passing is NOT proof of an unrestricted theorem."""
import hashlib,itertools,json,pathlib,platform,sys
from modal_model import Model
from examples import observations


def require(ok, label, model):
    if not ok: raise RuntimeError(label+': '+json.dumps(model.as_dict(),sort_keys=True))


def enumerate_checks():
    totals={'configurations':0,'negative_universal_premises':0,
            'negative_particular_premises':0,'affirmative_mismatch_premises':0,
            'reverse_universal_premises':0,'reverse_particular_premises':0,
            'nonempty_all_actual_terms':0}
    by_size=[]
    for n,k in ((1,1),(1,2),(1,3),(2,1),(2,2)):
        domain=set(range(n)); subsets=[{x for x in range(n) if mask>>x&1} for mask in range(1<<n)]
        count=0
        for vals in itertools.product(subsets,repeat=3*k):
            worlds=[dict(zip(('A','B','C'),vals[3*w:3*w+3])) for w in range(k)]
            for actual in range(k):
                m=Model(domain,worlds,actual); e=m.eval
                totals['configurations']+=1;count+=1
                totals['nonempty_all_actual_terms']+=int(all(worlds[actual][t] for t in 'ABC'))
                for t in 'ABC':
                    for s in 'ABC':
                        require(e('C','a',t,s)==e('C','e',t,s),'C universal quality',m)
                        require(e('C','i',t,s)==e('C','o',t,s),'C particular quality',m)
                        for f in 'aeio':
                            require(not e('N',f,t,s) or e('D',f,t,s),'N implies D',m)
                            require(not e('D',f,t,s) or e('P',f,t,s),'D implies P',m)
                if e('N','e','A','B') and e('C','a','A','C'):
                    totals['negative_universal_premises']+=1
                    require(e('D','e','B','C') and e('P','e','B','C'),'negative universal theorem',m)
                if e('N','e','A','B') and e('C','i','A','C'):
                    totals['negative_particular_premises']+=1
                    require(e('D','o','B','C') and e('P','o','B','C'),'negative particular theorem',m)
                if e('N','e','A','C') and e('C','a','A','B'):
                    totals['reverse_universal_premises']+=1
                    require(e('D','e','C','B') and e('D','e','B','C'),'reverse universal theorem',m)
                if e('N','e','A','C') and e('C','i','A','B'):
                    totals['reverse_particular_premises']+=1
                    require(e('D','o','C','B'),'reverse particular theorem',m)
                if e('N','a','A','C') and e('C','a','A','B'):
                    totals['affirmative_mismatch_premises']+=1
                    require(e('D','e','B','C'),'anchored affirmative mismatch theorem',m)
        by_size.append({'objects':n,'worlds':k,'designated_configurations':count})
    return {'totals':totals,'by_size':by_size}


def main():
    report={'scope':'Modern finite teaching semantics; not a general theorem proof or unique historical interpretation.',
            'python':platform.python_version(),'optimization':sys.flags.optimize,
            'enumeration':enumerate_checks(),'examples':observations(),
            'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(pathlib.Path(__file__).parent.glob('*.py'))}}
    print(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True))

if __name__=='__main__': main()
