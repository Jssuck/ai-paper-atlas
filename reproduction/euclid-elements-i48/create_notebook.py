"""Generate and execute an original five-cell teaching notebook without a kernel."""
import json,io,contextlib
cells=[('markdown','# I.48：逆命题需要新证明\n现代有理坐标教学模型，不是公理化证明。保存输出由标准库compile/exec真实生成，未启动Jupyter kernel。'),('code','from geometry import construct, verify, report, rational_sqrt\nfrom fractions import Fraction as Q\na = ((0,0),(3,0),(0,4))\np = construct(*a)\nprint("certificate valid:",verify(*a,p))'),('markdown','## 比较三角形\nD在AC垂线的另一侧，AD等于AB；不从BAC已直角开始。'),('code','r=report(p)\nprint("D =",r["D"])\nfor k in ["AB_squared","AD_squared","AC_squared"]:print(k,r[k])'),('markdown','## 从I.47到I.8\n比较DC与BC平方，再使用SSS数据。坐标模型中的点积用于证书检查和结果展示，而非construct入口条件。'),('code','for k in ["DC_squared","BC_squared","DAC_dot","BAC_dot"]:print(k,r[k])'),('markdown','## 不限水平或整数边长\n有理点的长度可能无理，但长度之比可为有理。'),('code','b=((2,3),(4,4),(0,7))\nq=construct(*b)\nprint(verify(*b,q))\nprint(report(q))'),('markdown','## 接近直角不等于满足精确前提\n微小扰动在入口拒绝；有限测试不替代综合几何证明。'),('code','try:\n    construct((0,0),(1,0),(Q(1,10**20),1))\nexcept ValueError as e:\n    print("rejected:",e)\nprint("Finite tests do not prove the theorem.")')]
ns={};out=[];n=0
for i,(kind,src) in enumerate(cells):
    c={'cell_type':kind,'id':f'i48-{i}','metadata':{},'source':src.splitlines(True)}
    if kind=='code':
        n+=1;b=io.StringIO()
        with contextlib.redirect_stdout(b):exec(compile(src,'notebook-cell','exec'),ns)
        c.update(execution_count=n,outputs=[{'output_type':'stream','name':'stdout','text':b.getvalue().splitlines(True)}])
    out.append(c)
nb={'cells':out,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'execution_note':'Executed with standard-library compile/exec, not Jupyter kernel.'},'nbformat':4,'nbformat_minor':5}
open('teaching.zh-CN.ipynb','w').write(json.dumps(nb,ensure_ascii=False,indent=2)+'\n');print('Executed and saved',n,'code cells; no Jupyter kernel.')
