# 欧几里得《几何原本》IV.5：给三个不共线的顶点构造外接圆

[中文深读](../../papers/ancient/euclid-elements-iv5.zh-CN.md)

这是现代坐标教学重构，不是古代作图工具的复刻。把圆心写成相对 A 的向量。从平方距离对中消去相同的二次项，得到两条垂直平分线的方程。联立用行列式精确求解，结果同时检查三个平方距离、面积半径恒等式、重心坐标符号与各顶点角度点积的对应。直角另查圆心恰是有限斜边的中点，不只是落在斜边所在直线上。表示半径平方而不求根，所以半径为无理数也不妨碍验证。

输入须为 Python 整数或标准库 Fraction 坐标；非共线是几何前提，重合点也因行列式为零拒绝。精确运算避免把微小的非零面积误判成零，但并不解决现实输入的测量噪声。

## 执行

实跑环境：Python 3.12.14，仅依赖标准库、无外部数据。从本目录运行：

```sh
python -B -m unittest -v
python -B circumcircle.py
python -B -O -m unittest -v
python -B -O circumcircle.py
python -B -OO -m unittest -v
python -B -OO circumcircle.py
python -B replay_notebook.py
```

[普通](normal.log)、[优化](O.log)、[最高优化](OO.log)模式各通过 8 项测试。[教学 Notebook](euclid-iv5.ipynb)分步展示圆心与三角形位置、直角换标记、近共线与完全共线，并回放参数网格。[回放脚本](replay_notebook.py)用 Python 标准库实际执行了 Notebook 的三个代码单元，见[实跑日志](notebook-replay.log)；未运行 Jupyter 内核。

在整数方格中固定一个顶点为原点，从其余 24 点取不重复无序点对，共 276 组。逐组检查三个顶点的六种标记顺序，共 1,656 个带标记的算例：锐角 192、直角 480（A、B、C 各 160）、钝角 816、共线拒绝 168。这个计数不包含内部参考调用，也不把换标记说成新的几何形状。测试另含非整数坐标、反射相似变换、重合点和非精确类型拒绝；有限结果不代替一般证明或数值稳定性评估。
