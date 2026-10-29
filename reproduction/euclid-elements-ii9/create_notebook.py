import json,io,contextlib
from pathlib import Path
cells=[]
def md(text):cells.append({'cell_type':'markdown','metadata':{},'source':text.splitlines(True)})
def code(text):cells.append({'cell_type':'code','metadata':{},'execution_count':None,'source':text.splitlines(True),'outputs':[]})
md('# II.9：同一条AF的两条平方和路线\n原创精确教学核验。下列已存输出由Python标准库逐格compile/exec真实产生，未启动Jupyter kernel；有限试验不替代一般证明。')
md('## 1 构图\nh为半段基系数，d为中点右侧偏移，0<d<h；非单位正交等长基需按基长换算实际长度。')
code('from geometry import construct, verify, normalized_segments\nfrom fractions import Fraction as Q\nc = construct(5,2)\nprint({k:tuple(map(str,v)) for k,v in c["points"].items()})\n')
md('## 2 四次I.47\n先验证六个直角、等长条件，再比较ACE、EGF、AEF和ADF；不是把目标结论当成输入。')
code('r = verify(c,5,2)\nfor name,(left,right) in r["routes"].items():\n print(name,str(left),"=",str(right))\nprint("two routes",str(r["lhs"]),str(r["rhs"]))\n')
md('## 3 左半分点\n交换端点身份把负偏移规范化，原始AD与DB交换，平方和不变。中点与端点仍拒绝。')
code('n = normalized_segments(5,-2)\nprint({k:str(v) for k,v in n.items()})\nprint("sum",verify(construct(n["h"],n["d"]),n["h"],n["d"])["lhs"])\n')
md('## 4 非单位正交基\n两基长均5，平方量乘25，而非乘5。')
code('scaled=verify(construct(5,2,u=(3,4),v=(-4,3)),5,2,u=(3,4),v=(-4,3))\nprint("scale squared",scaled["basis_norm_squared"],"sum",scaled["lhs"])\n')
md('## 5 反例与边界\n坐标篡改和退化输入被拒绝。这不是任意几何图的形式证明器。')
code('bad=construct();bad["points"]["F"]=(7,4)\ntry:\n verify(bad)\nexcept ValueError as e:\n print("tamper rejected:",str(e))\nfor d in [0,5,6]:\n try:\n  construct(5,d)\n except ValueError:\n  print("invalid d rejected",d)\n')
ns={};n=0
for c in cells:
 if c['cell_type']=='code':
  n+=1;out=io.StringIO()
  with contextlib.redirect_stdout(out):exec(compile(''.join(c['source']),'<teaching-cell>','exec'),ns)
  c['outputs']=[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(True)}]
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'language_info':{'name':'python','version':'3'},'execution_method':'stdlib compile/exec; no kernel'},'cells':cells}
for i,c in enumerate(cells):c['id']='ii9-'+str(i)
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('executed code cells:',n,'kernel_started=False')
