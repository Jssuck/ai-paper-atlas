"""Create a minimal tutorial; execute code with stdlib, not a Jupyter kernel."""
import json,io,contextlib
from pathlib import Path
cells=[]
def md(s): cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s): cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(True),'execution_count':None,'outputs':[]})
md('# Euclid II.3：整体乘所选分段\n\n先核查所选分段CB上的正方形，再检查其向A延出的矩形。原创精确有理数教学；不是一般证明或原尺规过程的完整复现。')
code('from fractions import Fraction as Q\nfrom geometry import construct, verify, summary, area\nA=(0,0); u=(6,0); v=(0,4); t=Q(1,3)\nprint(summary(A,u,v,t))')
md('## 点名与区域\nAE为整体矩形；AD为左矩形；CE（亦可称DB）为右侧正方形。')
code("certificate=construct(A,u,v,t)\nprint({k:tuple(map(str,p)) for k,p in certificate['points'].items()})\nprint('accepted:',verify(A,u,v,t,certificate))")
md('## 旋转与反射不改变判据\n下一例AB=5、AC=2、CB=3，面积15=6+9。')
code("print(summary((1,-2),(3,4),(-Q(12,5),Q(9,5)),Q(2,5)))\nprint(summary((0,0),(6,0),(0,-4),Q(1,3)))")
md('## 总面积相等仍可能是假图\n把左块平移后面积未变，但它已不与右块准确拼合。')
code("import copy\nbad=copy.deepcopy(certificate)\nbad['AD']=tuple((x+1,y) for x,y in bad['AD'])\nprint('area equality:',area(bad['AE'])==area(bad['AD'])+area(bad['CE']))\nprint('certificate accepted:',verify(A,u,v,t,bad))")
md('## 不可混用II.2的整体正方形\n把高设为AB=6不符合本篇CB=4的正方形。')
code("try:\n    construct(A,u,(0,6),t)\nexcept ValueError as error:\n    print('rejected:',error)\nprint('Finite cases do not prove the general theorem.')")
ns={};outputs=[]
for cell in cells:
    if cell['cell_type']!='code':continue
    out=io.StringIO()
    with contextlib.redirect_stdout(out): exec(compile(''.join(cell['source']),'notebook-cell','exec'),ns)
    text=out.getvalue();cell['outputs']=[{'output_type':'stream','name':'stdout','text':text.splitlines(True)}];outputs.append(text);print(text,end='')
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.12'},'execution_method':'stdlib compile/exec, not a kernel'},'cells':cells}
for i,c in enumerate(cells):c['id']='ii3-cell-'+str(i)
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('code_cells_executed=5; kernel_started=false; execution_count=null')
