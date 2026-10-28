"""Build and execute a small teaching notebook with stdlib, not a kernel."""
import contextlib, io, json
cells=[]
def md(s): cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s): cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(True),'execution_count':None,'outputs':[]})
md('# I.41：同底同平行带，面积为何二倍\n原创坐标教学。下面五格真实以标准库 compile/exec 执行，非 Jupyter kernel；有限例不证明一般定理。请从本附件目录启动。')
code("from geometry import make_certificate, verify_certificate\nfrom cases import example, valid_cases, invalid_cases, F\nc = make_certificate(example())\nprint(c['double_areas'])")
md('## 原证依赖与数值验证分层\nI.37 比较 ABC 与 EBC；I.34 二分平行四边形。以下标签展示依赖，不是机器证明核。')
code("print('\\n'.join(c['chain']))")
md('## 顶点不必落在线段 AD 内\n端点重合不会使三角形 EBC 退化；AE 两点名在 E=A 时失效，因此以支持线 AD 表述。')
code("for t in [-2, 0, F(1,2), 1, 3]:\n    r=make_certificate(example(t))\n    print(t, r['upper_position'], r['double_areas']['EBC'])")
md('## 前提是输入契约，不是面积比本身\n异侧但同绝对高度可碰巧保留面积比，却不满足原命题。')
code("rejected=0\nfor label,p in invalid_cases():\n    try: make_certificate(p)\n    except ValueError:\n        rejected+=1\nprint('direct rejections:',rejected)")
md('## 有限回归与证书换绑\n验证器重算不是独立数学核；需来源与技术独立审查。')
code("items=list(valid_cases())\nprint('valid rational instances:',len(items))\nprint('all certificates accepted:',all(verify_certificate(p,make_certificate(p)) for p in items))\nprint('same-area rebind rejected:',not verify_certificate(example(0),make_certificate(example(1))))")
ns={}
for i,c in enumerate([c for c in cells if c['cell_type']=='code'],1):
    out=io.StringIO()
    with contextlib.redirect_stdout(out): exec(compile(''.join(c['source']),f'cell-{i}','exec'),ns)
    c['execution_count']=i;c['outputs']=[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(True)}]
nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.12'},'execution_note':'Executed with standard library compile/exec, not a Jupyter kernel.'},'nbformat':4,'nbformat_minor':5}
for i,c in enumerate(cells): c['id']=f'i41-{i}'
open('teaching.zh-CN.ipynb','w').write(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('Built notebook; executed 5 code cells with stdlib compile/exec, not kernel.')
