"""Build actual stdlib compile/exec outputs, not kernel execution."""
import json,io,contextlib
from pathlib import Path
cells=[]; ns={}
def md(s): cells.append(dict(cell_type='markdown',metadata={},source=s.splitlines(True)))
def code(s):
 b=io.StringIO()
 with contextlib.redirect_stdout(b): exec(compile(s,'teaching-cell','exec'),ns)
 cells.append(dict(cell_type='code',metadata={},source=s.splitlines(True),execution_count=None,outputs=[dict(output_type='stream',name='stdout',text=b.getvalue().splitlines(True))]))
md('# III.24：先对齐底，再证明弓形重合\n面向熟悉坐标和分数的读者。目的：把原文叠合与现代刚体映射分开，检验等底、相似角与区域对应。不是原文算法或一般定理证明。默认技能helper未在本环境找到；依据Notebook结构指南生成，无安装。保存输出实际来自Python标准库compile/exec，非Jupyter kernel，execution_count=null。请在此目录运行。')
md('## 1. 从点积而不是结论测角\na=2,k=3/2，圆心(0,3/2)，半径5/2，取射线斜率1。练习：为什么cot=3/4不是3/2？答案：半底长a也进入分母。')
code('from geometry import *\ns=Segment(2,F(3,2)); p=s.arc_point(1)\nprint("P:",p,"cot:",s.measured_cot(p),"radius²:",s.radius2)\n')
md('## 2. 刚体对齐不预设相似\n目标基底采用有理旋转与反射。映射以两个正交框架定义，保持距离和所选侧；等底保证两端对应。映射构造未检查k相等，最后才核支撑圆是否一致。')
code('t=Segment(2,F(3,2),(5,-1),(F(3,5),F(4,5)),(F(4,5),F(-3,5)))\nprint("ends:",t.endpoints)\nprint("mapped P:",s.align_point_to(t,p))\nprint("same location before:",s.coincides(t),"circle matches after:",s.aligned_circle_matches(t))\n')
md('## 3. 镜像不是不等的反例\n反射改变选侧与圆心位置，但保持大小与所容角。原圆另侧则通常角互补，两种操作不能混淆；半圆是例外。')
code('m=Segment(2,F(3,2),n=(0,-1))\no=Segment(2,F(-3,2),n=(0,-1))\nprint("mirror:",s.similar(m),s.coincides(m))\nprint("same circle other side:",s.center==o.center,s.angle_cot,o.angle_cot)\n')
md('## 4. 条件和边界\n放大两倍保角但底不等，不能用刚体映射。练习：先构造映射就说明结论吗？答案：否，等底不同k也可以对齐底，却不对齐圆心。')
code('print("unequal k, equal bases:",s.aligned_circle_matches(Segment(2,2)))\nprint("scaled similar:",s.similar(Segment(4,3)))\ntry:\n    s.align_point_to(Segment(4,3),p)\nexcept ValueError as e:\n    print("rejected:",e)\n')
md('## 5. 有限精确网格\n包括小弓形、半圆、大弓形，有理正交方向与反射。没有枚举全部实数、全部刚体或整个连续区域；成员抽样不替代正文一般证明。三运行模式重复相同样本，不算三倍不同数据。')
code('print(grid())\n')
for i,c in enumerate(cells): c['id']='iii24-'+str(i)
nb=dict(nbformat=4,nbformat_minor=5,cells=cells,metadata=dict(kernelspec=dict(display_name='Python 3',language='python',name='python3'),language_info=dict(name='python'),execution_note='Actual stdlib compile/exec, not kernel'))
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('5 cells executed by stdlib compile/exec, null counts, NOT kernel')
