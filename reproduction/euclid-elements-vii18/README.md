# VII.18：分别乘同一个数

现代整数上的教学重构，不是古代实跑记录或一般命题的计算证明。按重复加法的乘法约定，给定大于 1 的 A、B、C，分别取 A 个 C 与 B 个 C 得 D、E。另行加出 C 个 A 与 C 个 B，核对 VII.16 的交换。现在 C 是共同乘数，按 VII.17 思路检查 A、B 分别恰好量度 D、E 共 C 次，A:D=B:E=1:C，再核对 A:B=D:E。测试用原始数的整数乘法与 Fraction 独立重算。

例如 A=4、B=6、C=3，积为 12、18，换乘数后仍是 12、18，积之比为 2/3。伪造 D=12、E=24 时比例变为 1/2。伪造 D=16、E=24 时虽然仍为 2/3，却不符合 C=3；程序都拒绝。

本程序可用约分计数核对相等或反向的 A、B，不把它们叫作古代的真份。单位和零只在独立的现代测试中讨论：C=1 不改比例，C=0 给出未定义的 0:0；首项为零而后项非零是另一种现代边界。

## 重跑

当前目录用 Python 3.9+ 标准库执行，无需联网。

```sh
python3 -B common_multiplicand.py
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

每种模式跑 5 项测试，三个输入各取 2 至 10 的网格共 729 组。Notebook 的三个代码单元用标准库实际顺序回放，不是 Jupyter 内核运行。
