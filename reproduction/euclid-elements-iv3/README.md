# 欧几里得《几何原本》IV.3：等角外切三角形的教学复现

[中文深读](../../papers/ancient/euclid-elements-iv3.zh-CN.md)

这是原命题的现代坐标重构，不是古代作图工具的复刻，也不数值逼近圆周上的角度。把参考三角形底边 `EF` 水平放置，取底角半角正切为两个正有理数，且乘积小于 1。由半角参数得到两个单位方向，进而获得参考三条边的外法向。整体旋转这三个方向，使底边的外法向对准所选 `KB` 的方向。这等价于用参考三角形的两个外角在 `KB` 两侧定位另外两个切点。最后两两解切线方程，求得 `M`（A、B 切线交点）、`N`（B、C）和 `L`（C、A）。

所有坐标均使用标准库 `Fraction`，不使用容差。除了点在线上，构造还检查相邻方向的叉积为正、相对顶点严格处于每条切线内侧、接触点严格落在边段内部，以及对应有向边经同一旋转和正比例缩放后完全一致。这些检查解释了为什么不能把任意三条相交切线直接当作外切三角形。

## 执行

实跑环境为 Python 3.12.14，仅用标准库、无外部数据。从本目录运行：

```sh
python -B -m unittest -v
python -B circumscribed_triangle.py
python -B -O -m unittest -v
python -B -O circumscribed_triangle.py
python -B -OO -m unittest -v
python -B -OO circumscribed_triangle.py
python -B replay_notebook.py
```

三种模式的原始输出见 [普通](normal.log)、[优化](O.log)、[最高优化](OO.log)，各有 8 个测试。用 [教学 Notebook](euclid-iv3.ipynb) 可分步检查一个直角实例、钝角的内角射线和无效输入，以及有理数参数网格。Notebook 用同目录 [回放脚本](replay_notebook.py) 依次执行全部 3 个 Python 代码单元，见[实跑日志](notebook-replay.log)；未运行 Jupyter 内核。

网格交叉取两个底角半角参数（各 10 个）、圆心（2 个）、半径（2 个）、底边长（2 个）、固定半径方向（3 个），共 2,400 次构造调用；有效者 1,584 次（锐角 456、直角 384、钝角 744），其余 816 次因两个角之和不小于 180° 被拒。它覆盖的是有理参数族和有限的取值范围，不代替一般证明，也不是计算性能基准。
