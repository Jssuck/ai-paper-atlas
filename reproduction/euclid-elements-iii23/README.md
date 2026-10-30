# III.23 最小精确教学复现

这是现代坐标重构和有限检验，不是原文算法、不证明一般定理，更不是现代 AI 实验。原文证法由同底同侧不同弓形取得 A-C-D 次序，借相似弓形定义得等角，再与三角形 CBD 外角大于不相邻内角矛盾。III.10 排除两圆第三公共点，属于嵌套判定所需前提；不能直接把图示包含当成所有情形。

## 建模与适用范围

固定 A=(-1,0), B=(1,0)。通过两点的有限非退化圆可写成 x²+y²-2ky=1，圆心 (0,k)，半径平方 1+k²。上侧弓形为圆盘与 y≥0 的交集；下侧类似。k 遍历实数时包括小弓形、半圆弓形和大弓形，不允许退化直线圆。

对非底线圆周点 P=(x,y)，向量 PA、PB 的点积是 x²+y²-1，叉积绝对值是 2|y|，故非反角 cot 为 k·sign(y)。角在 (0,π)，cot 严格递减且单射；不能用平方余弦或绝对 cot 混淆互补角。

射线 A+u(1,t) 的第二交点满足 u=2(1+kt)/(1+t²)。当 k1<k2，脚本选择正 t=1/[2(1+|k1|+|k2|)]，保证交点均在上侧且 A-C-D。两圆方程相减为 -2(k2-k1)y，故不同圆公共点必在 y=0，恰为 A、B；上侧圆盘交集严格嵌套。residual 检查验证代数条件，不以“同角必同圆”作前提。

point 是有理射线工具，可返回不同方向的交点；它拒绝底线射线以及与 A 重合的切线交点。ordered_witness 专门选择合法同侧射线。inside 包含底边和边界，但角计算拒绝 y=0。

## 文件与重跑

在本目录运行：python run_all.py。Python 3 标准库，无第三方依赖。

- [diagram.svg](diagram.svg) 与 [make_diagram.py](make_diagram.py)：显式 1000×480 的原创示意图；绘图浮点不进入精确计算。
- [geometry.py](geometry.py)：Fraction 精确圆、角 cot、点序及嵌套模型。
- [test_geometry.py](test_geometry.py)：20 个单元测试，覆盖正负 cot、退化拒绝、严格嵌套、反射及近相等。
- [run_examples.py](run_examples.py)：可核对精确示例。
- [teaching.zh-CN.ipynb](teaching.zh-CN.ipynb)：5 个教学代码单元。
- [create_notebook.py](create_notebook.py)、[verify_notebook.py](verify_notebook.py)：顺序 compile/exec 产生输出并回放逐字核验。**没有启动 Jupyter kernel，execution_count 均为 null**，不能当成 kernel 执行证据。本环境未找到技能默认 notebook helper，使用标准 Notebook 字段生成，无新安装。
- [run_all.py](run_all.py)：正常、-O、-OO 三模式重跑、写真实日志和摘要。
- [environment.json](environment.json)、[run-summary.json](run-summary.json)：实际环境与统计。
- [logs/test_geometry-normal.log](logs/test_geometry-normal.log)、[logs/test_geometry-O.log](logs/test_geometry-O.log)、[logs/test_geometry-OO.log](logs/test_geometry-OO.log)：三模式测试日志。
- [logs/run_examples-normal.log](logs/run_examples-normal.log)、[logs/verify_notebook-normal.log](logs/verify_notebook-normal.log)：示例和输出回放证据。

每模式检查 45 个 k 参数、1080 个圆周点角与侧、990 对严格嵌套圆，以及 20 个单元测试。不是 3 倍不同样本；三模式重复相同数据，用于排除依赖会被优化掉的 assert 验证。近相等例子保留 10^-30 的 cot 差，无浮点容差。

## 边界与反例解释

上侧 k=1 与下侧 k=-1 关于 AB 镜像，相似、全等但位置不重合。它只是否定“不指定侧仍位置唯一”的例子，**不是相似而大小不等的反例**。同一非直径圆两侧 cot 相反，通常不是相似弓形；半圆例外。不同同侧 k 的角不同，不能当作 III.23 假设成立的“反例”。

有限运行不覆盖全部实数参数、任意坐标系或综合几何连续性；一般性由正文证明承担。没有数据集、训练模型、统计基线或性能结论。

## 原文位置

Euclid III.23；Fitzpatrick 英译及希腊文 pp.92–93，定义 III.11 与 I.16。书目见[主文](../../papers/ancient/euclid-elements-iii23.zh-CN.md)。这里只保存原创代码与必要说明，不分发原文 PDF 或全文翻译。
