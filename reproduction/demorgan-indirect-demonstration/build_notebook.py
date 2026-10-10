"""Create an 8-cell Chinese tutorial with standard-library JSON only."""
import json
from pathlib import Path


def md(text):
    return {'cell_type': 'markdown', 'metadata': {}, 'source': text.splitlines(True)}


def code(text):
    return {'cell_type': 'code', 'metadata': {}, 'source': text.splitlines(True),
            'execution_count': None, 'outputs': []}


cells = [
    md('''# 逆否形式与间接证明：8 格教学实验

这是围绕 De Morgan 1852 年论文 pp.435–438 的现代教学重构，不是历史程序。
目标：区分等值命题与证明路径；检验共同论域的反例集合；知道经典等值的语义边界。
与本目录的 logic.py、oracle.py、run_examples.py 同目录运行。只需 Python 标准库。
本文件输出由标准库逐格执行器捕获，并非 Jupyter 内核输出；execution_count 保持 null。

## 1. 先手算四行
p→q 仅在 p 真、q 假时为假。¬q→¬p 是否也恰好在这行失败？q→p 呢？
'''),
    code('''from logic import truth_table
rows = truth_table()
for row in rows:
    print(row)
assert all(r['p_implies_q'] == r['not_q_implies_not_p'] for r in rows)
assert any(r['p_implies_q'] != r['q_implies_p'] for r in rows)
'''),
    md('''## 2. 从一个元素转向两个类
固定共同论域 U，not-B 指 U−B。Every A is B 的反例是 A∩(U−B)；
Every not-B is not-A 的反例是 (U−B)∩A。同一个元素见证两种失败。
这并不把“证明步骤相同”或“发现难度相同”包含进去。
空 A 的全称句也为真；这是本实验明确采用的无存在承诺的外延语义。
先猜 U={0,1,2}, A={0,1}, B={1,2} 的反例是谁，再执行。
'''),
    code('''from logic import class_case
from run_examples import finite_classes
r = class_case({0, 1, 2}, {0, 1}, {1, 2})
print('两种反例集合：', sorted(r['positive_counterexamples']), sorted(r['contrapositive_counterexamples']))
assert r['positive_counterexamples'] == r['contrapositive_counterexamples'] == {0}
assert class_case(set(), set(), set())['all_A_are_B']
summary = finite_classes()
print('论域大小 0–6；类对数：', summary['total_class_pairs'], '；不一致数：', summary['mismatches'])
'''),
    md('''## 3. 现代边界：两个可能继续获得信息的世界
这不是归给 1852 年作者的理论。设 0≤1，p 在两处都成立，q 只在 1 成立。
强迫 A→B：从当前世界可到达的每个世界，只要强迫 A 就强迫 B。
强迫 ¬A：所有这些世界都不强迫 A，因为 ¬A 定义为 A→⊥，而 ⊥ 无处强迫。

手算：0 尚未强迫 q，但后继 1 强迫 q，所以 0 也不强迫 ¬q。
没有世界强迫 ¬q，因此 0 强迫 ¬q→¬p。
在 0 本身 p 已成立、q 未成立，因此 0 不强迫 p→q。
1 强迫 p→q，所以 0 同样不强迫 ¬(p→q)。不要把“不强迫”读成“强迫否定”。
'''),
    code('''from logic import two_world_model, formula_suite
model, formulas = two_world_model(), formula_suite()
keys = ['p', 'q', 'not_q', 'p_implies_q', 'not_q_implies_not_p', 'not_of_p_implies_q']
for w in range(2):
    print('世界', w, {k: model.force(w, formulas[k]) for k in keys})
assert model.force(0, formulas['not_q_implies_not_p'])
assert not model.force(0, formulas['p_implies_q'])
assert not model.force(0, formulas['not_of_p_implies_q'])
'''),
    md('''## 4. 有限全检能查什么
枚举 1–3 世界上所有带标号自反、传递关系，包括非反对称的预序；
为 p、q 枚举全部向上封闭赋值，对每个世界检查 25 个明确列出的公式。
把递归强迫与独立的自底向上集合解释逐项比较，并检查公式的持久性。
覆盖所有这些有限对象，不覆盖所有公式、更大框架或任意证明。

练习：为何一世界模型找不到这类反例？因为唯一可达世界是自身，强迫退化为经典真值。
练习：若删除关系的自反边，为什么结果不可信？因为蕴涵可能漏查当前世界。
练习：若把 ¬q 写成 not force(q)，哪里坏了？它会把当前尚未建立 q 错当作已排除未来 q。
'''),
    code('''from oracle import exhaustive_small_frames
r = exhaustive_small_frames()
print(r['totals'])
assert r['totals']['frames'] == 34
assert r['totals']['models'] == 674
assert r['totals']['world_evaluations'] == 1976
assert r['totals']['formula_world_comparisons'] == 49400
assert r['totals']['forward_counterexamples'] == 0
assert r['totals']['reverse_counterexamples'] == 92
print('完整单元测试命令：python3 -m unittest -v test_logic')
''')]
notebook = {'cells': cells, 'metadata': {
    'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
    'language_info': {'name': 'python', 'file_extension': '.py'},
    'validation_note': 'Original stdlib scaffold. No package installs. Outputs populated by stdlib verification, not Jupyter.'},
    'nbformat': 4, 'nbformat_minor': 4}
Path('tutorial.ipynb').write_text(
    json.dumps(notebook, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Created 8 cells: 4 Markdown, 4 Python; no kernel execution claimed.')
