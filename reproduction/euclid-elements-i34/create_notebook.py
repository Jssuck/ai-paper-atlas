"""Stdlib notebook builder/executor; installed scaffold helper was not present."""
import json,io,contextlib
codes=[
"from geometry import make_certificate, verify_certificate\nfrom cases import EXAMPLE, positives, negatives\nc = make_certificate(EXAMPLE)\nprint(c['opposite_sides_squared'])",
"print(c['alternate_angles'])\nprint(c['opposite_angles'])",
"print(c['triangles'])\nprint(c['area'])",
"d = {'A':[0,0], 'B':[4,0], 'C':[1,3], 'D':[6,3]}\ntry:\n    make_certificate(d)\nexcept ValueError as e:\n    print('拒绝非平行四边形:', str(e))\nelse:\n    raise RuntimeError('unexpected acceptance')",
"n = 0\nfor d in positives():\n    if not verify_certificate(d, make_certificate(d)):\n        raise RuntimeError('failed')\n    n += 1\nprint('精确正例:', n)\nm = 0\nfor d in negatives():\n    try:\n        make_certificate(d)\n    except ValueError:\n        m += 1\n    else:\n        raise RuntimeError('negative accepted')\nprint('直接拒绝负例:', m)",
"import copy\nbad = copy.deepcopy(c)\nbad['area']['ABC'] = True\nprint('布尔替换通过:', verify_certificate(EXAMPLE, bad))\nshifted = {k:[v[0]+2,v[1]-1] for k,v in EXAMPLE.items()}\nprint('旧证书移绑通过:', verify_certificate(shifted, c))\nprint('有限运行不代替一般证明；此Notebook为compile/exec执行，非kernel。')"
]
texts=['# I.34 精确教学核验\n\n边界顺序A-C-D-B，对角线BC。以下六格由标准库compile/exec实跑，不是Jupyter内核复现。',
'## 1 前提与长度\n坐标是现代欧氏模型，并不认证古代尺规操作。',
'## 2 角\n角用归一化(点积,绝对叉积)保存，避免浮点近似。',
'## 3 分割\n检查两三角形对应边、对角线异侧及面积。',
'## 4 反例\n只保留一对平行仍不足。',
'## 5 有限样例族\n正例并非覆盖所有实数坐标；负例直接检查几何入口。',
'## 6 证书攻击\n布尔不是数值证书，平移后的输入需新证书。']
cells=[{'cell_type':'markdown','metadata':{},'source':texts[0].splitlines(True)}];ns={}
for i,code in enumerate(codes,1):
 cells.append({'cell_type':'markdown','metadata':{},'source':texts[i].splitlines(True)})
 out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(code,'cell-'+str(i),'exec'),ns)
 cells.append({'cell_type':'code','metadata':{},'execution_count':i,'source':code.splitlines(True),'outputs':[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(True)}]})
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'execution_method':'stdlib compile/exec, not kernel','scaffold_note':'skill helper absent; standard-library builder used'},'cells':cells}
open('teaching.zh-CN.ipynb','w').write(json.dumps(nb,ensure_ascii=False,indent=2)+'\n');print('Executed 6 code cells using compile/exec, not kernel')
