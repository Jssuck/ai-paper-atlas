"""Run actual subprocess checks, preserving evidence for three optimization modes."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parent
    evidence = root/'evidence'
    evidence.mkdir(exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
    records = []
    for mode, flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
        for label, tail in [('demo',['demo.py']),('tests',['-m','unittest','-v']),('mutations',['mutation_check.py']),('walkthrough',['walkthrough.py']),('independent_argument',['independent_argument_checks.py'])]:
            command = [sys.executable]+flags+tail
            result = subprocess.run(command,cwd=root,env=env,text=True,capture_output=True)
            stem=f'{label}_{mode}'
            (evidence/f'{stem}.stdout.txt').write_text(result.stdout)
            (evidence/f'{stem}.stderr.txt').write_text(result.stderr)
            records.append({'mode':mode,'check':label,'command':command,'exit_code':result.returncode,'stdout':f'{stem}.stdout.txt','stderr':f'{stem}.stderr.txt'})
    deterministic = all((evidence/f'{label}_normal.stdout.txt').read_bytes()==(evidence/f'{label}_{mode}.stdout.txt').read_bytes() for label in ('demo','mutations','walkthrough') for mode in ('O','OO'))
    summary={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'platform':platform.platform(),'implementation':platform.python_implementation(),'environment_overrides':{'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'},'files_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.glob('*.py'))},'commands':records,'deterministic_stdout_across_modes':deterministic,'passed':all(x['exit_code']==0 for x in records) and deterministic}
    (evidence/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    lines=['# 实际验证记录','',f"核验时间（UTC）：{summary['timestamp_utc']}",'',f"Python：{sys.version}",'',f"平台：{platform.platform()}",'',f"总结果：{'PASS' if summary['passed'] else 'FAIL'}。普通、-O、-OO 的演示、变异与演练 stdout 完全一致：{deterministic}。",'', '每种模式运行9个单元测试、8个行为变体和独立行列式／叉积审计（35,308个方程组、176,540次行操作）。45个参数组的整数正方形核对、729个二行系统的有理样点核对在单元测试内执行。样点测试不是一般证明。','', '## 命令和退出码','']
    for r in records:
        lines.append(f"- `{r['mode']}` / `{r['check']}`：`{' '.join(r['command'])}`；退出码 {r['exit_code']}；[stdout](evidence/{r['stdout']}) / [stderr](evidence/{r['stderr']})")
    lines+=['','[机器可读环境、命令与源码 SHA-256](evidence/summary.json)。无网络、随机数、第三方安装。所有拒绝检查使用显式异常，测试使用 unittest，不依赖可被优化移除的 assert。','', '验证器保存退出码与原始日志，任一子进程失败或跨模式确定性检查失败都会使其自身退出1。日志时间与主机信息是执行事实，不是历史来源证据。']
    (root/'VERIFICATION.zh-CN.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'passed':summary['passed'],'commands':len(records),'deterministic_stdout_across_modes':deterministic},indent=2))
    return 0 if summary['passed'] else 1

if __name__ == '__main__': raise SystemExit(main())
