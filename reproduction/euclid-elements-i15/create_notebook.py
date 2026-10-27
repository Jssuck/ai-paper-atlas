"""Build an original tutorial; skill helper unavailable in this executor."""
import json
from pathlib import Path
cells=[]
def md(s): cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(keepends=True)})
def code(s): cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(keepends=True),'execution_count':None,'outputs':[]})
md('# I.15：对顶角的两层证据\n\n本Notebook是原创教学重构。代码按标准库compile/exec真实顺序执行，不是Jupyter kernel。有限输入不能替代一般证明。')
md('## 1. 输入契约\nE位于AB和CD之间；两条支撑直线不同。坐标只收整数或有理数字符串，拒绝布尔与浮点。')
code("from geometry import certificate, verify, angle_ledger\nfrom cases import positives, run\nfrom copy import deepcopy\ndata = next(positives())\nprint(data)\n")
md('## 2. 检查反向比例\n生成证书先检查两组反向射线和非零行列式，不把结论当作输入。')
code("claim = certificate(data)\nprint('opposite scales:', claim['opposite_scales'])\nprint('cross:', claim['cross_AE_CE'])\nprint('verified:', verify(data, claim))\n")
md('## 3. 不使用acos的角描述\n点积与行列式绝对值经共同L1归一化给出普通角方向描述；这不是角度数值。')
code("print('CEA, AED, DEB, BEC:')\nprint(claim['angles_CEA_AED_DEB_BEC'])\nprint('vertical pairs:', claim['vertical_pairs_equal'])\n")
md('## 4. 原证加法结构的单独重构\n以一直角为1，x+y=2和y+z=2同减y。此模型不声称从坐标求出分数角度。')
code("print(angle_ledger('2/3', '4/3', '2/3'))\n")
md('## 5. 证书不能接受真假值与整数混淆\nPython一般相等会把True当作1；本核验器使用严格JSON结构。')
code("bad = deepcopy(claim)\nbad['schema_version'] = True\nprint('bool substituted for integer accepted:', verify(data, bad))\nbad = deepcopy(claim)\nbad['vertical_pairs_equal'][0] = 1\nprint('integer substituted for bool accepted:', verify(data, bad))\n")
md('## 6. 有限回归与边界\n包含平移、有理坐标、不同反向比例及退化输入。数量只是实际覆盖，不是所有几何配置。')
code("print(run())\n")
nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'scaffold_note':'Installed skill read; helper file unavailable, original JSON tutorial built with standard library.'},'nbformat':4,'nbformat_minor':5}
for i,c in enumerate(cells): c['id']='i15-cell-'+str(i)
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('Created six-code-cell tutorial; outputs not yet executed.')
