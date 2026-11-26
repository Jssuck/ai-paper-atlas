# 《几何原本》IX.29：奇数乘奇数

按 VII.定义15 以 $`A`$ 决定份数，取 $`A`$ 份 $`B`$，其中两输入均为不小于 3 的奇整数。每份先隔出一单位，再平分偶余量。把 $`A`$ 个隔出的单位两两配对，余一单位；每个总半部得到 $`A`$ 份 $`B`$ 的余量半数和每对单位中的一份。例：$`A=3,B=5`$，每个总半部得到 $`3\cdot2+1=7`$，总数为 $`7+7+1=15`$。

只将份数改成偶数（如 $`4\cdot5`$），或只将每份大小改成偶数（如 $`3\cdot6`$），均不保奇数积。程序同时排除现代单位、零、负数、非整数输入，以保留非单位正数模型。

在此目录用 Python 3.9+ 标准库运行：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

两个输入各取 1 至 64，基线用预先加法构造的奇数表验证输入，再以直接乘积对照取份和配对实现。每步取一份，日志步数不是所有算术运算的合计。有限核验不替代一般证明。Notebook 日志来自标准库实跑三个代码单元，不是 Jupyter 内核运行。

[Notebook](euclid-ix29.ipynb) · [普通模式](normal.log) · [-O](O.log) · [-OO](OO.log) · [Notebook 回放](notebook-replay.log)
