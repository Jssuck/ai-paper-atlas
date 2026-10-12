"""Review evidence recorder. Does not overwrite builder evidence."""
import subprocess,sys,os,json,hashlib,datetime,platform,tempfile,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'independent-review'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def files(): return {str(p.relative_to(ROOT)):sha(p) for p in sorted(ROOT.iterdir()) if p.suffix in ('.py','.md')}
before=files(); records=[]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
def run(label,command,cwd=ROOT):
    p=subprocess.run(command,cwd=cwd,env=env,text=True,capture_output=True)
    for stream in ('stdout','stderr'): (OUT/f'{label}.{stream}.txt').write_text(getattr(p,stream))
    records.append(dict(label=label,command=command,cwd='.' if cwd==ROOT else '<temporary-isolated-copy>',exit_code=p.returncode,stdout=f'{label}.stdout.txt',stderr=f'{label}.stderr.txt'))
    return p
for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
    for label,tail in [('tests',['-m','unittest','-v']),('reviewer',['independent-review/reviewer_checks.py']),('demo',['demo.py']),('mutations',['mutation_check.py']),('walkthrough',['walkthrough.py']),('argument_auditor',['independent_argument_checks.py'])]:
        p=run(f'{label}_{mode}',[sys.executable]+flags+tail)
        if p.returncode: raise RuntimeError(f'{label} {mode} failed')
# Logger behavior tested in isolated copies with controlled programs; originals unchanged.
probes={}
with tempfile.TemporaryDirectory(prefix='condillac-review-') as temp:
    tmp=Path(temp)
    for name in ['demo.py','walkthrough.py','mutation_check.py','independent_argument_checks.py']:
        (tmp/name).write_text("print('stable')\n")
    shutil.copy2(ROOT/'verify.py',tmp/'verify.py')
    (tmp/'test_probe.py').write_text('import unittest\nclass Probe(unittest.TestCase):\n def test_fail(self): self.fail("intentional reviewer failure")\n')
    p=run('logger_failed_test',[sys.executable,'verify.py'],tmp)
    summary=json.loads((tmp/'evidence/summary.json').read_text())
    probes['failed_test']={'exit':p.returncode,'passed':summary['passed'],'records':len(summary['commands']),'failing_records':sum(x['exit_code']!=0 for x in summary['commands'])}
    if p.returncode!=1 or summary['passed'] or len(summary['commands'])!=15: raise RuntimeError('failure propagation failed')
    (tmp/'test_probe.py').write_text('import unittest\nclass Probe(unittest.TestCase):\n def test_ok(self): self.assertTrue(True)\n')
    (tmp/'demo.py').write_text('import sys\nprint(sys.flags.optimize)\n')
    p=run('logger_nondeterministic',[sys.executable,'verify.py'],tmp)
    summary=json.loads((tmp/'evidence/summary.json').read_text())
    probes['nondeterministic']={'exit':p.returncode,'passed':summary['passed'],'deterministic':summary['deterministic_stdout_across_modes'],'all_children_succeeded':all(x['exit_code']==0 for x in summary['commands'])}
    if p.returncode!=1 or summary['passed'] or summary['deterministic_stdout_across_modes']: raise RuntimeError('determinism check failed')
    (tmp/'demo.py').write_text("print('stable')\n")
    p=run('logger_success',[sys.executable,'verify.py'],tmp)
    summary=json.loads((tmp/'evidence/summary.json').read_text())
    probes['success']={'exit':p.returncode,'passed':summary['passed'],'hashes_match':all(summary['files_sha256'][x.name]==sha(x) for x in tmp.glob('*.py'))}
    if p.returncode or not summary['passed'] or not probes['success']['hashes_match']: raise RuntimeError('logger positive control failed')
deterministic=all((OUT/f'{label}_normal.stdout.txt').read_bytes()==(OUT/f'{label}_{mode}.stdout.txt').read_bytes() for label in ['demo','mutations','walkthrough'] for mode in ['O','OO'])
after=files()
if not deterministic: raise RuntimeError('stdout differs across optimization modes')
if before!=after: raise RuntimeError('reviewed files changed during review; rerun required')
report={'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'platform':platform.platform(),'environment_overrides':{'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'},'independence':'Separate reviewer authored constructive checks and logger probes; existing argument auditor rerun but not claimed as reviewer work.','scope':'Modern teaching reconstruction only, not historical executable or independent source-image review.','path_display':'Working directory is relative to this package; disposable probe directories are labeled <temporary-isolated-copy>. Private absolute working-directory prefixes are omitted from public metadata.','reviewed_files_sha256':after,'review_artifacts_sha256':{p.name:sha(p) for p in sorted(OUT.iterdir()) if p.suffix in ('.py','.md')},'commands':records,'logger_probes':probes,'deterministic_stdout_across_modes':deterministic,'source_unchanged_during_review':before==after,'logs_sha256':{p.name:sha(p) for p in sorted(OUT.glob('*.txt'))},'limitations':['Finite adversarial tests support but do not prove universal correctness.','verify.py collects all results then exits nonzero: failure propagation is present, immediate fail-fast is not.','Subprocess timeout is not implemented; a nonterminating future child can stall verification.']}
(OUT/'review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','commands':len(records),'logger_probes':probes,'bound_files':len(after)},ensure_ascii=False,indent=2))
