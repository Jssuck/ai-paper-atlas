"""Reproduce the independent checks and deterministic report comparison."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shlex
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent
FILES=('logic.py','proofs.py','demo.py','test_model.py','verify.py','independent-review/audit_checks.py')
def hashes():
    return {f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in FILES}
def execute(mode):
    flags={'normal':[], 'O':['-O'], 'OO':['-OO']}[mode]
    command=[sys.executable,*flags,'-B','independent-review/audit_checks.py']
    start=datetime.now(timezone.utc).isoformat()
    result=subprocess.run(command,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log=f'UTC start: {start}\nCommand: {shlex.join(command)}\n'+result.stdout+f'\nExit code: {result.returncode}\n'
    (OUT/f'{mode}.log').write_text(log)
    counts=json.loads(result.stdout.strip().splitlines()[-1]) if result.returncode==0 else None
    return {'mode':mode,'command':command,'exit_code':result.returncode,'result':counts}
def main():
    before=hashes()
    runs=list(ThreadPoolExecutor(max_workers=3).map(execute,('normal','O','OO')))
    outputs=[]; report_checks=[]
    for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
        for seed in ('0','141','271828'):
            env=dict(os.environ,PYTHONHASHSEED=seed)
            command=[sys.executable,*flags,'-B','demo.py']
            proc=subprocess.run(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            name=f'demo-{mode}-seed{seed}.json'
            (OUT/name).write_bytes(proc.stdout)
            outputs.append(proc.stdout)
            report_checks.append({'mode':mode,'hashseed':seed,'command':command,'exit_code':proc.returncode,
                                  'sha256':hashlib.sha256(proc.stdout).hexdigest(),'stderr':proc.stderr.decode()})
    same=bool(outputs[0]) and all(output==outputs[0] for output in outputs)
    report_matches=(ROOT/'report.json').read_bytes()==outputs[0]
    after=hashes()
    summary={'run_started_source_hashes':before,'run_finished_source_hashes':after,
             'source_hashes_unchanged':before==after,'python':sys.version,'platform':platform.platform(),
             'runs':runs,'report_runs':report_checks,'all_nine_report_outputs_identical':same,
             'stored_report_matches':report_matches,
             'passed':before==after and all(r['exit_code']==0 for r in runs) and same and report_matches and all(r['exit_code']==0 for r in report_checks)}
    (OUT/'run-results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True))
    return 0 if summary['passed'] else 1
if __name__=='__main__':
    raise SystemExit(main())
