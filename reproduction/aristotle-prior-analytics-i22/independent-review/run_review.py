import subprocess,sys,json,hashlib,datetime,platform
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'independent-review'
records=[]
for label,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
    for command,filename in [(['independent-review/check.py'],f'result-{label}.json'),(['-m','unittest','-v','test_model.py'],f'author-tests-{label}.txt'),(['enumerate_models.py'],f'author-result-{label}.json')]:
        cmd=[sys.executable,*flags,*command];start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(cmd,cwd=root,text=True,capture_output=True)
        (out/filename).write_text(r.stdout if filename.endswith('.json') else r.stdout+r.stderr)
        records.append({'command':cmd,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':r.returncode,'stderr':r.stderr,'file':filename})
        if r.returncode:raise RuntimeError(r.stderr)
        if command==['enumerate_models.py']:
            expected=json.loads((root/'logs'/f'{label}-results.json').read_text())
            if json.loads(r.stdout)!=expected:raise RuntimeError('author saved result mismatch')
manifest=json.loads((root/'author-manifest.json').read_text());verified=[]
for p,h in manifest['files'].items():
    if hashlib.sha256((root/p).read_bytes()).hexdigest()!=h:raise RuntimeError(('manifest mismatch',p))
    verified.append(p)
(out/'commands.json').write_text(json.dumps({'environment':{'python':sys.version,'platform':platform.platform()},'runs':records,'author_hashes_verified':verified},indent=2)+'\n')
print('complete',len(verified))
