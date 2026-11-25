# 《几何原本》IX.2：从平方积恢复相似平面数

正整数教学重构。给定 $`A,B`$，要求 $`C=AB`$ 是平方数。从 $`D=A^2`$ 和 $`C`$ 构造比例中项 $`T=A\sqrt C`$，再除以 $`A`$ 取得 $`M=\sqrt C`$。随后用 $`k=\gcd(A,B)`$ 和约化两端的平方根 $`p,q`$，恢复有序因子 $`(p,kp),(q,kq)`$。这是一个构造见证，并非声称有序因子对唯一，也不是古代工具的复刻。

例：$`A=50,B=8`$ 得 $`C=400,D=2500,T=1000,M=20`$，以及因子 $`(5,10),(2,4)`$；$`6\cdot 10`$ 则不是平方。含 1 和相等端点按现代正整数约定测试，不能直接用来推断古代术语的范围。

在本目录使用 Python 3.9+ 标准库：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

独立基线遍历每个端点全部有序正整数因子对，然后比较两端能否有共同的约化因子比。验证范围为每个端点 1 至 150，有限枚举不替代一般证明。Notebook 日志来自标准库实跑三个代码单元，并非启动 Jupyter 内核。

## 文件

[深读正文](../../papers/ancient/euclid-elements-ix2.zh-CN.md) · [原典记录](source-review.zh-CN.md) · [独立核对](technical-review.zh-CN.md) · [源码](recover_similar_planes.py) · [测试](test_recover_similar_planes.py) · [Notebook](euclid-ix2.ipynb)

[普通](normal.log)、[优化](O.log)、[双优化](OO.log)、[Notebook 回放](notebook-replay.log)均为实际日志。
