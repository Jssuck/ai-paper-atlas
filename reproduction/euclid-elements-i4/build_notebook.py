"""Build a small self-contained notebook with only the standard library.

The notebook skill was read; its packaged helper/template was unavailable in
this environment. This explicit fallback is not represented as template use.
"""

import json
from pathlib import Path


def markdown(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": text.splitlines(keepends=True)}


def build():
    cells = [
        markdown("""# 《几何原本》I.4：精确有理 SAS 教学实验

**目标**：在现代实数内积平面中，以有理坐标、`Fraction` 和显式矩阵运算，检查两有标号非退化三角形的 SAS 数据，并构造验证等距仿射映射。

**边界**：这是原创教学模型和有限计算实验；不是古代叠合的物理复演，不是欧几里得原公设系统中的完整推导，也不是完整证明助理形式化。两边长度已相等时，夹角相等用内积相等表示；这里没有独立计算任何角函数。

请把工作目录设为此 Notebook 所在文件夹。代码无第三方依赖，也不使用 notebook 魔法命令。"""),
        code("""from fractions import Fraction as F
import json
import sys
from euclid_i4 import Triangle, Certificate, compare_sas, verify_certificate, result_record, InputError
from enumerate_cases import examples, run_enumeration
print('Python:', sys.version.split()[0])
print('Arithmetic: fractions.Fraction; no floating-point geometry')
"""),
        markdown(r"""## 1. 从 SAS 数据构造 Q 与 t

令 $u=B-A,v=C-A,U=E-D,V=F-D$。先检查 $u\cdot u=U\cdot U$、$v\cdot v=V\cdot V$、$u\cdot v=U\cdot V$。

设 $P=[u\ v],R=[U\ V]$；非退化保证 $P$ 可逆。直接计算 $Q=RP^{-1}$，$t=D-QA$。使用有理旋转而非只测试整点轴对称。"""),
        code("""source = Triangle((0, 0), (3, 0), (0, 2))
known = Certificate(((F(3,5), F(-4,5)), (F(4,5), F(3,5))), (F(7,3), F(-5,2)))
target = Triangle(*(known.apply(p) for p in source.vertices))
result = compare_sas(source, target, require_direct=True)
print(json.dumps(result_record(result), ensure_ascii=False, indent=2))
if result.certificate != known or not result.accepted:
    raise RuntimeError('Exact recovery failed')
"""),
        markdown("""## 2. 独立核对结论与非循环的代数理由

检查器不调用 SAS：直接核对 $Q^TQ=I$、三点映射、第三边平方、所有对应边平方、三个顶点的内积及相邻边平方。

一般代数理由是 $R^TR=P^TP$，故 $Q^TQ=P^{-T}R^TRP^{-1}=I$；三点映射由构造成立。这使用现代坐标和内积事实，不以待证 SAS 为子程序，也不声称把一般推导交给了证明助理。"""),
        code("""checks = verify_certificate(source, target, result.certificate)
print('AB², AC², BC²:', source.side_squares)
print('Each vertex: (incident side², dot, incident side²):', source.angle_data)
print('All explicit certificate checks:', checks)
if not all(checks.values()):
    raise RuntimeError('Certificate verification failed')
"""),
        markdown(r"""## 3. 允许反射的全等，不等于保向运动

$\det Q=+1$ 为保向等距映射；$\det Q=-1$ 为反向等距映射（允许反射的全等）。`require_direct=True` 只改变策略接受与否，不把已验证的镜像全等说成不全等。"""),
        code("""reflection = Certificate(((1,0),(0,-1)), (2,3))
mirror = Triangle(*(reflection.apply(p) for p in source.vertices))
ordinary = compare_sas(source, mirror)
direct_only = compare_sas(source, mirror, require_direct=True)
print('Allow reflection:', ordinary.congruent, ordinary.accepted, ordinary.certificate.determinant)
print('Require direct:', direct_only.congruent, direct_only.accepted, direct_only.reason)
if not ordinary.accepted or direct_only.accepted or not direct_only.congruent:
    raise RuntimeError('Reflection policy failed')
"""),
        markdown("""## 4. 剪切、错误对应、非夹角 SSA

剪切例保持从首顶点出发的两边长度，但改变夹角内积；其行列式仍为 1，故面积与保向本身不是等距的充分条件。

SSA 例：$(0,0),(4,0),(1,1)$ 与 $(0,0),(4,0),(3,3)$ 的第一边平方同为 16、对边平方同为 10，首顶点角因同射线而相同；另一边平方却分别是 2 与 18。给定的角不是两条给定边的夹角。"""),
        code("""records = examples()
print('Shear SAS comparisons:', records['shear']['result']['sas_equal'])
print('Shear orthogonal:', records['shear']['independent_certificate_checks']['orthogonal'])
print('Wrong scalene correspondence:', records['wrong_scalene_correspondence']['reason'])
ssa = records['ssa_nonincluded_angle_counterexample']
print('SSA sides AB²,AC²,BC²:', ssa['side_squares_AB_AC_BC'])
print('SSA same ray at A:', ssa['same_ray_AC'])
print('SSA accepted:', ssa['result']['accepted_under_policy'])
if records['shear']['result']['accepted_under_policy'] or ssa['result']['accepted_under_policy']:
    raise RuntimeError('Negative control incorrectly accepted')
"""),
        markdown("""## 5. 输入契约与退化边界

仅接受 `int`（不含 `bool`）和 `Fraction`。不把浮点小数“近似转成”精确输入；NaN/Infinity、字符串、错误维度、共线或重复顶点也明确报错。数学上的有限有理数需由调用者显式提供，例如 `F(1, 10)`，而非 `F(0.1)`。"""),
        code("""bad_inputs = [((0,0),(1,0),(2,0)), ((0.0,0),(1,0),(0,1)),
              ((float('nan'),0),(1,0),(0,1))]
for bad in bad_inputs:
    try:
        Triangle(*bad)
    except InputError as error:
        print(type(error).__name__ + ': ' + str(error))
    else:
        raise RuntimeError('Invalid input was not rejected')
"""),
        markdown("""## 6. 有限穷举：可复跑，不能冒充普遍证明

将首顶点固定为原点，取 $[-2,2]^2$ 中全部 25 个向量。逐一调用 API 检查 496 个非退化三角形的全部 246,016 个有序配对；另用 992 个有理旋转/反射和平移检查精确回收。该有限样本不覆盖所有有理数，更不覆盖所有实数。"""),
        code("""report = run_enumeration()
print(json.dumps({key: report[key] for key in ('grid', 'exhaustive_grid_api_results', 'rational_transform_cases')},
                 ensure_ascii=False, indent=2))
print('Conclusion: finite checks passed, not a complete formal proof.')
"""),
        markdown("""## 复现与执行说明

完整测试命令见 `README.md` 和 `logs/`。本次交付环境没有 Jupyter 内核及 nbclient；保存的代码单元输出由 `execute_notebook.py` 用标准库 `compile`/`exec` 按顺序真实执行并捕获。**不是 Jupyter 内核执行或内核兼容性认证**。本文件保留标准 nbformat 4 结构与 Python 3 kernelspec，供已有 Jupyter 的读者自行从头运行。

Notebook 技能说明已阅读，但其配套模板/生成器在当前环境不可读取；本文件由随附的 `build_notebook.py` 标准库回退生成，未声称使用不可用的模板。"""),
    ]
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
            "reproduction": {"template": "manual stdlib fallback; packaged skill template unavailable",
                             "execution": "not yet executed"},
        },
        "nbformat": 4, "nbformat_minor": 4,
    }
    Path("euclid_i4_tutorial.ipynb").write_text(json.dumps(notebook, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Wrote euclid_i4_tutorial.ipynb (standard-library fallback scaffold)")


if __name__ == "__main__":
    build()
