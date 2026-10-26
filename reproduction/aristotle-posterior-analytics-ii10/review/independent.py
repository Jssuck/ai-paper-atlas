"""Independent standard-library review; never rewrites source artifacts."""
from pathlib import Path
import hashlib, importlib.util, itertools, json, re, shutil, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]
def check(ok,msg):
    if not ok: raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
print('MODEL_SHA256',sha(root/'model.py'))
manifest=json.loads((root/'sha256.json').read_text())
for name,digest in manifest.items():check(sha(root/name)==digest,'manifest mismatch '+name)
print('ORIGINAL_MANIFEST',len(manifest),'entries verified; added independent review files excluded from original manifest')
with tempfile.TemporaryDirectory() as tmp:
    work=Path(tmp)
    for name in ('model.py','test_model.py','run_notebook.py','tutorial.ipynb'):shutil.copyfile(root/name,work/name)
    for opt in ([],['-O'],['-OO']):
        cmd=[sys.executable,*opt,'-m','unittest','-v','test_model']
        p=subprocess.run(cmd,cwd=work,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        print('COMMAND python3',' '.join(cmd[1:]));print(p.stdout,end='');check(p.returncode==0,'test failure')
    nb=json.loads((work/'tutorial.ipynb').read_text()); ids=[c.get('id','') for c in nb['cells']]
    check(len(ids)==len(set(ids)) and all(re.fullmatch('[A-Za-z0-9_-]{1,64}',i) for i in ids),'cell ids')
    before=(work/'tutorial.ipynb').read_bytes()
    p=subprocess.run([sys.executable,'run_notebook.py'],cwd=work,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    print('COMMAND python3 run_notebook.py');print(p.stdout,end='');check(p.returncode==0,'notebook failure')
    check(before==(work/'tutorial.ipynb').read_bytes(),'saved notebook differs from fresh execution')
    print('NOTEBOOK',len(ids),'unique stable IDs; saved outputs byte-identical; standard-library exec, NOT Jupyter kernel')
spec=importlib.util.spec_from_file_location('ii10_review_model',root/'model.py');m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
p=m.Proof('C','B','A','major','minor');tot=valid=empty=0
for n in range(6):
    universe=set(range(n));counts=[0,0,0]
    for c,b,a in itertools.product(range(1<<n),repeat=3):
        sets=[{i for i in range(n) if mask&(1<<i)} for mask in (c,b,a)]
        got=m.chain_report(p,universe,dict(zip(('C','B','A'),sets)))
        # Bitmask exclusion oracle; no model enumerate_chains or set-subset oracle.
        expected={'minor':(c&~b)==0,'major':(b&~a)==0,'conclusion':(c&~a)==0,'subject_exists':c!=0}
        check(got==expected,'independent bitmask mismatch');tot+=1;counts[0]+=1
        if expected['minor'] and expected['major']:
            check(expected['conclusion'],'transitivity counterexample');valid+=1;counts[1]+=1
            if c==0:empty+=1;counts[2]+=1
    check(counts==[8**n,4**n,3**n],'per-domain counting mismatch')
    print('DOMAIN_SIZE',n,'triples/valid/empty',counts)
print('INDEPENDENT_EXPANDED_TOTALS',tot,valid,empty,'mismatches=0 violations=0')
records=0
for args in itertools.product(('C','B','A','云'),repeat=5):
    p=m.Proof(*args);d=m.to_definition(p)
    check((d.subject,d.predicate,d.because_middle,d.minor_source,d.major_source)==(args[0],args[2],args[1],args[4],args[3]),'field-role mismatch')
    check(m.to_proof(d)==p,'proof roundtrip');check(m.to_definition(m.to_proof(d))==d,'definition roundtrip');records+=1
print('EXPANDED_RECORDS',records,'both roundtrips and field binding pass')
for name,digest in manifest.items():check(sha(root/name)==digest,'review mutated original '+name)
print('FINAL original artifact hashes unchanged; PASS')
