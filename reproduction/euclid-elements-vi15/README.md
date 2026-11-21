# VI.15 教学复现：共同的参考三角形

[中文深读](../../papers/ancient/euclid-elements-vi15.zh-CN.md)

这不是古希腊作图操作的重演。令 A 为原点，C=xu、D=−yu、B=zv、E=−wv；u、v 不共线，四个系数均为正。记方向行列式绝对值为 K，ABC、ADE、BAD 的面积依次为 xzK/2、ywK/2、yzK/2。两个以 BAD 为分母的面积比恰是 CA:AD=x:y 和 EA:AB=w:z。u、v 不必为单位向量；只有在同方向的长度比里相应的模长才约去。

## 复跑

在本目录使用 CPython 3.12.14；无第三方包或输入数据。

```sh
export PYTHONDONTWRITEBYTECODE=1
python3 -m unittest -v
python3 -O -m unittest -v
python3 -OO -m unittest -v
python3 replay_notebook.py
```

前三条测试命令对应 [normal.log](normal.log)、[O.log](O.log)、[OO.log](OO.log)。每种模式九项测试，其中一项对 1,024 个构型独立使用鞋带公式核对三个面积，并以坐标距离平方核查两个长度比；其他测试涉及退化、角度条件与共同线性变换。

[教学 Notebook](euclid-vi15.ipynb)可在已有 Jupyter 环境打开；本次用[标准库回放脚本](replay_notebook.py)按顺序执行三格 Python，保留[运行输出](notebook-replay.log)，未启动 Jupyter 内核。只用回放脚本执行可信的本仓库教学代码。

## 结果与边界

- 斜放例取 u=(1,0)、v=(1,1)，系数依次为 6、4、2、3，三个面积依次为 6、6、4，两个交叉边比都是 3/2。
- 取直角模型的 ABC，与单独构造的斜角 ADE 比较。把后者第二条单位方向从 (0,1) 换为 (3/5,4/5)，交叉边比不变，面积成为 6 和 24/5；若再把 w 改为 15/4，两面积恢复为 6，但交叉边比为 3/2 和 15/8。
- 这些有限精确构型核查了教学实现与反例，不能证明任意几何量上的一般定理；一般证明见正文。
