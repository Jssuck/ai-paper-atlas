"""Build a small teaching notebook. Scaffold helper was unavailable in executor.

Cells are JSON nbformat 4 and are executed separately by verify_notebook.py.
"""
import json
from pathlib import Path
cells=[]
def md(s):cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(keepends=True)})
def code(s):cells.append({'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':s.splitlines(keepends=True)})
md('# I.18：截取一个等腰三角形\n\n原创坐标教学重构。标准库精确二次域；下列记录由 compile/exec 生成，不是 Jupyter kernel。原证依赖 I.3、I.5、I.16 和角的严格包含；点积比较只是另一路现代核查，不能冒充原典证明。')
code('from geometry import *\nfrom cases import positives, negatives\na,b,c=point(0,0),point(1,1),point(4,0)\nk=construct(a,b,c)\nprint("AC squared:",dist2(a,c),"AB squared:",dist2(a,b))\nprint("certificate accepted:",accepted(a,b,c,k))\n')
md('## 1. 截取\n令 t 为 AB²/AC² 的正平方根。0<t<1 保证 D 严格在 AC 内部，AD=AB。此例 t=√(1/8)，不作浮点近似。')
code('t,d=parameters(a,b,c)\nprint("t =",t)\nprint("D =",tuple(map(str,d)))\nprint("AD squared =",dist2(a,d))\n')
md('## 2. 角的严格内部\nBD=(1−t)BA+tBC，两个系数严格正且 BA、BC 非共线，因此 BD 为角 ABC 的内部射线。')
code('print("cone coefficients:",str(1-t),str(t))\nprint("cone identity:",sub(d,b)==add(scale(1-t,sub(a,b)),scale(t,sub(c,b))))\n')
md('## 3. 原证路线与现代核查分开\n等腰底角、外角严格大于内对角和严格角部分，拼成 ABC > ABD = ADB > BCA。下面布尔量是精确坐标核查，不是形式化公理证明。')
code('for name,value in k["checks"].items():\n    print(name,value)\n')
md('## 4. 不可信证书\n输入绑定及严格 JSON 类型防止另一三角形的证书、篡改和 Python 中 True==1 的陷阱。')
code('import copy\nbad=copy.deepcopy(k)\nbad["checks"]["AD_equals_AB"]=1\nprint("Boolean replaced by integer accepted:",accepted(a,b,c,bad))\nprint("different input accepted:",accepted(point(1,0),b,c,k))\n')
md('## 5. 有限覆盖\n任意有理非共线输入是接口范围；下面只枚举有限样本，不能证明一般定理。等边界、反向边序和退化输入应拒绝。')
code('count=sum(accepted(*args,construct(*args)) for args in positives())\nrejected=0\nfor args in negatives():\n    try:\n        construct(*args)\n    except (TypeError,ValueError):\n        rejected+=1\nprint("positive certificates:",count,"negative inputs rejected:",rejected)\n')
md('## 练习与答案\n1. t=1 为什么不能支持严格结论？D=C，使角内部分拆不严格；两边相等只给底角相等。\n2. 删除 AC>AB 会怎样？t可能超过1，D不在AC内部，原证链失去前提。\n3. 代码接受原始浮点坐标吗？不接受，使用整数或Fraction。\n4. 代码的一次通过证明全部三角形吗？不，有限运行只检查已列样本。')
notebook={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},'cells':cells}
for index,cell in enumerate(cells):cell['id']=f'i18-{index:02d}'
Path(__file__).with_name('teaching.zh-CN.ipynb').write_text(json.dumps(notebook,ensure_ascii=False,indent=2)+'\n')
print('created teaching.zh-CN.ipynb; execution is a separate command')
