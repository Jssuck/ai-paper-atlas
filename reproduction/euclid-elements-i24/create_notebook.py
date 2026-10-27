"""Stdlib fallback: installed skill scaffold is absent from this environment."""
import json
from pathlib import Path
cells=[]
def md(s):cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s):cells.append({'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':s.splitlines(True)})
md('# Euclid I.24：精确坐标检验\n现代教学重构，不是原证或一般证明。六格由标准库 compile/exec 实跑，非 Jupyter kernel。')
code('from fractions import Fraction as Q\nfrom geometry import certify, verify, unit\nfrom cases import case, positives, negatives\nprint(unit(Q(1,3)))')
md('## 1 固定两边，增大夹角\nt 是正半角参数；不使用浮点角度。')
code("c=certify(case())\nprint({k:c[k] for k in ('EF_squared','EG_squared','gap')})")
md('## 2 三种配置\n同一夹角和 b=1，改变 a。分类对应 Heath 指出的原图外、共线、内三型。')
code("for a in (1,2,3):\n c=certify(case(a=a)); print(a,c['configuration'],c['EFG_determinant'])")
md('## 3 反射与有限网格\n反射不改变大小；有限证书不是一般定理的证明。')
code("cs=[certify(d) for d in positives()]\nprint('verified',sum(verify(d,c) for d,c in zip(positives(),cs)))")
md('## 4 证书不能接受 bool 冒充整数\n不只比较 Python 数值相等。')
code("c=certify(case()); c['EFG_orientation']=True\nprint('tampered accepted',verify(case(),c))\nif verify(case(),c): raise RuntimeError('tamper accepted')")
md('## 5 面积不是本命题结论\n钝角继续变大可以使面积减小，同时对边仍增大。')
code("print('heights',unit(Q(2))[1],unit(Q(3))[1])\nprint('base squared gap',certify(case(s=2,t=3))['gap'])")
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'language_info':{'name':'python','version':'3'},'execution_method':'stdlib compile/exec; not kernel'},'cells':cells}
for i,c in enumerate(cells):c['id']='i24-'+str(i)
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('created tutorial with six code cells; stdlib scaffold fallback')
