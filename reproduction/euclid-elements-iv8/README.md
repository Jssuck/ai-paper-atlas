# 《几何原本》IV.8：内接圆的精确教学复现

本文档对应[中文深读](../../papers/ancient/euclid-elements-iv8.zh-CN.md)。输入是按边界顺序给出的四个有理顶点，顺、逆时针均可；实现先核验非退化正方形，再以对角点中点为圆心、四边中点为触点，返回半径平方。使用平方量是为了保留精确性，不是假定真实半径一定有理。核验器检查线段归属、垂直、点到支持直线的距离，以及圆心位于与正方形内部相同的一侧。圆盘被四边围住的理由见深读中的证明；代码不在连续圆盘上采样。

## 运行

Python 3.12.14，零第三方依赖。在本目录运行：

```sh
python -B inscribed_circle.py
python -B -m unittest -v
python -B -O -m unittest -v
python -B -OO -m unittest -v
python -B replay_notebook.py
```

- [实现](inscribed_circle.py)、[测试源文件](test_inscribed_circle.py)
- [Notebook](euclid-iv8.ipynb)、[标准库回放脚本](replay_notebook.py)
- [普通日志](normal.log)、[`-O` 日志](O.log)、[`-OO` 日志](OO.log)、[回放日志](notebook-replay.log)

三种 Python 模式各通过 8 项测试。演示返回旋转正方形的圆心 `(3/2, 8/3)` 与半径平方 `5`；矩形 `(0,0), (4,0), (4,2), (0,2)` 的中心对四条边所在直线的距离平方依次是 `1, 4, 1, 4`，不可能有同一个有正半径的内接圆同时接触矩形四边：若贴住每对对边，圆心必须在两对平行线的公共中线上，两个间距却分别为 2 和 4。小网格含 3 个有理起点，每个配 120 个非零边向量，共 360 个正方形证书通过，另 3 个零边长输入被拒。平移、转动或缩放相关的案例不视为统计独立样本。交叉顶点次序、错证书和浮点/布尔输入也单独测试。

当前环境未提供 Jupyter 脚本模板助手及 Jupyter 内核，在上一教学 Notebook 的标准结构上制作本 Notebook，并通过 Python 标准库依次实际执行了三个代码单元；这不是 Jupyter 内核执行记录。原文不是实验报告，没有原始数据集、硬件基线、统计指标。上述结果不能替代一般数学证明。
