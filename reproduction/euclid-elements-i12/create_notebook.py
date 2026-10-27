"""Build an original nbformat 4.5 tutorial with plain-Python execution provenance.
Installed skill guidance was read; its scaffold helper was not present locally.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
cells=[]
def md(text):cells.append({'cell_type':'markdown','id':f'md-{len(cells)}','metadata':{},'source':text.strip().splitlines(keepends=True)})
def code(text):cells.append({'cell_type':'code','id':f'code-{len(cells)}','metadata':{},'source':text.strip().splitlines(keepends=True),'execution_count':None,'outputs':[]})
md('''# Euclid I.12：从线外点向无限直线引垂线
目标：跟踪异侧辅助点、圆的两交点、中点与直角结论的不同责任。
这是原创现代精确坐标教学重构；它不实现古代所有尺规子程序，不以有限测试证明一般定理。
公开输出用标准库 compile/exec 在共享命名空间顺序执行，不是 Jupyter kernel，不声称验证 Notebook 浏览器显示。''')
code('''from pathlib import Path
if not Path('geometry.py').is_file():
    raise RuntimeError('请在 Notebook 所在目录执行')
from dataclasses import replace
from fractions import Fraction as F
from geometry import *
from cases import positive_cases, rejected_cases
print('Rational inputs; exact single quadratic extension; no floating predicates.')''')
md('''## 1. 圆线交点的精确计算
取 A=(0,0), B=(1,0), C=(2,3), D=(4,-1)。D 与 C 位于 AB 异侧。
圆半径平方为20，交点横坐标为2±√11。先解交点，再取中点，不把垂足坐标直接当证明。''')
code('''a,b,c,d=point(0,0),point(1,0),point(2,3),point(4,-1)
k=construct(a,b,c,d)
for label,p in [('E',k.e),('G',k.g),('H',k.h)]:
    print(label,tuple(map(str,p)))
print('r squared:',str(k.radius_squared))
print('all certificate checks:',check_certificate(a,b,c,d,k))''')
md('''## 2. 无限直线不等于给定线段
H=(2,0) 在线段 AB 之外，参数 t=2 仍是合法垂足。改变异侧 D 改变辅助圆及弦长，却不改变垂足。
端点交换只交换两个交点的命名，不改变几何构造结论。''')
code('''print('foot t:',str(foot_parameter(a,b,k.h)))
k2=construct(a,b,c,point(-7,-4))
print('changed D; same foot:',k2.h==k.h,'same radius:',k2.radius_squared==k.radius_squared)
swapped=construct(b,a,c,d)
print('swapped labels:',swapped.e==k.g and swapped.g==k.e,'same H:',swapped.h==k.h)''')
md('''## 3. 为什么必须检查构造证书，而不只看垂直结论
保持 H=(2,0)，伪造 E=(3,0),G=(1,0)。中点和垂直性仍成立，但它们不在指定半径平方20的圆上。
因此“得到了垂足”和“执行了本次指定构造”是不同层次的核验。''')
code('''forged=replace(k,e=point(3,0),g=point(1,0))
facts=check_certificate(a,b,c,d,forged)
print({name:facts[name] for name in ['H_is_midpoint','perpendicular_modern_check','E_on_prescribed_circle']})
print('full certificate accepted:',accepted(a,b,c,d,forged))''')
md('''## 4. 拒绝不等于数学上不可能
D 与 C 同侧时，圆可能不交线、相切，也可能仍为割线。I.12 的异侧取点给出统一充分保证。
本检查器认证所指定的异侧版本，拒绝同侧输入并不证明它一定没有两交点。''')
code('''for label,D in [('same side small radius',point(2,2)),('same side large radius',point(12,2)),('D on line',point(2,0))]:
    try:
        construct(a,b,c,D)
    except ValueError as exc:
        print(label,'rejected:',str(exc))
print('same-side large circle r squared:',str(dist2(c,point(12,2))))
print('line distance squared: 9; 101 > 9, so that excluded variant is nevertheless a secant.')''')
md('''## 5. 有限运行及带答案练习
问题：若 E=G，能否继续用两相等邻角调用直角定义？答案：不能；弦退化，H 的两侧不再给出反向非零射线。
问题：若 H 在 AB 线段之外，是否违反本命题？答案：不违反，它要求无限直线。
下面检查648个正证书和16个负证书；这不是全部有理输入，也不是一般定理的证明。''')
code('''positives=list(positive_cases()); negatives=list(rejected_cases())
if not all(accepted(*row) for row in positives):raise RuntimeError('positive failure')
if any(accepted(*row) for name,*row in negatives):raise RuntimeError('negative failure')
print('positive certificates:',len(positives),'negative certificates:',len(negatives))
print('negative cases:',', '.join(row[0] for row in negatives))''')
notebook={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'execution_note':'Plain Python compile/exec, not a Jupyter kernel.'},'nbformat':4,'nbformat_minor':5}
(ROOT/'teaching.zh-CN.ipynb').write_text(json.dumps(notebook,ensure_ascii=False,indent=2)+'\n')
print('Created tutorial with 6 code cells; not yet executed.')
