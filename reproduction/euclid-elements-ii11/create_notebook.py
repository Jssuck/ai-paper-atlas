"""Execute teaching cells with standard-library compile/exec; not a Jupyter kernel."""
import json,io,contextlib
from pathlib import Path
pairs=[('1. 精确代数域','from fractions import Fraction as F\nfrom geometry import Q5,make_certificate,validate_certificate\nr=Q5(0,1)\nprint("sqrt5 squared =",r*r)\n'),('2. 构造与内部点','c=make_certificate(1)\nm=validate_certificate(c)\nprint("x =",m["x"])\nprint("strict interior:",0<m["x"]<1)\n'),('3. 两条证明路线','for k in ["EF2","EB2","II6_left","square_AB","AE2"]: print(k,"=",m[k])\n'),('4. 同减公共矩形','for k in ["FK","AK","FH","HD","target_left","target_right"]: print(k,"=",m[k])\n'),('5. 换尺度与拒绝错误点','for a in [F(1,7),F(2,3),5]:\n mm=validate_certificate(make_certificate(a,u=(3,4),v=(-4,3)))\n print("a",a,"scale2",mm["scale2"],"equal",mm["FH"]==mm["HD"])\nc["points"]["H"]=(Q5(F(1,2)),Q5(0))\ntry: validate_certificate(c)\nexcept ValueError as e: print("rejected:",str(e))\n')]
cells=[{'cell_type':'markdown','metadata':{},'source':['# II.11：精确补方与公共矩形相减\n','真实执行方式：标准库 compile/exec，不是 Jupyter kernel。坐标在 Q(√5) 中精确；有限例子不是一般定理证明。']}]
ns={}
for i,(title,code) in enumerate(pairs,1):
 cells.append({'cell_type':'markdown','metadata':{},'source':['## '+title]})
 out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(code,'<teaching-cell>','exec'),ns)
 cells.append({'cell_type':'code','metadata':{},'source':code.splitlines(True),'execution_count':i,'outputs':[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(True)}]})
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'},'execution_method':'standard library compile/exec; no kernel started'},'cells':cells}
for i,c in enumerate(cells):c['id']='ii11-'+str(i)
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('executed 5 cells via compile/exec; no kernel started')
