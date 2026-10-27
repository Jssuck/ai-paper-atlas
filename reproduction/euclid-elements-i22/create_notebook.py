"""Build the small tutorial notebook using the standard nbformat JSON structure.
Installed skill was read; its helper/template was not locally available.
"""
import json
from pathlib import Path

def md(s):return {'cell_type':'markdown','metadata':{},'source':s.splitlines(True)}
def code(s):return {'cell_type':'code','metadata':{},'source':s.splitlines(True),'outputs':[],'execution_count':None}
cells=[md('# I.22：三边如何构造两个镜像顶点\n这是原创坐标教学重构，不是古代原证的机器认证。以下六格用标准库 compile/exec 顺序执行，并非 Jupyter kernel。'),
code("from geometry import construct, verify, classify, Quad\nfrom fractions import Fraction as Q\nprint('exact rational inputs, one quadratic field')"),
md('## 1. 直角例\n三边分别为 FK=3、GK=4、FG=5；投影不是任意选择。'),
code("c = construct(3,4,5)\nprint(c['K'])\nprint(c['squared_distances'])"),
md('## 2. 非有理高度\n等边三角形的高度平方为3/4，不以浮点近似替代。'),
code("e = construct(1,1,1)\nprint(e['height_squared'])\nprint((Quad(0,1,Q(3,4))*Quad(0,1,Q(3,4))).rational_value())"),
md('## 3. 镜像而非唯一坐标\n固定基边，正负高度给两个顶点；两者边长相同。'),
code("print(construct(2,3,4,1)['K'])\nprint(construct(2,3,4,-1)['K'])"),
md('## 4. 严格条件不能换成非严格\n相切只给退化图形；分离与包含均无交点。'),
code("for lengths in [(1,1,2),(3,1,2),(1,1,3),(3,1,1),(2,3,4)]:\n    print(lengths, classify(*lengths))"),
md('## 5. 证书不是任意JSON\n输入、方向和类型必须完全绑定。有限测试不证明所有输入，也不证明古代公设已有圆交点存在性。'),
code("import copy\nprint(verify(c,3,4,5))\nt = copy.deepcopy(c); t['schema_version'] = True\nprint(verify(t,3,4,5))\nprint(verify(c,4,3,5))")]
nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'},'execution_method':'standard-library compile/exec, not a Jupyter kernel'},'nbformat':4,'nbformat_minor':5}
for i,cell in enumerate(cells):cell['id']=f'i22-{i:02d}'
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('created tutorial: six code cells')
