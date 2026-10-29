"""Build and run five tutorial cells. Standard-library compile/exec, no kernel."""
import json,io,contextlib
from pathlib import Path
steps=[
('参数与点资格','a=AC,b=BC=BD；正交等长基的长度另乘系数。a=b也合法。','from fractions import Fraction as Q\nfrom geometry import construct,verify\nc=construct()\nr=verify(c)\nprint(c["points"])'),
('四个小平方','先核对每一格，不从最终恒等式倒推。','print({k:str(r[k]) for k in ("CK","KD","GR","RN")})'),
('四块矩形与八格曲尺形','AG和CK合成AK，八块互不重叠格面积为四倍AK。','print({k:str(r[k]) for k in ("AG","MQ","QL","RF")})\nprint("gnomon",r["gnomon"],"four AK",4*r["AK"])\nprint("plus OH",r["gnomon"]+r["OH"],"whole",r["whole"])'),
('有理数及非单位基','基向量(3,4),(-4,3)长度5，面积乘25。','a,b=Q(2,3),Q(5,7)\nz=verify(construct(a,b),a,b)\nprint("rational whole",z["whole"])\ns=verify(construct(u=(3,4),v=(-4,3)),u=(3,4),v=(-4,3))\nprint("scaled whole",s["whole"])'),
('错误证书','篡改交点Q必须被拒绝；有限检查不替代一般证明。','bad=construct()\nbad["points"]["Q"]=(Q(3),Q(3))\ntry:\n    verify(bad)\nexcept ValueError as e:\n    print("rejected:",e)\nelse:\n    raise RuntimeError("tampering accepted")')]
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'execution_note':'compile/exec stdout capture, no kernel; execution_count null'},'cells':[]};ns={}
for i,(title,note,code) in enumerate(steps):
 nb['cells'].append({'cell_type':'markdown','id':f'note-{i}','metadata':{},'source':[f'## {title}\n',note]})
 out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(code,'<tutorial>','exec'),ns)
 nb['cells'].append({'cell_type':'code','id':f'code-{i}','metadata':{},'execution_count':None,'source':code.splitlines(True),'outputs':[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(True)}]})
 print(f'cell {i+1}:\n'+out.getvalue())
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('5 cells executed using compile/exec; no kernel started')
