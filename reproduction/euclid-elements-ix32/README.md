# 《几何原本》IX.32：从二开始倍增的数

从二开始实际倍增至少一次，得到 4、8、16 等。程序以两条路径核对结果：用重复加自身构造序列，用真因子及其商枚举两个均非单位的因子对。只有偶数×偶数的分解且至少有一个这样的分解，才被视为通过。二是起始项而不是倍增后的项；在这个模型中二无非单位因子对。四有 $`2\times2`$；十二既有 $`2\times6`$ 又有 $`3\times4`$，故不属于“仅偶×偶”；九有奇因子对但无偶因子对。

枚举的对不计方向，奇因子出现在哪边不影响排除；`odd_factor_pairs` 也包括两个因子都是奇数的模型边界。程序另以反复取半报告剩余奇数。把全部 2 至 256 都反向分类是现代教学检验，不将逆命题归于此处原文。

运行需 Python 3.9+ 标准库：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

独立基线将所有积不超过 256 的有序大小 $`2\le a\le b`$ 的整数因子对按积归组，不用求余搜索。有限验证不替代一般证明。Notebook 由标准库实跑三个代码单元，未使用 Jupyter 内核。

实跑环境为 CPython 3.12.14：[普通](normal.log)、[-O](O.log)、[-OO](OO.log)；[Notebook](euclid-ix32.ipynb)及[回放日志](notebook-replay.log)。
