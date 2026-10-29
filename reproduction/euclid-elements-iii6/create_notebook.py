"""Five-cell tutorial scaffold, using the standard nbformat structure."""
import json
from pathlib import Path
cells=[]
def md(s):cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s):cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(True),'execution_count':None,'outputs':[]})
md('# III.6：相切不共心\n现代有理坐标教学重构。保存输出来自标准库compile/exec，非Jupyter内核；execution_count保留null。有限实跑不是一般证明。')
code("from geometry import *\nc = certificate(*EXAMPLES['external'])\nprint(c['classification'], c['contact'], c['center_distance_squared'])\n")
md('内切及交换两圆次序，接触点保持相同。')
code("for key in ('internal','internal_swapped','oblique_external','oblique_internal'):\n    c = certificate(*EXAMPLES[key])\n    print(key, c['contact'], verify(c))\n")
md('重合圆不是相切；公共点也不能单独证明相切。')
code("print(relation((0,0),2,(0,0),2))\nprint(relation((0,0),2,(0,0),3))\nprint(relation((0,0),5,(6,0),5))\ntry:\n    certificate((0,0),5,(6,0),5)\nexcept ValueError as e:\n    print(str(e))\n")
md('根轴方程及接触点半径验证。unique_contact依赖文档中的一般恒等式推导，不是枚举穷尽点集。')
code("c = certificate(*EXAMPLES['internal'])\nprint(c['radical_normal'], c['radical_offset'])\nprint(c['contact_distance1_squared'], c['contact_distance2_squared'])\n")
md('核验有限变换网格和类型敏感的防篡改检查。')
code("print('finite configurations',sum(verify(certificate(*a)) for a in grid()))\nc=certificate(*EXAMPLES['external'])\nc['unique_contact']=1\nprint('integer pretending to be boolean',verify(c))\n")
nb={'nbformat':4,'nbformat_minor':4,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},'cells':cells}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('created five code cells; execution_count null')
