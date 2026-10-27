"""Standard-library nbformat-4 scaffold; no external dependencies."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
cells = []


def markdown(source):
    cells.append({'cell_type': 'markdown', 'id': f'md-{len(cells):02d}', 'metadata': {},
                  'source': source.strip().splitlines(keepends=True)})


def code(source):
    cells.append({'cell_type': 'code', 'id': f'code-{len(cells):02d}', 'metadata': {},
                  'execution_count': None, 'outputs': [],
                  'source': source.strip().splitlines(keepends=True)})


markdown(r'''
# Euclid《几何原本》I.10：不是先写下中点

**目标**：依次调用 I.1、I.9、I.4，用现代精确坐标检查线段二等分；这是构造与证明的调用顺序，不是命题间的单向依赖链。
给定任意两个**不同的有理坐标点** $A,B$，构造等边顶点 $C$，构造 $\angle ACB$ 的内角平分射线，再**求解射线与 $AB$ 的交点** $D$。

这是原创教学重建，不是古代程序、物理尺规器或形式化定理证明。坐标公式和 Python 是现代检验工具；不能归给欧几里得。

**运行**：在本 Notebook 所在目录启动 Python/Jupyter，按顺序运行全部单元格；只用标准库。随附输出实际由 `verify_notebook.py` 的共享命名空间 `compile/exec` 产生，**不是 Jupyter kernel 执行记录**。`kernelspec` 仅供用户选择兼容内核，不构成已运行内核的证据。
''')
code('''
from pathlib import Path
if not Path("geometry.py").is_file():
    raise RuntimeError("请把工作目录切换到本 Notebook 所在目录后重跑。")
from fractions import Fraction as R
from geometry import (Q3, point, sub, construct, check_certificate, accepted,
                      intersect_open_ray_segment, dist2)
from cases import rejected_cases, example_report
print("精确数域 Q(sqrt(3))；无浮点几何判定；输出交点由行列式方程解得。")
''')
markdown(r'''
## 1. I.1 两支与 I.9 内向选择

先在 $AB$ 上取等边顶点 $C$。因为 $CA=CB$，I.9 所需等距截点可直接用 $A,B$，这里不必另调用 I.3 截长。
再在 $AB$ 上取与 $C$ 异侧的等边顶点 $F$；I.9 输出射线 $CF$。选择异侧是构造的一部分，不是“只要两个角相等就接受”。

两种 $C$ 都应成功；它们交换 $C,F$，但得到同一个 $D$。
''')
code('''
A, B = point(0, 0), point(2, 0)
certificates = [construct(A, B, branch) for branch in (1, -1)]
for cert in certificates:
    print("branch:", cert.branch, "C:", tuple(map(str, cert.c)),
          "F:", tuple(map(str, cert.f)), "D:", tuple(map(str, cert.d)),
          "s:", str(cert.s), "t:", str(cert.t), "accepted:", accepted(A, B, cert))
if certificates[0].d != certificates[1].d:
    raise RuntimeError("两支结果不同")
''')
markdown(r'''
## 2. 求交点，不预置中点

令 $w=F-C,\ e=B-A$，求解
$$C+s w=A+t e.$$
使用一般的二维直线交点公式：
$$s=\frac{(A-C)\times e}{w\times e},\qquad
  t=\frac{(A-C)\times w}{w\times e}.$$
程序先检查分母非零，再检查 $s>0$ 与 $0<t<1$，最后返回 $D=C+s w$。因此“交点存在且位于线段内部”是明确核查项，不是从图形观感跳过的前提。

下面故意输入**不是角平分线**的射线：一般求交器给 $t=1/3$，而非硬编码 $1/2$。
''')
code('''
D, s, t = intersect_open_ray_segment(point(1, 2), point(0, -1),
                                    point(0, 0), point(3, 0))
print("一般交点：D =", tuple(map(str, D)), "; s =", str(s), "; t =", str(t))
if t != Q3(R(1, 3)):
    raise RuntimeError("求交器错误")
''')
markdown(r'''
## 3. I.4 前提与结论分开检查

在 $\triangle ACD$、$\triangle BCD$ 中：$CA=CB$，$CD$ 为共同正长边，$\angle ACD=\angle BCD$。这对应 I.4 的边角边使用；由此得到 $AD=DB$。

检查器同时要求 $D\in AB$ 且 $0<t<1$。只检查 $AD=DB$ 绝不充分：垂直平分线上有无穷多个不在 $AB$ 上的等距点。

角相等用精确点积的符号与平方交叉乘积核查；内部方向另用有向叉积核查，避免把反向射线当成内角平分线。
''')
code('''
checks = check_certificate(A, B, certificates[0])
for name, passed in checks.items():
    print(name, ":", passed)
if not all(checks.values()):
    raise RuntimeError("有效证书未通过")
print("通过项数：", len(checks))
''')
markdown(r'''
## 4. 负例不是装饰

下面保留等距但非中点、反向等角射线、边界/错误内部射线、零射线、六类字段篡改与输入绑定问题。每个例子必须有失败项；不是要求每一个谓词都失败。

特别观察：`equidistant_but_not_midpoint` 的距离相等仍为真；`reversed_equal_angle_ray` 的等角仍为真，但内向及正射线参数为假。
''')
code('''
for label, a, b, bad in rejected_cases():
    facts = check_certificate(a, b, bad)
    if all(facts.values()):
        raise RuntimeError("误收负例：" + label)
    print(label, "=> rejected; failed:", ", ".join(k for k, v in facts.items() if not v))
''')
markdown(r'''
## 5. 有限实跑与一般推导不同

设 $M=(A+B)/2$，$e=B-A\ne0$，$R$ 表示旋转 $90^\circ$，$\delta=\pm\sqrt3/2$。I.1 及 I.9 的坐标模型给出
$$C=M+\delta R(e),\quad F=M-\delta R(e),\quad w=-2\delta R(e).$$
因为 $e\cdot e>0$，
$$w\times e=2\delta(e\cdot e)\ne0,$$
而两个求交分子都等于 $\delta(e\cdot e)$，故**求解之后**得到 $s=t=1/2$，并由此得到 $D=M$。这个推导说明模型覆盖所有不同有理端点（数学公式也适用于实端点）；下面的有限测试不是该结论的证明。

枚举范围：3 个平移原点 × 24 个非零有理向量 × 5 种相似变换 × 2 支 = 720 份证书。包含有理旋转、反射、$10^{-80}$ / $10^{80}$ 缩放；它们不是 720 个互不相似的几何类型。单测还覆盖 $10^{150}$ 平移叠加 $10^{-150}$ 位移，及 $10^{\pm200}$ 缩放。
''')
code('''
from run_examples import run
report = run()
print("正例证书数：", report["positive_certificates"])
print("分组：", report["positive_families"])
print("拒绝负例数：", report["negative_certificates"])
print("逐例精确记录 SHA-256：", report["positive_records_sha256"])
for example in report["examples"]:
    if example["name"].startswith("article_"):
        print("正文对应实跑：", example["name"], "D=", example["certificate"]["d"],
              "平方长度=", example["squared_lengths"])
print("局限：有限测试不是一般证明；本 Notebook 没有执行于 Jupyter kernel。")
''')
markdown(r'''
## 结语与复现边界

- **算法输出**是方程求得的交点；中点公式只用于 I.1 的现代坐标表达、事后推导和独立测试预期。
- **证书**不是防篡改签名；它重新计算几何事实，不信任外部传入的“通过”标签。文件完整性另用 `SHA256SUMS.json` 检查。
- **有限证据**：`run_all.py` 实跑普通、`-O`、`-OO` 三种模式；实际命令、环境、退出码和日志在同目录。
- **不覆盖**：所有实数的机器表示、物理尺规操作、I.1 圆交点连续性的一般证明、I.4 的独立形式化证明，以及 Notebook 浏览器/内核兼容性的实际运行验证。
- **继承**：精确数域与角谓词改写自本项目原创 I.9 教学代码；I.10 求交器、输入绑定证书、测试族与本 Notebook 为此次新增。
''')
notebook = {
    'nbformat': 4, 'nbformat_minor': 5,
    'metadata': {
        'kernelspec': {'display_name': 'Python 3 (user-selected kernel)', 'language': 'python', 'name': 'python3'},
        'language_info': {'name': 'python'},
        'execution_provenance': {'method': 'not yet executed; run verify_notebook.py', 'jupyter_kernel_used': False},
    },
    'cells': cells,
}
(ROOT / 'teaching.zh-CN.ipynb').write_text(json.dumps(notebook, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'created': 'teaching.zh-CN.ipynb', 'code_cells': sum(c['cell_type']=='code' for c in cells),
                  'scaffold': 'standard-library scaffold; no dependencies installed'}))
