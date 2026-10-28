"""Original stdlib scaffold: installed skill read, local helper absent. Not kernel."""
import json,io,contextlib
texts=['# I.40：等底等积与平行\n\n有理坐标教学模型，非原文合成证明。原文 ABC/DCE、辅助 F；本模型推广为 ABC/DEF、辅助 G，把原 C 拆为底端点 C 和 E。有限实验不证明一般定理。',
'## 1 规范输入与结论\n六点模型两底可分离、交叠、共端或重合，必须等长且共线。',
'## 2 辅助交点\nG=E+t(D−E)；内外两例故意不等积，仅演示反证所比较的整体与真部分。',
'## 3 合法边界与非法输入\nA=D 时 AD 不定义；同一平行线存在，但不能冒称由两重合点定义了直线。',
'## 4 证书严格绑定\n不是只核零行列式：所有原始坐标和重算字段都绑定。',
'## 5 有限批量核验\n实际执行方式为标准库 compile/exec、非 Jupyter kernel；不代表形式化证明。']
codes=[
"from geometry import make_certificate, verify_certificate, construction_trace\nfrom cases import EXAMPLE, build, positives, negatives\nc=make_certificate(EXAMPLE)\nprint(c['trace']['input'])\nprint(c['conclusion'])\nprint(c['trace']['double_area'])",
"for k in [4,1,2]:\n    t=construction_trace(build(k=k))\n    print(t['branch'], 't='+t['t'], 'G=',t['G'], t['double_area'])\n    print('whole/part:',t['whole'],t['part'])",
"print(make_certificate(build(d=1))['conclusion'])\nfor label,data in negatives():\n    try:make_certificate(data)\n    except ValueError as e:print(label,':',str(e))\n    else:raise RuntimeError('invalid geometry accepted')",
"import copy\nbad=copy.deepcopy(c);bad['trace']['cross']['BC_AD']=True\nprint('布尔篡改通过:',verify_certificate(EXAMPLE,bad))\nprint('同面积移绑通过:',verify_certificate(build(a=2),c))\nprint('原证书通过:',verify_certificate(EXAMPLE,c))",
"count=0\nfor data in positives():\n    if not verify_certificate(data,make_certificate(data)):raise RuntimeError('verification failed')\n    count+=1\nprint('有限合法例:',count)\nprint('有限实跑不证明一般定理；标准库 compile/exec 非 kernel。')"]
cells=[{'cell_type':'markdown','id':'intro','metadata':{},'source':texts[0].splitlines(True)}];ns={}
for i,code in enumerate(codes,1):
    cells.append({'cell_type':'markdown','id':'text-'+str(i),'metadata':{},'source':texts[i].splitlines(True)})
    out=io.StringIO()
    with contextlib.redirect_stdout(out):exec(compile(code,'cell-'+str(i),'exec'),ns)
    cells.append({'cell_type':'code','id':'code-'+str(i),'metadata':{},'execution_count':i,'source':code.splitlines(True),'outputs':[{'output_type':'stream','name':'stdout','text':out.getvalue().splitlines(True)}]})
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'execution_method':'standard-library compile/exec, not kernel','scaffold_note':'Installed notebook skill read; local new_notebook.py not installed; original standard-library builder used without installation.'},'cells':cells}
open('teaching.zh-CN.ipynb','w').write(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('Executed 5 code cells using standard-library compile/exec, not kernel')
