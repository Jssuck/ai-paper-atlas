"""Build and execute six teaching cells with stdlib, not a Jupyter kernel."""
import json,io,contextlib
sources=[
"from geometry import make_certificate, verify_certificate\nfrom cases import BASE, NEGATIVE, positive_cases\nprint('Exact rational model; stdlib compile/exec, not kernel')",
"c = make_certificate(BASE)\nprint(c['premises'])",
"print(c['sas'])\nprint(c['conclusion'])",
"bad = NEGATIVE[0]\ntry:\n    make_certificate(bad)\nexcept ValueError as e:\n    print('Crossed correspondence rejected:', str(e))",
"n = sum(verify_certificate(d, make_certificate(d)) for d in positive_cases())\nprint('Finite positive inputs:', n)",
"import copy\nchanged = copy.deepcopy(c)\nchanged['conclusion']['AC_squared'] = True\nprint('Forged certificate accepted:', verify_certificate(BASE, changed))\nprint('Finite checks do not prove the general theorem.')"
]
cells=[{'cell_type':'markdown','metadata':{},'source':['# I.33：对应关系与平行等长连接\n','现代有理坐标教学模型，不认证尺规操作史；六格用标准库 compile/exec 实跑，非 Jupyter kernel。\n','安装技能的本地 scaffold 脚本不可用，采用最小 nbformat 4 结构并回放校验。']}]
ns={}
for i,s in enumerate(sources,1):
 b=io.StringIO()
 with contextlib.redirect_stdout(b):exec(compile(s,'cell-'+str(i),'exec'),ns)
 cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(True),'execution_count':i,'outputs':[{'output_type':'stream','name':'stdout','text':b.getvalue().splitlines(True)}]})
nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},'nbformat':4,'nbformat_minor':5}
for i,c in enumerate(cells):c['id']='i33-cell-'+str(i)
open('teaching.zh-CN.ipynb','w').write(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('Executed six code cells with compile/exec; no kernel started')
