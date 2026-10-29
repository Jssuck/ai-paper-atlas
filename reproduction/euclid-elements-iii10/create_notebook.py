"""Local nbformat4 scaffold: installed helper unavailable, no installation needed."""
import json,io,contextlib
from pathlib import Path
codes=["from geometry import *\nprint('Fraction arithmetic; compile/exec, not Jupyter kernel')",
"c=classify((0,0),25,(6,0),25)\nprint(printable(c))\nprint('exact common points:',printable(rational_intersections((0,0),25,(6,0),25)))",
"for d in [1,2,3]:\n    c=classify((0,0),1,(d,0),1)\n    print('center distance',d,'count',c['count'],'N',c['discriminant'])\nprint('irrational points are not rounded:',rational_intersections((0,0),1,(1,0),1))",
"print('coincident:',classify((0,0),1,(0,0),1))\nprint('concentric unequal:',classify((0,0),1,(0,0),4))\nprint('three common points:',printable(same_circle_from_three([(5,0),(0,5),(-5,0)],(0,0),25,(0,0),25)))",
"for d in ['1999999999999999999/1000000000000000000','2','2000000000000000001/1000000000000000000']:\n    c=classify((0,0),1,(d,0),1)\n    print('d =',d,'count =',c['count'])\nprint('Finite cases illustrate, never prove the general theorem.')"]
labels=['精确输入与执行边界','根轴、判别量与两个有理交点','两交点、相切、相离及无理坐标','重合例外与三点约束','接近相切时不使用浮点容差']
ns={};cells=[{'cell_type':'markdown','metadata':{},'source':'# III.10：两不同圆至多两个公共点\n现代坐标教学重构，不是古代算法。五个代码单元以标准库 compile/exec 实跑，未启动 Jupyter kernel；有限实验不是一般证明。'}]
for i,(label,code) in enumerate(zip(labels,codes)):
 cells.append({'cell_type':'markdown','metadata':{},'source':'## '+str(i+1)+'. '+label})
 out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(code,'<notebook-cell>','exec'),ns)
 cells.append({'cell_type':'code','metadata':{'execution_method':'compile/exec, not kernel'},'execution_count':None,'source':code,'outputs':[{'output_type':'stream','name':'stdout','text':out.getvalue()}]})
for i,c in enumerate(cells):c['id']='iii10-cell-'+str(i)
Path('teaching.zh-CN.ipynb').write_text(json.dumps({'nbformat':4,'nbformat_minor':5,'metadata':{'language_info':{'name':'python','version':'3'},'execution_method':'standard-library compile/exec, not Jupyter kernel'},'cells':cells},ensure_ascii=False,indent=2)+'\n')
print('Executed 5 code cells via compile/exec; outputs saved; not kernel.')
