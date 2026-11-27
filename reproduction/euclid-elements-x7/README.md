# 《几何原本》X.7：不可公度的量没有整数比

对正量 $`A,B`$，程序用 $`A^2`$ 和 $`B`$ 表示输入。要比较 $`A/B`$ 同候选 $`m/n`$，只需取出 $`n^2A^2-m^2B^2`$ 的符号，因为两侧均为正。$`A=\sqrt{2}, B=1`$ 时差为 $`2n^2-m^2`$。例如 $`99:70`$ 很接近，但差仍为 $`-1`$；正对照 $`A=\sqrt{9/4}`$ 的 $`3:2`$ 则使差为零。

$`q`$ 倍缩放两个量，使差乘上 $`q^2`$，不改变符号。候选的两个整数按同倍放大也不改变符号。比较仅对本精确输入表示法成立；程序不使用浮点数，有限网格未找到相等比不构成无理性证明。

在本目录使用 Python 3.9+ 标准库：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

测试中两个候选数各取 1 至 128；独立基线分别用整数平方根和精确有理比验证符号。Notebook 日志记录标准库实际回放三个代码单元，不是 Jupyter 内核运行。

复现文件：[教学源码](ratio_witness.py)、[测试](test_ratio_witness.py)、[Notebook](euclid-x7.ipynb)、[回放器](replay_notebook.py)。实跑日志：[常规](normal.log)、[优化](O.log)、[双重优化](OO.log)、[Notebook](notebook-replay.log)。
