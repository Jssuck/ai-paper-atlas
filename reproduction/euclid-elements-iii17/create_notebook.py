"""Local nbformat4 scaffold: installed helper not present. Not kernel execution."""
import json,io,contextlib
from pathlib import Path
cells=[]
def md(s):cells.append(dict(cell_type='markdown',metadata={},source=s.splitlines(True)))
def code(s):cells.append(dict(cell_type='code',metadata={},source=s.splitlines(True),execution_count=None,outputs=[]))
md('# III.17：从圆外点作切线\n原创有理教学模型，不是任意实数求交程序。下面五格实际由标准库compile/exec执行，非Jupyter kernel；有限例不证明一般定理。')
code("from geometry import *\nc=construct(3,5)\nfor k in ['E','A','D','F','B']:print(k,c[k])\nprint('verified:',verify(c))")
md('## 两个镜像\n辅助直线与大圆的两个交点分别产生两个接点；不是两段同一条切线。')
code("other=construct(3,5,side=-1)\nprint('upper:',c['B'],'lower:',other['B'])\nprint('directions:',c['direction'],other['direction'])")
md('## 从垂直到整条直线在外\n检验幂值等于参数平方乘方向长度平方。全称命题仍依赖正文代数证明。')
code("for t in [-2,-1,0,1,2]:print(t,line_power(c,t),t*t*norm(c['direction']))")
md('## 圆上点与可行域\n内点数学上不存在切线；外点1,2被拒只是本实现不处理无理根，不能推断不可作图。')
code("from run_examples import examples\nexamples()")
md('## 有限回归\n检查平移、旋转、有理缩放及两个分支。不是几何定理的穷尽验证。')
code("print(grid())\nbad=dict(c);bad['B']=(0,0)\nprint('tampered certificate accepted:',verify(bad))")
env={};n=0
for cell in cells:
 if cell['cell_type']!='code':continue
 n+=1;s=io.StringIO()
 with contextlib.redirect_stdout(s):exec(compile(''.join(cell['source']),f'cell-{n}','exec'),env)
 cell['execution_count']=n;cell['outputs']=[dict(output_type='stream',name='stdout',text=s.getvalue().splitlines(True))]
 print('executed cell',n);print(s.getvalue(),end='')
for i,c in enumerate(cells):c['id']=f'iii17-{i}'
nb=dict(nbformat=4,nbformat_minor=5,metadata=dict(kernelspec=dict(display_name='Python 3',language='python',name='python3'),language_info=dict(name='python',version='3'),execution_method='stdlib compile/exec; not Jupyter kernel'),cells=cells)
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('5 code cells; standard-library execution, not Jupyter kernel')
