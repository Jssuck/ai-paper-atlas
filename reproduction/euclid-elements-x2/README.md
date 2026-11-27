# 《几何原本》X.2：交替相减的精确轨迹

`rational_trace(a,b)` 以整商批处理相减，接受整数及 `Fraction`，其中 $`a\ge b>0`$。每行记录 $`(x,y,q,r)`$，满足 $`x=qy+r`$。共同度量在 $`(x,y)`$ 与 $`(y,r)`$ 之间不变；若 $`r>0`$，由 $`q\ge1`$ 与 $`y>r`$ 得 $`x>2r`$，所以按奇偶下标分成的两条余量子链分别严格减去超过一半。等量输入作为现代的一步终止边界。

确切比较 $`\sqrt2`$ 与 $`99/70`$ 相对 1 的轨迹。两者的前六个商都是 $`1,2,2,2,2,2`$，而有理例第六步余量为零。符号例用系数对表示 $`a+b\sqrt2`$，令 $`t=\sqrt2-1`$。因为 $`0<t<1`$ 且 $`1=2t+t^2`$，后续除法可把这一恒等式乘以 $`t^i`$，每一步保留正余量；不终止由恒等式和正性证明，不由 Notebook 扫描证明。

独立有理基线以分母最小公倍数通分，直接调用 `math.gcd`，并逐行核验共同度量及严格收缩。输入值由分子 1 至 16、分母 1 至 4 生成、去重，再配成 $`a\ge b`$ 的有序对。有限验证不代替一般证明。

仅需 Python 3.9+ 标准库（实跑 CPython 3.12.14）：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

Notebook 日志为实际运行三个代码单元的标准库回放，不是 Jupyter 内核运行。

[Notebook](euclid-x2.ipynb) · [常规日志](normal.log) · [优化日志](O.log) · [双优化日志](OO.log) · [Notebook 回放日志](notebook-replay.log)。
