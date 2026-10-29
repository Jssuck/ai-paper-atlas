"""Create original teaching cells in standard nbformat 4 structure."""
import json
from pathlib import Path
cells=[]
def md(s): cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s): cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(True),'execution_count':None,'outputs':[]})
md('# Euclid III.3：平分与垂直，条件不能省\n\n本目录中运行。原证正向用I.8及直角定义，逆向用I.5/I.26。本Notebook独立采用现代有理坐标，不冒充古代证明或一般尺规系统。E是圆心，A、B为不同圆周点且AB非直径；F严格在弦内。')
code('from fractions import Fraction as Q\nfrom geometry import certificate,verify_certificate,perpendicular,grid\nc=certificate((0,0),25,(-3,4),(3,4),(0,4))\nprint(c["branch"],"AF2",c["AF_squared"],"BF2",c["BF_squared"],"dot",c["dot_EF_AB"])')
md('## 1 等价的数值证书\n由等半径展开，AF²−BF²=2 EF·AB。非零方向下，点积为零认证垂直；距离非负使平方相等可推出距离相等。原文证明仍应单独阅读。')
code('c=certificate((0,0),25,(-3,4),(3,4),(1,4))\nprint("bisects",c["bisects"],"perpendicular",c["perpendicular"])\nprint("identity",c["AF_squared"]-c["BF_squared"],2*c["dot_EF_AB"],"verified",verify_certificate(c))')
md('## 2 直径反例\nA=(-5,0)、B=(5,0)的中点就是圆心。方向(1,1)的中心线平分这条弦，却不垂直。不能拿EF=0与任何向量点积都为零去制造直角。')
code('print("diagonal versus diameter perpendicular",perpendicular((1,1),(10,0)))\ntry: perpendicular((0,0),(10,0))\nexcept ValueError as e: print(type(e).__name__,str(e))')
md('## 3 不过圆心也不够\n圆心(0,0)、半径5，弦从(-3,4)到(3,4)。垂线x=1在F=(1,4)相交，但AF=4、FB=2；它不经过圆心，不能套用III.3。')
code('print("off-center vertical perpendicular",perpendicular((0,1),(6,0)))\nprint("AF2",Q(16),"BF2",Q(4),"equal",Q(16)==Q(4))')
md('## 4 有限测试与伪证书\n网格含中点和非中点，不仅验证前提为真的案例。严格字段类型拒绝True与1互换。')
code('rows=list(grid())\nprint("grid",len(rows),"midpoints",sum(x["bisects"] for x in rows),"verified",all(verify_certificate(x) for x in rows))\nbad=dict(rows[0]);bad["equivalent"]=1\nprint("integer-as-bool accepted",verify_certificate(bad))')
md('## 练习及答案\n1. F=(-3/2,4)时？AF²=9/4，BF²=81/4，点积=-9，两边差=-18=2(-9)，既非平分也非垂直。\n2. 若AB为直径，逆向垂直是否仍平分？是，但本命题双向整体规格排除直径，程序不借此声称扩展支持。\n3. 为何EF非零？若F=E且F在AB上，AB经过圆心，与非直径条件冲突。\n\nNotebook使用标准库compile/exec顺序执行并保存输出，不是Jupyter kernel；内核集成未测。有限有理案例不能替代一般实数几何证明。')
for i,c in enumerate(cells): c['id']=f'iii3-{i+1:02}'
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'}},'cells':cells}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Created 5 code cells using the Python standard library.')
