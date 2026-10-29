"""Create a small standard-library tutorial notebook; no kernel execution claimed."""
import json
from pathlib import Path
cells=[]
def md(s): cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s): cells.append({'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':s.splitlines(True)})
md('# III.4：不能同时平分，不是一个也不能平分\n精确有理数教学核验。代码在相同目录运行。保存输出来自标准库compile/exec，非Jupyter内核。有限样本不是一般证明。')
code("from geometry import examples, verify, grid, scalar, point, sub, norm\ncs=examples()\nprint('named examples:', len(cs))\nprint('all valid:', all(verify(c) for c in cs.values()))\n")
md('## 两条均非直径，但一条弦确实被平分\n先预测midpoint_AC、midpoint_BD，再执行。')
code("c=cs['only_AC_midpoint']\nprint('E:', c['E'])\nprint('parameters:', c['t'], c['u'])\nprint('midpoints:', c['midpoint_AC'], c['midpoint_BD'])\nprint('original domain:', c['theorem_applies'])\n")
md('## 证明接口：两方向残差不能同时消失\n这只是现代坐标恒等式检查，不是原文的直角反证。')
code("print('direction determinant:', c['det'])\nprint('center residuals:', c['dot_v'], c['dot_w'])\nz=c['input'];E=point(c['E'])\nprint('EB squared:', norm(sub(point(z['B']),E)))\nprint('ED squared:', norm(sub(point(z['D']),E)))\n")
md('## 放宽到两条直径\n两弦互相平分，但交点就是圆心。原命题排除这个输入。')
code("d=cs['two_diameters']\nprint('both midpoints:', d['both_midpoints'])\nprint('at center:', d['at_center'])\nprint('original domain:', d['theorem_applies'])\n")
md('## 有限变换检查与练习\n练习：为什么not(A and B)不等于not A and not B？答案：第二格的单平分案例满足前者，不满足后者。')
code("rows=grid()\nprint('finite cases:', len(rows))\nprint('valid:', all(verify(c) for c in rows))\nprint('both-midpoint cases:', sum(c['both_midpoints'] for c in rows))\n")
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'},'execution_note':'Saved outputs produced by standard-library compile/exec, not a Jupyter kernel.'},'cells':cells}
for i,c in enumerate(cells): c['id']=f'iii4-{i+1}'
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('tutorial notebook created')
