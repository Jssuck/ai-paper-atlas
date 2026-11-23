# VII.24：互素性在乘积下保持

现代正整数上的教学重构，不是古代实跑记录或一般定理的计算证明。设 A、B 各与 C 互素，D=A×B。假设共同非单位公度 E 能量度 C 与 D，令 F=D/E。沿 VII.23，E 和 A 互素；沿 VII.19，E:A=B:F；VII.21 将 E:A 判为最小对，VII.20 则要求 B、F 分别是 E、A 的同一整数倍。故 E 也量度 B，与 B、C 互素矛盾。

A=8、B=9、C=35 得 D=72，和 C 无共同非单位公度。若仅放开 B 与 C 的互素条件，(8,10,35) 有 E=5，证书得到 F=16，5:8=10:16，且 5 确实量度 10。若仅放开 A 与 C 的互素条件，(8,9,14) 的乘积与 14 有公度 2。测试用独立枚举因数和 Fraction 核对。

给定的数都大于 1。在第一互素条件仍保留时，F=1 会使 E=D 且 A|E|C，已冲突；同倍次数为 1 则是另一个问题，可作为现代算术边界直接核对。

## 重跑

本目录使用 Python 3.9+ 标准库，不需联网。

```sh
python3 -B coprime_product.py
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

三模式各 5 项测试；网格扫描 1,331 个三元组，其中 488 组满足定理前提，另核对 346 个保留第一互素条件的 E 见证。Notebook 有三个通过标准库实际回放的 Python 代码单元，不是 Jupyter 内核运行。
