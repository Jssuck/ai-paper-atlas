"""Local nbformat4 scaffold + actual compile/exec, NOT a Jupyter kernel run."""
import json,io,contextlib
from pathlib import Path
lessons=[
('1. 半径和而非半径差','from fractions import Fraction as Q\nfrom geometry import Circle,relation,verify_contact,contact_candidate,grid\na=Circle((0,0),3)\nb=Circle((5,0),2)\nprint(relation(a,b))'),
('2. 独立输入公共点，检查结论','print(verify_contact(a,b,(3,0)))\nprint("separate construction:",contact_candidate(a,b))'),
('3. 非轴向平移及交换圆心','a=Circle((2,-3),3)\nb=Circle((5,1),2)\nt=(Q(19,5),Q(-3,5))\nprint(verify_contact(a,b,t))\nprint(verify_contact(b,a,t))'),
('4. 共线内切不等于外切','a=Circle((0,0),3)\nb=Circle((1,0),2)\nprint(relation(a,b))\ntry:\n    verify_contact(a,b,(3,0))\nexcept ValueError as exc:\n    print("expected rejection:",str(exc))\nelse:\n    raise RuntimeError("invalid input accepted")'),
('5. 精确有限实验不是一般定理','print("configurations:",grid())\nprint("Both circle orders checked. Finite tests are not a general proof.")')]
cells=[{'cell_type':'markdown','metadata':{},'source':['# III.12：外切圆与接点的介于关系\n','现代有理坐标教学模型；前提是圆盘内域分离和给定公共圆周点，结论为半径和距离、共线及严格介于。\n','此文件五个代码格用标准库 compile/exec 真正执行并保存 stdout，非 Jupyter kernel。已读 Notebook 技能；本环境 helper 路径不存在且技能资源不可读取，故用本地 nbformat4 scaffold，无安装。']}]
namespace={}
for number,(title,code) in enumerate(lessons,1):
 cells.append({'cell_type':'markdown','metadata':{},'source':[title]});out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(code,f'cell-{number}','exec'),namespace)
 cells.append({'cell_type':'code','metadata':{},'execution_count':number,'source':code.splitlines(True),'outputs':[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(True)}]});print('cell',number,'executed')
for i,c in enumerate(cells):c['id']=f'iii12-{i:02d}'
nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'},'execution_note':'stdlib compile/exec, not Jupyter kernel'},'nbformat':4,'nbformat_minor':5}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n');print('5 code cells saved; non-kernel execution')
