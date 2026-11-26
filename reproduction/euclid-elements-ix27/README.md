# 《几何原本》IX.27：奇数减偶数

给定奇数 $`A`$ 与偶数 $`B`$，要求 $`A>B\ge2`$。先从被减数 $`A`$ 分离单位（原图的 AD），再从偶数 $`A-1`$ 中减去 $`B`$，最后把单位放回。例：$`19-8=(18-8)+1=10+1=11`$，去单位后的差可分两半，每半为 5。

边界 $`A=B+1`$（如 $`3,2`$）给出中间差 $`0`$ 和末项 $`1`$，程序把它明确标为现代补充，此时不套用要求严格正差的 IX.24。程序拒绝逆序、零或负数以及不符奇偶条件的输入。

在此目录运行，需 Python 3.9+ 标准库：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

独立基线用加法计数表判定奇偶，从 $`B+1`$ 开始按每步加 2 计数到 $`A`$。有序两项各取 1 至 64。有限核验不代替一般证明；Notebook 日志来自标准库实跑三个代码单元，不是 Jupyter 内核运行。

[Notebook](euclid-ix27.ipynb) · [Notebook 运行日志](notebook-replay.log) · [普通日志](normal.log) · [-O 日志](O.log) · [-OO 日志](OO.log)。
