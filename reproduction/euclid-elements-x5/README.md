# 《几何原本》X.5：公度量给出整数比

`ratio_witness(a,b,d)` 接受精确正有理量及候选公度量 $`d`$，核验 $`a=kd,b=ld`$ 的计数 $`k,l`$ 都为正整数。`compare(u,v)` 对照 $`ua`$ 与 $`vb`$、$`uk`$ 与 $`vl`$，用 $`-1,0,1`$ 分别表示小于、等于和大于。例：$`a=21/10,b=9/10,d=3/10`$ 给出 $`(k,l)=(7,3)`$；用乘数 $`(1,3),(3,7),(1,2)`$ 可分别见到三种比较结果。把同一公度量均分为四份，会同时放大两个计数，却不改变比；整体缩放三个量则保持计数不变。

本程序是有理量的现代教学模型，不是任意实数量的公度判定器。输入量与候选公度量均不得为浮点数、零或负数；若候选量不能整份度量两个量，也拒绝。

在此目录运行，使用 Python 3.9+ 标准库：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

独立基线直接约分 $`a/b`$ 并作整数交叉比较。网格取三个尺度 $`1/2,2/3,5/4`$，两计数与两乘数各取 1 至 8。有限核验不替代一般证明。Notebook 日志来自标准库实跑三个代码单元，不是 Jupyter 内核运行。

[Notebook](euclid-x5.ipynb) · [普通模式](normal.log) · [优化模式](O.log) · [双重优化模式](OO.log) · [Notebook 回放记录](notebook-replay.log)
