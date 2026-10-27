"""Six-step tutorial. Skill scaffold helper is not present in this executor."""
import json
from pathlib import Path
cells=[]
def md(t):cells.append({'cell_type':'markdown','metadata':{},'source':t.splitlines(keepends=True)})
def code(t):cells.append({'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':t.splitlines(keepends=True)})
md('# I.17：从外角比较到任两角和的严格上界\n原创现代教学模型；不是欧几里得原文符号，也不是一般公理体系的机器证明。这里由标准库 compile/exec 顺序执行，未使用 Jupyter kernel。')
code("from geometry import construct,verify,ledger\nfrom cases import run_cases\np={'A':[1,2],'B':[0,0],'C':[3,0]}\nc=construct(p)\nprint(c['input'])\nprint(c['oriented_double_area'])")
md('## 外角严格大于远内角\n每个角以未归一化的点积、叉积绝对值表示。AB这行比较A内角与B外角，外角方向来自把CB越过B延长。')
code("print(c['pairs']['AB'])")
md('## 相同正因子下的两个表达式\n外角减远角的正弦分子，与这两个内角之和的正弦分子相同；不需要先假定三内角和定理。')
code("for pair,w in c['pairs'].items():\n    print(pair,w['external_minus_remote_sine_numerator'],w['pair_sum_sine_numerator'],w['pair_sum_lt_two_right_angles'])")
md('## 有序角量账本\n已知a<e及b+e=2R，同加b给a+b<2R。这是抽象前提核验，不表示任意输入都来自某个真实三角形。')
code("print(ledger('1/2','1/2','3/2'))\ntry: ledger(1,1,1)\nexcept ValueError as error: print('strict premise rejected:',error)")
md('## 输入绑定及严格JSON类型\n布尔True不能冒充整数schema=1；换输入也不能复用旧证书。')
code("import copy\nbad=copy.deepcopy(c);bad['schema']=True\nprint('valid:',verify(p,c),'bool schema:',verify(p,bad),'changed input:',verify(dict(p,A=[2,2]),c))")
md('## 有限覆盖与边界\n检查有理欧氏平面中的正负方向、非法输入和角量账本。不认证所有几何模型或一般公理定理，也不把两角上界当作三角和等式。')
code("print(run_cases())\nprint(c['conclusion'])")
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'scaffold':'manual schema; installed skill helper absent'},'cells':cells}
for i,c in enumerate(cells):c['id']=f'i17-cell-{i:02d}'
Path(__file__).with_name('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('Created 6 code cells; not yet executed.')
