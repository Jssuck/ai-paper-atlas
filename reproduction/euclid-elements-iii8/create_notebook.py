"""Local nbformat 4 scaffold: installed skill helper was unavailable; no installs."""
import json
from pathlib import Path
cells=[]
def md(s):cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s):cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(True),'execution_count':None,'outputs':[]})
md('# III.8：外点到圆周的两条距离分支\n原创有理坐标教学实验，非原典证明器。输出以标准库compile/exec实际运行并重放，非Jupyter kernel；execution_count保留null。')
code("from fractions import Fraction as F\nfrom geometry import *\nc=certificate(5,13,(3,4))\nprint('distance squared',c['squared_distance'])\nprint('bounds',c['minimum_squared'],c['maximum_squared'])\nprint('branch',c['branch'])\n")
md('暴露近弧不是朝向外点的整个半圆；阈值为dx=r²。')
code("for r,d,p in [(5,6,(3,4)),(3,5,(F(9,5),F(12,5)))]:\n    c=certificate(r,d,p)\n    print('point',p,'branch',c['branch'],'horizon',c['horizon'])\n")
md('同一视线可以命中两个不同长度的点，因此不能把视角作为全半圆的一一排序。')
code("s=secant(5,13,(3,4))\nprint('parameters',s['parameters'])\nprint('points',s['points'])\nprint('squared lengths',s['squared_lengths'])\nprint('squared product',s['squared_lengths'][0]*s['squared_lengths'][1])\n")
md('等长点是轴镜像；最短与最长端点只有一个，不得声称所有长度都恰有两个点。')
code("for value in (63,64,116,324,325):\n    print(value,equal_shell(5,13,value))\n")
md('有限样本检查只能发现实现或示例错误，不能替代几何的一般证明。')
code("from run_examples import report\nr=report()\nprint('finite configurations',r['finite_configurations'])\nprint('branch comparisons',r['adjacent_branch_comparisons'])\nfor d in (0,2,5):\n    try: certificate(5,d,(3,4))\n    except ValueError as e: print('rejected',d,str(e))\n")
nb={'nbformat':4,'nbformat_minor':4,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},'cells':cells}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n');print('local scaffold: five code cells; execution_count null; skill helper unavailable')
