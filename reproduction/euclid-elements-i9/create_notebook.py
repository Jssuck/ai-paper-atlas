"""Create a small nbformat 4 tutorial using only the standard library.
The installed skill's scaffold helper was unavailable; no package installed.
"""
import json
from pathlib import Path
cells=[]
def md(s): cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s): cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(True),'execution_count':None,'outputs':[]})
md('# Euclid I.9：选对等边顶点，还要核查内射线\n\n原创教学坐标模型，不是完整尺规引擎。一般证明见正文；有限枚举不证明定理。所有几何判定在 Q(√3) 中精确计算。请从本目录顺序执行。')
code('from geometry import *\na,d,e=canonical(1,1)\nf=construct(a,d,e)\nprint("F =", tuple(str(x) for x in f))\nprint(certificate(a,d,e,f))\n')
md('## 为什么“夹角相等”还不够？\n两等边顶点中，同侧顶点可能仍在内射线上，也可能等于 A，或位于反向射线上。下列三例分别展示三种情况。不能把“同侧”一概写成“外角平分线”。')
code('for u in (Q3(2),S,Q3(1)):\n    a,d,e=canonical(u,1)\n    wrong=point(u-S,0)\n    checks=certificate(a,d,e,wrong)\n    print("u =", str(u), "F =", tuple(str(x) for x in wrong))\n    print(checks)\n')
md('## 不等距截取破坏证明前提\n这不是以失败实例代替证明，而是防止实现只检查输出外观。')
code('try:\n    construct(point(0,0),point(1,1),point(2,-2))\nexcept ValueError as error:\n    print(type(error).__name__ + ": " + str(error))\n')
md('## 有限枚举与边界\n8×8 组正有理参数，3 次平移、4 个直角旋转、2 种端点顺序。数值族不覆盖全部平面角；旋转也不是任意实数旋转。枚举只检验模型和程序的这些输入。')
code('from run_examples import examples\nresult=examples()\nprint("positive certificates:", result["positive_certificates"])\nprint("same-side cases:", len(result["same_side_branch_cases"]))\nprint("other rejected certificates:", len(result["additional_rejected_certificates"]))\n')
md('## 练习与答案\n1. u=2,v=1 的同侧分支为何拒绝？答：它虽给出内向等角射线，却不满足本实现固定的“与 A 异侧”构造证书。\n2. u=1,v=1 的同侧分支为什么不能用？答：两夹角仍相等，但射线不在原凸角内部。\n3. 1536 次通过能证明所有角吗？答：不能；一般结论依赖正文证明，程序只核查有限族。\n\n执行说明：仓库保存的是 verify_notebook.py 逐 cell compile/exec 的真实标准 Python 输出，不宣称由 Jupyter kernel 或浏览器执行。')
for i,c in enumerate(cells): c['id']=f'i9-{i:02d}'
nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'}},'nbformat':4,'nbformat_minor':5}
Path(__file__).with_name('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
