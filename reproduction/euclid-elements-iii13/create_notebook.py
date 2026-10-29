"""Local nbformat4 fallback: installed helper absent and resource unavailable. No kernel."""
import json,io,contextlib
from pathlib import Path
cells=[]
def md(s):cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s):cells.append({'cell_type':'code','execution_count':None,'metadata':{},'outputs':[],'source':s.splitlines(True)})
md('# III.13：接点唯一性与前提\n这是现代有理坐标教学，不是一般定理证明。代码按 compile/exec 顺序实际执行，非 Jupyter kernel。')
code("from geometry import *\na=Circle((0,0),5)\nprint('outer radius:',a.radius)")
md('## 外侧：开圆盘不交与一个共有边界点\n数值分离判据的等价性由正文证明，未假设唯一性。')
code("b=Circle((8,0),3)\nprint(contact_certificate(a,b,(5,0),'external'))")
md('## 内侧：真包含与共有边界点\n排除重合圆；验证输入点与唯一候选公式相同。')
code("inner=Circle((2,0),3)\nprint(contact_certificate(a,inner,(5,0),'internal'))\nprint(same_contact(a,inner,(5,0),(5,0),'internal'))")
md('## 两交点不是相切\n弦中点严格在两个开圆盘内，直接否定外侧分离。这个事实本身不排除内含，内含情形需另一条论证。')
code("crossing=Circle((6,0),5)\nprint(chord_midpoint_certificate(a,crossing,(3,4),(3,-4)))\nprint('proper containment:',contains(a,crossing))")
md('## 重合圆与拒绝对照\n同一圆可有任意多个共有点，不满足真包含规格。有限样例仅检验实现。')
code("from run_examples import examples\nexamples()")
env={};n=0
for cell in cells:
 if cell['cell_type']!='code':continue
 n+=1;s=io.StringIO()
 with contextlib.redirect_stdout(s):exec(compile(''.join(cell['source']),f'cell-{n}','exec'),env)
 cell['execution_count']=n;cell['outputs']=[{'output_type':'stream','name':'stdout','text':s.getvalue().splitlines(True)}]
 print('executed cell',n);print(s.getvalue(),end='')
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'},'execution_method':'stdlib compile/exec; not a Jupyter kernel'},'cells':cells}
for n,c in enumerate(cells):c['id']=f'iii13-{n}'
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('5 code cells executed; not a Jupyter kernel')
