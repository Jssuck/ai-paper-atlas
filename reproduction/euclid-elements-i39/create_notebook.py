"""Original stdlib scaffold; installed skill helper unavailable. Not a kernel run."""
import json,io,contextlib
texts=['# I.39：从等积回到平行\n\n现代有理坐标教学，有限样本不证明一般定理。原文依靠 I.31、I.37 与整体大于部分，而非行列式公式。',
'## 1 输入与结论\nB,C 是共同底的端点，A,D 是同侧且不同的顶点。',
'## 2 辅助交点的三个位置\nE 在射线 BD 上，t 为两有向面积之比；t<1 为内部，t>1 为延长，t=1 则 E=D。非等积两例仅展示反证所比较的整体和部分，不是假装满足定理。',
'## 3 方向、同侧与退化\n同侧不可删除；异侧等积也不能得到 AD 平行。A=D 不定义 AD，直接拒绝。',
'## 4 严格绑定而非仅比较面积\n所有原始坐标规范化后参与证书重算；整数与等价规范字符串表示同一点。',
'## 5 有限批量核验\n这是普通 Python compile/exec 的实际记录，不是 Jupyter kernel 执行或形式化证明。']
codes=[
"from geometry import make_certificate, verify_certificate, construction_trace\nfrom cases import EXAMPLE, build, positives, negatives\nc=make_certificate(EXAMPLE)\nprint(c['trace']['input'])\nprint(c['conclusion'])\nprint(c['trace']['area'])",
"for k in [4,1,2]:\n    t=construction_trace(build(k=k))\n    print(t['branch'], 't='+t['t'], 'E=',t['E'], t['area'])\n    print('whole/part:',t['whole'],t['part'])",
"for label,data in negatives():\n    try:make_certificate(data)\n    except ValueError as e:print(label,':',str(e))\n    else:raise RuntimeError('invalid geometry accepted')\nprint('反射后同侧:',make_certificate(build(h=-2))['conclusion'])",
"import copy\nbad=copy.deepcopy(c);bad['trace']['cross']['BC_AD']=True\nprint('布尔篡改通过:',verify_certificate(EXAMPLE,bad))\nprint('同面积移绑通过:',verify_certificate(build(a=2),c))\nprint('原证书通过:',verify_certificate(EXAMPLE,c))",
"count=0\nfor data in positives():\n    if not verify_certificate(data,make_certificate(data)):raise RuntimeError('verification failed')\n    count+=1\nprint('有限正例:',count)\nprint('有限实跑不证明一般定理；标准库 compile/exec 非 kernel。')"]
cells=[{'cell_type':'markdown','id':'intro','metadata':{},'source':texts[0].splitlines(True)}];ns={}
for i,code in enumerate(codes,1):
    cells.append({'cell_type':'markdown','id':'text-'+str(i),'metadata':{},'source':texts[i].splitlines(True)})
    out=io.StringIO()
    with contextlib.redirect_stdout(out):exec(compile(code,'cell-'+str(i),'exec'),ns)
    cells.append({'cell_type':'code','id':'code-'+str(i),'metadata':{},'execution_count':i,'source':code.splitlines(True),
                  'outputs':[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(True)}]})
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
'language_info':{'name':'python'},'execution_method':'standard-library compile/exec, not kernel',
'scaffold_note':'Installed skill read; local new_notebook.py absent and skill helper resource unavailable; original builder used.'},'cells':cells}
open('teaching.zh-CN.ipynb','w').write(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('Executed 5 code cells using standard-library compile/exec, not kernel')
