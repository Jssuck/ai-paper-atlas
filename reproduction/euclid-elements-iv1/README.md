# 欧几里得 IV.1：弦长与两圆交点的最小复现

这是现代教学证书，不是原文的程序或实验。令原圆圆心为原点、半径为 R，固定弦端 C=(R,0)，用以 C 为心、给定长度 L 为半径的辅助圆对应原文步骤。原文在 L=2R 时直接取直径；这里额外用两方程统一表示该边界。零长退化和超长无解是教学补充。

两个圆的平方距离方程相减确定横坐标 x=R−L²/(2R)，然后 y²=R²−x²。点记录为横坐标、纵坐标平方、纵坐标符号，避免近似根号。`verifies` 把所得点重新代回两条原始距离方程；网格独立按 L 与 2R 比较期待交点个数。非零严格次直径有两个关于直径对称的点，直径有一个对踵点，超出直径无点，零仅返回重合端点，不是正常的弦。允许有理半径和长度；这不穷尽实数输入，也不是尺规作图软件。

## 实跑

Python 3.12.14，仅标准库。请在本目录运行：

```text
python chord_insertion.py
python -m unittest -v
python -O chord_insertion.py
python -O -m unittest -v
python -OO chord_insertion.py
python -OO -m unittest -v
python replay_notebook.py
```

- [实现](chord_insertion.py)、[八个测试](test_chord_insertion.py)、[Notebook](euclid-iv1.ipynb)、[纯 Python 回放器](replay_notebook.py)。
- [普通](normal.log)、[-O](O.log)、[-OO](OO.log)三轮各通过八项测试。416 组有限网格：16 个零长、304 个非退化次直径、16 个直径、80 个超长。
- [回放日志](notebook-replay.log)由 Python 顺序执行 Notebook 的三个代码格；未运行 Jupyter 内核。
