"""Dependency-free nbformat 4.5 tutorial scaffold; this does not execute cells."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
cells=[]
def md(text):
    cells.append({'cell_type':'markdown','id':f'md-{len(cells)}','metadata':{},'source':text.strip().splitlines(keepends=True)})
def code(text):
    cells.append({'cell_type':'code','id':f'code-{len(cells)}','metadata':{},'execution_count':None,'outputs':[], 'source':text.strip().splitlines(keepends=True)})
md('''# Euclid I.11：在线上给定点立垂线
目标：区分古代的等距截取—等边辅助—I.8—直角定义，与现代精确坐标核验。
本 Notebook 是原创教学重建，有限运行不证明一般定理。输入 A、B 不同，C 在闭线段 AB；端点需要延长支撑线。
随附输出由标准 Python compile/exec 共享命名空间顺序实跑，**不是 Jupyter kernel 执行记录**；未验证 Notebook 浏览器显示。
在本文件所在目录运行，只用标准库。''')
code('''from pathlib import Path
if not Path('geometry.py').is_file():
    raise RuntimeError('请在 Notebook 所在目录运行')
from fractions import Fraction as R
from dataclasses import replace
from geometry import *
from cases import positive_cases, rejected_cases
print('Exact Q(sqrt(3)); no floating-point geometric predicates.')''')
md('''## 1. 内点及等边两支
CD=CE，DF=EF，CF 共边；I.8 使邻角相等。由于 CD 与 CE 是反向射线，定义10把这两个相等邻角称为直角。
程序的坐标表达是现代模型，不是欧几里得写出的公式。''')
code('''A,B,C=point(0,0),point(6,0),point(3,0)
h=R(1,6)
plus,minus=[construct(A,B,C,h,s) for s in (1,-1)]
for k in (plus,minus):
    print('branch',k.branch,'D',tuple(map(str,k.d)),'E',tuple(map(str,k.e)),
          'F',tuple(map(str,k.f)),'accepted',accepted(A,B,C,h,k))
print(check_certificate(A,B,C,h,plus))''')
md('''## 2. 端点不偷换成内部点
C=A 时 D 落在 AB 外。若只允许在原有限线段内截取，原内点图式不能直接执行；本程序明示使用支撑线延长。
即使 C 是内点，截取参数 h 过大也会超出端点。''')
code('''endpoint=construct(A,B,A,h)
print('endpoint extension:',extension_report(A,B,endpoint))
print('endpoint accepted:',accepted(A,B,A,h,endpoint))
large=construct(A,B,C,R(2))
print('large cut extension:',extension_report(A,B,large))''')
md('''## 3. 两条射线，不是两条垂直直线
两支顶点在 AB 两侧；CF 的方向向量相反，支撑直线相同。改变正截取长度亦不改变支撑直线。
这些有限检查不构成唯一性定理的形式化证明。''')
code('''u,v=sub(plus.f,C),sub(minus.f,C)
print('cross of directions:',str(cross(u,v)))
print('dot sign:',dot(u,v).sign())
long=construct(A,B,C,R(2))
print('cross after changing cut:',str(cross(u,sub(long.f,C))))''')
md('''## 4. 反例：等边辅助仍不足
取 C=(2,0)、D=(1,0)、E=(4,0)，即 CD≠CE。在 DE 上作等边三角形，F 横坐标为 5/2 而不是 2，故 CF 不垂直原直线。
反之，直接选一个垂直点可以满足垂直结论，却不满足这一次等边构造；完整证书不应误收。''')
code('''C2=point(2,0);D,E=point(1,0),point(4,0)
bad=Certificate(1,D,E,equilateral_vertices(D,E)[0])
facts=check_certificate(A,B,C2,h,bad)
print('F:',tuple(map(str,bad.f)))
print({n:facts[n] for n in ('equilateral_DFE','CD_equals_CE','perpendicular_modern_check')})
shortcut=replace(plus,f=point(3,1))
print('perpendicular alone:',check_certificate(A,B,C,h,shortcut)['perpendicular_modern_check'])
print('full construction accepted:',accepted(A,B,C,h,shortcut))''')
md('''## 5. 回归证据与练习
预测：端点交换并反转分支，F 不变；若 h=0，则三角形退化，程序拒绝。
答案：前者交换 D、E 并抵消方向反转；后者不能产生非零 CF 与两三角形。
下面实际运行有限测试族，不声称枚举全部有理输入。''')
code('''positives=list(positive_cases()); negatives=list(rejected_cases())
if not all(accepted(a,b,c,h,k) for a,b,c,h,k in positives):
    raise RuntimeError('positive rejection')
if any(accepted(a,b,c,h,k) for name,a,b,c,h,k in negatives):
    raise RuntimeError('negative acceptance')
print('positive certificates:',len(positives),'negative certificates:',len(negatives))
print('endpoint swap F equal:',construct(B,A,C,R(1,6),-1).f==plus.f)
try:
    construct(A,B,C,0)
except ValueError as exc:
    print('zero cut rejected:',str(exc))''')
notebook={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
 'language_info':{'name':'python'},'execution_note':'Outputs supplied by plain-Python compile/exec, not a Jupyter kernel.'},'nbformat':4,'nbformat_minor':5}
(ROOT/'teaching.zh-CN.ipynb').write_text(json.dumps(notebook,ensure_ascii=False,indent=2)+'\n')
print('Created tutorial with 6 code cells; not yet executed.')
