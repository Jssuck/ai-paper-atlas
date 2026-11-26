# 《几何原本》IX.24：偶数减偶数仍为偶数

`even_difference(a,b)` 要求两个偶数满足 $`A>B\ge2`$。先取两数各自的半数，将较小半数从较大半数中去掉，留下的差正是原差的一半。例如 $`18-8=10`$；两半数 $`9,4`$ 相减得到 $`5`$，故 $`10=5+5`$。最小合法例 $`4-2=2`$，半部可以是单位。

程序拒绝相等、倒序以及零和负数输入。在现代整数中，相等时差为零，倒序时差可为负，两者仍可为偶数。奇数相减有时同样为偶数，不等于它符合本命题前提。

在本目录运行，仅需 Python 3.9+ 标准库：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

独立基线在两个输入各取 1 至 64 时，从较小数开始每次加 2，计数直至到达较大数，与取半后相减的实现核对。有限核验不替代一般证明。Notebook 日志记录标准库实跑三个代码单元，不是 Jupyter 内核运行。

[Notebook](euclid-ix24.ipynb) · [Notebook 运行日志](notebook-replay.log) · [普通日志](normal.log) · [-O 日志](O.log) · [-OO 日志](OO.log)。
