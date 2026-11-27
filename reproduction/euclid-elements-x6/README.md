# 《几何原本》X.6：从数比构造公度量

给定正量 $`A`$ 与正整数比 $`m:n`$，构造 $`C=A/m`$、$`F=nC`$。若另给 $`B`$，只有在 $`F=B`$ 时返回见证，$`A,B`$ 分别包含 $`m,n`$ 份 $`C`$。给定 $`21/10,9/5`$，$`14:12`$ 与 $`7:6`$ 均有效，而 $`7:5`$ 无效。比为 $`1:1`$ 时第二量等于第一量；同步正比例缩放各量也会缩放公度量。

推论示范在两端之间的比例中项 $`G`$；只记录精确的平方 $`G^2=AF`$，不把根用浮点数近似。例：$`A=2`$、$`m:n=2:1`$ 时 $`F=1`$、$`G^2=2`$。程序仅为正有理量教学实现，不是一般实量判定器。

在本目录使用 Python 3.9+ 标准库：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

独立基线对两量各取 $`1/3,2/3,\ldots,8/3`$、两整数计数各取 1 至 8，以交叉乘积验证比值声明。有限核验不替代一般证明。Notebook 日志来自标准库顺序执行三个代码单元，不是 Jupyter 内核实跑。

复现文件：[教学源码](ratio_witness.py)、[测试](test_ratio_witness.py)、[Notebook](euclid-x6.ipynb)、[回放器](replay_notebook.py)。实跑日志：[常规](normal.log)、[优化](O.log)、[双重优化](OO.log)、[Notebook](notebook-replay.log)。
