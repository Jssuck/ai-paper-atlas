"""Tutorial follows nbformat 4 structure; standard library only."""
import json
from pathlib import Path
cells=[]
def md(s):cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s):cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(True),'execution_count':None,'outputs':[]})
md('# III.7：从偏心内点到圆周的距离\n现代有理坐标教学重构，非原典证明器。保存输出来自标准库compile/exec，不是Jupyter kernel。')
code("from geometry import *\nc=certificate(*EXAMPLES['simple'])\nprint(c['interior_point'],c['nearest'],c['farthest'])\nprint(c['minimum_squared'],c['distance_squared'],c['maximum_squared'])\n")
md('镜像点具有相同距离；有限测试不证明一般恰两点结论。')
code("print(c['mirror'],c['mirror_distance_squared'])\nprint(c['above_minimum'],c['below_maximum'])\n")
md('在同一开半圆，向近端的轴投影增加，距离平方严格减少。')
code("print(compare((0,0),5,2,(1,0),(-3,4),(3,4)))\n")
md('圆心、圆周端点与外点不在内点非圆心域。')
code("for d in (0,5,6):\n    try: certificate((0,0),5,d,(1,0),(3,4))\n    except ValueError as e: print(d,str(e))\n")
md('504个有限有理构形与类型敏感证书核查。')
code("print('finite configurations',sum(verify(certificate(*a)) for a in grid()))\nc['distinct_mirror']=1\nprint('integer pretending to be boolean',verify(c))\n")
nb={'nbformat':4,'nbformat_minor':4,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},'cells':cells}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n');print('created five code cells; execution_count null')
