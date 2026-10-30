"""Generate a transparent stdlib compile/exec teaching notebook, not kernel output."""
import json,io,contextlib
from pathlib import Path
cells=[]; ns={'__name__':'__notebook__'}
def md(s): cells.append(dict(cell_type='markdown',metadata={},source=s.splitlines(True)))
def code(s):
 b=io.StringIO()
 with contextlib.redirect_stdout(b): exec(compile(s,'notebook-cell','exec'),ns)
 cells.append(dict(cell_type='code',metadata={},source=s.splitlines(True),execution_count=None,outputs=[dict(output_type='stream',name='stdout',text=b.getvalue().splitlines(True))]))
md('# III.22：四边形的次序是条件\n面向熟悉三角形角和与Python的读者。目标：区分圆周点集合与按边界排列的四边形；精确核对互补角。\n顺序：正例→原证替换→交叉反例→近退化→有限网格。输出来自Python标准库compile/exec，未启动Jupyter kernel；计数保持null。')
md('## 1. 正方形只是特殊正例\n四个cot均为0，不代表所有内接四边形均为矩形。')
code('from fractions import Fraction as F\nfrom geometry import certificate,circle_points,grid\nfrom independent_oracle import check\nQ=((1,0),(0,1),(-1,0),(0,-1))\nprint(certificate(Q)["cots"])\n')
md('## 2. 原证的两次III.21替换\ntriangle ABC的BAC=BDC、ACB=ADB，后两角拼成ADC。负cot不可取绝对值。')
code('z=certificate(tuple(circle_points()[:4]))\nprint("四内角cot:",z["cots"])\nprint("原证替换:",z["same_segment"],"拼角:",z["split_matches_D"],"三角形关系:",z["triangle_sum"])\n')
md('## 3. 练习：把B、C交换，结论还可直接用吗？\n答案：不能；这不是凸四边形边界次序，程序应拒绝。非反角的两对角和在这个交叉正方形例子中为90度而非180度。')
code('try:\n    certificate((Q[0],Q[2],Q[1],Q[3]))\nexcept ValueError as e:\n    print("已拒绝:",e)\n')
md('## 4. 很近不等于重合\n有理运算可区分距离极近的合法点；若设t=0则重复点应拒绝。')
code('t=F(1,10**12)\np=((1-t*t)/(1+t*t),2*t/(1+t*t))\nprint("近退化精确和:",certificate((Q[0],p,Q[1],Q[2]))["opposite_sums"])\n')
md('## 5. 有限网格与独立浮点检查\n扩展练习：更换有理参数集合再跑。任何有限网格都不是一般证明；浮点oracle有容差。')
code('print(grid())\nprint(check())\n')
nb=dict(nbformat=4,nbformat_minor=5,metadata=dict(kernelspec=dict(display_name='Python 3',language='python',name='python3'),language_info=dict(name='python'),execution_note='stdlib compile/exec; not Jupyter kernel'),cells=cells)
for i,c in enumerate(cells): c['id']='iii22-'+str(i)
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('Created 5 executed-by-compile/exec cells; execution_count null; no kernel used')
