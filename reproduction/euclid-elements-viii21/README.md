# VIII.21 教学复现：由最小平面链恢复第三对边

配套[深读](../../papers/ancient/euclid-elements-viii21.zh-CN.md)、[原典核对](source-review.zh-CN.md)和[独立技术核对](technical-review.zh-CN.md)。这是原证明的现代正整数重构：约出前三项的最小比，再找两次缩放量。等端点、单位因子在此作为现代边界，并非古代词义的推断。

只需标准库。实跑使用 CPython 3.12.14。在本目录执行：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

- [源码](solid_factorization.py)、[测试](test_solid_factorization.py)、[Notebook](euclid-viii21.ipynb) 和[回放工具](replay_notebook.py)。
- [普通日志](normal.log)、[-O 日志](O.log)、[-OO 日志](OO.log) 各 5 项通过；[Notebook 日志](notebook-replay.log) 是 3 个代码单元的标准库回放，不是 Jupyter 内核运行记录。

独立的端点基线检查约化端点是否为完全立方，而不调用前三项约化构造。对 1 到 100 的有序端点，10,000 对中 140 对有整数两中项（包括等端点）。通过类的中项由基线重造再传入构造代码，核对边和缩放量；其余 9,860 对各测一条不合法的候选四项链，不穷举其所有中间项组合。有限运行不承担一般证明，不使用外部数据，且无速度基准。
