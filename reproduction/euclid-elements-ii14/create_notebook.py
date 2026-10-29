"""Fallback standard-library scaffold: installed skill helper absent locally."""
import json
from pathlib import Path
cells=[]
def md(text):cells.append(dict(cell_type='markdown',metadata={},source=text.splitlines(True)))
def code(text):cells.append(dict(cell_type='code',metadata={},source=text.splitlines(True),execution_count=None,outputs=[]))
md('''# Euclid II.14：把矩形面积变成正方形

教学目标：理解等积而非同形；把 II.5 的平方差和 I.47 串接起来；区分几何构造、现代有理数模型及有限检验。输入是已经得到的正边长矩形，不实现 I.45 的任意直线形转换。只需 Python 标准库，从本文件所在目录运行。''')
code('from fractions import Fraction as F\nfrom geometry import construct, sqrt_interval, check_interval\nr=construct(9,4)\nprint(r["branch"], "area =",r["area"], "EH² =",r["side_squared"])')
md('''## 1. 按原证明次序

B—G—E—F，BE=9，EF=ED=4。G 是 BF 中点：GF=GH=13/2，GE=5/2。II.5 给出 BE·EF+GE²=GF²；I.47 给出 EH²+GE²=GH²；同量减去 GE²，得到 EH²=BE·EF。

代码以有理平方量代表无理长度也可能出现的 EH；不把近似开方当作构造证明。''')
code('print("II.5:",r["area"],"+",r["offset_squared"],"=",r["radius_squared"])\nprint("I.47:",r["side_squared"],"+",r["offset_squared"],"=",r["radius_squared"])\nprint("checks:",r["checks"])')
md('''## 2. 等边分支不是遗漏

若两边已相等，矩形本来就是正方形，无须半圆。将 E=G 的情形硬塞进非退化三角形 GHE 的 I.47 调用是不合适的。交换输入仅改变命名，不改变等积目标。''')
code('s=construct(F(7,3),F(7,3))\nprint(s)\nprint("swap invariant:",construct(9,4)==construct(4,9))')
md('''## 3. 无理边长的有理包围

面积为 2，边长为 √2。二分保持 lo²≤2≤hi²，而不宣称某个有限小数等于 √2。初始上界 max(1,area)，每步区间宽度减半（碰到精确根即归零）；固定步数保证绝对宽度界，不保证固定相对精度，极端数值可需更多步。''')
code('lo,hi=sqrt_interval(2,16)\nprint(lo,"<= sqrt(2) <=",hi)\nprint("width =",hi-lo,"postcondition:",check_interval(2,lo,hi))')
md('''## 4. 边界与反例

输入严格正 int 或 Fraction；float、bool 和非正数拒绝。不能用半差 GE 直接作新正方形边，也不能误把 BE 而非 BF 作为半圆直径。这里的精确有理算术可避免浮点平方差消减，但不是任意实数构造器。''')
code('print("extreme ratio:",construct(10**120,F(1,10**120))["side_squared"])\nprint("wrong GE²:",F(9-4,2)**2,"!=",36)\nfor x in [0,-1,True,2.0]:\n    try: construct(x,1)\n    except (TypeError,ValueError) as error: print(type(error).__name__,str(error))')
md('''## 5. 练习与答案

把 9×4 矩形缩放 1/3，目标面积变为 4，正方形边长变为 2。把 2×1 矩形交换边，结果不变。为什么禁止面积 0？原构造要求正长度、严格内点和非退化目标，零面积不能作为这套前提下的实例。

运行 `python -B run_all.py`，查看真实日志及原创图 figures/ii14-equal-area.svg。本 Notebook 通过标准库 compile/exec 逐格执行并保存输出，不是 Jupyter kernel 运行；不宣称验证 kernel 集成。已读安装技能，但本地 new_notebook.py helper 不存在，故用可复现 JSON 生成器；未安装新依赖。有限实例不是一般定理证明。''')
nb=dict(nbformat=4,nbformat_minor=5,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'}},cells=cells)
for i,c in enumerate(cells):c['id']=f'ii14-{i+1:02}'
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Notebook scaffold: 5 code cells; standard-library fallback, not installed helper.')
