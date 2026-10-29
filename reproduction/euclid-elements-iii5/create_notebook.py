"""Small standard-library notebook scaffold; execution is separate."""
import json
from pathlib import Path
cells=[]
def md(s):cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s):cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(True),'execution_count':None,'outputs':[]})
md('# III.5：同心与公共点\n标准库精确教学重构；下面保存的是compile/exec的stdout，不是Jupyter内核输出，execution_count保持null。有限案例不代替一般证明。')
code("from geometry import certificate, circle_relation, verify, EXAMPLES, grid\nc = certificate(*EXAMPLES['crossing_upper'])\nprint(c['classification'], c['center_distance_squared'])\n")
md('一个公共点不区分相切与相交。')
code("for name in ('crossing_lower','external_tangent','internal_tangent'):\n    c = certificate(*EXAMPLES[name])\n    print(name, c['classification'], c['linear_lhs'], c['linear_rhs'])\n")
md('重合圆有公共点且同心，说明必须保留两圆互异条件。')
code("c = certificate(*EXAMPLES['coincident'])\nprint(c['classification'], c['same_center'], c['distinct_circles'])\nprint(circle_relation((0,0),25,(0,0),9))\nprint(circle_relation((0,0),1,(5,0),1))\n")
md('验证器区分布尔值与数值；改动未获证据支持的分类会被拒绝。')
code("c = certificate(*EXAMPLES['crossing_upper'])\nprint('original', verify(c))\nc['same_center'] = 0\nprint('bool replaced by integer', verify(c))\n")
md('有限变换网格只检查实现。负尺度是中心缩放，单坐标变号才是这里的镜像。')
code("count = sum(verify(certificate(*a)) for a in grid())\nprint('verified finite configurations', count)\n")
nb={'nbformat':4,'nbformat_minor':4,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},'cells':cells}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('created five code cells; execution_count null')
