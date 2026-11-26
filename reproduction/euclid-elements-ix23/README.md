# 《几何原本》IX.23：奇数个奇数的和

`odd_count_odd_sum(terms)` 接受奇数个（至少三项）不小于 3 的奇整数。先按 IX.22 将偶数项前缀分为相等的两半；末项去掉一个单位后也可等分。两部分的半数相加，再恢复末项去掉的单位。例：$`(3,5,7)`$ 的前缀半数为 $`4`$，末项余量半数为 $`3`$，故总和 $`15=7+7+1`$。

单项和等于该项，所以单个奇数的情况是直接成立的，不需要将 IX.22 应用于空前缀。为展示非空前缀的构造，程序不接受单项。也不接受单位 1、零、负项或空输入；这些边界不改变现代整数中的奇偶规律。

在本目录使用 Python 3.9+ 标准库：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

独立基线遍历长度 1 至 5、每项 1 至 7 的有序列。合法输入的前缀直接将原项逐对求和，从预生成的等半表查询，而不是逐项去单位；总和另直接求取。有限核验不替代一般证明。Notebook 日志来自标准库实跑三个代码单元，不是 Jupyter 内核运行。

[Notebook](euclid-ix23.ipynb) · [Notebook 运行日志](notebook-replay.log) · [普通日志](normal.log) · [-O 日志](O.log) · [-OO 日志](OO.log)。
