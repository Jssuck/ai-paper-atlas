# VIII.24 教学复现：把整数中项传到同比端点

配套[深读](../../papers/ancient/euclid-elements-viii24.zh-CN.md)、[原典核对](source-review.zh-CN.md)、[独立技术核对](technical-review.zh-CN.md)。输入目标端点 A、B 和平方见证 C、D，依次检查平方前提、同比、最小链缩放以及返回的整数根。单位和等端点只按现代正整数模型测试。

CPython 3.12.14，仅标准库。在本目录执行：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

- [源码](transfer_square.py)、[测试](test_transfer_square.py)、[Notebook](euclid-viii24.ipynb) 和[回放脚本](replay_notebook.py)。
- [普通](normal.log)、[-O](O.log)、[-OO](OO.log) 各 5 项通过；[Notebook 回放](notebook-replay.log)使用标准库执行 3 个代码单元，不是 Jupyter 内核运行。

有限对照用精确分数与直接生成的平方表：见证根各取 1 至 8，目标端点各取 1 至 100，共 640,000 组输入。200 组通过，1,008 组有相同比但目标首项不是平方，638,792 组比例不同。另测非平方见证、分数缩放、倒序、单位、等端点和 41 位根。见证根不同但减到同一比的输入是独立测试用例，不是不同的数学比例。没有外部数据或作者实验；日志时间不是性能基准，有限对照不能替代一般证明。
