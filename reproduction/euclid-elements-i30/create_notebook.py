import json
from pathlib import Path
cells=[]
def md(s): cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s): cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(True),'execution_count':None,'outputs':[]})
md('# I.30：方向共线、位置分离与平行传递\n原创有理坐标教学模型，不是原文证明。标准库 compile/exec 执行，非 Jupyter kernel；有限例不证明一般定理。从本目录运行。')
code('from geometry import make_certificate, verify_certificate\nfrom cases import example, positives, negatives\nd = example()\nc = make_certificate(d)\nprint(c["scales"], c["distinctness_determinants"])')
md('两个比例可以异号。直线没有固定朝向，不应把负比例当作不平行。')
code('print(c["transversal"])\nprint(c["conclusion"])')
md('检查有限族，覆盖斜率、侧向、相反方向、旋转和平移。')
code('count = 0\nfor item in positives():\n    if not verify_certificate(item, make_certificate(item)): raise RuntimeError("failed")\n    count += 1\nprint("positive inputs:", count)')
md('严格平行不能包含重合。每个负例直接调用生成器，防止空证书掩盖错误。')
code('rejected = 0\nfor item in negatives():\n    try: make_certificate(item)\n    except ValueError: rejected += 1\n    else: raise RuntimeError("invalid input accepted")\nprint("direct rejections:", rejected)')
md('证书必须绑定调用者给出的完整输入。哈希不是身份认证。')
code('from copy import deepcopy\nother = deepcopy(d)\nother["B"] = ["3", "1"]\nprint("rebound accepted:", verify_certificate(other, c))\nbad = deepcopy(c)\nbad["schema"] = True\nprint("boolean substitution accepted:", verify_certificate(d, bad))')
md('最后运行单元测试。空间仅不相交反例与一般坐标证明见 WALKTHROUGH.zh-CN.md。')
code('import unittest\nsuite = unittest.defaultTestLoader.loadTestsFromName("test_geometry")\nresult = unittest.TextTestRunner(verbosity=1).run(suite)\nif not result.wasSuccessful(): raise RuntimeError("test failures")')
nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'},'execution_method':'not executed yet'},'nbformat':4,'nbformat_minor':5}
for i,c in enumerate(cells):c['id']=f'i30-cell-{i:02}'
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('created six-code-cell tutorial')
