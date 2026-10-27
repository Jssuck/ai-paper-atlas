"""Stdlib scaffold fallback: installed skill helper absent; no installs."""
import json
from pathlib import Path
cells=[]
def md(s):cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s):cells.append({'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':s.splitlines(True)})
md('# Euclid I.25：从较大底到较大夹角\n现代 Gram 数据的精确教学实验，不是原典证明或完整形式化。六格用标准库 compile/exec 实跑，不是 Jupyter kernel。')
code("from geometry import certify, classify, verify\nfrom cases import case, positives\nc=certify(case())\nprint(c['metric'])")
md('## 1 依赖记录\n原典排除等角用 I.4，排除较小角需交换三角形使用 I.24；三分性是逻辑背景。程序保存该结构，不形式化证明 I.4/I.24。')
code("print(c['branches'])")
md('## 2 等底及反向底\n这些是边界比较，不满足 I.25 的严格较大底前提。')
code("print(classify(case(d=3,e=3)))\nprint(classify(case(d=3,e=0)))")
md('## 3 有限精确网格\n250 个有理 Gram 数据只是实现检查。')
code("ds=positives()\nprint('cases',len(ds),'verified',sum(verify(d,certify(d)) for d in ds))")
md('## 4 类型攻击\nPython 中 True==1，证书必须拒绝这种类型替换。')
code("bad=certify(case());bad['schema_version']=True\nprint('bool accepted',verify(case(),bad))\nif verify(case(),bad):raise RuntimeError('type attack accepted')")
md('## 5 删除一个边相等条件\n第一对边都长1；第二对分别长10与1。角60°的底平方91，而角90°的底平方2。较大底不再保证较大角。')
code("bad_input=case();bad_input['ABC']={'a2':[1,1],'b2':[100,1],'dot':[5,1]};bad_input['DEF']={'a2':[1,1],'b2':[1,1],'dot':[0,1]}\ntry: certify(bad_input)\nexcept ValueError as e: print(str(e))\nelse: raise RuntimeError('missing hypothesis accepted')")
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'language_info':{'name':'python','version':'3'},'execution_method':'stdlib compile/exec; not kernel'},'cells':cells}
for i,c in enumerate(cells):c['id']='i25-'+str(i)
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('created six-code-cell tutorial with stdlib scaffold fallback')
