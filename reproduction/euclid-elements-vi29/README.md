# 《几何原本》VI.29：给定面积，作同形超出块

[中文精读](../../papers/ancient/euclid-elements-vi29.zh-CN.md)重建原文构造。这里用精确坐标和平方证书作有限复核，而不是尺规程序的直接执行。

## 运行

仅依赖 Python 3.9+ 标准库：

```sh
python -B -m unittest -v
python -B -O -m unittest -v
python -B -OO -m unittest -v
python -B replay_notebook.py
```

[程序](excess.py)、[测试](test_excess.py)、[Notebook](euclid-vi29.ipynb)。实跑：[常规](normal.log)、[`-O`](O.log)、[`-OO`](OO.log)、[回放](notebook-replay.log)。回放执行 3 个纯 Python 单元，未调用 Jupyter 内核或验证前端渲染。

## 对照与限制

- 正总底 L，正高宽比 r，超出底 x>0，则应用面积是 r·x·(L+x)。令 m=L/2，扩大图形对应底 d=√(m²+目标面积/r)，取 x=d−m>0。另一代数分支 x=−m−d 小于 −L，不能表示正超出底。零目标仅对应 x=0 的退化边界，未纳入。
- L=10、r=2、目标 48 时，m=5、d=7、x=2。鞋带公式从坐标核对原角块面积 50、两补形各 20、超出角块 8，全图 98，差 48。目标改为 49 时 d²=99/2，精确存储平方证书；输出 `None` 仅指不存在有理超长，不表示无实根。应用面积展开时的根项系数为零，常数项恰为 49。
- 有理网格共 144 组：4 种总底 × 4 种超出底 × 3 个高宽比 × 3 个偏斜。用实坐标从应用图的面积回推超出底，并核对四分块面积、补形等积、对角交点和面积转移。测试另取超过 VI.27 缺块最大值的正面积 400，仍可构造。有限实跑不证明一般定理，也不使用浮点近似坐标伪装精确作图。
