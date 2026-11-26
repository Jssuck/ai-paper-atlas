# 《几何原本》IX.26：奇数减奇数

`odd_pair_difference(a,b)` 接受两个奇整数 $`A>B\ge3`$。各去一个单位，得到两个偶余量 $`A-1,B-1`$；它们之差就是原来的差。程序再按 IX.24 将两个偶余量各折半，给出差的半数。例：$`19-9=10`$，偶余量为 $`18,8`$，半数为 $`9,4`$，得到 $`10=5+5`$。

程序拒绝相等、逆序、单位作输入及零和负数。在现代整数中，$`9-9=0`$、$`9-19=-10`$、$`3-1=2`$，仍符合奇数相减得偶数的更广表述。

在本目录使用 Python 3.9+ 标准库：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

独立基线用计数表核对输入，从原较小项开始每次加 2，直到原较大项，累计差的半数；两个输入各取 1 至 64。有限核验不是一般证明。Notebook 日志来自标准库顺序执行三个代码单元，不是 Jupyter 内核运行。

[Notebook](euclid-ix26.ipynb) · [Notebook 运行日志](notebook-replay.log) · [普通日志](normal.log) · [-O 日志](O.log) · [-OO 日志](OO.log)。
