"""Create a small portable tutorial notebook, using only JSON stdlib.
Skill helper was not present/readable in this executor; no skill installed.
"""
import json
from pathlib import Path
cells=[]
def md(s):cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s):cells.append({'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':s.splitlines(True)})
md('# I.14：补角关系什么时候能推出一条直线？\n\n现代教学重构，不是欧氏原证机器认证。Notebook随包以标准库 compile/exec 顺序执行，不宣称Jupyter kernel执行。')
code('from fractions import Fraction as F\nfrom geometry import build_certificate, inspect_configuration, verify_certificate, angle_model\nfrom cases import run_cases\nprint("Exact Fraction model; no trigonometric floating point")\n')
md('## 1. 同时满足两个前提\n公共射线BA沿正横轴，BC向右上，BD向左下。证书在检查异侧和角和后生成相反射线比例见证。')
code('args=((0,0),(1,0),(2,2),(-1,-1))\ncert=build_certificate(*args)\nprint("side crosses:",cert["side_crosses"])\nprint("angle product:",cert["angle_product"])\nprint("positive scale:",cert["positive_scale"])\nprint("replay:",verify_certificate(cert,*args))\n')
md('## 2. 删除异侧前提\n45°和135°的两条射线在同侧，角和仍为半周，却不共线。度数只是此特殊图形的现代说明。')
code('bad=inspect_configuration((0,0),(1,0),(1,1),(-1,1))\nprint({k:bad[k] for k in ("opposite_sides","supplementary","opposite_rays")})\ntry:\n    build_certificate((0,0),(1,0),(1,1),(-1,1))\nexcept ValueError as e:\n    print(type(e).__name__+": "+str(e))\n')
md('## 3. 两个直角也不够\n同侧两条射线重合，仍各与BA成直角；结论需要相反射线而不只是共线。')
code('overlap=inspect_configuration((0,0),(1,0),(0,1),(0,2))\nprint({k:overlap[k] for k in ("opposite_sides","supplementary","conclusion_cross","conclusion_dot","opposite_rays")})\nprint("60+120 same side:",angle_model(F(1,6),F(1,3),1,1))\n')
md('## 4. 输入绑定与篡改\n证书必须针对独立给出的原输入重算；不能仅信任证书内自报的输入。')
code('altered=dict(cert); altered["positive_scale"]="2"\nprint("tampered:",verify_certificate(altered,*args))\nprint("changed common ray:",verify_certificate(cert,(0,0),(2,0),(2,2),(-1,-1)))\n')
md('## 5. 有限回归\n这些输入覆盖多个平移、旋转、反射、比例和符号，不穷尽有理输入，更不能替代一般角序/旋转论证。')
code('result=run_cases()\nprint({k:result[k] for k in ("positive_certificates","negative_certificates","rational_turn_inputs","positive_replay","negative_rejection")})\n')
md('## 复盘题（含答案）\n1. 为何负实数乘积足够？答：两个普通角都在0到半周之间，其和在0到一周之间，负实方向只有半周。\n2. 为何不能丢异侧？答：同侧45°+135°或同侧90°+90°分别给出不共线和重合反例。\n3. 此程序认证原典全套公理了吗？答：没有，它采用现代有理向量、普通角与旋转语义。')
nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'scaffold_provenance':'Notebook skill read; helper unavailable; standard-library JSON fallback; no installation'},'nbformat':4,'nbformat_minor':5}
for i,c in enumerate(cells):c['id']='i14-'+str(i)
Path(__file__).with_name('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('created tutorial notebook with 6 code cells; execution is a separate command')
