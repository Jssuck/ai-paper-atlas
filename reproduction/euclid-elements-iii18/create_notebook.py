"""Standard-library fallback builder: installed skill CLI unavailable locally."""
import json,io,contextlib
from pathlib import Path
texts=[('III.18：垂足怎样给出反证','from geometry import *\nprint("Exact rational teaching model; not an ancient proof engine")'),('切线候选：方向没有预先筛选','c=certify((0,0),(3,0),3,(0,1))\nprint(c["kind"], verify(c))\nprint([line_power(c,t) for t in [-2,-1,0,1,2]])'),('斜线：垂足是严格内部见证','d=certify((0,0),(3,0),3,(1,1))\nprint("t =",d["t"], "H =",d["h"], "power =",d["power"])'),('射线不能替代整条直线','e=certify((0,0),(3,0),3,(1,2))\nprint("forward powers", [line_power(e,t) for t in [0,1,2]])\nprint("backward interior witness", e["t"], e["power"])'),('有限遍历与拒绝篡改','print(grid())\nf=dict(d); f["power"]=0\nprint("tamper accepted:",verify(f))')]
cells=[];env={}
for n,(title,code) in enumerate(texts,1):
 cells.append(dict(cell_type='markdown',metadata={},source=[title+'\n']))
 out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(code,f'cell-{n}','exec'),env)
 cells.append(dict(cell_type='code',metadata={},execution_count=n,source=code.splitlines(True),outputs=[dict(output_type='stream',name='stdout',text=out.getvalue().splitlines(True))]))
nb=dict(nbformat=4,nbformat_minor=5,metadata=dict(language_info=dict(name='python',version='3'),execution_method='stdlib compile/exec; not a Jupyter kernel'),cells=cells)
for n,c in enumerate(cells):c['id']=f'iii18-{n}'
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n');print('executed five code cells with compile/exec, not Jupyter kernel')
