# VIII.16：边长与平方的非整除

现代整数教学重构，不是古代实跑或一般证明。第一支：若 C² 不整除 D²，则 C 不整除 D，来自 VIII.14「边整除推出平方整除」的逆否。第二支：若 C 不整除 D，则 C² 不整除 D²，来自 VIII.14 另一方向的逆否。程序 branches_triggered 按原文顺序记录（平方不整除、边不整除）；余数和分母仍按（边、平方）顺序。输出中的 bridge 回看 VIII.14，不表示 VIII.16 重造了中项。若 D/C 约分后的分母为 q，D²/C² 的约分分母便为 q²；程序核对这一条件与两个整数余数一致。测试独立用 Fraction 和 divmod 检查。

(6,9) 的公度为 3，却不意味着 6 量度 9；边长和平方余数分别为 3、9。(4,12) 的两个负前提都不触发，不是反例；反转到 (12,4) 两个负前提均成立。历史式教学输入限定为不同的非单位正整数，单位和相等只在显式现代模式使用。

## 重跑

在本目录使用 Python 3.9+ 标准库，无需联网。

```sh
python3 -B square_nondivisibility.py
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

每种模式 5 项测试，枚举两边各取 1 至 40 的 1,600 对，每支有 1,442 对前提成立、158 对不触发；另测试大整数与非法输入。Notebook 三个代码单元按序用标准库回放，并非运行 Jupyter 内核。

实跑环境：Linux / CPython 3.12.14。回到[中文精读](../../papers/ancient/euclid-elements-viii16.zh-CN.md)，查看[原典核对](source-review.zh-CN.md)和[独立技术核对](technical-review.zh-CN.md)。

[实现](square_nondivisibility.py) · [测试](test_square_nondivisibility.py) · [Notebook](euclid-viii16.ipynb) · [重放脚本](replay_notebook.py)

[普通模式](normal.log) · [-O](O.log) · [-OO](OO.log) · [Notebook 重放](notebook-replay.log)
