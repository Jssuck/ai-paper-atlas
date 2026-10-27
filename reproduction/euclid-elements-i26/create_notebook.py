"""Create an original tutorial; template helper unavailable in this environment."""
import json
from pathlib import Path
cells=[]
def md(s):cells.append({'cell_type':'markdown','metadata':{},'source':s.splitlines(True)})
def code(s):cells.append({'cell_type':'code','metadata':{},'source':s.splitlines(True),'execution_count':None,'outputs':[]})
md('# I.26 两角一边：精确有限核验\n本 Notebook 是原创教学坐标模型，不是古希腊原证，也不是一般定理的形式化证明。角键用内积除以行列式绝对值；无浮点误差容限。发布记录通过标准库 compile/exec 顺序执行，未通过 Jupyter kernel。请在本目录运行。')
code('from geometry import make_certificate, verify_certificate, triangle, angle_key, length2\nfrom cases import example, positive_cases, negative_cases\nprint("精确有理坐标；不调用浮点三角函数")')
md('## 1 夹边案\nB 对 E、C 对 F；给定 BC=EF。读取角键和三边平方，直接查看结论。')
code('data = example("included")\ncertificate = make_certificate(data)\nprint(certificate["angle_keys"])\nprint(certificate["squared_sides_AB_BC_AC"])\nprint(verify_certificate(data, certificate))')
md('## 2 对边案\n相同角对应，但给定边改为 AB=DE。不能把一般 SSA 误称本命题。')
code('opposite = example("opposite")\nprint(make_certificate(opposite)["given_edge_index"])\nprint(verify_certificate(opposite, make_certificate(opposite)))')
md('## 3 有限覆盖\n36 种非退化形状、3 种有理等距变换、2 个给定边分支。包含镜像、钝角与非整数坐标。216 个验收不替代一般证明。')
code('inputs = list(positive_cases())\naccepted = sum(verify_certificate(d, make_certificate(d)) for d in inputs)\nprint({"cases": len(inputs), "accepted": accepted})')
md('## 4 不满足前提的输入\n两角相等但缩放、错误顶点对应、共线退化、SSA 均不能当作 I.26 的完整前提。')
code('for name, bad in negative_cases().items():\n    try:\n        make_certificate(bad)\n        raise RuntimeError("unexpected acceptance")\n    except ValueError as error:\n        print(name, ":", str(error))')
md('## 5 证书必须绑定调用者的输入\n整数 schema=1 不允许被布尔 True 替换；另一合法输入的证书也不允许移植。')
code('import copy\nforged = copy.deepcopy(certificate)\nforged["schema"] = True\nprint("bool schema accepted:", verify_certificate(data, forged))\nother = example(); other["triangle_2"] = [["20","3"],["20","0"],["16","0"]]\nprint("different input accepted:", verify_certificate(data, make_certificate(other)))')
md('## 复盘\n为什么拒绝共线？行列式为零，角键无定义且三角形假设失效。为什么不直接用 assert？优化模式可删除断言，生产验收用显式异常和布尔返回。为什么不声称原证实跑？本程序直接计算前提和结论，未编码 I.4/I.16 的通用证明规则或几何位置公理。')
nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'},'execution_method':'standard-library compile/exec, not Jupyter kernel'},'nbformat':4,'nbformat_minor':5}
Path('teaching.zh-CN.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
print('created six-code-cell tutorial')
