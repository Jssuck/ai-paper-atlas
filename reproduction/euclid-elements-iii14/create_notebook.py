"""Local nbformat4 scaffold: installed helper absent; standard-library execution, not kernel."""
import json,io,contextlib
from pathlib import Path
cells=[]
def md(s):cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s):cells.append({'cell_type':'code','execution_count':None,'metadata':{},'outputs':[],'source':s.splitlines(True)})
md('# III.14：等弦与等距\n同圆内两弦长度相等，当且仅当圆心到弦所在直线的距离相等。有限有理实验不是一般证明。本Notebook以标准库compile/exec实际运行，非Jupyter kernel。')
code("from geometry import *\nc=Circle((0,0),5)\nq=chord(c,(-4,3),(4,3))\nprint(q)")
md('## 垂足为何是中点\n程序先按投影计算参数，不把1/2作为输入；等半径端点使投影参数为1/2。')
code("print('projection parameter:',q['projection_parameter'])\nprint('half chord squared + distance squared:',q['half_length2']+q['distance2'])")
md('## 双向比较\n比较长度平方与距离平方，非负性使平方相等与长度相等一致。')
code("for ends in [((-4,-3),(4,-3)),((-3,4),(3,4))]:\n    x=compare(c,(-4,3),(4,3),*ends)\n    print(x['equal_chords'],x['equal_distances'],x['equivalence_holds'])")
md('## 直径的垂距为零\n圆心自身是垂足；不把零长线段当成一条有方向的垂线。')
code("diameter=chord(c,(-5,0),(5,0))\nprint('foot:',diameter['foot'],'distance squared:',diameter['distance2'])\nprint(compare(c,(-5,0),(5,0),(0,-5),(0,5))['equivalence_holds'])")
md('## 删掉同半径条件会怎样\n不同圆半径5与4有同长8的弦，但距离分别3与0；退化端点被拒绝。')
code("from run_examples import examples\nexamples()")
env={};n=0
for cell in cells:
 if cell['cell_type']!='code':continue
 n+=1;s=io.StringIO()
 with contextlib.redirect_stdout(s):exec(compile(''.join(cell['source']),f'cell-{n}','exec'),env)
 cell['execution_count']=n;cell['outputs']=[{'output_type':'stream','name':'stdout','text':s.getvalue().splitlines(True)}]
 print('executed cell',n);print(s.getvalue(),end='')
for n,c in enumerate(cells):c['id']=f'iii14-{n}'
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'},'execution_method':'stdlib compile/exec; not Jupyter kernel'},'cells':cells}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('5 code cells executed; not a Jupyter kernel')
