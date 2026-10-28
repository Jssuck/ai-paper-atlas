"""Original nbformat 4.5 tutorial, stdlib execution; scaffold CLI unavailable."""
import json,io,contextlib
cells=[]
def md(s):cells.append({'cell_type':'markdown','id':'m'+str(len(cells)),'metadata':{},'source':s})
def code(s):cells.append({'cell_type':'code','id':'c'+str(len(cells)),'metadata':{},'source':s,'outputs':[],'execution_count':None})
md('# I.45：两块等积平行四边形的拼接\n原创有限精确模型；不是尺规模拟或一般定理证明。标准库compile/exec，非Jupyter kernel。')
code('from geometry import construct,verify,area\nfrom cases import BASE,valid_cases,INVALID\nc=construct(BASE)\nprint(list(map(str,c["areas"])))')
md('严格凸四边形由DB分成ABD与DBC，输入范围不包括一般凹多边形。')
code('print({k:list(map(str,v)) for k,v in c["points"].items()})\nprint("verified",verify(BASE,2,1,2,c))')
md('共边HG的两侧各一块，拼合输出K-F-L-M，不是任意两等积图形都能拼合。')
code('P=c["points"]\nprint("seed",area([P[k] for k in "KFGH"]))\nprint("added",area([P[k] for k in "HGLM"]))\nprint("whole",area([P[k] for k in "KFLM"]))')
md('锐角、直角、钝角都可在q>0规范中表达。')
code('for p in (-2,0,1):\n    z=construct(BASE,2,p,2)\n    print(p,verify(BASE,2,p,2,z),str(z["areas"][2]))')
md('最后检查有限网格和非法输入；通过不证明无限域一般命题。')
code('n=sum(verify(*a,construct(*a)) for a in valid_cases())\nr=0\nfor name,*a in INVALID:\n    try: construct(*a)\n    except ValueError: r+=1\nprint("valid",n,"invalid rejected",r)')
ns={};count=0
for c in cells:
 if c['cell_type']=='code':
  count+=1;out=io.StringIO()
  with contextlib.redirect_stdout(out):exec(compile(c['source'],'<teaching-cell>','exec'),ns)
  c.update(execution_count=count,outputs=[{'output_type':'stream','name':'stdout','text':out.getvalue()}])
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'name':'python3','display_name':'Python 3','language':'python'},'language_info':{'name':'python','version':'3'},'execution_note':'stdlib compile/exec, not kernel'},'cells':cells}
open('teaching.zh-CN.ipynb','w').write(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('executed',count,'code cells via stdlib compile/exec; no kernel')
