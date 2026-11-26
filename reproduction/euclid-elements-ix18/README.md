# 《几何原本》IX.18：从平方的整除构造比例续项

正整数教学重构。给定有序的 $`(A,B)`$，对 $`B^2`$ 作除法，记录商和余数。余数为零时，商 $`D`$ 为整数见证：$`A:B=B:D`$。非单位输入接口 `extend_nonunit` 要求 $`A,B>1`$，并以精确分数核验给出的见证。现代接口 `square_measure` 接受单位输入，`modern_unit` 仅标识输入有单位。即使两个输入都大于 1，输出也可能等于 1：例如 $`(4,2)`$ 的商为 $`1`$。这个输出按现代算术纳入，并不声称三个量都是古代意义的非单位数。

例如 $`(4,6)`$ 给出 $`36=4\cdot9`$，故续项为 $`9`$；反向 $`(6,4)`$ 的余数为 $`4`$，没有见证。$`(6,10)`$ 同样非互素却不能续接整数。$`(1,4)`$ 有现代见证 $`16`$，而 $`(4,1)`$ 没有。

在本目录使用 Python 3.9+ 标准库：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

独立基线以重复加 $`A`$ 搜索，等于或超过 $`B^2`$ 时停止，不用整除判断或余数生成候选；因 $`A\ge1`$，最多 $`B^2`$ 步。两个输入各取 1 至 40。有限检查不能替代一般证明。Notebook 日志为标准库实际执行三个代码单元，并非 Jupyter 内核运行。

[Notebook](euclid-ix18.ipynb) · [普通测试日志](normal.log) · [优化测试日志](O.log) · [二级优化日志](OO.log) · [Notebook 重放日志](notebook-replay.log) · [中文深读](../../papers/ancient/euclid-elements-ix18.zh-CN.md)
