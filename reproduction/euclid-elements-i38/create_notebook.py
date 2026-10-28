"""Standard-library notebook builder. Helper unavailable; no kernel claim."""
import json,io,contextlib
codes=[
"from geometry import make_certificate, verify_certificate\nfrom cases import EXAMPLE, build, positives, negatives\nc=make_certificate(EXAMPLE)\nprint(c['input'])\nprint(c['area'])",
"print('G/H:',c['vertices'])\nprint('平行叉积:',c['parallel_checks'])\nprint('AB/DF二分:',c['halves'])",
"for s in [-2, '1/2', 0, 1, 3]:\n    r=make_certificate(build(s=s))\n    print('底平移',s,r['area'])\nprint('反向端点:',make_certificate(build(direction=-1))['signed_double_areas'])",
"for label,data in [('A=D',build(a=0,d=0)),('G=H',build(a=0,d=-2)),('B=F',build(s=-1))]:\n    print(label,make_certificate(data)['area'])\nfor data in negatives():\n    try: make_certificate(data)\n    except ValueError as e: print('拒绝:',str(e))\n    else: raise RuntimeError('非法几何被接受')",
"count=0\nfor data in positives():\n    if not verify_certificate(data,make_certificate(data)): raise RuntimeError('certificate failed')\n    count+=1\nprint('有限正例:',count)\nimport copy\nbad=copy.deepcopy(c);bad['area']['ABC']=True\nprint('布尔篡改通过:',verify_certificate(EXAMPLE,bad))\nprint('同面积移绑通过:',verify_certificate(build(a=1),c))\nprint('有限实跑不证明一般定理；标准库compile/exec非kernel。')"]
texts=['# I.38：等底而不必同底\n\n现代有理坐标教学；I.36整体等积和I.34二分是原证明依赖，不由这些有限例证明。',
'## 1 六点输入与同一对平行支持线',
'## 2 补成GBCA与DEFH\nG=A−(C−B)，H=D+(F−E)，分别由对角线AB和DF平分。',
'## 3 改变底的位置和方向\n等长不要求同端点、有向向量相同或互不相交。',
'## 4 标签重合不等于退化\n支持线本身为几何对象；不能用相同两标签确定一条新线。异侧等高虽可等积，却不满足本命题共同上支持线前提。',
'## 5 有限核验和完整输入绑定']
cells=[{'cell_type':'markdown','id':'intro','metadata':{},'source':texts[0].splitlines(True)}]
ns={}
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
