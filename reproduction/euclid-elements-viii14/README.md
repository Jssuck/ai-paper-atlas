# VIII.14：平方数的量度与边长的量度

这是现代整数教学重构，不是古代实跑或一般命题的计算证明。给定边长 C、D，构造 A=C²、E=CD、B=D²。若 C 量度 D 共 k 次，则 E=kA、B=kE，所以 A 量度 B 共 k² 次。反向若 B 可被 A 量度，沿 VIII.7 先确认 E 可被 A 量度，再用 E/A=D/C 还原边长的量度次数。程序分开记录两个方向的检查。

例如 (4,12) 得 (16,48,144)，边长量度次数 3，平方端点量度次数 9。反向的 (12,4) 不满足相应量度关系，(6,9)、(4,10)、(2,3) 的增长分母不为 1，三个正向量度均不成立。若约分后的 D/C 分母是 q，则 B/A 的约分分母是 q²。独立基线用原始整数求余与 Fraction 检查。显式现代模式另外纳入单位和等边。

## 重跑

在本目录使用 Python 3.9+ 标准库，无需安装或联网。

```sh
python3 -B square_divisibility.py
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

每模式运行 5 项测试。有限网格扫描两边各取 1 至 40 的 1,600 对；另查超大整数与非法输入。Notebook 三个代码单元以标准库真实顺序回放，并非 Jupyter 内核运行。

实跑环境：Linux / CPython 3.12.14。回到[中文精读](../../papers/ancient/euclid-elements-viii14.zh-CN.md)，查看[原典核对](source-review.zh-CN.md)和[独立技术核对](technical-review.zh-CN.md)。

[实现](square_divisibility.py) · [测试](test_square_divisibility.py) · [Notebook](euclid-viii14.ipynb) · [重放脚本](replay_notebook.py)

[普通模式](normal.log) · [-O](O.log) · [-OO](OO.log) · [Notebook 重放](notebook-replay.log)
