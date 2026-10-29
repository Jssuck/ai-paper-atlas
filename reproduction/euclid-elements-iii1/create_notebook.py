"""Standard-library fallback: installed skill helper unavailable locally."""
import json
from pathlib import Path
cells=[]
def md(s): cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s): cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(True),'execution_count':None,'outputs':[]})
md('# Euclid III.1：从弦证据恢复圆心\n\n目标：分开给定圆、有限点证据与已知中心测试生成器。本程序输入 A、B 及垂直平分线与圆周的交点 C、E；不输入圆心，不实现一般圆周求交或图像识别。只用 Python 标准库，在本文件目录运行。')
code('from fractions import Fraction as Q\nfrom geometry import recover_center, verify_certificate, sample\nr = recover_center((-3,4),(3,4),(0,5),(0,-5))\nprint("D =",r["D"],"F =",r["F"],"radius squared =",r["radius_squared"])')
md('## 1. 两次平分不是同一步\nD 是 AB 中点，F 是 CE 中点。D 一般不是圆心。原证先把任意圆心限制到垂直平分线上；同线且到 C、E 等距进一步选出 F。四点共圆检查是教学输入的契约，不代表核查了无限多个圆周点。')
code('from geometry import distance_squared\nprint("radii squared:",[distance_squared(r["F"],r[k]) for k in ("A","B","C","E")])\nprint("D is not center:",r["D"] != r["F"],"certificate:",verify_certificate(r))')
md('## 2. 初始弦恰为直径\n此时 D=F，不存在有意义的射线 DF。不要把重合点硬塞入原文非退化角图。两次中点算法仍有定义；证明应另述这个分支。')
code('d = recover_center((-5,0),(5,0),(0,5),(0,-5))\nprint(d["branch"],"D = F:",d["D"]==d["F"])')
md('## 3. 坐标表示不影响结果\n下一格先用已知圆心的 fixture 生成输入，再交给不接收圆心的 recover_center。它测试实现的等变性，不是演示从真实未知圆提取交点。')
code('points=sample(cosine=Q(3,5),sine=Q(4,5),offset=(3,-7))\ns=recover_center(*points)\nprint("transformed F =",s["F"],"radius squared =",s["radius_squared"])')
md('## 4. 失败输入与练习\n把 F 篡改为 D，检查应失败；把 C 改为 (0,6)，四点不再属于恢复出的同一圆。为何严格拒绝 float 和 bool？前者不代表此接口的精确有理数据，后者在 Python 中会与 0/1 相等，不能静默当坐标。')
code('bad=dict(r);bad["F"]=bad["D"]\nprint("wrong center accepted:",verify_certificate(bad))\ntry: recover_center((-3,4),(3,4),(0,6),(0,-5))\nexcept ValueError as e: print(type(e).__name__,str(e))\ntry: recover_center((True,4),(3,4),(0,5),(0,-5))\nexcept TypeError as e: print(type(e).__name__,str(e))')
md('## 答案与运行边界\n上面错误中心被拒。原例的半径平方为25；缩放1/3后为25/9，平移不改变半径。为什么一个弦中点不够？同一弦的垂直平分线上有无限多个候选圆心，需圆周的额外证据。\n\n此 Notebook 由标准库 compile/exec 顺序执行并保存输出，非 Jupyter kernel，未验证内核集成。安装技能的本地 scaffold helper 不存在，采用本生成器；没有安装依赖。有限测试不是一般证明；有理坐标子域不覆盖所有尺规构造。')
for i,c in enumerate(cells): c['id']=f'iii1-{i+1:02}'
nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'}},'cells':cells}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Created tutorial: 5 code cells; standard-library fallback scaffold.')
