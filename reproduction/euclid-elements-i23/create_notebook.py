"""Create a native nbformat 4 tutorial; requires only Python's standard library."""
import json
from pathlib import Path
cells=[]
def add(kind,text):
    c={'cell_type':kind,'id':f'i23-{len(cells):02d}','metadata':{},'source':text.splitlines(True)}
    if kind=='code':c.update(execution_count=None,outputs=[])
    cells.append(c)
add('markdown','''# I.23：把三边证书变成角相等证书
这是现代精确坐标教学重构，不是欧几里得圆规操作程序。原证先用 I.22 构造三边，再用 I.8（SSS）认定角。取源 C、D、E；目标 A、B 定义基射线。G 在 AB 射线上，F 在指定侧，AF=CD、AG=CE、FG=DE。

下面 6 个 Python 格由标准库 compile/exec 顺序执行并保存 stdout；没有启动 Jupyter kernel。仅有限案例检验，不证明一般定理。
''')
add('code',"from geometry import construct, verify\nfrom fractions import Fraction as Q\nargs=((0,0),(2,0),(1,2),(3,-1),(4,0),1)\nc=construct(*args)\nprint('d:',c['radicand'])\nprint('F:',c['F'])\nprint('G:',c['G'])\nprint('verified:',verify(c,*args))\n")
add('markdown','''## 精确表达与三边
点的含义为 constant + sqrt(radicand) × sqrt_coefficient。此例 d=5/2，G 的系数为 (1,1)，F 的系数为 (-2/5,6/5)。不把根号转成浮点。源三边平方为 4、5、5。
''')
add('code',"print(c['checks'])\nif [c['checks'][k] for k in ('AF2','AG2','FG2')]!=['4','5','5']:\n    raise RuntimeError('three-side mismatch')\nprint('exact three-side identities passed')\n")
add('markdown','''## 镜像不是失败
side=1 指 cross(AG,AF)>0，side=-1 为另一侧。源有向比较也取 cross(CE,CD)，不是 cross(CD,CE)。两支均复制普通内角；只有一支保持这个有向约定。
''')
add('code',"mirror=construct(*args[:-1],-1)\nfor item in (c,mirror):\n    print(item['side'],item['checks']['AG_cross_AF'],item['signed_orientation_preserved'])\n")
add('markdown','''## 严格证书及输入绑定
verify 重新构造规范 JSON 并比较，不是独立形式证明内核。布尔值 True 不得冒充整数 1，修改输入不得沿用旧证书。
''')
add('code',"import copy\nbad=copy.deepcopy(c);bad['side']=True\nprint('bool tamper:',verify(bad,*args))\nchanged=(*args[:2],(2,3),*args[3:])\nprint('different input:',verify(c,*changed))\nif verify(bad,*args) or verify(c,*changed):\n    raise RuntimeError('tampering accepted')\n")
add('markdown','''## 退化域外输入
零角、平角、零射线不是本实现接受的非退化直线角。AB 也不能是零向量。禁止浮点和布尔坐标；可输入整数、有理数字符串、Fraction。
''')
add('code',"for E in ((2,0),(-2,0),(0,0)):\n    try:\n        construct((0,0),(1,0),E,(0,0),(1,0))\n    except ValueError as exc:\n        print(E,str(exc))\n    else:\n        raise RuntimeError('degenerate angle accepted')\n")
add('markdown','''## 有限回归集
六组源形状、四组目标射线、三种源截点缩放、两侧支，共 144 证书。源截点改变会改变三角形尺寸，不改变相同两射线所夹普通角；证书仍须分别绑定输入。本程序只覆盖有理输入及单根式输出，不声称穷尽古典几何。
''')
add('code',"from cases import run\nprint(run())\n")
nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'execution_note':'Executed by standard-library compile/exec, not a Jupyter kernel.'},'nbformat':4,'nbformat_minor':5}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('created native nbformat 4 tutorial: 6 code cells')
