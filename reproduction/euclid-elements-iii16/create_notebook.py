"""Local nbformat4 scaffold; installed helper unavailable. Not kernel execution."""
import json,io,contextlib
from pathlib import Path
cells=[]
def md(s):cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s):cells.append({'cell_type':'code','execution_count':None,'metadata':{},'outputs':[],'source':s.splitlines(True)})
md('# III.16：切线与不可插入直射线\n现代精确有理模型。有限实跑不是一般证明，不给角隙赋正实数角度。标准库compile/exec，非Jupyter kernel。')
code("from geometry import *\nc=Circle((0,5),25)\np=(0,0)\na=analyze(c,p,(1,0))\nprint(a['kind'], a['k'], a['distance2'])\nprint('tangent noncontact power:',ray_power(c,p,(1,0),2))")
md('# 向内射线\n从接点出发的方向与指向圆心向量点积为正。计算第二交点和严格内部见证，不预设接点唯一。')
code("a=analyze(c,p,(3,4))\nprint('second:',a['second_parameter'],a['second_point'])\nprint('interior:',a['interior_parameter'],a['interior_point'],a['interior_power'])")
md('# 射线与整条直线不同\n向外射线没有新的交点，但反向射线有，不能将它叫切线。')
code("a=analyze(c,p,(3,-4))\nprint(a['kind'], 'other line parameter:',a['second_parameter'])\nprint('positive parameter power:',ray_power(c,p,(3,-4),1))")
md('# 任意有限的狭小倾斜\n参数n越大，方向越贴近水平线，但始终能构造严格内部点。这里只执行三例，不以三例证明全称命题。')
code("for n in [1,10,1000000]:\n a=narrow_example(n)\n print(n, a['interior_parameter'],a['interior_power'])")
md('# 输入与证书检查\n拒绝非圆周接点、零方向；对照包含三种方向类型和直径。')
code('from run_examples import examples\nexamples()')
env={};n=0
for cell in cells:
 if cell['cell_type']!='code':continue
 n+=1;s=io.StringIO()
 with contextlib.redirect_stdout(s):exec(compile(''.join(cell['source']),f'cell-{n}','exec'),env)
 cell['execution_count']=n;cell['outputs']=[{'output_type':'stream','name':'stdout','text':s.getvalue().splitlines(True)}]
 print('executed cell',n);print(s.getvalue(),end='')
for n,c in enumerate(cells):c['id']=f'iii16-{n}'
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'},'execution_method':'stdlib compile/exec; not Jupyter kernel'},'cells':cells}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('5 code cells executed; not a Jupyter kernel')
