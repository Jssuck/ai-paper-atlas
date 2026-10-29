"""Local nbformat4 scaffold; installed template helper absent; no dependencies installed."""
import json,io,contextlib
from pathlib import Path
codes=["from geometry import *\nfrom run_examples import cases\nprint('Exact Fraction reconstruction; compile/exec, not a Jupyter kernel')",
"p=[(5,0),(0,5),(-3,-4)]\nc=make_certificate(p,(0,0))\nprint('center =',c['center'],'radius squared =',c['radius_squared'])",
"c=make_certificate([(5,0),(-5,0),(0,5)],(0,0))\nprint('zero midpoint directions =',c['zero_midpoint_directions'])\nprint('certificate valid =',verify_certificate(c))",
"p=[(3,4),(3,-4),(-5,0)]\nprint('two distances squared =',distance2(p[0],(3,0)),distance2(p[1],(3,0)))\ntry:\n    make_certificate(p,(3,0))\nexcept ValueError as e:\n    print('three-point check rejects:',str(e))",
"for name,p,d in cases:\n    c=make_certificate(p,d)\n    print(name, c['center'], verify_certificate(c))"]
texts=['# III.9：三个等距点与圆心\n实际输出由标准库compile/exec顺序执行保存，不是Jupyter内核执行。有限实例不证明一般定理。',
'## 1. 精确表示与执行边界','## 2. 三点恢复中心','## 3. 直径零方向不应使证书失败','## 4. 两点等距不足','## 5. 任意三点外心与已知圆心的不同语境']
ns={};cells=[{'cell_type':'markdown','metadata':{},'source':texts[0]}]
for label,code in zip(texts[1:],codes):
    cells.append({'cell_type':'markdown','metadata':{},'source':label})
    out=io.StringIO()
    with contextlib.redirect_stdout(out):exec(compile(code,'<notebook-cell>','exec'),ns)
    cells.append({'cell_type':'code','metadata':{'execution_method':'python compile/exec, not kernel'},'source':code,'execution_count':None,'outputs':[{'output_type':'stream','name':'stdout','text':out.getvalue()}]})
Path('teaching.zh-CN.ipynb').write_text(json.dumps({'nbformat':4,'nbformat_minor':5,'metadata':{'language_info':{'name':'python','version':'3'},'execution_method':'standard-library compile/exec, not Jupyter kernel'},'cells':cells},ensure_ascii=False,indent=2)+'\n')
print('Executed 5 code cells via compile/exec; saved outputs; non-kernel.')
