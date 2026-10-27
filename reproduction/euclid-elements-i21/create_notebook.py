"""Standard-library tutorial builder; installed helper path unavailable. No kernel claimed."""
import json
from pathlib import Path
cells=[]
def md(s):cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(keepends=True)})
def code(s):cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(keepends=True),'execution_count':None,'outputs':[]})
md('# I.21：内部折线的长度和夹角\n现代有理坐标核验；非古代形式证明。标准库compile/exec真实执行，不是Jupyter kernel。')
md('## 1. 严格内部点\n先检查重心系数均为正，不能把画在里面当作证据。')
code("from geometry import *\nfrom cases import *\nfrom copy import deepcopy\ndata=(point(0,4),point(-3,0),point(4,0),point(0,1))\nc=construct(*data)\nprint(c['barycentric'])")
md('## 2. 延长交点\nE由重心坐标精确求出。B-D-E及A-E-C的顺序保证原证中的线段拼接。')
code("print({'E':c['E'],'t':c['extension_factor']})\nprint({k:v for k,v in c['checks'].items() if 'order' in k or 'decomposition' in k})")
md('## 3. 两次三角不等式\n原证I.20为一般结论；此处根式比较是独立坐标核验。中间量是BE+EC。')
code("print({k:v for k,v in c['checks'].items() if 'I20' in k or 'bridge' in k or 'outer_gt_inner' in k})\nprint('irrational equality',sum_compare(2,8,18,0))")
md('## 4. 两次外角不等式\nBDC > CED = CEB > BAC。角比较无需反三角函数，但只认证给定精确输入。')
code("print({k:v for k,v in c['checks'].items() if 'I16' in k or 'CED_' in k or 'BDC_gt' in k})")
md('## 5. 篡改和输入绑定\n把布尔True换成整数1不能被接受。')
code("bad=deepcopy(c)\nbad['checks']['strict_interior']=1\nprint('type tampering',accepted(*data,bad))\nprint('changed input',accepted(*data[:3],point(0,2),c))")
md('## 6. 有限运行与边界\n120个严格内部有理构型与12个非法输入；不是一般定理证明。D落在BC上时夹角可成为平角，但严格内部前提已经失效。')
code("ps=positive_cases();ns=invalid_cases()\npassed=sum(accepted(*d,construct(*d)) for d in ps)\nrejected=0\nfor d in ns:\n    try:construct(*d)\n    except ValueError:rejected+=1\nprint({'positive':passed,'invalid_rejected':rejected})\nif passed!=len(ps) or rejected!=len(ns):raise RuntimeError('case failure')")
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},'cells':cells}
for i,c in enumerate(cells):c['id']='i21-'+str(i)
Path(__file__).with_name('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'created':'teaching.zh-CN.ipynb','code_cells':6}))
