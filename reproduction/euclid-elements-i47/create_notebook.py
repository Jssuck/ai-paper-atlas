"""Create and actually execute a self-contained five-cell teaching notebook."""
import json,io,contextlib
cells=[('markdown','# I.47：从局部全等到两块等积\n现代有理坐标教学模型；不是尺规模拟，也不是对一般定理的有限证明。以下保存的输出由标准库compile/exec真实生成，未启动Jupyter kernel。'),('code','from geometry import construct, verify, report, area\nfrom fractions import Fraction\nargs = ((0,0),(3,0),(0,4))\nc = construct(*args)\nprint("certificate valid:", verify(*args,c))'),('markdown','## 两对三角形\n原证I.4的三角形为ABD/FBC与ACE/KCB；现代程序以精确边长平方、夹角点积及行列式面积核查。'),('code','r = report(c)\nfor name in ["ABD","FBC","ACE","KCB"]: print(name,r[name])'),('markdown','## I.41的两次倍积与矩形分割\n输入只要求非零垂直两边；没有输入斜边长度或勾股关系。'),('code','for name in ["left_rectangle","AB_square","right_rectangle","AC_square","BC_square"]: print(name,r[name])'),('markdown','## 不需要整数勾股三元组\n等腰直角三角形仍有全部有理顶点坐标，无需取斜边长度的平方根。'),('code','q = construct((0,0),(1,0),(0,1))\nprint("unit right triangle:", verify((0,0),(1,0),(0,1),q))\nprint(report(q))'),('markdown','## 反例与范围\n非直角输入在构造入口直接拒绝；这不同于先假定所证结论。'),('code','try:\n    construct((0,0),(1,0),(1,1))\nexcept ValueError as e:\n    print("rejected:",e)\nprint("Finite tests do not prove the theorem.")')]
ns={};out=[];count=0
for i,(kind,src) in enumerate(cells):
    cell={'cell_type':kind,'id':f'i47-{i}','metadata':{},'source':src.splitlines(True)}
    if kind=='code':
        count+=1;b=io.StringIO()
        with contextlib.redirect_stdout(b):exec(compile(src,'notebook-cell','exec'),ns)
        cell.update(execution_count=count,outputs=[{'output_type':'stream','name':'stdout','text':b.getvalue().splitlines(True)}])
    out.append(cell)
nb={'cells':out,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'execution_note':'Executed using standard-library compile/exec, not a Jupyter kernel.'},'nbformat':4,'nbformat_minor':5}
open('teaching.zh-CN.ipynb','w').write(json.dumps(nb,ensure_ascii=False,indent=2)+'\n');print('Executed and saved',count,'code cells; no Jupyter kernel.')
