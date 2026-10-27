"""Focused tutorial; installed skill's scaffold helper is unavailable locally."""
import json
from pathlib import Path
cells=[]
def md(t):cells.append({'cell_type':'markdown','metadata':{},'source':t.splitlines(keepends=True)})
def code(t):cells.append({'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':t.splitlines(keepends=True)})
md('# I.16：辅助中点、内射线与严格外角不等式\n原创教学重构。有限运行不替代一般证明；输出由标准库 compile/exec 顺序执行，不是 Jupyter kernel。')
code("from geometry import construct, verify\nfrom cases import run_cases\np={'A':[1,2],'B':[0,0],'C':[3,0],'D':[5,0]}\nc=construct(p)\nprint(c['points'])")
md('## 首个内对角\nE 是 AC 中点，F=A+C−B。CF=CA+3CD/2，因此 CF 严格在外角 ACD 内。原证 SAS 与坐标检查属于不同论证层。')
code("print(c['coefficients']['CF_in_CA_CD'])\nprint({k:v for k,v in c['checks'].items() if k in ('AE_equals_EC','BE_equals_EF','vertical_at_E','BAC_equals_ECF','CF_inside_ACD')})")
md('## 第二个内对角\nM 是 BC 中点，N=B+C−A，G=2C−A。CN=CB+CG，先证 BCG 大于 ABC，再用对顶角转回 ACD。')
code("print({k:v for k,v in c['checks'].items() if k in ('BM_equals_MC','AM_equals_MN','vertical_at_M','ABC_equals_MCN','CN_inside_BCG','BCG_equals_ACD')})")
md('## 输入绑定和严格类型\nPython 的 True==1 不能让布尔模式号冒充整数模式号。')
code("import copy\nbad=copy.deepcopy(c);bad['schema']=True\nprint('original:',verify(p,c),'bool schema:',verify(p,bad),'changed input:',verify(dict(p,D=[6,0]),c))")
md('## 方向不是图像印象\nD 必须在 BC 越过 C 的延长线上；重合、回退、离线全部拒绝。')
code("for d in ([3,0],[2,0],[5,1]):\n    try: construct(dict(p,D=d))\n    except ValueError as e: print(d,str(e))")
md('## 有限覆盖与范围\n有理平面坐标不是球面几何，也不是机器认证的一般几何公理证明。')
code("print(run_cases())\nprint(c['conclusions'])")
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'scaffold':'manual schema; installed skill helper absent'},'cells':cells}
for i,c in enumerate(cells):c['id']=f'i16-cell-{i:02d}'
Path(__file__).with_name('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('Created 6 code cells; not yet executed.')
