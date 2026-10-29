"""Generate the original teaching notebook using the Python standard library."""
import json
from pathlib import Path
cells=[]
def md(s): cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s): cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(True),'execution_count':None,'outputs':[]})
md('# Euclid III.2：弦的内点为何严格在圆内\n\n在本目录运行。原文通过等腰底角、外角与大角对大边归谬（I.5、I.16、I.19）；本 Notebook 是另列的现代有理坐标教学重构，不冒充原证或自动证明器。圆心与正半径平方已经给定。')
code('from fractions import Fraction as Q\nfrom geometry import certificate, verify_certificate\nr=certificate((0,0),25,(-3,4),(3,4),Q(1,2))\nprint("E =",r["E"],"distance squared =",r["distance_squared"],"gap =",r["gap"])')
md('## 1. 恒等式到严格性\n半径平方减去内点距离平方等于 t(1-t) 乘弦长平方。端点互异及 0<t<1 缺一不可。这里的圆内是距离平方小于半径平方。')
code('print("identity:",r["distance_squared"]+r["gap"]==r["radius_squared"])\nprint("strict gap:",r["gap"]>0,"verified:",verify_certificate(r))')
md('## 2. 直径的中点\n当 E 恰为圆心，原来的角图会退化。距离平方方法仍有定义，得到零距离和正间隙。应在文字证明单列此分支，而非给零射线命名角。')
code('d=certificate((0,0),25,(-5,0),(5,0),Q(1,2))\nprint("branch =",d["branch"],"distance squared =",d["distance_squared"],"gap =",d["gap"])')
md('## 3. 端点不是严格内点\n闭弦包含圆周端点，只有开弦严格在内。把端点参数误说为 0<t<1 会使“全部点严格在内”成为假命题。')
code('for t in (0,1):\n    e=certificate((0,0),25,(-3,4),(3,4),t)\n    print("t =",t,"branch =",e["branch"],"gap =",e["gap"])')
md('## 4. 输入与伪证书\n接口拒绝外插参数、重合端点和非精确类型。不能靠把浮点负误差截为零来认证严格性。证书所有字段都重新计算。')
code('bad=dict(r);bad["gap"]=Q(0)\nprint("forged gap accepted:",verify_certificate(bad))\nfor t in (2,True):\n    try: certificate((0,0),25,(-3,4),(3,4),t)\n    except (ValueError,TypeError) as e: print(type(e).__name__,str(e))')
md('## 练习与答案\n1. 四分点距离平方？取 t=1/4，E=(-3/2,4)，距离平方73/4，间隙27/4。\n2. A=B时为何不能得严格内点？弦长平方为0，恒等式右侧为0。接口拒绝此输入。\n3. 外插是否仍在圆内？对单位圆的直径端点(-1,0),(1,0)，t=2得到(3,0)，在外部。\n\n本文件由标准库 compile/exec 顺序执行保存输出，非 Jupyter kernel；未测试内核集成。由随附 create_notebook.py 生成教学内容，无额外依赖。有限有理案例不是一般证明，也不穷尽所有实数点。')
for i,c in enumerate(cells): c['id']=f'iii2-{i+1:02}'
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'}},'cells':cells}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Created 5 code cells using the Python standard library.')
