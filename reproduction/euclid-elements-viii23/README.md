# VIII.23 教学复现：核查三步后的整数立方根

配套[深读](../../papers/ancient/euclid-elements-viii23.zh-CN.md)、[原典核对](source-review.zh-CN.md)、[独立技术核对](technical-review.zh-CN.md)。用精确整数运算检查正整数四项链、首项立方与两次交叉等式，再由首根的平方去除第二项，得到末项立方根。这不是古典运行记录，也没有下载外部数据。

使用 CPython 3.12.14，仅标准库。在本目录运行：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

- [源码](cube_endpoints.py)、[测试](test_cube_endpoints.py)、[Notebook](euclid-viii23.ipynb) 和[回放脚本](replay_notebook.py)。
- [普通](normal.log)、[-O](O.log)、[-OO](OO.log) 各 5 项通过；[Notebook 日志](notebook-replay.log) 来自标准库回放 3 个代码单元，不声称使用 Jupyter 内核。

有界对照：端点从 1 至 216 取 46,656 对有序输入，立方表和约化端点比用于独立分类，得到 36 对满足条件、290 对有两个整数中项但首项不是立方、46,330 对没有两个整数中项。负例不代表穷举所有可能的错误中项。另有 41 位根、倒序、单位和等端点的现代测试。有限证据不代替证明，日志时间不是性能基准。
