"""Independent set/profile oracle and mutation audit; no theorem from finite checks."""
import hashlib, itertools, json, pathlib, platform, random, subprocess, sys, types
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import model


def need(condition, message):
    if not condition: raise RuntimeError(message)


def oracle(n, rows, actual, p, s, f, mode):
    # Decode into lists of object IDs, independently of author extension API.
    subjects=[x for x in range(n) if (rows[actual][s]//(2**x))%2]
    per_object=[]
    for x in subjects:
        profile=[bool((r[p]//(2**x))%2) for r in rows]
        if f in 'EO': profile=[not v for v in profile]
        count=sum(profile)
        if mode=='actual': value=profile[actual]
        elif mode=='possible': value=count>0
        elif mode=='necessary': value=count==len(rows)
        else: value=0<count<len(rows)
        per_object.append(value)
    return (False not in per_object) if f in 'AE' else (True in per_object)


def compare(cls, cases):
    totals={'configurations':0,'categorical':0,'extensions':0,'persistent':0,'rigid':0,'joint':0}
    for n,rows,actual in cases:
        obj=cls(n,rows,actual); totals['configurations']+=1
        sets=[[{x for x in range(n) if (mask//2**x)%2} for mask in row] for row in rows]
        for p,P in enumerate('ABC'):
            need(obj.rigid(P)==all(row[p]==sets[actual][p] for row in sets),'rigid'); totals['rigid']+=1
            for w in range(len(rows)):
                need(obj.extension(P,w)==sets[w][p],'extension'); totals['extensions']+=1
            for s,S in enumerate('ABC'):
                need(obj.persistent_exclusion(P,S)==all(not(row[p]&row[s]) for row in sets),'exclusion'); totals['persistent']+=1
                for positive in (True,False):
                    target=sets[actual][s]
                    want=any(all((x in row[p])==positive for x in target) for row in sets)
                    need(obj.jointly_possible(P,S,positive)==want,'joint'); totals['joint']+=1
                for f in 'AEIO':
                    for mode in ('actual','possible','necessary','contingent'):
                        need(obj.categorical(P,S,f,mode)==oracle(n,rows,actual,p,s,f,mode),'categorical '+str((n,rows,actual,P,S,f,mode)))
                        totals['categorical']+=1
    return totals


def cases():
    for n in (1,2):
        for flat in itertools.product(range(2**n),repeat=6):
            rows=(tuple(flat[:3]),tuple(flat[3:]))
            for actual in (0,1): yield n,rows,actual
    rng=random.Random(18003719)
    for _ in range(128):
        rows=tuple(tuple(rng.randrange(8) for _ in range(3)) for _ in range(3))
        for actual in (0,1,2): yield 3,rows,actual


def negative():
    count=0
    def reject(call):
        nonlocal count
        try: call()
        except ValueError: count+=1; return
        raise RuntimeError('invalid input not rejected')
    valid=((0,0,0),)
    for n in (0,-1,True,False,1.0,'1',None): reject(lambda n=n:model.Model(n,valid))
    for rows in ((),[],None,[(0,0,0)],(0,),((0,0),),((0,0,0,0),),([0,0,0],),((2,0,0),),((-1,0,0),),((True,0,0),),((0.0,0,0),)):reject(lambda rows=rows:model.Model(1,rows))
    for actual in (-1,1,True,False,0.0,'0',None):reject(lambda actual=actual:model.Model(1,valid,actual))
    m=model.Model(1,valid)
    for bad in ('D','',None,0,[],True):
        reject(lambda bad=bad:m.extension(bad))
        reject(lambda bad=bad:m.categorical(bad,'B','A'))
        reject(lambda bad=bad:m.categorical('A',bad,'A'))
        reject(lambda bad=bad:m.rigid(bad))
        reject(lambda bad=bad:m.persistent_exclusion('A',bad))
        reject(lambda bad=bad:m.jointly_possible(bad,'B'))
    for bad in ('X','',None,0,[],True): reject(lambda bad=bad:m.categorical('A','B',bad))
    for bad in ('Q','',None,0,[],True): reject(lambda bad=bad:m.categorical('A','B','A',bad))
    for bad in (-1,1,True,False,0.0,'0'):reject(lambda bad=bad:m.extension('A',bad))
    for bad in (0,1,None,'true',[]):reject(lambda bad=bad:m.jointly_possible('A','B',bad))
    for args in ((0,2),(-1,2),(True,2),(1.0,2),(1,0),(1,-1),(1,False),(1,2.0)):reject(lambda args=args:next(model.models(*args)))
    return count


def mutations():
    source=(ROOT/'model.py').read_text()
    changes=[('possible-as-necessary',"'possible': any(signs)","'possible': all(signs)"),
      ('necessity-as-possibility',"'necessary': all(signs)","'necessary': any(signs)"),
      ('contingent-as-possible','any(signs) and not all(signs)','any(signs)'),
      ('all-forms-existential',"return all(answers) if form in ('A', 'E') else any(answers)",'return any(answers)'),
      ('wrong-actual','signs[self.actual]','signs[0]'),
      ('negative-is-positive',"(form in ('A', 'I'))","(form in ('A', 'E', 'I', 'O'))"),
      ('persistent-is-one-world','return all(x.isdisjoint(y) for x, y in zip(left, right))','return any(x.isdisjoint(y) for x, y in zip(left, right))'),
      ('rigid-is-vacuous','return all(self.extension(term, w) == actual for w in range(len(self.worlds)))','return True'),
      ('joint-is-every-world','return any(s <= p if positive else s.isdisjoint(p) for p in ps)','return all(s <= p if positive else s.isdisjoint(p) for p in ps)')]
    out=[]
    tiny=[(1,(tuple(flat[:3]),tuple(flat[3:])),a) for flat in itertools.product(range(2),repeat=6) for a in (0,1)]
    for i,(name,old,new) in enumerate(changes):
        need(source.count(old)==1,'mutation target count')
        module=types.ModuleType('mutant_'+str(i));sys.modules[module.__name__]=module
        exec(compile(source.replace(old,new),'mutant','exec'),module.__dict__)
        try:compare(module.Model,tiny)
        except RuntimeError:out.append({'name':name,'detected':True})
        else:raise RuntimeError('undetected mutant '+name)
    return out


def main():
    totals=compare(model.Model,cases())
    totals['invalid_input_probes']=negative()
    totals['mutations']=mutations()
    # Regenerate the author's outputs, compare exact parsed JSON without trusting it as oracle.
    import demo
    result=demo.run()
    stored=json.loads((ROOT/'results/demo.json').read_text())
    need(json.loads(json.dumps(result))==stored,'author output mismatch')
    for name in ('demo-O.json','demo-OO.json'):need((ROOT/'results'/name).read_bytes()==(ROOT/'results/demo.json').read_bytes(),'mode output mismatch')
    totals['author_rerun']={k:result[k] for k in ('configurations','checks','forward_bridge_cases','reverse_rigid_bridge_cases','raw_rule_counterexamples','contingent_quality_equivalences')}
    totals['named_models_checked']=len(model.named_models())
    for m in model.named_models().values():compare(model.Model,[(m.n,m.worlds,m.actual)])
    totals['author_failed_pairs']=len(result['failed_family_pairs'])
    totals['scope']='Complete n=1,2 two labelled worlds/both actual points plus deterministic 128 three-object three-world rows/all three actual points. No general completeness claim.'
    print(json.dumps(totals,indent=2))

if __name__=='__main__':main()
