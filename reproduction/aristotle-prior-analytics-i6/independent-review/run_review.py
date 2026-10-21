"""Re-execute independent and author checks; public paths are relative."""
from pathlib import Path
import hashlib,json,subprocess,sys,platform
R=Path(__file__).resolve().parents[1];D=R/'independent-review'
runs=[]
for name,flags in [('normal',[]),('optimized',['-O']),('double-optimized',['-OO'])]:
    for label,args in [('author',['-m','unittest','-v','test_third_figure']),('independent',['independent-review/audit_third_figure.py'])]:
        p=subprocess.run([sys.executable,*flags,*args],cwd=R,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (D/f'{label}-{name}.log').write_text('COMMAND: python '+' '.join(flags+args)+'\n'+p.stdout,encoding='utf8')
        if p.returncode:raise SystemExit(p.returncode)
        runs.append({'kind':label,'mode':name,'exit_code':p.returncode})
        if label=='independent':
            result=json.loads(p.stdout);(D/f'results-{name}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
results=[(D/f'results-{name}.json').read_bytes() for name in ['normal','optimized','double-optimized']]
if not all(x==results[0] for x in results):raise RuntimeError('independent reports differ')
names=['third_figure.py','test_third_figure.py','run_verification.py','README.md','WALKTHROUGH.md','REPORT.md','report.json','witnesses.json']
files=sorted([R/n for n in names]+[p for p in (R/'logs').iterdir() if p.is_file()])
(D/'reviewed-files.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(R))+'\n' for p in files),encoding='utf8')
summary={'status':'PASS','runs':runs,'independent_reports_identical':True,'reviewed_file_count':len(files),'environment':{'python':platform.python_version(),'implementation':platform.python_implementation(),'system':platform.system(),'machine':platform.machine()},'result':json.loads(results[0])}
(D/'verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':'PASS','runs':len(runs),'reviewed_files':len(files),'independent_checks_per_mode':summary['result']['total_checks']}))
