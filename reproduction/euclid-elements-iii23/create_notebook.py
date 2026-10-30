"""Saved output from compile/exec; no Jupyter kernel is started."""
import json,io,contextlib
from pathlib import Path
cells=[];ns={}
def md(s):cells.append(dict(cell_type='markdown',metadata={},source=s.splitlines(True)))
def code(s):
 b=io.StringIO()
 with contextlib.redirect_stdout(b):exec(compile(s,'teaching-cell','exec'),ns)
 cells.append(dict(cell_type='code',metadata={},source=s.splitlines(True),execution_count=None,outputs=[dict(output_type='stream',name='stdout',text=b.getvalue().splitlines(True))]))
md('# III.23：同底、同侧与位置唯一性\n读者：熟悉圆方程和分数运算者。目标：检查嵌套、A-C-D点序和外角严格不等。原文使用III.11定义和I.16；以下是现代坐标教学重构，并非古代算法或一般证明。\n所有保存输出由Python标准库compile/exec顺序产生，不是Jupyter kernel运行；execution_count均为null。本机未找到技能脚本new_notebook.py，按Notebook结构指南生成。\n参数：A=(-1,0),B=(1,0),圆x²+y²-2ky=1；上侧内角cot=k。')
code('from geometry import *\nprint(ordered_witness(0,1))\n')
md('## 1. 外角不是差一个符号\nA-C-D沿同一射线，ACB是三角形CBD在C的外角，ADB=CDB。cot在(0,π)严格递减，cot(C)<cot(D)意味着角C>角D。负cot表示钝角，不能取绝对值。')
code('print(ordered_witness(-1,1))\n')
md('## 2. 去掉同侧后的非重合，不是大小不等\n上侧k=1与下侧k=-1互为关于AB的反射，相似且全等，但不是同一位置的集合。它只能反驳“不限侧也位置唯一”，不是原句similar and unequal的反例。')
code('p=point(1,F(1,4)); q=point(-1,F(-1,4))\nprint("reflection:",p,q,"cots:",cot(p),cot(q),"congruent, noncoincident, NOT unequal")\n')
md('## 3. 近相等与退化\n练习：k差10^-30能否判作相等？答案：不能；这里使用精确Fraction。t=0使射线落在底线上，必须拒绝。')
code('z=ordered_witness(1,1+F(1,10**30))\nprint("exact cot difference:",z["cot_D"]-z["cot_C"])\ntry:\n    point(1,0)\nexcept ValueError as e:\n    print("rejected:",e)\n')
md('## 4. 有限网格不是一般定理\n练习：增加参数范围，是否证明全部实数k？答案：否。程序只验证有限有理样本；正文的代数恒等式及几何证明承担一般论证。')
code('print(grid())\n')
for i,c in enumerate(cells):c['id']='iii23-'+str(i)
nb=dict(nbformat=4,nbformat_minor=5,cells=cells,metadata=dict(kernelspec=dict(display_name='Python 3',language='python',name='python3'),language_info=dict(name='python'),execution_note='Python stdlib compile/exec, not Jupyter kernel'))
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('5 code cells executed with compile/exec; null execution counts; no kernel')
