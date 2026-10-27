"""Standard-library scaffold: installed skill read, local helper unavailable."""
import json
from pathlib import Path
cells=[]
def md(s): cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s): cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(True),'execution_count':None,'outputs':[]})
md('# I.28：两个局部角条件，一项平行结论\n\n现代有理坐标教学，不是原文证明内核。随附执行器使用标准库compile/exec，**不是Jupyter kernel**。从本目录运行。')
code('from geometry import make_certificate, verify_certificate\nfrom cases import positives, negative_cases, sample\ncertificate=make_certificate(sample())\nprint(certificate["angle_keys"])\n')
md('E=(0,0), F=(2,0), B=(1,1), D=(3,1)。G=2E−F，故GEB和EFD都是135度；cot指标均为−1。')
code('interior=make_certificate(sample("interior_sum"))\nprint(interior["angle_keys"])\nprint(interior["direction_determinant"],interior["same_scale"])\nprint(verify_certificate(sample("interior_sum"),interior))\n')
md('同侧内角BEF=45度、EFD=135度。指标1与−1的和为0，只有在角都在(0,π)中时才等价于和为π；不能把角大小与cot值相加混为一谈。')
code('rejected=[]\nfor name,bad in negative_cases().items():\n    try: make_certificate(bad)\n    except ValueError: rejected.append(name)\n    else: raise RuntimeError(name)\nprint("directly rejected:",len(rejected))\n')
code('import copy\nattack=copy.deepcopy(certificate)\nattack["schema"]=True\nprint("bool schema accepted:",verify_certificate(sample(),attack))\nprint("mode rebound accepted:",verify_certificate(sample("interior_sum"),certificate))\n')
md('有限有理样例含正负斜率、反射、旋转、平移、尺度，不能代替一般证明。')
code('count=0\nfor data in positives():\n    if not verify_certificate(data,make_certificate(data)): raise RuntimeError("failed")\n    count+=1\nprint("positive cases:",count)\n')
code('import unittest\nfrom test_geometry import Checks\nresult=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(Checks))\nif not result.wasSuccessful(): raise RuntimeError("tests failed")\n')
md('复盘：同侧位置和完整射线很重要；指标保留符号；验证证书须由调用方提供独立可信输入。现代模型中的等价不等于原书在I.28已证明I.29。')
nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'}},'nbformat':4,'nbformat_minor':4}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('created 6 code cells; not yet executed')
