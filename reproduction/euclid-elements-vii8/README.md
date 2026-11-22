# 《几何原本》VII.8：同样的若干份相减

[中文精读](../../papers/ancient/euclid-elements-vii8.zh-CN.md)重建古代证明。本目录用整数坐标重现复制、逐份扣除和合计，有限测试不替代一般证明。

## 运行

仅依赖 Python 3.9+ 标准库：

```sh
python -B -m unittest -v
python -B -O -m unittest -v
python -B -OO -m unittest -v
python -B replay_notebook.py
```

[程序](subtract_same_parts.py)、[测试](test_subtract_same_parts.py)、[Notebook](euclid-vii8.ipynb)。实跑：[普通](normal.log)、[`-O`](O.log)、[`-OO`](OO.log)、[回放](notebook-replay.log)。逐格编译执行 3 个纯 Python 单元，未启动 Jupyter 内核或验证前端渲染。

## 核验与限制

- 要求 AB/CD 与 AE/CF 为同一个最简真分数 m/n，且 1<m<n。复制 GH=AB，将其分为 m 个大小为 u 的块；从每一块扣去 v（0<v<u）。实算每一段余长 u−v，检查它是 FD=CD−CF 的一份 1/n，这是 VII.7 型的局部结论。合计余段后，用独立的 `Fraction` 比较余比与原比。
- 以 (AB,CD,AE,CF)=(10,15,6,9) 为例，GH=10 的端点为 (0,5,10)，切点 3、8，每个局部余段为 2，是 FD=6 的一份 1/3，合计 4 得 2/3。
- 50 个最简多份比（n=3 至 14），每比遍历 u=2 至 12 与 1≤v<u，共 3,300 组。v=1 和 u−v=1 各 550 例，有交集。题设的四个数均大于 1；某组件或局部余长为 1 并不是把单位当成题设里的数。
- 拒绝失配、零扣除、全扣除以及落在 VII.7 而非 VII.8 范围的单位分数。失配例 (10,15,6,12) 的余比为 4/3，不是原 2/3；这里仅以现代分数记录反例，不称大于 1 的比为较大数的若干真份。显式组件序列用于教学，不是空间优化算法。
