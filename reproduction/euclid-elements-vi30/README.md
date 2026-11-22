# 《几何原本》VI.30：分割线段成中外比

[中文精读](../../papers/ancient/euclid-elements-vi30.zh-CN.md)重建原文作图。本目录是精确坐标模型，不是对古代尺规操作的执行，也不把有限测试当作一般证明。

## 运行

仅依赖 Python 3.9+ 标准库：

```sh
python -B -m unittest -v
python -B -O -m unittest -v
python -B -OO -m unittest -v
python -B replay_notebook.py
```

[程序](extreme_mean.py)、[测试](test_extreme_mean.py)、[Notebook](euclid-vi30.ipynb)。实跑：[常规](normal.log)、[`-O`](O.log)、[`-OO`](OO.log)、[回放](notebook-replay.log)。回放逐格运行 3 个纯 Python 单元，未调用 Jupyter 内核或验证前端渲染。

## 模型与边界

- 固定线段长 L>0，长段 x，短段 L−x。将 VI.29 取为单位高宽比、目标面积 L²，可得幅度 d²=(L/2)²+L²，超出底 x=d−L/2。用有理数对 (a,b) 表示 a+b√5，计算正负号时不用浮点近似；此代码不提供任意根式域。
- L=10 时，长段为 −5+5√5，短段为 15−5√5。独立从矩形坐标的鞋带行列式核对 L²=x(L+x)，从两等面积图形扣除公共矩形 Lx，得到 L(L−x)=x²，实际面积为 150−50√5。日志为避免把根式转成浮点，保留系数对。
- 测试对 35 个正有理输入（7 个分子、5 个分母的组合，允许归约后的值重复）检查长度约束、加和、面积转移和平方关系。共轭根同时让 x 与 L+x 为负，虽满足代数方程仍不符合正长度要求；固定长段角色后交换切分的长短段不保留等式。只测试正有理 L 在所用二次域内的模型。
