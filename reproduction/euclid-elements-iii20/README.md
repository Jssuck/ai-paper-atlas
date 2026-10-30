# III.20 最小教学复现：同弧、二倍角与边界

[中文深读](../../papers/ancient/euclid-elements-iii20.zh-CN.md) · [Notebook](teaching.zh-CN.ipynb) · [图示](diagram.svg)

## 定位与范围

这是原创现代解析几何教学模型，不是古代程序的重建。原证的加法、减法分支、一边穿过圆心的边界、底弦为直径，以及反角扩展分别列举；后两类全范围角度处理不能说成 Euclid 原文已经逐项陈述。没有以 III.21 或后继命题作前提。

有限实跑只检查所列有理点，不证明所有实数圆点的定理。一般证明见深读。SVG 中浮点三角函数只用于画图，测试和等式判定全部使用 Python 标准库 `fractions.Fraction`。

## 精确模型

`geometry.py` 的 `evaluate(A,B,C,O=(0,0))` 要求 A、B、C 为同一非零圆上三个互异点，每个坐标必须为整数或 Fraction（拒绝浮点与 bool）。先检验共圆、非零半径和互异条件，再计算：

- u = B−A，v = C−A；d = u·v，k = cross(u,v)，D = (u·u)(v·v)。三个互异圆点不共线，故 k 非零。
- 二倍普通圆周角的单位方向为 `((d*d-k*k)/D, 2*d*abs(k)/D)`。这是余弦、正弦二元组，不是弧度。
- s = sign(cross(C−B,A−B))。A 在有向弦 B→C 左侧时，所选不含 A 的弧为 B→C 的逆时针弧；在右侧则为顺时针弧。该事实可由单位圆的半平面分割直接验证，不以圆周角定理为前提。
- b = B−O，c = C−O，R² = b·b。所选圆心角方向为 `(b·c/R², s*cross(b,c)/R²)`。
- `check` 逐项比较上述两个精确二元组，不使用容差，也不以 `assert` 作生产校验。

所选圆心角在 (0, 2π)，二倍普通圆周角也在 (0, 2π)，因此相同单位方向不会遗失一个整周的差异。d 的正、零、负分别标记所对劣弧、半圆、优弧；优弧要求反角而非总取较小圆心角。旋转方向 s 与反角并非一回事。

圆心位置用 O−A = λu+μv 的精确系数判定：λ、μ 都正为角内；都非负且至少一个零为边界；其他为角外。`side_through_center` 和 `base_diameter` 是两个独立标记，不能混为一谈。

## 真运行

在本目录执行：

```sh
python run_all.py
```

无第三方依赖或安装。`run_all.py` 生成 Notebook、SVG，并分别以普通、`-O`、`-OO` 模式执行测试、算例、Notebook 顺序执行和保存输出回放；日志保留真实退出码。它只写本目录日志与生成物。

- 每种模式 16 个 unittest 测试方法，全部通过。
- 每种模式 10 个有理圆点的 720 个互异有序三元组 × 3 种相似变换，共 2160 例。变换含旋转、平移、缩放与反射。
- 弧类计数：minor 1578、major 390、semicircle 192。
- 圆心位置：inside 996、outside 780、boundary 384。
- 角边过心 384 例；底弦直径 192 例。两种边界不等价。
- 5 个具名算例另验；非法点、重复点、零半径、浮点输入、错误小圆心角规则均有测试。
- 5 个 Notebook 代码单元实作 `compile/exec` 并校验保存的输出；**并非 Jupyter kernel 执行**。没有声称完整复现某个古代实验。

精确环境、运行时刻与退出码分别见 [environment.json](environment.json)、[run-summary.json](run-summary.json)、[真实测试日志](logs/test_geometry-normal.log)、[算例日志](logs/run_examples-normal.log)、[Notebook 日志](logs/verify_notebook-normal.log)。优化模式日志在同目录。

Notebook 技能的本地脚手架未提供可读脚本，因此 `create_notebook.py` 使用标准库生成 nbformat 4.5 结构，保留 cell id、代码单元输出和明确执行方式。读者可以在本目录以真实 Jupyter kernel 再执行，但这不是本次已完成的验证。

## 文件与自查

| 文件 | 用途 |
|---|---|
| [geometry.py](geometry.py) | 精确模型、样本与变换 |
| [test_geometry.py](test_geometry.py) | 16 个测试方法，含 2160 例有限枚举 |
| [run_examples.py](run_examples.py) | 加法、减法、两种边界、反角错误规则 |
| [create_notebook.py](create_notebook.py) / [verify_notebook.py](verify_notebook.py) | 可重建 Notebook 与顺序执行回放 |
| [make_diagram.py](make_diagram.py) | 本地 SVG 图示生成，无外链、脚本或第三方字体 |
| [run_all.py](run_all.py) | 三种 Python 模式下的统一运行命令 |

局限：有理点样本不覆盖所有实数点；没有浮点稳健性或图形识别实验；正弦余弦对的等式只是现代解析重构的检查对象，不能替代原文等腰三角形与外角定理的证明。
