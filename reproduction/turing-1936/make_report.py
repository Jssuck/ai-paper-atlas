"""Render small article-ready trace tables from the actual JSON capture."""
import json
from pathlib import Path
r = json.loads(Path('results.json').read_text())
print('# 实际运行轨迹与可插入正文的小结\n')
print('以下数据读取自 results.json；表中每一行是完成指定步数后的配置。空纸带记为 ∅，空输出记为 ε。cap_reached 只表示模拟预算用完。\n')
for key, title in [('alternating_6', 'A：交替序列，6步'),
                   ('source_aligned_alternating_12', 'A2：间隔格版本，12步'),
                   ('one_then_silent_12', 'B：输出一次后继续移动，12步'),
                   ('delayed_20_at_cap_24', 'C：等待20步，第21步才首次输出')]:
    case = r['cases'][key]
    print('## ' + title + '\n')
    print('| 步数 | 状态 | 读头 | 当前读符号 | 本步输出 | 累计输出 | 非空白格 |')
    print('|---:|---|---:|---|---|---|---|')
    for row in case['trace']:
        if key == 'delayed_20_at_cap_24' and 3 < row['step'] < 19:
            continue
        tape = ', '.join(f'{k}:{v}' for k, v in row['tape'].items()) or '∅'
        print(f"| {row['step']} | {row['state']} | {row['head']} | {row['scanned']} | {row['emitted'] or 'ε'} | {row['output'] or 'ε'} | {tape} |")
    if key == 'delayed_20_at_cap_24':
        print('\n为便于阅读省略第4–18步，完整轨迹保存在 JSON 中。')
    print(f"\n末状态：{case['status']}。\n")
print('## 正文可用的结果陈述\n')
environment = r['environment']
print(f"实际执行环境：{environment['implementation']} {environment['python'].split()[0]}。依赖：{environment['dependencies']}。")
print('测试结果请单独查看 [tests.log](tests.log)；本报告不从轨迹数据推断测试是否通过。\n')
for key, title in [('alternating_6', '交替机'),
                   ('source_aligned_alternating_12', '间隔格版本'),
                   ('one_then_silent_12', '输出一次后继续移动'),
                   ('delayed_20_at_cap_20', '等待机的较短观察'),
                   ('delayed_20_at_cap_24', '等待机的较长观察')]:
    case = r['cases'][key]
    first = next((row['step'] for row in case['trace'] if row['emitted']), None)
    first_text = f"；观察到首次输出在第{first}步" if first is not None else '；本次未观察到输出'
    print(f"- {title}：执行{case['steps']}步，累计输出 {case['output'] or 'ε'}{first_text}。")
enumeration = r['finite_enumeration']
histogram = '、'.join(f"{length}位{count}台" for length, count in
                      enumeration['observed_output_length_histogram'].items())
print(f"\n受限表类实际枚举{enumeration['machine_count']}张表，每台观察上限{enumeration['cap_per_machine']}步；输出长度分布：{histogram}。\n")
print('这些是教学实现的实际有限运行证据。具体例子的无限行为可从其规则另作归纳证明；有限样本、超时和小规模穷举都不证明或反驳任意机器上的不可判定性定理。')
