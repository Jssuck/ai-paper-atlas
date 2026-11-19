# 《几何原本》IV.9：外接圆的精确教学复现

对应[中文深读](../../papers/ancient/euclid-elements-iv9.zh-CN.md)。程序接受按边界顺序给出的四个有理顶点，两个绕行方向均可。它核验非退化正方形，求两条对角线交点，返回圆心及半径平方。独立核验器用循环边的等长、直角、有向转角检查输入，再比较到四个实际顶点的距离平方；不把“画得像圆”当作证据。上述是现代精确数值教学模型，不是欧几里得原来的方法。

## 运行

Python 3.12.14，零第三方依赖。从当前目录运行：

```sh
python -B circumcircle.py
python -B -m unittest -v
python -B -O -m unittest -v
python -B -OO -m unittest -v
python -B replay_notebook.py
```

- [实现](circumcircle.py)、[测试](test_circumcircle.py)
- [Notebook](euclid-iv9.ipynb)、[标准库回放](replay_notebook.py)
- [普通模式日志](normal.log)、[`-O` 日志](O.log)、[`-OO` 日志](OO.log)、[回放日志](notebook-replay.log)

## 结果与边界

三个 Python 模式各通过 8 项测试。旋转例圆心为 `(3/2,8/3)`，平方半径为 `10`。矩形对照的四个平方距离均为 `5`，说明超出正方形输入规格不等于不可共圆。非正方形菱形的对角线交点到各顶点的平方距离为 `20,5,20,5`；若假定有外接圆，相对顶点各给出一条垂直平分线，两线交点迫使圆心就是此点，故不存在共同圆。网格认证 360 个非零边正方形并拒绝 3 个零边长输入；若干案例仅是彼此的平移、旋转或缩放，不是统计独立样本。另检查交叉边序、同点/共线、错误圆心与半径，以及不精确的输入。

本环境无 Notebook 生成助手或 Jupyter 内核，Notebook 沿用训练目录的既有结构，依序用 Python 标准库实际回放 3 个代码单元。回放日志不是 Jupyter 内核日志。原文不是实验论文，无原始数据集、硬件基线、统计指标；有限测试不能代替数学证明。
