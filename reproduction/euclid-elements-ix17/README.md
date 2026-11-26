# 《几何原本》IX.17：互素端点的连比链不能整数续接

正整数教学模型。对给定有序连比链，以精确分数计算唯一的后续项。若首末端点都大于 1 且互素，原命题排除整数续项。例：$`(8,12,18,27)`$ 的后续项为 $`81/2`$，倒序则为 $`16/3`$。原链扩大两倍后，$`(16,24,36,54)`$ 可续接 $`81`$；这不反驳命题，因为端点不再互素。含单位、齐项及两项的最短输入，按程序的现代域约定处理；命题所需端点条件由单独接口检查。

在本目录使用 Python 3.9+ 标准库：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

基线对长度 2 至 4、各项 1 至 20 的有序输入，先比较全部相邻精确分数。对成立的连比链，另逐一检查整数 $`1\le k\le bL`$ 是否满足 $`ak=bL`$，其中 $`a,b`$ 是头两项，$`L`$ 是末项。因为 $`a\ge1`$，这个搜索范围不会遗漏整数候选。有限核验不替代一般证明。Notebook 日志是标准库实跑三个代码单元，不是 Jupyter 内核运行。

[Notebook](euclid-ix17.ipynb) · [普通测试日志](normal.log) · [优化测试日志](O.log) · [二级优化日志](OO.log) · [Notebook 重放日志](notebook-replay.log) · [中文深读](../../papers/ancient/euclid-elements-ix17.zh-CN.md)
