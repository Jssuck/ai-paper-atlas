"""Own nbformat 4.5 scaffold; installed skill's helper is absent."""
import json,io,contextlib
sections=[('模型与原图点名','from fractions import Fraction as Q\nfrom geometry import construct, verify, summary\na=((0,0),(6,0),(0,2),[Q(1,6),Q(1,2)])\nc=construct(*a)\nprint(c["lower"])\nprint(c["upper"])'),('先核验几何证书，再读取面积','print(verify(*a,c))\nprint(summary(*a))'),('斜置矩形与不同切点','print(summary((1,-2),(4,2),(-3,1),[Q(1,5),Q(3,5)]))'),('面积相等不够：换序破坏绑定','bad=dict(c)\nbad["tiles"]=c["tiles"][::-1]\nprint(verify(*a,bad))'),('非法切分直接拒绝','for cuts in [[Q(1,2),Q(1,2)],[True],[0.5]]:\n    try: construct((0,0),(6,0),(0,2),cuts)\n    except ValueError as e: print(type(e).__name__+": "+str(e))')]
cells=[{'cell_type':'markdown','id':'intro','metadata':{},'source':['# II.1：矩形分割证书\n','五代码格使用标准库 compile/exec 真实执行与回放，未启动 Jupyter kernel。有限有理样例不能证明一般定理。原图三段点名B-D-E-C与G-K-L-H；任意有限分段属于教学重构。']}];ns={}
for i,(title,src) in enumerate(sections,1):
    cells.append({'cell_type':'markdown','id':f'm{i}','metadata':{},'source':[title]})
    b=io.StringIO()
    with contextlib.redirect_stdout(b):exec(compile(src,'teaching-cell','exec'),ns)
    cells.append({'cell_type':'code','id':f'c{i}','metadata':{},'execution_count':i,'source':src.splitlines(True),'outputs':[{'output_type':'stream','name':'stdout','text':b.getvalue().splitlines(True)}]})
nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},'nbformat':4,'nbformat_minor':5}
open('teaching.zh-CN.ipynb','w').write(json.dumps(nb,ensure_ascii=False,indent=2)+'\n');print('Executed 5 code cells using compile/exec; no Jupyter kernel started.')
