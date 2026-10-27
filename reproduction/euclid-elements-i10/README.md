# Euclid《几何原本》I.10：线段二等分的精确教学复现

**结论**：在现代坐标模型中，给定任意不同的有理坐标端点 A、B，先按 I.1 构造等边顶点 C，再用 I.9 得到 ∠ACB 的内角平分射线，实际解出它与 AB 的交点 D，并逐项核查 I.4 的边角边前提及 AD=DB。

这是一组原创教学程序，不是古代实验数据、古人使用的算法或形式化定理证明；有限实跑不代替一般证明。代码只用 Python 标准库，未安装依赖，也不执行网络访问。

## 历史依赖与现代模型分工

[I.10 原文与 David Joyce 导读](https://mathcs.clarku.edu/~djoyce/elements/bookI/propI10.html)中的本构造与证明依次调用 **I.1、I.9、I.4**；这表示调用顺序，不是命题之间的单向依赖链。原文先在 AB 上作等边三角形，再平分顶角，最后以边角边得到两段相等。此处 F 是解释 I.9 中间步骤的辅助点，不是 I.10 原文额外命名的点。

因为 CA=CB，I.9 所需的等距截点可直接取 A、B，无须另实现 I.3 截长：在 AB 上取与 C 异侧的另一个等边顶点 F，得到射线 CF。两支等边顶点都单独检查。这里的“两个圆交点”由现代坐标公式建模，不是对圆交点存在性或尺规物理操作的一般程序证明。

### 不是把中点赋值后冒充构造

`equilateral_vertices` 的现代 I.1 公式使用 `(A+B)/2` 表达两个圆交点的中心；这不等于直接把输出 D 设成中点。`construct` 的输出 D 只来自一般求交器 `intersect_open_ray_segment`：

```text
w = F − C，e = B − A
C + s w = A + t e
s = cross(A − C, e) / cross(w, e)
t = cross(A − C, w) / cross(w, e)
D = C + s w
```

求交器显式拒绝零方向、退化线段、平行/重合支撑线、落在射线背后的交点、端点交点与线段外交点；通过时要求 **s>0 且 0<t<1**。单测还向它输入一条不平分线段的射线，实际得到 `t=1/3`，以排除求交器硬编码中点的可能。

## 精确算术与证书

`Q3` 用两个 `Fraction` 系数表示 `a+b√3`。加、减、乘、除及符号判定均精确：异号项用 `a²` 与 `3b²` 比较，不转成浮点数。输入坐标要求 `int` 或 `Fraction`；拒绝浮点、布尔值及字符串，避免隐式数值解释。中间点可以含 √3；构造入口则只接受有理端点。

角相等与射线内部方向必须分开：

- 内部：两个有向叉积与原凸角的方向同号。原角是小于平角的凸角。
- 等角：非零向量的点积符号相同，且平方余弦的交叉乘积相等。只比较平方会误认补角；只比较等角会误收反向射线。

`Certificate` 保存分支、C、F、D、s、t，不保存可信“通过”标签。`check_certificate(A,B,cert)` 从**外部给定的可信端点**重新计算 22 项事实：输入有效性、格式、I.1 分支及等边、I.9 等距截点/等边辅助点/异侧/非零/严格内向/等角、唯一线交点、两种参数表达、AB 共线、正射线参数、严格线段内部参数、I.4 等边/公共正长边/夹角相等/非退化及 SAS 汇总，最后才是 AD=DB。

I.4 的公共边是同一条 CD，因此公共性本身是恒等事实；程序另要求 CD 非零以及两三角形不退化。检查器同时检查 SAS 前提与距离结论，而非借几份测试证明 I.4。证书是几何一致性报告，不是数字签名或来源认证。

## 任意输入的坐标推导（与有限测试区分）

令 `e=B−A≠0`、`q=e·e>0`、`M=(A+B)/2`，令 `R(e)` 为 e 逆时针旋转 90°，`δ=±√3/2`。I.1 的两个候选及 I.9 异侧选择给出：

```text
C = M + δ R(e)
F = M − δ R(e)
w = F − C = −2δ R(e)
```

于是 `cross(w,e)=2δq≠0`；两个求交分子 `cross(A−C,e)` 和 `cross(A−C,w)` 都为 `δq`。因此**通过求解**得到 `s=t=1/2`，它们自动满足正射线及线段内部条件，输出 `D=C+s w=M`。

方向也可直接核对：`cross(A−C,B−C)`、`cross(A−C,w)`、`cross(w,B−C)` 均为 `δq`，故射线严格内向；`(A−C)·w=(B−C)·w=3q/2` 且 `|CA|²=|CB|²=q`，因此两夹角相等。CA=CB、CD 共边和相等夹角对应 I.4 的 SAS，得到 AD=DB；配合已证的内部交点，D 才是线段中点。

这段代数推导解释公式为什么适用于任意不同有理端点（数学上也适用于实端点），但本仓库没有把它编码为证明助理的形式证明。有限测试只为实现提供回归证据。

## 负例与实跑范围

12 份拒绝证书包括：

1. 等距但非中点：用 C 冒充 D，AD=DB 仍成立，却不在 AB 上。
2. 反向等角射线：等角仍成立，但非内向且交点的射线参数为负。
3. 边界射线、错误内部射线、零射线。
4. 篡改 D、s、t、分支或 C；测试另外逐字段改动 F。
5. 将证书重新绑定到不同输入，以及重合端点。

三种 Python 模式各执行 **25 项 unittest** 和 **720 份正例证书 + 12 份负例证书**。正例为 3 个平移原点 × 24 个非零有理向量 × 5 种相似变换 × 2 支。五组分别是恒等、有理旋转并缩放、反射、`10^-80` 缩放及 `10^80` 缩放，各 144 份。它们不是 720 个不同的相似类，也不是所有有理输入的枚举。

单测另覆盖端点交换、垂直/斜线段、`10^±200` 缩放、`10^150` 平移叠加 `10^-150` 位移、字段篡改、无效交点，以及 160 步 Pell 近抵消符号测试。对 1089 组有理系数的符号结果另外用 100 位 Decimal 交叉核对；Decimal 只用于这项有限单测，不参与几何判定。

## 运行与核验

在本目录执行：

```sh
python3 run_all.py
```

入口会依次执行 `test_geometry.py`、`run_examples.py` 的普通、`-O`、`-OO` 三种模式，逐份比较输出完全相同，再生成并执行 Notebook。逻辑门禁用显式异常和 unittest，不依赖会被优化去掉的裸 `assert`；运行脚本也检查这一点。

正文手算例 `A=(0,0), B=(6,0)` 与第 7 题 `A=(-2,1), B=(4,9)` 另有具名实跑记录及单测。它们分别得到 `D=(3,0)` 与 `D=(1,5)`；相关平方长度也保存在示例结果中。正文手算推导与程序输出是不同证据，不把手算写成运行日志。

最小用法：

```python
from fractions import Fraction as R
from geometry import point, construct, check_certificate
A, B = point(R(1, 3), R(-2, 5)), point(R(7, 3), R(8, 5))
cert = construct(A, B, branch=1)
print(tuple(map(str, cert.d)))  # ('4/3', '3/5')
print(all(check_certificate(A, B, cert).values()))  # True
```

公开证据：

| 文件 | 含义 |
|---|---|
| `environment.json` | 实际 Python/系统/架构、标准库范围及未使用的可选包检测 |
| `run-summary.json` | 真实执行命令 argv、时间、退出码、耗时及三模式一致性 |
| `logs/tests-*.log` | 三模式单测 stdout/stderr 与退出码 |
| `logs/examples-*.log`、`results-*.json` | 三模式真实结果：分组统计、拒绝原因、八份完整示例证书 |
| `positive_records_sha256`（结果内） | 按确定顺序生成的全部正例精确记录摘要；可由相同代码重算 |
| `teaching.zh-CN.ipynb` | 六个已执行代码单元格的中文教学 Notebook |
| `notebook-check.json`、`logs/notebook-*.log` | Notebook 生成、顺序执行的真实检查结果 |
| `SHA256SUMS.json` | 本目录公开文件 SHA-256；排除自身与 Python 缓存 |

Notebook 使用 nbformat 4.5 的 JSON 结构，含顺序执行输出。**实际执行器是标准 Python `compile/exec` 共享命名空间，不是 Jupyter kernel，也没有验证浏览器显示**。采用标准库 scaffold，未安装依赖。`create_notebook.py` 与 `verify_notebook.py` 完整公开这个过程。

重跑会更新实际时间、耗时、日志和相应哈希。验证现有快照完整性而不重跑：

```sh
python3 - <<'PY'
import hashlib, json
from pathlib import Path
root = Path('.')
sums = json.loads((root / 'SHA256SUMS.json').read_text())
bad = [name for name, expected in sums.items()
       if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected]
if bad:
    raise SystemExit('hash mismatch: ' + ', '.join(bad))
print('verified files:', len(sums))
PY
```

## 继承与边界

精确 `Q(√3)` 算术、等边坐标公式、内角/等角谓词，改写自本项目原创相邻 [I.9 geometry.py](../euclid-elements-i9/geometry.py)；保留思想但加强了输入类型约束。I.10 构造、一般求交器、输入绑定证书、测试族、运行证据和 Notebook 为此次新增。没有引入外部代码依赖。

不覆盖：任意实数的机器输入、通用尺规作图器、圆交点连续性的一般证明、I.4 的独立证明、古代公理体系的全部序关系前提，以及 Notebook 的 kernel/浏览器实际验证。以上局限不能通过“多跑几个例子”消除。
