"""Standard-library tutorial builder; installed helper path was unavailable.
No Jupyter kernel is claimed. Six executable cells are replayed by verify_notebook.
"""
import json
from pathlib import Path
cells=[]
def md(s):cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(keepends=True)})
def code(s):cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(keepends=True),'execution_count':None,'outputs':[]})
md('# I.20：把两段和放到一条直线上\n现代精确坐标教学，不冒充原典形式证明；执行方式为标准库compile/exec，非Jupyter kernel。')
md('## 1. 给定三角形\nA=(0,0)、B=(3,0)、C=(0,4)，把BA越过A延长，AD=AC=4，得到D=(-4,0)。')
code("from geometry import *\nfrom cases import positive_cases,invalid_cases\nfrom copy import deepcopy\ntri=(point(0,0),point(3,0),point(0,4))\ncert=construct(*tri)\nprint(cert['D'])\nprint(cert['t'])")
md('## 2. 点序不是图像猜测\nCA是CB、CD的正线性组合，所以射线CA位于角BCD内部。单二次域计算保留精确性。')
code("print(cert['CA_cone_coefficients'])\nprint({k:v for k,v in cert['checks'].items() if 'cone' in k or 'between' in k})")
md('## 3. 原证和现代检验分层\n原证使用I.5、整体大于部分、I.19；这里点积比较只是独立现代核验，不能用True字段代替这些证明。')
code("print(cert['checks'])\nprint('replay',accepted(*tri,cert))")
md('## 4. 严格JSON与输入绑定\n布尔与整数不可混同；更换输入后原证书不能沿用。')
code("bad=deepcopy(cert)\nbad['checks']['t_positive']=1\nprint('integer replacing true accepted',accepted(*tri,bad))\nprint('changed input accepted',accepted(point(0,0),point(3,0),point(0,5),cert))")
md('## 5. 有限真实运行\n遍历128个有理坐标输入。数量不是一般证明，优化模式另由命令日志记录。')
code("cases=positive_cases()\npassed=sum(accepted(*c,construct(*c)) for c in cases)\nprint({'cases':len(cases),'passed':passed})\nif passed!=len(cases):raise RuntimeError('positive check failed')")
md('## 6. 删除非退化前提\n共线1、2、3长度给等号而不是严格不等；这种输入被几何构造拒绝，但独立长度比较器仍能展示边界。')
code("rejected=0\nfor c in invalid_cases():\n    try:construct(*c)\n    except ValueError:rejected+=1\nprint({'invalid':len(invalid_cases()),'rejected':rejected})\nprint('1+2>3',sum_greater(1,4,9))\nif rejected!=len(invalid_cases()):raise RuntimeError('negative check failed')")
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},'cells':cells}
for i,c in enumerate(cells):c['id']='i20-'+str(i)
Path(__file__).with_name('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'created':'teaching.zh-CN.ipynb','code_cells':6}))
