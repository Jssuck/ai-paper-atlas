"""Build and execute educational cells with compile/exec; no kernel is started."""
import json,io,contextlib
from pathlib import Path
texts=[
('输入与几何资格','a、b为AC、CB的基系数；实际长度还乘基向量长度，均严格正，等分合法。','from fractions import Fraction as Q\nfrom geometry import construct, verify\nc=construct()\nr=verify(c)\nprint(c["points"])'),
('余形同加共同正方形','AG=GE；各加CF得到AF=CE。','print("AG=",r["AG"],"GE=",r["GE"],"CF=",r["CF"])\nprint("AF=",r["AF"],"CE=",r["CE"])'),
('重叠必须计两次','两个矩形的面积和并非并集：并集为曲尺形，交集为CF。','print("sum",r["AF"]+r["CE"],"union",r["gnomon"],"overlap",r["CF"])\nprint("whole+CF",r["whole"]+r["CF"],"2AF+DG",2*r["AF"]+r["DG"])'),
('有理输入及缩放','正交基(3,4),(-4,3)长5，面积乘25。','z=verify(construct(Q(2,3),Q(5,7)),Q(2,3),Q(5,7))\nprint({k:str(v) for k,v in z.items()})\ns=verify(construct(u=(3,4),v=(-4,3)),u=(3,4),v=(-4,3))\nprint("scaled whole",s["whole"])'),
('拒绝不合构造的证书','满足最终面积恒等式不等于所有点资格成立；篡改G必须拒绝。','bad=construct()\nbad["points"]["G"]=(Q(3),Q(3))\ntry:\n    verify(bad)\nexcept ValueError as e:\n    print("rejected:",e)\nelse:\n    raise RuntimeError("tampering accepted")')]
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
