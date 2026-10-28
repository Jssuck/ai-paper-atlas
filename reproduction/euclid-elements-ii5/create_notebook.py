"""Standard-library execution and output capture, not a Jupyter kernel."""
import json,io,contextlib
from pathlib import Path
texts=[
('输入与范围','本Notebook只检查右半内切的有理坐标模型。输入t=CD/CB严格在0与1之间。有限实跑不证明一般命题。','from fractions import Fraction as Q\nfrom geometry import construct, verify\nc = construct()\na = verify(c)\nprint("A-C-D-B; t=2/5")\nprint(c["points"])'),
('余形及中间矩形','先比较CH与HF，再分别加DM得到CM与DF。','for name in ("CH", "HF", "DM", "CM", "DF", "AL"):\n    print(name, a[name])'),
('磬折形与补方','AH与磬折形等积，再加LG补满平方。','print("AH", a["AH"], "gnomon", a["gnomon"])\nprint(a["AH"], "+", a["LG"], "=", a["square"])'),
('分数实例','坐标单位改变不改变推理链。','z = verify(construct(u=(1,0), v=(0,1), t=Q(2,7)), u=(1,0), v=(0,1), t=Q(2,7))\nprint(z["AH"], "+", z["LG"], "=", z["square"])'),
('拒绝伪证书','等面积不够；点H必须处在原对角线上。','bad = construct()\nbad["points"]["H"] = (Q(2),Q(2))\ntry:\n    verify(bad)\nexcept ValueError as e:\n    print("rejected:", str(e))\nelse:\n    raise RuntimeError("tampering accepted")')]
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'execution_note':'Sequential compile/exec with stdout capture; no kernel; execution_count remains null'},'cells':[]}
ns={}
for i,(title,note,code) in enumerate(texts):
 nb['cells'].append({'cell_type':'markdown','id':f'note-{i}','metadata':{},'source':[f'## {title}\n',note]})
 out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(code,'<teaching>','exec'),ns)
 nb['cells'].append({'cell_type':'code','id':f'code-{i}','metadata':{},'execution_count':None,'source':code.splitlines(True),'outputs':[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(True)}]})
 print(f'cell {i+1}:\n'+out.getvalue())
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('5 code cells executed with compile/exec; no kernel started')
