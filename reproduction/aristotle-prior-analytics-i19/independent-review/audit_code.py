"""Independent bit-mask oracle; no author predicate implementation is reused."""
import hashlib,itertools,json,pathlib,platform,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from modal_model import Model

MODES=('D','N','C','P','Box'); FORMS='aeio'; TERMS='ABC'

def check(ok,message):
    if not ok: raise RuntimeError(message)

def cat(p,s,form):
    if form=='a': return s & ~p == 0
    if form=='e': return s & p == 0
    if form=='i': return s & p != 0
    return s & ~p != 0

def oracle(rows,r,n,mode,form,p,s):
    full=(1<<n)-1
    if mode=='D':return cat(rows[r][p],rows[r][s],form)
    if mode=='Box':return all(cat(row[p],row[s],form) for row in rows)
    union=0; intersection=full
    for row in rows:
        union |= row[p]; intersection &= row[p]
    if mode=='C':
        eligible=union & ~intersection & full
    elif mode=='N':eligible=intersection if form in 'ai' else full & ~union
    else:eligible=union if form in 'ai' else full & ~intersection
    subject=rows[r][s]
    return (subject & ~eligible == 0) if form in 'ae' else (subject & eligible != 0)

def invalid_checks():
    empty={'A':set(),'B':set(),'C':set()}; good=Model([0],[empty])
    cases=[]
    for value in (None,1,'0',{True},{0.0},{'0'},iter([0])):
        cases.append((lambda value=value:Model(value,[empty]),TypeError))
    cases.append((lambda:Model([],[empty]),ValueError))
    for value in (None,1,'world',iter([empty]),{}):
        cases.append((lambda value=value:Model([0],value),TypeError))
    cases.extend([(lambda:Model([0],[]),ValueError),(lambda:Model([0],[None]),TypeError)])
    for value in ({},{'A':set(),'B':set()},{**empty,'D':set()},{**empty,'A':{1}}):
        cases.append((lambda value=value:Model([0],[value]),ValueError))
    for key in TERMS:
        for value in (None,0,'0',{False},{0.0},iter([0])):
            cases.append((lambda key=key,value=value:Model([0],[{**empty,key:value}]),TypeError))
    for value in (True,False,0.0,None,'0'):
        cases.append((lambda value=value:Model([0],[empty],value),TypeError))
    for value in (-1,1,100):cases.append((lambda value=value:Model([0],[empty],value),ValueError))
    for i in range(4):
        for value in (None,True,0,[],{},'unknown'):
            q=['D','a','A','B'];q[i]=value
            cases.append((lambda q=q:good.eval(*q),ValueError if value=='unknown' else TypeError))
    for i,(f,expected) in enumerate(cases):
        try:f()
        except expected:pass
        except Exception as e:raise RuntimeError('wrong validation exception '+str(i)) from e
        else:raise RuntimeError('invalid input accepted '+str(i))
    source={'A':{0},'B':{0},'C':set()}; model=Model([0],[source]);source['A'].clear()
    check(model.eval('D','a','A','B'),'caller mutation leaked')
    try:model.worlds[0]['A']=frozenset()
    except TypeError:pass
    else:raise RuntimeError('public world mapping mutable')
    return len(cases)

def enumerate_oracle():
    comparisons=0;configs=0;size_counts=[]
    mutations={name:None for name in ('actual_zero','swap_terms','N_as_Box','Box_as_N','P_as_N','C_as_P','e_as_a','o_as_i','i_as_a')}
    for n,k in ((1,1),(1,2),(1,3),(2,1),(2,2)):
        count=0
        for vals in itertools.product(range(1<<n),repeat=3*k):
            rows=[dict(zip(TERMS,vals[3*w:3*w+3])) for w in range(k)]
            worlds=[{t:{x for x in range(n) if row[t]&(1<<x)} for t in TERMS} for row in rows]
            for r in range(k):
                m=Model(list(range(n)),worlds,r);configs+=1;count+=1
                for mode,form,p,s in itertools.product(MODES,FORMS,TERMS,TERMS):
                    expected=oracle(rows,r,n,mode,form,p,s)
                    got=m.eval(mode,form,p,s);comparisons+=1
                    check(type(got) is bool and got==expected,'oracle disagreement '+str((n,k,r,rows,mode,form,p,s)))
                    if not all(v is not None for v in mutations.values()):
                        altered={
                            'actual_zero':oracle(rows,0,n,mode,form,p,s),
                            'swap_terms':oracle(rows,r,n,mode,form,s,p),
                            'N_as_Box':oracle(rows,r,n,'Box' if mode=='N' else mode,form,p,s),
                            'Box_as_N':oracle(rows,r,n,'N' if mode=='Box' else mode,form,p,s),
                            'P_as_N':oracle(rows,r,n,'N' if mode=='P' else mode,form,p,s),
                            'C_as_P':oracle(rows,r,n,'P' if mode=='C' else mode,form,p,s),
                            'e_as_a':oracle(rows,r,n,mode,'a' if form=='e' else form,p,s),
                            'o_as_i':oracle(rows,r,n,mode,'i' if form=='o' else form,p,s),
                            'i_as_a':oracle(rows,r,n,mode,'a' if form=='i' else form,p,s)}
                        for name,value in altered.items():
                            if mutations[name] is None and expected!=value:
                                mutations[name]={'n':n,'rows':rows,'actual':r,'query':[mode,form,p,s],'expected':expected,'mutated':value}
        size_counts.append({'objects':n,'worlds':k,'configurations':count})
    check(all(x is not None for x in mutations.values()),'mutation survived')
    return {'configurations':configs,'comparisons':comparisons,'by_size':size_counts,'semantic_mutants_detected':mutations}

def rerun_author():
    flag=[] if sys.flags.optimize==0 else ['-'+('O'*sys.flags.optimize)]
    result=subprocess.run([sys.executable,*flag,'run_checks.py'],cwd=ROOT,capture_output=True,text=True)
    check(result.returncode==0,'author enumeration rerun failed')
    actual=json.loads(result.stdout)
    label=('normal','O','OO')[sys.flags.optimize]
    saved=(ROOT/'logs'/f'{label}.log').read_text()
    old=json.loads(saved[saved.index('{'):])
    check(actual==old,'author saved enumeration differs from rerun')
    tests=subprocess.run([sys.executable,*flag,'-m','unittest','-v','test_model.py'],cwd=ROOT,capture_output=True,text=True)
    check(tests.returncode==0 and 'Ran 17 tests' in tests.stderr and '\nOK\n' in tests.stderr,'author unittest rerun failed')
    for name,digest in json.loads((ROOT/'manifest.json').read_text())['sha256'].items():
        check(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,'author manifest mismatch '+name)
    return {'enumeration_exact_json_match':True,'unit_tests':17,'unit_test_output':tests.stderr,'manifest_entries_verified':10,'enumeration':actual['enumeration']}

if __name__=='__main__':
    report={'scope':'Independent bounded implementation audit; not a general theorem or historical semantics proof.',
      'python':platform.python_version(),'optimization':sys.flags.optimize,'invalid_input_cases':invalid_checks(),
      'oracle':enumerate_oracle(),'author_rerun':rerun_author(),
      'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ('modal_model.py','examples.py','test_model.py','run_checks.py','run_all.sh','README.md','manifest.json')},
      'audit_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True))
