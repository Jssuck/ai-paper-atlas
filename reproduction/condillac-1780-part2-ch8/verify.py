"""Actually run three optimization modes and preserve local evidence; fail closed."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import unittest


def fingerprints(root):
    paths=sorted(root.glob('*.py')) + [root/'README.md',root/'MODEL.zh-CN.md',root/'WALKTHROUGH.zh-CN.md']
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def main():
    root=Path(__file__).resolve().parent
    evidence=root/'evidence'
    evidence.mkdir(exist_ok=True)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
    before=fingerprints(root)
    count=unittest.defaultTestLoader.discover(str(root)).countTestCases()
    records=[]
    checks=[('demo',['demo.py']),('tests',['-m','unittest','-v']),
            ('mutations',['mutation_check.py']),('walkthrough',['walkthrough.py']),
            ('independent_argument',['independent_argument_checks.py'])]
    for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
        for label,tail in checks:
            command=[sys.executable]+flags+tail
            result=subprocess.run(command,cwd=root,env=env,text=True,capture_output=True)
            stem=f'{label}_{mode}'
            (evidence/f'{stem}.stdout.txt').write_text(result.stdout,encoding='utf-8')
            (evidence/f'{stem}.stderr.txt').write_text(result.stderr,encoding='utf-8')
            records.append({'mode':mode,'check':label,'command':[Path(sys.executable).name]+flags+tail,'exit_code':result.returncode,
                            'stdout':f'{stem}.stdout.txt','stderr':f'{stem}.stderr.txt'})
    after=fingerprints(root)
    stable=before==after
    deterministic=all((evidence/f'{label}_normal.stdout.txt').read_bytes()==
                      (evidence/f'{label}_{mode}.stdout.txt').read_bytes()
                      for label in ('demo','mutations','walkthrough') for mode in ('O','OO'))
    summary={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'python':sys.version,'interpreter_basename':Path(sys.executable).name,
             'command_display_note':'Commands show the portable interpreter basename; subprocesses used the running interpreter via sys.executable.',
             'platform':platform.platform(),
             'implementation':platform.python_implementation(),
             'environment_overrides':{'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'},
             'unit_test_count_per_mode':count,'files_sha256_before':before,'files_sha256_after':after,
             'source_files_unchanged_during_run':stable,'commands':records,
             'deterministic_stdout_across_modes':deterministic,
             'passed':all(r['exit_code']==0 for r in records) and deterministic and stable}
    (evidence/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# 实际验证记录','',f"执行时间（UTC）：{summary['timestamp_utc']}",'',
           f"Python：{sys.version}",'',f"平台：{platform.platform()}",'',
           f"总结果：{'PASS' if summary['passed'] else 'FAIL'}。每种模式运行{count}个单元测试；13个行为故障探针另行执行。",'',
           f'普通、-O、-OO 的 demo／mutations／walkthrough stdout 字节一致：{deterministic}。',
           f'运行前后被记录源码及静态文档哈希不变：{stable}。','',
           '## 真实命令与日志','',
           '命令按可移植解释器名称展示；实际子进程使用运行本验证器的同一个 sys.executable。安装目录不写入公开记录。','']
    for record in records:
        lines.append(f"- `{record['mode']}` / `{record['check']}`：`{' '.join(record['command'])}`；退出码 {record['exit_code']}；[stdout](evidence/{record['stdout']}) / [stderr](evidence/{record['stderr']})")
    lines+=['','[环境、命令、退出码与文件 SHA-256 汇总](evidence/summary.json)。', '',
            '作者单元测试涵盖输入拒绝、同答案多世界、空域、逐步改写、编码纤维、测量策略和可执行因果机制。变异分类器另检验 baseline_error、invalid_baseline、mutant_error、survived 与 killed；异常不算击杀。', '',
            '独立论证审计由另一审计者编写，采用位掩码分割与逐层有限深度树存在性 oracle。该脚本输出自己的范围、实际案例数和模型／脚本哈希；其 optimization 字段按模式变化，不要求整份 stdout 相同。独立审核意见与作者本地运行日志分开。', '',
            '每个子进程都真实运行；任一非零退出、指定演示跨模式不一致或被记录文件运行中改变，均使 verify.py 退出1。本验证器调用的核心、演示、作者测试和穷举论证审计不使用网络、随机数或第三方安装；其他独立审核可使用固定种子补充案例。拒绝检查不依赖 assert。有限核对不是史学证据，也不是未给假设范围内的一般证明。']
    (root/'VERIFICATION.zh-CN.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'passed':summary['passed'],'commands':len(records),
                      'unit_tests_per_mode':count,'deterministic_stdout_across_modes':deterministic,
                      'source_files_unchanged_during_run':stable},indent=2))
    return 0 if summary['passed'] else 1


if __name__=='__main__': raise SystemExit(main())
