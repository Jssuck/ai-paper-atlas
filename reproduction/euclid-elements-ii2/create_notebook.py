"""Original nbformat 4.5 fallback; installed skill helper was unavailable.
Run in a fresh namespace with compile/exec; this does not start a Jupyter kernel.
"""
import json,io,contextlib
sections=[('1. 按原文点名构造正方形和切点','from fractions import Fraction as Q\nfrom geometry import construct, verify, summary\na=((0,0),(6,0),(0,6),Q(1,3))\nc=construct(*a)\nprint(c["points"])'),('2. 区域证书与鞋带面积','print(verify(*a,c))\nprint(summary(*a))'),('3. 旋转和反射不改变结论','print(summary((1,2),(4,6),(-3,5),Q(2,5)))\nprint(summary((1,2),(4,6),(5,-1),Q(2,5)))'),('4. 面积相等不能代替区域绑定','b=((0,0),(6,0),(0,6),Q(1,2))\nbad=construct(*b)\nbad["AF"],bad["CE"]=bad["CE"],bad["AF"]\nprint(verify(*b,bad))\nprint("segment squares:",2**2+4**2,"whole square:",6**2)'),('5. 原文内点模型拒绝退化和外切','for t in [0,1,Q(3,2),True,0.5]:\n    try: construct((0,0),(6,0),(0,6),t)\n    except ValueError as e: print(type(e).__name__+": "+str(e))')]
cells=[{'cell_type':'markdown','id':'intro','metadata':{},'source':['# II.2：整线与两段的矩形\n','目标：区分区域分割、面积数值与原文几何证明。点序为 A-D-E-B；AF 表示 A-D-F-C 区域，CE 表示 C-F-E-B 区域。\n','五格代码采用标准库 compile/exec 真运行并保存输出，未启动 kernel。有限有理坐标检查不能证明一般命题；不能据此声称复现整部《原本》。']}];ns={}
for i,(title,src) in enumerate(sections,1):
    cells.append({'cell_type':'markdown','id':f'm{i}','metadata':{},'source':[title]})
    b=io.StringIO()
    with contextlib.redirect_stdout(b):exec(compile(src,'teaching-cell','exec'),ns)
    cells.append({'cell_type':'code','id':f'c{i}','metadata':{},'execution_count':None,'source':src.splitlines(True),'outputs':[{'output_type':'stream','name':'stdout','text':b.getvalue().splitlines(True)}]})
nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},'nbformat':4,'nbformat_minor':5}
open('teaching.zh-CN.ipynb','w').write(json.dumps(nb,ensure_ascii=False,indent=2)+'\n');print('Executed 5 code cells using compile/exec; no Jupyter kernel started.')
