# 《几何原本》VIII.26：相似平面数的平方比

用正整数重构原文的两步：从有序因子对 $`(a,b),(c,d)`$ 得到 $`A=ab,C=bc=ad,B=cd`$，再把三项同时除以最大公约数。所得最小链的两端为平方；这不要求原端点各为平方。

例如 $`(2,6),(3,9)`$ 构造 $`(12,18,27)`$，约去 $`3`$ 得 $`(4,6,9)`$。因此 $`12:27=4:9`$。反过来，$`(2,6),(1,12)`$ 的面积都为 $`12`$，但给定因子不相似，程序不把相等面积当作相似见证。含单位与相等给定对属于本实现的现代约定。

在此目录使用 Python 3.9+，无需第三方依赖：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

四个因子各取 1 至 12，以精确分数核对因子对应，用端点乘积的整数平方根与端点最大公约数交叉核验。有限测试不替代一般证明。Notebook 日志来自标准库顺序执行三个代码单元，不是 Jupyter 内核的执行记录。

## 文件

[深读正文](../../papers/ancient/euclid-elements-viii26.zh-CN.md) · [原典核对](source-review.zh-CN.md) · [独立技术核对](technical-review.zh-CN.md) · [源码](square_ratio.py) · [测试](test_square_ratio.py) · [Notebook](euclid-viii26.ipynb)

实际日志：[普通](normal.log)、[优化](O.log)、[双优化](OO.log)、[Notebook 回放](notebook-replay.log)。
