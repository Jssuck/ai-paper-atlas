"""Original tutorial; stdlib execution, not a Jupyter kernel."""
import contextlib,io,json
cells=[]
def md(s):cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s):cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(True),'execution_count':None,'outputs':[]})
md('# I.42：给定角内构造等积平行四边形\n原创有理坐标教学，需从本目录运行。五格用标准库compile/exec真实执行，非Jupyter kernel。有限检验不替代原证。')
code("from geometry import make_certificate, verify_certificate\nfrom cases import example,valid_cases,invalid_cases,Q\nc=make_certificate(example())\nprint(c['points'])\nprint(c['double_areas'])")
md('## 中点先把三角形减半\nI.38给两小三角形等积，区域分割给二倍；I.41给平行四边形的另一个二倍。程序标签不是形式化证明。')
code("print('\\n'.join(c['chain']))")
md('## 角可锐、直、钝，交点也可与原顶点重合\n用过A的支持线描述，F=A或G=A时不使用无定义的两点名。')
code("for x in [Q(-1,3),-1,-2,0,1,100]:\n    r=make_certificate(example(x))\n    print(x,r['points'],r['double_areas']['FECG'])")
md('## 相反射线不是同侧角复制\n即使某种面积公式出现偶合，非法输入仍须在构造前拒绝。')
code("n=0\nfor label,p in invalid_cases():\n    try: make_certificate(p)\n    except ValueError: n+=1\nprint('invalid cases directly rejected:',n)")
md('## 有限回归与防止证书换绑\n精确有理数只覆盖此数据域，不认证所有实数、尺规可作性或任意输入角的原始复制过程。')
code("ps=list(valid_cases())\nprint('valid cases:',len(ps))\nprint('all accepted:',all(verify_certificate(p,make_certificate(p)) for p in ps))\nprint('same-area rebind rejected:',not verify_certificate(example(-1),c))")
ns={}
for i,c in enumerate([c for c in cells if c['cell_type']=='code'],1):
 out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(''.join(c['source']),f'cell-{i}','exec'),ns)
 c['execution_count']=i;c['outputs']=[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(True)}]
for i,c in enumerate(cells):c['id']=f'i42-{i}'
nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.12'},'execution_note':'stdlib compile/exec, not a Jupyter kernel'},'nbformat':4,'nbformat_minor':5}
open('teaching.zh-CN.ipynb','w').write(json.dumps(nb,ensure_ascii=False,indent=2)+'\n');print('Executed 5 cells using stdlib compile/exec, not a kernel.')
