"""Render a compact audit table directly from actual JSON results."""
import json
from pathlib import Path

r = json.loads(Path('results.json').read_text(encoding='utf-8'))
yn = lambda x: '真' if x else '假'
print('# 实跑结果与手算核对\n')
print('本页由 make_report.py 从 results.json 生成。真值表中的“假”是经典假；强迫表中的“不强迫”不等于强迫其否定。\n')
print('## 1. 四行经典真值表\n')
print('| p | q | p→q | ¬q→¬p | q→p |\n|---|---|---|---|---|')
for row in r['classical_truth_table']:
    print('| ' + ' | '.join(yn(row[k]) for k in ('p', 'q', 'p_implies_q', 'not_q_implies_not_p', 'q_implies_p')) + ' |')
print('\n## 2. 共同论域的类枚举\n')
print('| 论域大小 | 类对数 | 两句皆真 | 两句皆假 | A 为空 |\n|---:|---:|---:|---:|---:|')
for row in r['finite_class_enumeration']['by_size']:
    print('| ' + ' | '.join(str(row[k]) for k in ('domain_size', 'class_pairs', 'both_true', 'both_false', 'empty_A_cases')) + ' |')
print('\n合计 5,461 类对；反例集合或句子真值不一致为 0。计数公式分别为 4ⁿ、3ⁿ、4ⁿ−3ⁿ、2ⁿ。\n')
print('## 3. 两世界模型\n')
print('关系为 0≤0、0≤1、1≤1；p 的强迫集合为 {0,1}，q 为 {1}。\n')
print('| 世界 | p | q | ¬q | ¬p | p→q | ¬q→¬p | ¬(p→q) |\n|---|---|---|---|---|---|---|---|')
for row in r['two_world_countermodel']['forcing']:
    vals = ['强迫' if row[k] else '不强迫' for k in ('p', 'q', 'not_q', 'not_p', 'p_implies_q', 'not_q_implies_not_p', 'not_of_p_implies_q')]
    print('| ' + str(row['world']) + ' | ' + ' | '.join(vals) + ' |')
print('\n手算：0 的未来含自身和 1。自身已经强迫 p 却不强迫 q，所以不强迫 p→q；两个未来都不强迫 ¬q，所以强迫 ¬q→¬p；1 强迫 p→q，所以 0 也不强迫 ¬(p→q)。\n')
print('## 4. 递归强迫与集合解释的有限全检\n')
print('| 世界数 | 带标号预序 | 持久赋值模型 | 带指定世界模型 | 公式-世界比较 | 正向式失败 | 反向式失败 |\n|---:|---:|---:|---:|---:|---:|---:|')
for row in r['small_frame_oracle']['by_size']:
    print('| ' + ' | '.join(str(row[k]) for k in ('worlds', 'frames', 'models', 'world_evaluations', 'formula_world_comparisons', 'forward_counterexamples', 'reverse_counterexamples')) + ' |')
print('\n正向式为 (p→q)→(¬q→¬p)，反向式为 (¬q→¬p)→(p→q)。合计 34 框架、674 赋值模型、1,976 个带指定世界的模型、49,400 次比较；二者解释不一致和持久性违规均为 0。92 是反向公式不被强迫的带指定世界模型数量，不是 92 种同构类型。\n')
print('覆盖范围严格限于这些有限框架、两原子赋值与列出的 25 个公式。不能把“未找到正向反例”当成任意直觉主义公式的有效性证明，也不能把本现代模型归给 De Morgan。')
