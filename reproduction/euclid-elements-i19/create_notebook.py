"""Build a small tutorial notebook using only the standard library.
The installed skill's scaffold helper is not exposed at the documented local path;
this explicit nbformat-4 builder supplies the required cells and metadata instead.
"""
import json
from pathlib import Path
cells=[]
def md(s):cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(keepends=True)})
def code(s):cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(keepends=True),'execution_count':None,'outputs':[]})
md('# I.19：三分排除不等于自动取逆命题\n本教学使用现代有理坐标与独立关系表；不是欧几里得形式化体系，也不是一般定理证明。实跑为标准库 compile/exec，而非 Jupyter kernel。')
md('## 1. 从独立角比较进入\n普通角的余切严格递减，dot/abs(cross) 可精确比较；不调用浮点反三角函数。')
code("from geometry import inspect_triangle, build_certificate, verify_certificate, infer_side\nfrom cases import positive_cases, invalid_cases\nfrom copy import deepcopy\nr=inspect_triangle([0,0],[3,0],[0,4])\nprint(r)")
md('## 2. 两个排除分支\n证书记录 I.5 与交换标签后的 I.18；坐标计算是另一路现代一致性核验，不证明这些历史依赖。')
code("certificate=build_certificate([0,0],[3,0],[0,4])\nprint(certificate['excluded'])\nprint(certificate['remaining'])\nprint(verify_certificate([0,0],[3,0],[0,4],certificate))")
md('## 3. 删除前提会怎样\n不可比较不是线段的通常关系，而是人为反模型，展示三分性角色。')
code("print('完整假设',infer_side(1))\nprint('删除全序',infer_side(1,total=False))\nprint('删除等长保等角',infer_side(1,equal_implies_equal=False))\nprint('删除反序保反角',infer_side(1,less_implies_less=False))")
md('## 4. 证书必须绑定输入和类型\nPython 中 True == 1；本检查器不把这种相等误认为JSON证书相同。')
code("bad=deepcopy(certificate)\nbad['schema']=True\nprint('布尔替换通过？',verify_certificate([0,0],[3,0],[0,4],bad))\nprint('换输入通过？',verify_certificate([0,0],[3,0],[0,5],certificate))")
md('## 5. 真正跑有限样例\n有限输入数量不是普遍定理证明。')
code("cases=positive_cases()\npassed=sum(verify_certificate(*case,build_certificate(*case)) for case in cases)\nprint({'positive_cases':len(cases),'passed':passed})\nif passed!=len(cases): raise RuntimeError('certificate failure')")
md('## 6. 拒绝退化和不满足题设的输入\n错误输入不被计为数学反例；现代抽象模型的反例另在第3步。')
code("rejected=0\nfor case in invalid_cases():\n    try: build_certificate(*case)\n    except ValueError: rejected+=1\nprint({'invalid_inputs':len(invalid_cases()),'rejected':rejected})\nif rejected!=len(invalid_cases()): raise RuntimeError('negative failure')")
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},'cells':cells}
for i,c in enumerate(cells):c['id']='i19-'+str(i)
Path(__file__).with_name('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'created':'teaching.zh-CN.ipynb','code_cells':6}))
