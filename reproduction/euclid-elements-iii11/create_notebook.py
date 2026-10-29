"""Build and execute a small nbformat4 teaching notebook without a Jupyter kernel."""
import json,io,contextlib
from pathlib import Path
lessons=[
('1. 精确模型与输入','from fractions import Fraction as Q\nfrom geometry import Circle, relation, verify_contact, contact_candidate, grid\nouter=Circle((0,0),5)\ninner=Circle((3,0),2)\nprint(relation(outer,inner))'),
('2. 独立提供切点，再核对结论','certificate=verify_contact(outer,inner,(5,0))\nprint(certificate)'),
('3. 平移旋转，不只检验水平图','a=Circle((2,-3),5)\nb=Circle((Q(19,5),Q(-3,5)),2)\nprint(verify_contact(a,b,(5,1)))\nprint("modern candidate:",contact_candidate(a,b))'),
('4. 两交点反例不满足内含','other=Circle((6,0),5)\nprint(relation(outer,other))\ntry:\n    verify_contact(outer,other,(3,4))\nexcept ValueError as exc:\n    print("expected rejection:",str(exc))\nelse:\n    raise RuntimeError("invalid certificate accepted")'),
('5. 有限遍历的范围','print("exact certificates:",grid())\nprint("Finite tests are not a proof for arbitrary real circles.")')]
cells=[{'cell_type':'markdown','metadata':{},'source':['# III.11：内切圆的共线结论\n','现代有理坐标教学重构，不是古典证明器。五格使用 Python 标准库 compile/exec 真正运行；未调用 Jupyter kernel。模板 helper 在本环境不可得，因此使用本地 nbformat4 scaffold；没有安装软件。\n','输入核验先检查圆盘包含及给定公共点，再检查共线；候选构造与核验分离。']}]
namespace={}
for number,(title,code) in enumerate(lessons,1):
 cells.append({'cell_type':'markdown','metadata':{},'source':[title]})
 out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(code,f'cell-{number}','exec'),namespace)
 cells.append({'cell_type':'code','metadata':{},'execution_count':number,'source':code.splitlines(True),'outputs':[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(True)}]})
 print('cell',number,'executed')
nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'},'execution_note':'stdlib compile/exec, not Jupyter kernel'},'nbformat':4,'nbformat_minor':5}
for i,c in enumerate(cells):c['id']=f'iii11-{i:02d}'
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('5 code cells saved; non-kernel execution')
