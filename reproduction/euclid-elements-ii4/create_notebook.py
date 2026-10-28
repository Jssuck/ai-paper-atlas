"""Build tutorial and execute code via stdlib compile/exec, not a Jupyter kernel."""
import contextlib,io,json
from pathlib import Path
texts=[('markdown','# Euclid II.4：四区域证书\n现代有理坐标教学；有限检查不是一般证明。代码以标准库 compile/exec 实跑，未启动 Jupyter kernel。'),('code','from fractions import Fraction as Q\nfrom geometry import construct, verify\nc = construct()\nprint(verify(c))'),('markdown','外方边长5，AC=2、CB=3；先检查几何资格，再报告面积。'),('code',"print({k: c['points'][k] for k in ['C','G','H','K','F']})"),('markdown','旋转不会改变面积，反射只改变方向。'),('code','print(verify(construct((1,-2),(3,4),(-4,3),Q(2,5)),(1,-2),(3,4),(-4,3),Q(2,5)))'),('markdown','等边菱形不是正方形；必须核实直角。'),('code',"try:\n    construct(u=(5,0),v=(3,4))\nexcept ValueError as e:\n    print(type(e).__name__ + ': ' + str(e))"),('markdown','分数例仍是有限有理坐标，不覆盖不可通约一般情形。'),('code','print(verify(construct(t=Q(1,3)),t=Q(1,3)))')]
cells=[]; ns={};count=0
for typ,src in texts:
 cell={'cell_type':typ,'metadata':{},'source':src.splitlines(keepends=True)}
 if typ=='code':
  count+=1;out=io.StringIO()
  with contextlib.redirect_stdout(out):exec(compile(src,'<tutorial>','exec'),ns)
  cell.update(execution_count=None,outputs=[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(keepends=True)}])
 cells.append(cell)
Path('teaching.zh-CN.ipynb').write_text(json.dumps({'nbformat':4,'nbformat_minor':5,'metadata':{'language_info':{'name':'python'},'execution_method':'stdlib compile/exec; no kernel'},'cells':[dict(c,id='cell-'+str(i)) for i,c in enumerate(cells)]},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'executed_code_cells':count,'method':'compile/exec','kernel_started':False}))
