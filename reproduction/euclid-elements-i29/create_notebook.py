"""Stdlib fallback scaffold: installed skill read; local template helper unavailable."""
import json
from pathlib import Path
cells=[]
def md(s):cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s):cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(True),'execution_count':None,'outputs':[]})
md('# Euclid I.29：平行假设与三个角结论\n运行环境：Python 3 标准库。本Notebook按六格compile/exec执行，非Jupyter kernel。模型验证不替代原文第五公设反证。')
code('from geometry import make_certificate, verify_certificate\nfrom cases import EXAMPLE, positives, negatives\nc = make_certificate(EXAMPLE)\nprint(c["input"])\n')
md('## 1. 侧向与比例\n交点不同、截线非共线、同侧及正比例分别检查。')
code('print("side determinants:", c["side_determinants"])\nprint("positive scale:", c["positive_scale"])\n')
md('## 2. 不开根号的角指标\ncos符号与cos平方共同唯一决定0到π的角；不能只比较平方。')
code('print(c["angles"])\nprint(c["conclusions"])\n')
md('## 3. 有限正例\n旋转、平移、改变斜率和正尺度，不声称穷尽。')
code('samples = list(positives())\nprint("positive inputs:", len(samples))\nprint("all verified:", all(verify_certificate(x, make_certificate(x)) for x in samples))\n')
md('## 4. 负输入必须直接拒绝\n不是只让空证书验证失败。')
code('rejected = 0\nfor x in negatives():\n    try:\n        make_certificate(x)\n    except ValueError:\n        rejected += 1\n    else:\n        raise RuntimeError("bad input accepted")\nprint("negative inputs rejected:", rejected)\n')
md('## 5. 完整测试\n有限测试发现程序错误，不是一般几何证明。')
code('import unittest\nfrom test_geometry import GeometryTests\nresult = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(GeometryTests))\nif not result.wasSuccessful():\n    raise RuntimeError("tests failed")\n')
nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'},'scaffold':'original standard-library fallback; installed helper unavailable'},'nbformat':4,'nbformat_minor':5}
for i,c in enumerate(cells):c['id']='i29-cell-'+str(i+1)
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n');print('created six-code-cell tutorial')
