"""Local nbformat4 scaffold; installed helper absent. Not kernel execution."""
import json,io,contextlib
from pathlib import Path
cells=[]
def md(s):cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s):cells.append({'cell_type':'code','execution_count':None,'metadata':{},'outputs':[],'source':s.splitlines(True)})
md('# III.15：弦长次序与圆心距离\n有限精确有理实验，不是一般证明。标准库compile/exec，非Jupyter kernel。')
code("from geometry import *\nc=Circle((0,0),5)\nq=chord(c,(-4,3),(4,3))\nprint('length squared:',q['length2'],'distance squared:',q['distance2'])")
md('# 独立投影\n先投影得到垂足，再检验中点和平方关系，不用待证关系筛输入。')
code("print('foot:',q['foot'],'parameter:',q['projection_parameter'])\nprint('half squared + distance squared:',q['half_length2']+q['distance2'])")
md('# 次序反转的两个方向\n正长度平方严格单调。输出1表示第一条更长/更远，-1表示更短/更近。')
code("x=compare(c,(-4,3),(4,3),(-3,4),(3,4))\nprint(x['length_order'],x['distance_order'],x['order_reversal_holds'])\ny=compare(c,(-3,4),(3,4),(-4,3),(4,3))\nprint(y['length_order'],y['distance_order'],y['order_reversal_holds'])")
md('# 直径最大与等号条件\n所有直径都并列最大，不能说每条直径严格大于其他直径。零距不当作非退化三角形。')
code("q=chord(c,(-5,0),(5,0))\nprint(q['length2'],4*q['radius2'],q['distance2'],q['diameter'])\nprint(compare(c,(-5,0),(5,0),(0,-5),(0,5))['length_order'])")
md('# 同圆条件与非法输入\n不同半径时可同时更长且更远，退化端点与非圆周端点拒绝。')
code('from run_examples import examples\nexamples()')
env={};n=0
for cell in cells:
 if cell['cell_type']!='code':continue
 n+=1;s=io.StringIO()
 with contextlib.redirect_stdout(s):exec(compile(''.join(cell['source']),f'cell-{n}','exec'),env)
 cell['execution_count']=n;cell['outputs']=[{'output_type':'stream','name':'stdout','text':s.getvalue().splitlines(True)}]
 print('executed cell',n);print(s.getvalue(),end='')
for n,c in enumerate(cells):c['id']=f'iii15-{n}'
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'},'execution_method':'stdlib compile/exec; not Jupyter kernel'},'cells':cells}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('5 code cells executed; not a Jupyter kernel')
