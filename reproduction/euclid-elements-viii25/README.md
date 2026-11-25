# 《几何原本》VIII.25：立方比的传递

这是原文推理的正整数教学重构。输入 `(A,B,C,D)`，要求 $`A,C,D`$ 是立方数，且给定顺序满足 $`A:B=C:D`$。从参照对 $`C,D`$ 的整数立方根得到最简根比 $`p:q`$，构造四项最小链 $`(p^3,p^2q,pq^2,q^3)`$。用最小链首项整除 $`A`$ 所得的倍数，把该链扩展到端点 $`A,B`$；第一比例中项除以 $`A`$ 的根的平方，得到 $`B`$ 的根。程序另核查第二中项以及所得根的立方。

- $`(8,27,64,216)`$：直接把参照端点变为目标端点的倍率是 $`1/8`$，但最小链 $`(8,12,18,27)`$ 对目标链的倍率是 $`1`$。
- $`(24,81,64,216)`$：前后比相同，但 $`24`$ 和 $`81`$ 都不是立方数，因而不满足命题前提。
- 单位及齐项用例属于本实现采用的现代正整数约定。

## 运行

Python 3.9+；仅使用标准库。在本目录运行：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

测试用独立的精确分数比和整数立方表核对 $`360{,}000`$ 组输入，其中 $`A,B`$ 各取 1 至 100，参照两根各取 1 至 6。对满足前提的输入，另用精确分数乘率直接生成两个中项。这是有限验证，不替代一般证明。Notebook 回放日志来自标准库顺序执行三个代码单元，并非 Jupyter 内核实跑。

## 文件

[深读正文](../../papers/ancient/euclid-elements-viii25.zh-CN.md) · [原典核对](source-review.zh-CN.md) · [独立技术核对](technical-review.zh-CN.md) · [源码](transfer_cube.py) · [测试](test_transfer_cube.py) · [Notebook](euclid-viii25.ipynb)

实际日志：[普通](normal.log)、[优化](O.log)、[双优化](OO.log)、[Notebook 回放](notebook-replay.log)。
