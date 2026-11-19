# 欧几里得《几何原本》IV.4：内切圆的教学复现

[中文深读](../../papers/ancient/euclid-elements-iv4.zh-CN.md)

代码是现代坐标重构，不是历史尺规工具的复刻。坐标和边长必须是有理数。先以对边长加权得到内心，取二倍面积除以周长作为半径；再用两组单位边向量之和构造 B、C 的内角平分射线，联立检查它们的交点。不把两种实现的精确相等当作一般性证明。

垂足 E、F、G 分别对应 AB、BC、CA。程序检查：半径为每条边朝内的有向距离，半径向量与边正交，三个垂足严格位于相应边段内部，每个顶点引出的两条切线段等长。测试同时改变标签顺序，覆盖顺、逆时针两种边界方向。坐标有理不意味着边长有理，例如两个直角边长均为 1 时斜边不可用 Fraction 表示；拒绝此类输入是程序域的限制，不是原命题的限制。

## 实跑

环境为 Python 3.12.14，仅用标准库，无外部数据。从本目录执行：

~~~sh
python -B -m unittest -v
python -B incircle.py
python -B -O -m unittest -v
python -B -O incircle.py
python -B -OO -m unittest -v
python -B -OO incircle.py
python -B replay_notebook.py
~~~

[普通](normal.log)、[-O](O.log)、[-OO](OO.log)三个日志中，各有 8 项通过的单元测试。网格有四个模板（一个锐角、一个直角、两个钝角），分别取 6 种顶点排列、3 种正比例尺度、4 种旋转和 2 种平移，共 576 个变换算例（锐角 144，直角 144，钝角 288）。另验 3 个拒绝样本（重复顶点、三点共线和不在精确域内的无理边长）。有效算例检查相似变换前后的同标签结果；不存在训练数据、计时基准或历史实现可重跑。

[教学 Notebook](euclid-iv4.ipynb)可分步执行，随附[标准库回放脚本](replay_notebook.py)及[实际输出](notebook-replay.log)。本次依次以 compile/exec 运行了全部 3 个 Python 单元，没有运行 Jupyter 内核。
