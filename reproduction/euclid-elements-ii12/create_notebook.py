"""Build and execute a standard-library teaching notebook; no Jupyter kernel."""
import json,io,contextlib
from pathlib import Path

def md(s):return {'cell_type':'markdown','metadata':{},'source':s.splitlines(True)}
def code(s):return {'cell_type':'code','metadata':{},'source':s.splitlines(True),'execution_count':None,'outputs':[]}
cells=[md('# II.12：外投影带来的正面积校正\n原创教学重构。精确有理坐标模型，不是原文算法或通用证明器。此文件由 Python compile/exec 顺序执行，未启动 Jupyter kernel。有限例子不证明一般命题。'),
code('from fractions import Fraction as F\nfrom geometry import normalized, construct\nr=normalized(5,2,3)\nprint({k:str(r[k]) for k in ["AB2","AC2","BC2","correction"]})'),
md('## 按依赖检查\n先以 II.4 展开 CD 上的平方，再以 I.47 替换两个直角三角形的平方和。所有量为精确 Fraction，不以容差代替相等。'),
code('print(r["checks"])\nprint("D =",r["D"],"; projection parameter =",r["t"])'),
md('## 非整数与非有理边长\n有理坐标的长度可能无理；用 -点积直接计算 AC × AD，避免开方与数值误差。'),
code('s=construct((0,0),(-2,0),(1,1))\nprint({k:str(s[k]) for k in ["AC2","AD2","AC_times_AD","BC2"]})'),
md('## 错误迁移\n把外部投影的校正改成减号，或漏掉二倍，均不能得到 BC²。直角和锐角输入不满足本命题假设，程序拒绝而不悄悄更改定理。'),
code('print("true =",r["BC2"],"; wrong minus =",r["AB2"]+r["AC2"]-r["correction"])\nfor B in [(0,3),(2,3)]:\n    try: construct((0,0),B,(5,0))\n    except ValueError as e: print(str(e))'),
md('## 有限回归\n5 × 5 × 5 × 2 = 250 个有理参数组合，包含关于基线的镜像；这只是实现检验，不是全称证明。'),
code('values=[F(1,7),F(1,2),F(1),F(3),F(11,2)]\nn=0\nfor c in values:\n    for d in values:\n        for h in values:\n            for sign in [-1,1]:\n                q=normalized(c,d,sign*h)\n                if not all(q["checks"].values()): raise RuntimeError("check failed")\n                n+=1\nprint("exact cases checked:",n)')]
for i, cell in enumerate(cells): cell["id"]="ii12-cell-"+str(i)
ns={}; count=0
for cell in cells:
    if cell['cell_type']!='code':continue
    count+=1;out=io.StringIO()
    with contextlib.redirect_stdout(out):exec(compile(''.join(cell['source']),'<notebook>','exec'),ns)
    cell['execution_count']=count;cell['outputs']=[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(True)}]
nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'},'execution_note':'Executed by compile/exec, not a Jupyter kernel'},'nbformat':4,'nbformat_minor':5}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('executed_code_cells='+str(count)+'; method=compile/exec; kernel_started=false')
