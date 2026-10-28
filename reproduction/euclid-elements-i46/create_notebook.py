"""Original nbformat tutorial. Installed scaffold path unavailable; stdlib fallback."""
import json,io,contextlib
cells=[]
def md(s):cells.append({'cell_type':'markdown','id':'m'+str(len(cells)),'metadata':{},'source':s})
def code(s):cells.append({'cell_type':'code','id':'c'+str(len(cells)),'metadata':{},'source':s,'outputs':[],'execution_count':None})
md('# I.46：指定线段上的正方形\n有理坐标教学重构，不是尺规模拟。原证依I.11/I.3/I.31/I.34/I.29与定义22，不能用I.47替代。此文件以标准库compile/exec真实执行，非Jupyter kernel。')
code('from geometry import construct,verify,area\nfrom cases import valid_cases,INVALID\nc=construct((0,0),(3,4))\nprint({k:list(map(str,v)) for k,v in c["points"].items()})')
md('边界顺序A-D-E-B。C只标示垂直射线，选择在D以外；它不是正方形顶点。')
code('print("verified",verify((0,0),(3,4),1,c))\nprint("side squared",c["side_squared"])\nprint("area",area([c["points"][k] for k in "ADEB"]))')
md('同一底边的两侧各能构造。方向参数只允许整数+1或-1。')
code('for s in (-1,1):\n    z=construct((0,0),(3,4),s)\n    print(s,"D=",z["points"]["D"],"verified",verify((0,0),(3,4),s,z))')
md('矩形不足以成为正方形；证书不由构造器自行盖章。')
code('import copy\nbad=copy.deepcopy(c)\nbad["points"]["E"]=(0,0)\nprint("tampered accepted",verify((0,0),(3,4),1,bad))')
md('有限案例只验证实现行为，不能代替一般证明。')
code('n=sum(verify(A,B,s,construct(A,B,s)) for A,B,s in valid_cases())\nr=0\nfor name,A,B,s in INVALID:\n    try: construct(A,B,s)\n    except ValueError:r+=1\nprint("valid",n,"invalid rejected",r)')
ns={};n=0
for c in cells:
 if c['cell_type']=='code':
  n+=1;o=io.StringIO()
  with contextlib.redirect_stdout(o):exec(compile(c['source'],'<teaching-cell>','exec'),ns)
  c.update(execution_count=n,outputs=[{'output_type':'stream','name':'stdout','text':o.getvalue()}])
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'name':'python3','display_name':'Python 3','language':'python'},'language_info':{'name':'python','version':'3'},'execution_note':'stdlib compile/exec, not Jupyter kernel'},'cells':cells}
open('teaching.zh-CN.ipynb','w').write(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('executed',n,'code cells by stdlib compile/exec; no kernel')
