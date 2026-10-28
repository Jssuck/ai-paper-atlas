# Euclid II.1：矩形分割的精确有理数教学检验

这是原创的低成本教学复现，不是对古代原文的翻译，不是通用自动定理证明器，也不以有限测试证明一般命题。数学原证及历史边界见配套中文深读；原文定位：[Joyce，第二卷命题 1](https://mathcs.clarku.edu/~djoyce/elements/bookII/propII1.html)。

## 原图与现代模型分开

原图沿 BC 依次取 B、D、E、C，以 BG 等于给定长度 A；BG 垂直 BC，GH 平行 BC，D、E、C 处的平行线分别到 K、L、H。整体矩形 BH 分成 BK、DL、EH。矩形名称采用对角顶点，BK 并不是线段面积。

这里输入 B、C、G 的二维有理坐标和严格递增的内部切分参数。**A 的长度由非零向量 BG 表示**，不是额外的输入线段；程序不复现 I.3 截取等长线段的尺规步骤。代码以参数序列 `(0, t1, ..., tn, 1)` 将底边分成任意有限正段，是原文一般陈述的现代教学表示；图上三段仅是一个具体实例。无切点表示整体一段；不接受无穷分割。

`geometry.construct` 提供顶点证书，`geometry.verify` 独立检查证书，不调用构造函数。验证内容包括：

- 输入是精确 `int` 或 `Fraction`，特别排除 Python 的 `bool`、浮点数和数值字符串；
- BC、BG 非零且点积精确为零，切点严格内部且按序；
- 下边各点确为 B 加参数倍 BC，上边各点恰好平移 BG；
- 每块四顶点顺序、正边长、连续边垂直、对边平行且等长；
- 相邻块共用同一边，朝向一致，块数、端点、整体输入均匹配；
- 各块鞋带面积之和等于整体鞋带面积。

连续参数区间和相同高度给出无间隙、内部不重叠的结构证书；面积求和只是最后一项交叉核查，不是唯一条件。例如把块的次序反转，面积和仍正确，但证书被拒绝。采用精确运算避免“小偏差容差”掩盖非垂直。模型的几何解释依赖实平面的向量与凸矩形性质，不能把运行结果当作这些性质的形式化证明。

## 运行

仅需 Python 3 标准库，无第三方依赖，无网络、数据集或服务调用：

```bash
cd reproduction/euclid-elements-ii1
python run_all.py
```

本次真实执行环境见 [environment.json](environment.json)，命令、退出码和时间见 [run-summary.json](run-summary.json)。运行器在普通、`-O`、`-OO` 三种模式各执行 **21 项 unittest**，均通过；核心验证使用显式分支，不依赖可能被优化去掉的 `assert`。

- [results.json](results.json)：**96 个有效几何案例通过，16 个非法输入被拒绝**。有效族覆盖三种平移、四种底边方向、两种垂线比例和四种分割；不等于穷尽输入空间。
- 原图教学数值 BC=6、BG=2，三段宽 1、2、3：整体面积 12，分块面积 2、4、6。
- 斜向矩形例：底边向量 (3,4)，高向量 (-4,3)，整体面积 25，分块面积 5、10、10。
- 测试还包括 100 块、极小正高度、错误绑定、缺失/多余字段、顶点篡改、错序、重复块、退化以及精确非垂直反例。案例族计数与 unittest 项数是不同口径，不相加伪称独立实验。

完整原始输出：[普通](logs/tests-normal.log)、[-O](logs/tests-O.log)、[-OO](logs/tests-OO.log)、[案例](logs/examples.log)。

## Notebook 的实际执行边界

[teaching.zh-CN.ipynb](teaching.zh-CN.ipynb) 有 **5 个代码格**。`create_notebook.py` 用标准库 `compile/exec` 顺序执行并记录输出；`verify_notebook.py` 在新命名空间再次执行并逐格比较输出。结果见 [notebook-check.json](notebook-check.json)、[执行日志](logs/notebook-execute.log)、[回放日志](logs/notebook-replay.log)。

**未启动 Jupyter kernel，也未验证 Jupyter 前端渲染、内核协议、交互部件或第三方扩展。** 已安装技能建议的模板生成脚本在本环境不可用，因此采用自建 nbformat 4.5 JSON；没有安装额外软件。Notebook 的数值实验范围和命令行相同，不声称完整复现几何学。

## 原创图

![按原图点名绘制的三段矩形：面积 2、4、6](figures/partition.svg)

`draw_figure.py` 生成原创 SVG；它是教学示意图，不是原版扫描图。已用本地 Inkscape 导出 1080×470 PNG 并逐项目视检查：B-D-E-C、G-K-L-H 对齐，三块面积标注和左下直角记号可见，文本无遮挡。Inkscape 报告默认配置及字体缓存目录不可写的警告，但导出退出码为 0，实际 PNG 可读取；这些警告不影响标准库数值实验。生成日志见 [figure.log](logs/figure.log)。

## 文件导览与限制

- `geometry.py`：构造、独立结构验证、精确面积。
- `cases.py`、`test_geometry.py`：案例族和 21 项测试。
- `run_examples.py`：案例汇总及数值结果。
- `run_all.py`：七条命令的真实执行与日志保存。
- Notebook 生成/复核脚本和绘图脚本均可独立运行。

有限有理坐标不能覆盖不可公度长度的全体实例；鞋带公式、内积与参数化是现代教学重构，不是欧几里得的符号。此实验不建立古代作者的代数观念、不证明命题的历史起源、不证明一般矩形分割定理，也不扩展到 II.2。严谨的一般解释仍应回到正文的构造、共同高度、逐块对应及整体等于部分之和。
