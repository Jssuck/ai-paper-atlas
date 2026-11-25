# VIII.20 教学复现：从整数比例链找回相似边

这是[中文深读](../../papers/ancient/euclid-elements-viii20.zh-CN.md)的现代整数构造，不是古代运行记录。依 [原典与版本核对](source-review.zh-CN.md)补出第一次量尽所确定的第二个积，核验 `A=D*F, C=E*F=D*G, B=E*G`。接受正整数 1 和等端点作为现代边界，不将它们混入古典用语。

只需 Python 3 标准库（实跑 Python 3.12.14）。在本目录执行：

```sh
python3 -B -m unittest -v
python3 -B -O -m unittest -v
python3 -B -OO -m unittest -v
python3 -B replay_notebook.py
```

- [构造源码](plane_factorization.py) · [测试](test_plane_factorization.py) · [Notebook](euclid-viii20.ipynb) · [回放脚本](replay_notebook.py)
- [常规日志](normal.log) · [优化 -O](O.log) · [优化 -OO](OO.log) · [Notebook 实跑](notebook-replay.log) · [独立核对](technical-review.zh-CN.md)

各测试模式 5 项通过；Notebook 逐单元回放 3 个代码单元，不声称用 Jupyter 内核运行。Notebook 的演示可交互重算，不需下载包和数据。

有限核对：枚举 1 至 100 的 10,000 对有序端点 `A,B`，整数平方根先确定乘积是否为完全平方。310 对有确切的整数中项，其他 9,690 对的向下取整候选均被拒。归一化的独立参照从端点最大公因数出发，而不是重复从 `gcd(A,C)` 求最小比；另以精确分数和四个乘积核查构造。此处每对端点只检验一个平方根候选，不是穷举所有错误的中项，也不是一般定理的证明。不做性能排名，日志时间不是基准数据。
