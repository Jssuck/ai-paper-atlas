# 《几何原本》IV.2：同角三角形的精确有理坐标重构

这是[中文精读](../../papers/ancient/euclid-elements-iv2.zh-CN.md)的现代教学附件，不是古代尺规步骤的逐操作复刻。纸面证明使用切弦角与交替弓形；此处以有理坐标射线与圆相交构造，再直接根据实际输出三点核验角与圆周条件，不以作图角的预设作为核验结论。

把切点固定于原点，目标圆心为 (0,R)，切线水平；正半轴承接原图 AH，负半轴承接 AG。给定非共线三点 D,E,F。用某角两个向量的点积 p 与行列式绝对值 q 作为有向余弦分量与非负正弦分量的共同尺度表示；q 严格正。用 (pE,qE) 作为 AC 方向，(-pF,qF) 作为 AB 方向。对于向内射线 u，由原点出发与圆相交的非零参数是 2R u_y/(u·u)。所得点 A,B,C 要分别对应 D,E,F；以严格单调的余切 p/q 检查角匹配，保留点积符号以区分锐角与钝角。所有输入、坐标和中间量用整数或 Fraction。

- 固定正例：D=(-1,2)，E=(0,0)，F=(4,0)，R=5。E 是钝角；构造 B=(-100/29,40/29)、C=(-4,8)。两三角形按标签的余切同为 (9/8,-1/2,5/2)。
- 反例：交换 B、C 仍同在目标圆，却丢失标签约定；等比例放大保持各角却不能通过圆周检查。共线模板、零半径、切向及向外射线也不属于构造输入。
- 有限网格：模板 E 固定原点，D、F 分别遍历坐标 -2 至 2 的 25 个格点，分别取半径 1/3、5，共 1250 个参数组合。992 个有效模板/半径组合通过核验（128 锐角、320 直角、544 钝角）；258 个共线或重复点组合被排除。这不是独立随机样本、性能指标或所有实数三角形的证明；有理输入是代码接口的限制。

## 运行

Python 3.12.14，标准库即可。在本目录运行：

    python -B inscribed_triangle.py
    python -B -m unittest -v
    python -B -O inscribed_triangle.py
    python -B -O -m unittest -v
    python -B -OO inscribed_triangle.py
    python -B -OO -m unittest -v
    python -B replay_notebook.py

[源码](inscribed_triangle.py) · [测试](test_inscribed_triangle.py) · [Notebook](euclid-iv2.ipynb) · [普通模式日志](normal.log) · [优化日志](O.log) · [双优化日志](OO.log) · [Notebook 回放日志](notebook-replay.log)。Notebook 的 Python 单元在同一个命名空间按顺序用 compile/exec 回放；没有启动 Jupyter 内核。
