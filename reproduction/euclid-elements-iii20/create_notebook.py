"""Standard-library fallback: installed skill helper was not available locally."""
import json
from pathlib import Path
cells=[]
def md(s):cells.append(dict(cell_type='markdown',metadata={},source=s.splitlines(True)))
def code(s):cells.append(dict(cell_type='code',metadata={},source=s.splitlines(True),execution_count=None,outputs=[]))
md('# Euclid III.20：同弧条件与现代扩展\n\n从本目录启动。仅 Python 标准库；Fraction 精确运算。以下是现代教学模型，不是古代算法复现，不以有限样本证明一般定理。已用 compile/exec 顺序执行并回放核验；不是 Jupyter kernel 执行。')
code('from geometry import EXAMPLES, check, grid\nfrom fractions import Fraction\nprint("exact model: Fraction; no angle rounding in checks")\n')
md('## 1. 原证两分支\n加法与减法的样本；输出 central 与 doubled 是所选圆心角和二倍圆周角的余弦、正弦，不是弧度值。')
code('for name in ("addition", "subtraction"):\n    r=check(*EXAMPLES[name])\n    print(name, r["center_location"], r["arc"], r["central"], r["doubled"])\n')
md('## 2. 两种不同边界\n一条圆周角边通过圆心，不等于所对底弦为直径。')
code('for name in ("side_boundary", "base_diameter"):\n    r=check(*EXAMPLES[name])\n    print(name, r["side_through_center"], r["base_diameter"], r["central"])\n')
md('## 3. 反角的现代扩展与错误 minor 规则\n反角对应的 sine 为负；只取较小圆心角会将该符号改错。此扩展不能归于 Euclid 原证已经全部陈述。')
code('r=check(*EXAMPLES["reflex_extension"])\nwrong=(r["central"][0], abs(r["central"][1]))\nprint("selected", r["central"], "wrong minor", wrong)\nif wrong == r["doubled"]: raise RuntimeError("counterexample lost")\n')
md('## 4. 有限穷举\n10 个有理圆点的 720 个互异有序三元组，经 3 种相似变换（含反射）共 2160 个样本。不是对所有实数点的穷举。')
code('print(grid())\n')
n=dict(cells=cells,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'execution_method':'stdlib compile/exec; not a kernel'},nbformat=4,nbformat_minor=5)
for i,c in enumerate(cells):c['id']='iii20-'+str(i)
Path('teaching.zh-CN.ipynb').write_text(json.dumps(n,ensure_ascii=False,indent=2)+'\n')
