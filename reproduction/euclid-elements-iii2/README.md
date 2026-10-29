# Euclid III.2：弦内点的精确教学核验

本目录是中文深读的最小教学复现，不是 Euclid 的一般定理证明器、原始实验复现或完整尺规系统。

## 来源与两层论证

原文见 [Euclid III.2（Joyce 转录）](https://mathcs.clarku.edu/~djoyce/elements/bookIII/propIII2.html)。原证使用圆的定义、I.5 等腰底角、I.16 外角及 I.19 大角对大边反证，末尾略去排除圆周内点的细节。本实现另用现代二维坐标及平方距离恒等式；不声称 Euclid 使用它。原文定位与版本差异请参见 [中文深读](../../papers/ancient/euclid-elements-iii2.zh-CN.md)。

给定圆心 D、正半径平方 r²、两个互异圆周点 A、B，令 E=(1−t)A+tB。程序精确计算：

- r²−DE² = t(1−t)AB²；
- 0<t<1 时右侧严格为正，故 E 严格在圆内；
- t=0 或1只是端点，间隙为零；
- 直径中点 E=D 时距离为零，单列 `center` 分支，避免在零射线上构造角。

恒等式可由双线性展开一般证明。程序仅检查有限实例，有限运行不能证明一般定理。使用有理坐标子域，未覆盖所有实数圆/点，未实现圆心寻找、一般求交或连续性公理。

## 接口契约

`geometry.certificate(center, radius_squared, a, b, t)` 接受 `int` 或 `Fraction` 的坐标和标量；拒绝 `bool`、`float`、字符串。半径平方必须正，A≠B 且两端距离平方都等于 r²。允许 0≤t≤1 以展示端点边界，拒绝外插。返回标准化 Fraction 字段。

`verify_certificate(record)` 重新计算全部字段，要求精确字段集合和类型。只有调用该函数得到 True 才表示该格式的精确教学实例通过；不认证对象的真实几何来源、无限圆周或原证明历史。把圆心作为已知输入是本单元的前提，不把 III.1 的问题偷当已经实现。

## 可重跑方法与环境

Python 标准库，无额外依赖；Python 版本见 [environment.json](environment.json)。在本目录执行：

```sh
python -B run_all.py
```

执行器依序运行测试（普通、`-O`、`-OO`）、命名算例、Notebook生成/执行、SVG生成；任一步非零就停止。所有命令/标准输出和退出码见 [run-summary.json](run-summary.json) 与 [logs](logs)。不把三个模式当成三个独立实现。

## 本次真实结果

- 23 项单元测试，每个模式均通过；每模式包含900组有限网格：10个单位圆有理点的45对 × 2个平移 × 2个正尺度 × 5个参数。
- 测试包括直径/圆心、端点、极小正间隙、旋转/缩放/平移、重合点、错误圆周、非正半径、外插、非法类型与篡改证书。
- [五个命名算例](run_examples.py) 输出真实保存于 [examples.log](logs/examples.log)。普通中点：DE²=16、间隙9；四分点：DE²=73/4、间隙27/4；直径中点：DE²=0、间隙25；端点间隙0；平移缩放例：DE²=16/9、间隙1。
- [Notebook](teaching.zh-CN.ipynb) 的5格代码经 `compile/exec` 顺序执行，保存输出；**非 Jupyter kernel**，未核验内核集成。使用可重建的 [create_notebook.py](create_notebook.py) 生成教学内容，无额外依赖。
- [原创SVG](figures/chord-interior.svg) 表示真实可行圆弦及中点，不把反证中假设的“外部弦”画成真实可能配置。SVG由 [draw_figure.py](draw_figure.py) 生成。

测试通过并非“任意浮点输入也可靠”，也不能以采样点的有限间隙推出整个连续弦的性质。一般证明在正文独立重建。
