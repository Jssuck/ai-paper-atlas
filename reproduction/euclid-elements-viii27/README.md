# 《几何原本》VIII.27：相似立体数的立方比

这是基于正整数的教学重构。给定有序三因子 $`(a,b,c)`$ 与 $`(d,e,f)`$，先核对对应因子是否成比例，再构造四项 $`(abc,dbc,dbf,def)`$。全链约去同一个最大公约数后，最简链的两个端点都是立方数；原端点不必是立方。

例如 $`(2,4,6),(3,6,9)`$ 产生 $`(48,72,108,162)`$，约去 $`6`$ 得 $`(8,12,18,27)`$。商按右除左为 $`(3/2)^3`$，而原文方向的端点比是 $`48:162=8:27`$。$`(2,4,6),(2,3,8)`$ 虽同积 $`48`$，却不是相似见证。单位和齐项属于现代实现边界。

在本目录运行，仅需 Python 3.9+ 标准库：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

六个因子各取 1 至 6，用精确分数判断对应，再由体积直接构造乘率幂基线并核对端点最大公约数。有限算例不替代一般证明。Notebook 日志记录标准库回放三个代码单元，未启动 Jupyter 内核。

## 文件

[深读正文](../../papers/ancient/euclid-elements-viii27.zh-CN.md) · [原典核对](source-review.zh-CN.md) · [独立核对](technical-review.zh-CN.md) · [源码](cube_ratio.py) · [测试](test_cube_ratio.py) · [Notebook](euclid-viii27.ipynb)

[普通](normal.log)、[优化](O.log)、[双优化](OO.log)、[Notebook 回放](notebook-replay.log)均为实际日志。
