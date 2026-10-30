"""Build and actually execute five tutorial cells, without a Jupyter kernel."""
import json,io,contextlib
from pathlib import Path
cells=[];env={};counter=0
def md(s):cells.append(dict(cell_type='markdown',metadata={},source=s.splitlines(True)))
def code(s):
 global counter
 counter+=1;out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(s,f'cell-{counter}','exec'),env)
 cells.append(dict(cell_type='code',metadata={},source=s.splitlines(True),execution_count=counter,outputs=[dict(output_type='stream',name='stdout',text=out.getvalue().splitlines(True))]))
md('# III.19：接点法线是一条过心直线\n原创有理坐标教学；标准库 compile/exec 实跑，不是 Jupyter kernel。一般证明见正文，有限测试不是证明。')
code("from geometry import *\na=((0,0),(3,4),5,(-4,3),(-3,-4))\nc=certify(*a)\nprint(c)\nprint('valid',verify(*a,c))")
md('## 反向参数不是失败\n把方向改成向外后，圆心在负参数处。因此整线过心，正半射线不过心。')
code("out=certify(*a[:-1],(3,4))\nprint('parameter',out['t'],'positive ray reaches centre',out['ray_reaches_centre'])")
md('## 不预设任意过接点线都相切\n非切线输入被代数条件拒绝，该条件的全称意义由正文配方论证承担。')
code("try:\n    certify(*a[:3],(1,0),(0,1))\nexcept ValueError as e:\n    print('rejected:',e)")
md('## 证书可被检查和拒绝')
code("bad=dict(c);bad['t']=F(2)\nprint('tampered accepted',verify(*a,bad))")
md('## 有限网格\n平移、方向缩放和正负法向参数；不穷尽实数几何。')
code("print(grid())")
nb=dict(nbformat=4,nbformat_minor=5,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'execution_note':'stdlib compile/exec; not kernel'},cells=cells)
for i,c in enumerate(cells):c['id']=f'iii19-{i}'
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('executed',counter,'code cells using stdlib compile/exec, not kernel')
