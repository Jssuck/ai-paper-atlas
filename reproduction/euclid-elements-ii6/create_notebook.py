"""Build/execute a teaching notebook via standard-library compile/exec, not kernel.
Installed skill helper was not present locally; structure follows its documented fallback.
"""
import json,io,contextlib
from pathlib import Path
texts=[
('输入与几何资格','a=AC=CB，b=BD，均严格正；u/v为等长正交基。坐标是教学模型，有限核查不是一般证明。','from fractions import Fraction as Q\nfrom geometry import construct, verify\nc = construct()\nr = verify(c)\nprint("a=3, b=2; A-C-B-D")\nprint(c["points"])'),
('三块矩形等积','原论证先由I.36比较AL与CH，再由I.43比较CH与HF。','for name in ("AL", "CH", "HF"):\n    print(name, r[name])'),
('曲尺形与补方','AL加CM组成AM；HF加CM组成曲尺形。再补LG为整平方。','print("AM", r["AM"], "gnomon", r["gnomon"])\nprint(r["AM"], "+", r["LG"], "=", r["square"])'),
('精确分数','不用浮点容差，有理输入仍为精确值。','z = verify(construct(Q(2,3), Q(5,7)), Q(2,3), Q(5,7))\nprint(z["AM"], "+", z["LG"], "=", z["square"])'),
('拒绝伪证书','只满足终式不够，H还须是指定对角线与竖线的交点。','bad = construct()\nbad["points"]["H"] = (Q(6),Q(3))\ntry:\n    verify(bad)\nexcept ValueError as e:\n    print("rejected:", str(e))\nelse:\n    raise RuntimeError("tampering accepted")')]
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'execution_note':'Sequential compile/exec with stdout capture; no Jupyter kernel; execution_count null'},'cells':[]}
ns={}
for i,(title,note,code) in enumerate(texts):
 nb['cells'].append({'cell_type':'markdown','id':f'note-{i}','metadata':{},'source':[f'## {title}\n',note]})
 out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(code,'<teaching>','exec'),ns)
 nb['cells'].append({'cell_type':'code','id':f'code-{i}','metadata':{},'execution_count':None,'source':code.splitlines(True),'outputs':[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(True)}]})
 print(f'cell {i+1}:\n'+out.getvalue())
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('5 code cells executed with compile/exec; no kernel started')
