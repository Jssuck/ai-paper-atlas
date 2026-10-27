"""Build a small v4 tutorial notebook; only Python standard library is needed.

The installed skill's scaffold file was not locally available. This explicit
v4 builder is the fallback; it does not install packages or claim kernel use.
"""
import json
from pathlib import Path
cells=[]
def md(text):cells.append({'cell_type':'markdown','metadata':{},'source':text.splitlines(keepends=True)})
def code(text):cells.append({'cell_type':'code','metadata':{},'source':text.splitlines(keepends=True),'execution_count':None,'outputs':[]})
md('# Euclid I.13：从射线顺序到两直角\n\n这是原创教学重构，不是原文翻译。普通角取值在零与半周之间；有限实跑不证明一般命题。下列格按标准库 compile/exec 顺序执行，不是 Jupyter kernel。')
code('from fractions import Fraction as F\nfrom geometry import build_certificate, verify_certificate, angle_partition\nfrom cases import evaluate\nb,c,d,a=(0,0),(1,0),(-2,0),(1,2)\ncert=build_certificate(b,c,d,a)\nprint(cert["ray_order_case"])\nprint(cert["rotation_product"])\n')
md('## 1. 相邻角的方向见证\nBC、BD 必须是反向射线，BA 必须离开底线。两个复数式旋转对相乘得负实数；每个虚部为正排除了反身角和周数混淆。这里没有把向量角度假定为有理数。')
code('print("first:",cert["first_rotation"],"second:",cert["second_rotation"])\nprint("verified:",verify_certificate(cert,b,c,d,a))\n')
md('## 2. 垂线两侧的两种顺序\n辅助垂线应选择 BA 所在半平面。斜射线位于垂线之前或之后，必须分别安排小角加法；垂直情形可直接由直角定义处理。')
code('for point in ((1,2),(0,2),(-1,2),(1,-2)):\n    q=build_certificate(b,c,d,point)\n    print(point,q["orientation"],q["ray_order_case"])\n')
md('## 3. 独立的有理角度模型\n这层以周为单位，预先采用角度加法和直角为四分之一周。不是从上面的有理坐标计算角度。它演示加法分拆，不是用 1/2−t 的定义重新“证明”几何定理。')
code('for t in (F(1,8),F(1,4),F(3,8)):\n    p=angle_partition(t)\n    print(str(t),[str(x) for x in p["ordered_sectors"]],str(p["sum"]))\n')
md('## 4. 拒绝篡改与不满足前提的输入\n证书必须绑定独立给出的输入，不能仅检查一行声称结论。共线但同向也不够。')
code('from copy import deepcopy\nbad=deepcopy(cert);bad["rotation_product"]=["10","0"]\nprint("tampering accepted:",verify_certificate(bad,b,c,d,a))\ntry:\n    build_certificate(b,c,(2,0),a)\nexcept ValueError as exc:\n    print(type(exc).__name__+": "+str(exc))\n')
md('## 5. 有限回归集\n平移、旋转、反射、不等长底线射线均被取样。一般恒等式和角度公理的论证见 WALKTHROUGH，不由样本数量保证。')
code('result=evaluate()\nfor key in ("positive_certificates","negative_certificates","angle_partition_cases","ray_order_counts"):\n    print(key,result[key])\n')
md('## 复盘\n问：只见乘积为负实数，为什么还不够？答：如果不限制每个普通角在 (0,π)，可以混入反身角及整周；正虚部提供这一步的方向见证。\n\n问：程序核验了 Euclid 的全部公理吗？答：没有。向量空间、点序与角度解释是现代模型前提。')
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'scaffold':'explicit v4 builder; bundled helper unavailable in current filesystem'},'cells':cells}
for i,cell in enumerate(cells):cell['id']=f'i13-{i:02d}'
Path(__file__).with_name('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('Wrote teaching.zh-CN.ipynb: 6 code cells; execution is a separate step.')
