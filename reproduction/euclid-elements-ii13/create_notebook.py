"""Fallback scaffold: installed skill helper unavailable; standard-library JSON."""
import json
from pathlib import Path
cells=[]
def md(s): cells.append(dict(cell_type='markdown',metadata={},source=s.splitlines(True)))
def code(s): cells.append(dict(cell_type='code',metadata={},execution_count=None,outputs=[],source=s.splitlines(True)))
md('''# Euclid II.13：从内垂足的面积差到精确投影

面向具备初等几何和 Python 基础的读者。学习目标：区分原命题的全锐三角形与仅 B 锐角的现代推广；用有理坐标验证面积恒等式，而不把数值检验冒充欧几里得证明。

仅用 Python 标准库；从本 Notebook 所在目录运行。先认识原图：B=(0,0)、C=(5,0)、A=(2,4)，D=(2,0)。本例三角皆锐，D 在 BC 内部。''')
code('from fractions import Fraction as F\nfrom geometry import verify\nr = verify((2,4), (0,0), (5,0), original_only=True)\nprint(r["domain"], r["case"], "D =", r["D"], "t =", r["t"])')
md('''## 1. 原证明的链条，不从余弦定理倒推

BC 在 D 分为 BD、DC，II.7 给出 BC²+BD²=DC²+2·BC·BD。给两边同加 AD²，再用两次 I.47：BD²+AD²=BA²，DC²+AD²=AC²。由此 BC²+BA²=AC²+2·BC·BD。

代码中的 II7_algebra 是相同代数等式的检查标签，不意味着 II.7 的原始“内部分割”构形可以不加说明地用于外垂足。''')
code('print("II.7:", r["bc2"]+r["bd2"], "=", r["dc2"]+r["twice_rectangle"])\nprint("add AD²:", r["ad2"])\nprint("II.13:", r["lhs"], "=", r["ac2"], "+", r["twice_rectangle"])\nprint(r["checks"])')
md('''## 2. 任意有理坐标：避免平方根

记 v=C−B，u=A−B。t=(u·v)/(v·v)，D=B+tv。B 严格锐等价于 u·v>0；BC·BD=t|v|²=u·v，所以即使 BC 或 BD 的长度无理，矩形面积仍可精确表示为有理数。生产校验使用异常而非 assert，不受 -O/-OO 删除断言影响。''')
code('q=verify((0,2),(0,0),(1,1))\nprint("BC² =", q["bc2"], "BD² =", q["bd2"], "BC·BD =", q["rectangle"])')
md('''## 3. 三种足位置，以及一个容易漏掉的区别

全锐三角形必有 0<t<1，但逆命题不成立：内垂足时顶角 A 仍可能钝或直。因此 domain 与 case 分开返回。t=1 是 C 处直角；t>1 是 C 处钝角。后两者属于现代推广，不能称作原命题的全锐三角形。

现代推广的统一根据是展开 |u−v|²=|u|²+|v|²−2u·v；这与原证明的历史次序不同。''')
code('examples=[("all acute",(2,4)),("right C",(5,3)),("obtuse C",(7,3)),("obtuse A",(2,1))]\nfor name,A in examples:\n    s=verify(A,(0,0),(5,0))\n    print(name, s["domain"], s["case"], "t=",s["t"], "gap=",s["lhs"]-s["ac2"])')
md('''## 4. 检查定义域与边界

B 非锐、共线和重合点被拒绝；bool 与 float 坐标也被拒绝，防止近似值混入。极小正投影仍保持严格正，而不是被浮点容差抹为零。''')
code('tiny=verify((F(1,10**100),4),(0,0),(5,0),original_only=True)\nprint("tiny projection positive:",tiny["t"]>0)\nfor A in [(0,4),(-2,4),(2,0),(True,4),(2.0,4)]:\n    try:\n        verify(A,(0,0),(5,0))\n    except (ValueError,TypeError) as error:\n        print(type(error).__name__, str(error))')
md('''## 5. 自己尝试

把三个顶点同时平移、作有理正交旋转，或缩放 2/3：t 与 case 不变，面积量随缩放因子平方变化。检查 test_geometry.py 中对应测试。

插图见 figures/ii13-projection-cases.svg。运行 `python run_all.py` 得到三模式真实测试日志和本 Notebook 的 compile/exec 逐格重放日志。这不是 Jupyter kernel 执行；不声称验证浏览器排版或 kernel 集成。安装的技能已读取，但其 new_notebook.py 本地 helper 不存在，因此本脚本保留标准 nbformat 结构作可复现替代；未安装依赖。

数值实例和有限测试不能证明所有三角形；证明承担这一任务，检查器帮助发现标注、定义域与计算错误。''')
nb=dict(nbformat=4,nbformat_minor=5,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'}},cells=cells)
for i,c in enumerate(cells): c['id']=f'ii13-{i+1:02}'
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Notebook scaffold written; 5 code cells; fallback helper mode.')
