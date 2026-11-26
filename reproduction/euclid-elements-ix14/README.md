# 《几何原本》IX.14：最小公倍数没有外来素因子

正整数教学重构。给定非空素数列，`prime_lcm` 将其去重并相乘；重复项目不增添新的整除约束。对一个公共倍数，`strip_foreign_prime` 先检查候选素数不在给定列中且确实整除此倍数，再除掉一份，核验剩余值仍为较小公共倍数。这个操作只能提供非最小证据，并非把任意候选一步变成最小值。

例如给定 $`2,3,5`$，$`210`$ 可剥去 $`7`$ 成 $`30`$，而最小值 $`30`$ 不具有这个见证。$`60`$ 的素因子也无外来项目，却不是最小值。合数输入不适用：$`4,6`$ 的最小公倍数是 $`12`$，其中素因子 $`3`$ 不等于任一输入。单素数输入按现代程序约定作为边界。

在本目录运行，需 Python 3.9+ 标准库：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

独立基线逐个扫描正整数候选，直到找到首个公倍数，再和标准库 `math.lcm` 比较。范围是从 $`2,3,5,7`$ 选取长度 1 至 4 的有序列；外来候选另取 $`2,3,5,7,11`$ 中未列入者。有限检查不是一般证明。Notebook 日志来自标准库实跑三个代码单元，不是 Jupyter 内核运行。

[Notebook](euclid-ix14.ipynb) · [普通测试日志](normal.log) · [优化测试日志](O.log) · [二级优化日志](OO.log) · [Notebook 重放日志](notebook-replay.log) · [中文深读](../../papers/ancient/euclid-elements-ix14.zh-CN.md)
