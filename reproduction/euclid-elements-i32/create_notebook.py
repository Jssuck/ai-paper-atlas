"""Original stdlib notebook writer; installed scaffold helper unavailable."""
import json,io,contextlib
codes=[
"from geometry import make_certificate, verify_certificate\nfrom cases import fixture, positives, negatives\nprint('Exact rational coordinate model; not a general synthetic proof')",
"x=fixture()\nc=make_certificate(x)\nprint(c['angles'])\nprint(c['products'])",
"print('bound certificate:', verify_certificate(x,c))\nprint('different A:', verify_certificate(fixture(h=2),c))",
"bad=fixture(); bad['E']=['2','-1']\ntry:\n    make_certificate(bad)\nexcept ValueError as e:\n    print('opposite parallel ray rejected:', str(e))",
"count=sum(verify_certificate(d,make_certificate(d)) for d in positives())\nprint('positive inputs checked:', count)\nrejected=0\nfor name,d in negatives():\n    try: make_certificate(d)\n    except ValueError: rejected+=1\n    else: raise RuntimeError(name)\nprint('negative inputs directly rejected:',rejected)",
"print('I.32 uses I.29 and therefore Euclidean parallel-postulate dependence.')\nprint('Finite coordinate checks do not prove the general theorem or axiom independence.')"
]
notes=['# I.32：外角与三角形角和\n六格标准库compile/exec真实执行，非Jupyter kernel。',
'## 1. 模型边界','## 2. 精确角对与乘积','## 3. 完整输入绑定','## 4. 平行射线仍需方向','## 5. 有限正负样例','## 6. 结论边界']
cells=[{'cell_type':'markdown','metadata':{},'source':[notes[0]]}];ns={}
for i,code in enumerate(codes,1):
 cells.append({'cell_type':'markdown','metadata':{},'source':[notes[i]]})
 buf=io.StringIO()
 with contextlib.redirect_stdout(buf): exec(compile(code,'notebook-cell-'+str(i),'exec'),ns)
 cells.append({'cell_type':'code','execution_count':i,'metadata':{},'source':code.splitlines(True),'outputs':[{'output_type':'stream','name':'stdout','text':buf.getvalue().splitlines(True)}]})
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'},'execution_method':'stdlib compile/exec; not a Jupyter kernel'},'cells':cells}
open('teaching.zh-CN.ipynb','w').write(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('6 code cells executed with stdlib compile/exec (not kernel)')
