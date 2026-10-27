"""Standard-library notebook scaffold; installed helper unavailable locally."""
import json
from pathlib import Path
cells=[]
def md(s): cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s): cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(True),'execution_count':None,'outputs':[]})
md('# I.27：角相等与两条无限直线\n\n这是现代有理坐标教学核验；非欧几里得原始证明内核。随附执行器使用标准库 compile/exec，**不是 Jupyter kernel**。从本目录运行。')
code('from geometry import make_certificate, verify_certificate\nfrom cases import positives, negative_cases\ndata = {"E":["0","0"],"F":["2","0"],"A":["1","1"],"D":["1","-1"]}\ncertificate = make_certificate(data)\nprint(certificate["angle_keys"])\n')
md('两角都是锐角；射线在横截线异侧。方向行列式为零，横截偏移非零，故直线不重合。')
code('print(certificate["direction_determinant"])\nprint(certificate["transversal_side_determinants"])\nprint(certificate["opposite_scale"])\nprint(verify_certificate(data, certificate))\n')
md('平方余弦会混淆互补角；这里的有符号指标不会。六类失败均应由生成器直接拒绝。')
code('rejected=[]\nfor name,bad in negative_cases().items():\n    try: make_certificate(bad)\n    except ValueError: rejected.append(name)\n    else: raise RuntimeError(name)\nprint(rejected)\n')
code('import copy\nattack=copy.deepcopy(certificate)\nattack["schema"]=True\nprint("bool schema accepted:",verify_certificate(data,attack))\nother=next(positives())\nprint("other input accepted:",verify_certificate(other,certificate))\n')
md('有理变换批量检查只是有限样例，不证明一般定理。')
code('count=0\nfor p in positives():\n    if not verify_certificate(p,make_certificate(p)): raise RuntimeError("failed")\n    count+=1\nprint("positive cases:",count)\n')
code('import unittest\nfrom test_geometry import Checks\nresult=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(Checks))\nif not result.wasSuccessful(): raise RuntimeError("tests failed")\n')
md('复盘：同侧不是内错角；角指标符号不可丢；证书必须绑定调用方独立持有的输入。一般中性几何证明仍须 I.16 的两方向反证。')
nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},'nbformat':4,'nbformat_minor':4}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('created 6 code cells; not yet executed')
