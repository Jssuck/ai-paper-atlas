# Euclid II.14：矩形等积作方的精确有理教学复现

[中文深读](../../papers/ancient/euclid-elements-ii14.zh-CN.md) · [Notebook](teaching.zh-CN.ipynb) · [原创构造图](figures/ii14-equal-area.svg)

## 范围与证据等级

本包实现的是 **已给定正边长矩形 → 等积正方形** 的现代坐标教学模型。原命题先依 I.45 把给定直线形转为等积矩形；本包不实现任意多边形分割、I.45 构造、通用尺规作图器或一般几何定理证明器。没有数据集、训练或性能基线，指标为精确等式、输入域、根区间不变量是否成立；运行速度不是研究结论。

令长边 BE=L、短边 ED=S，L≥S>0。L=S 时返回已有正方形。L>S 时取 B=0、E=L、F=L+S、G=(L+S)/2，半圆半径 r=(L+S)/2，GE=d=(L−S)/2。程序检查 II.5 形式的 LS+d²=r²，I.47 形式的 EH²+d²=r²，并核对 EH²=LS；它不是从浮点近似开方来判断相等。证明必须由正文承担，有限测试不能证明一般定理。

输入只接受严格正 `int` 或 `fractions.Fraction`，拒绝 `bool`、浮点（含 NaN/Inf）、字符串、零和负数。输出 `side_squared` 是精确有理面积；正方形边本身未必有理。不等边返回 `semicircle` 分支的 G/E/F/radius/offset 等数据；等边返回 `already_square` 及有理边 `side`，不虚构非退化 GHE 三角形。

`sqrt_interval(area, steps=80)` 另作有理上下界二分，初始区间 [0,max(1,area)]，若上端或中点平方恰等于面积就返回单点，否则每步宽度减半。保证 `lo²≤area≤hi²` 及绝对宽度界 `max(1,area)/2**steps`，**不保证固定相对精度，也不保证所有有理平方根有限步命中**。步数只接受 0–10000 的整数（非 bool）；没有浮点 sqrt、容差判等或外部符号库。

## 重跑

Python 3.12；仅标准库；从本目录运行：

```sh
python -B run_all.py
```

也可分别执行：

```sh
python -B -m unittest -v test_geometry
python -B -O -m unittest -v test_geometry
python -B -OO -m unittest -v test_geometry
python -B run_examples.py
python -B draw_figure.py
python -B create_notebook.py
python -B verify_notebook.py
```

`run_all.py` 真实启动子进程、保存各返回码，任何步骤失败整体失败；日志中的本地解释器和构件目录已替换为通用标记，不含账户路径。运行会重建 Notebook、图和本包的生产日志，不覆盖独立审查文件。生产校验用异常，不依赖可被 `-O` 删除的 `assert`。

## 这次实际覆盖

- [23 项 unittest](test_geometry.py) 在 normal/`-O`/`-OO` 三模式全部通过；其中精确矩形网格 400 组。
- 等边、交换、正有理边、面积 2 的无理边、10^120 对 10^-120 极端比例、极小正面积、极接近等边、3 种尺度；原图点序与圆方程；误用半差、算术平均或错误半圆直径的反例。
- 两个长度位置各 10 个非法类型、各 3 个非正数；根迭代参数、根区间端点以及后置条件反例。
- [8 个命名算例及 1 个根包围](logs/examples.log)；[全部运行返回码](run-summary.json)；[环境](environment.json)。
- [Notebook](teaching.zh-CN.ipynb) 的 5 个代码格按序实际 `compile/exec` 执行，输出已保存；[核验记录](notebook-check.json)。**这不是 Jupyter kernel 运行**，不声称验证 kernel 集成、Notebook 前端或浏览器排版。已阅读安装的 Notebook 技能，但本地脚手架 helper 不存在；[生成器](create_notebook.py) 为标准库可复现替代，没有安装新包。
- [SVG](figures/ii14-equal-area.svg) 是自绘 9×4 矩形和边长 6 正方形，两个图均 40 px/单位，正方形另行摆放。它不是古版插图复制，也不能替代证明。

生产日志：[normal](logs/tests-normal.log)、[-O](logs/tests-O.log)、[-OO](logs/tests-OO.log)、[图](logs/figure.log)、[Notebook生成](logs/notebook-scaffold.log)、[逐格执行](logs/notebook-replay.log)。独立来源和技术复核由另外的审查者完成并另存报告，不能将本包自身测试当独立审查。

## 来源与限制

原几何次序可核对 [Joyce II.14](https://mathcs.clarku.edu/~djoyce/elements/bookII/propII14.html)：I.45、II.5、I.47 串接。代码与图均为原创教学材料；既不是古代程序，也不是全面复现古典几何基础。实数长度、圆线交点存在的公理细节及多边形作图不是此有理数测试的覆盖范围。
