import json,io,contextlib
from pathlib import Path
cells=[];ns={}
def md(text):cells.append({'cell_type':'markdown','id':'md-'+str(len(cells)),'metadata':{},'source':text.splitlines(True)})
def code(text):
 out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(text,'<teaching-cell>','exec'),ns)
 cells.append({'cell_type':'code','id':'code-'+str(len(cells)),'metadata':{'execution_method':'standard-library compile/exec; not Jupyter kernel'},'source':text.splitlines(True),'execution_count':None,'outputs':[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(True)}]})
md('# II.10：向外延长与同一AG的两条路线\n原创精确教学核验。以下五格通过标准库compile/exec真实执行，未启动Jupyter kernel；有限实例不证明一般定理。')
code("from geometry import construct,verify,side_diagonal\nfrom fractions import Fraction as Q\nc=construct(3,2)\nr=verify(c,3,2)\nprint({k:tuple(map(str,v)) for k,v in c['points'].items()})")
md('## 检查四次I.47\n先验证直角、等长和点证书，再比较四个平方关系。')
code("print({k:tuple(map(str,v)) for k,v in r['routes'].items()})\nprint('AG squared =',r['squares']['AG'],'; two routes =',r['lhs'],r['rhs'])")
md('## 变换保持什么\n非单位正交等长基把所有平方统一乘以基长平方。')
code("kw={'origin':(7,-4),'u':(0,2),'v':(2,0)}\nz=verify(construct(3,2,**kw),3,2,**kw)\nprint('basis norm squared =',z['basis_norm_squared'],'; lhs =',z['lhs'])")
md('## 非法证书不是近似正确\n故意移动G，验证器必须拒绝。')
code("bad=construct();bad['points']['G']=(Q(8),Q(-3))\ntry:\n    verify(bad)\nexcept ValueError as e:\n    print('rejected:',str(e))\nelse:\n    raise RuntimeError('tampering accepted')")
md('## 现代整数旁支\nh=s、t=d，因而AC=s、DB=d、CD=s+d、AD=2s+d。检验差值符号翻转，不宣称这是古代整数近似史的完整复现。')
code("for row in side_diagonal(8):\n    print(row['s'],row['d'],row['difference'],'->',row['next_s'],row['next_d'],row['next_difference'])")
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'language_info':{'name':'python'},'execution_note':'Executed using Python compile/exec, not a Jupyter kernel'},'cells':cells}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('5 code cells executed with compile/exec; kernel_started=false')
