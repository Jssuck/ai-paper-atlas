# 《几何原本》IX.20：给定有限素数集，找一个外部素数

`extend_primes(members)` 核对非空输入中的每一项为素数，再对不同的素数求积 $`L`$（在这样的输入上等于最小公倍数）。取 $`N=L+1`$。程序用试除找到其最小非单位因子；这个因子必为素数，且不在给定集合中。如果 $`N`$ 本身为素数，便返回 $`N`$ 和余因子 1。试除和选取最小素因子是现代教学实现，不是原文对选取方式的要求。

给定前六个素数时，$`N=30031=59\cdot509`$，不能假定 $`L+1`$ 总是素数。给定 $`3,7`$ 时，$`N=22`$，新素数为 $`2`$，也不保证它比给定的每个素数都大。重复输入去重，空输入不在本实现域内。

在本目录使用 Python 3.9+ 标准库：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

独立基线对 30,031 以内的整数筛出素数，再对前六个素数的所有非空子集以 `math.lcm` 生成 $`N`$、按筛得的素数表找最小因子。有限检查不代替一般证明。Notebook 日志记录标准库实际回放三个代码单元，不是 Jupyter 内核运行。

文件：[教学 Notebook](euclid-ix20.ipynb) · [默认测试](normal.log) · [优化测试](O.log) · [二级优化测试](OO.log) · [Notebook 回放](notebook-replay.log)。
